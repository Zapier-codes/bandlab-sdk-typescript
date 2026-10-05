#!/usr/bin/env python3
"""Scrub a browser HAR capture so it is safer to hand back, and check that it is.

Requirements and the hand-back process: docs/research/HAND-BACK.md (sections 4 and 6).
Standard library only (Python 3.8+), so it runs in Termux with no installs.

  Scrub:  python3 scripts/research/scrub-har.py RAW.har -o docs/research/captures/G01-03-send-message.har \\
              --email you@example.com --username yourname --name "Your Name"
  Check:  python3 scripts/research/scrub-har.py --check FILE.har --email you@example.com --username yourname

BEST EFFORT. It removes what it knows how to recognise. Skim the output yourself before sharing it.

What it does
  - never modifies the input; writes a separate file and refuses to overwrite one unless --force
  - keeps only known HAR fields (anything else is dropped)
  - drops credential headers and all cookies; other headers keep their NAME but not their value
    (except content-type, accept, content-length)
  - drops static assets (images, fonts, scripts, CSS, media), OPTIONS preflights, and URL fragments
  - keeps JSON bodies and URL-encoded form bodies; drops every other body (HTML, multipart, binary)
  - redacts the VALUES of sensitive keys (password, token, secret, ...); key names are kept
  - replaces owner identifiers (--email/--username/--name), every email address, JWTs, bearer tokens,
    UUIDs and long hex ids with stable placeholders (the same id gets the same placeholder in a file)
  - shortens long JSON arrays so files stay small
After writing, it runs --check on its own output and deletes the output if the check fails.

Exit codes: 0 ok / clean, 1 the check found problems, 2 bad input or usage.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from urllib.parse import quote, unquote_plus

VERSION = "1"
REDACTED = "REDACTED"
MARKER = "Scrubbed by scripts/research/scrub-har.py v%s (best effort; run --check and skim before sharing)." % VERSION

UUID_RE = re.compile(r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b")
HEX_RE = re.compile(r"\b[0-9a-fA-F]{24,}\b")
EMAIL_RE = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)+")
JWT_RE = re.compile(r"\beyJ[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]{5,}\.[A-Za-z0-9_-]*")
BEARER_RE = re.compile(r"\b(bearer|basic)(\s+)([A-Za-z0-9._~+/=-]{6,})", re.I)
USERINFO_RE = re.compile(r"(//)[^/@\s]+@")

SENSITIVE_WORDS = {
    "password", "passwd", "pwd", "passcode", "pass", "token", "tokens", "secret", "secrets", "apikey",
    "authorization", "auth", "session", "cookie", "cookies", "credential", "credentials", "signature",
    "sig", "otp", "pin", "jwt", "bearer",
}
CODE_CONTEXT = {"verification", "confirmation", "confirm", "verify", "reset", "login", "sms", "email", "auth",
                "access", "security", "one"}
SENSITIVE_COMPOUNDS = ("password", "passwd", "apikey", "accesstoken", "refreshtoken", "authorization")

CRED_HEADER_RE = re.compile(
    r"^(authorization|proxy-authorization|cookie|set-cookie)$|token|secret|session|csrf|xsrf|api[-_]?key|"
    r"signature|credential|(?<![a-z])auth(?![a-z])",
    re.I,
)
KEEP_VALUE_HEADERS = {"content-type", "accept", "content-length"}
URLISH_HEADERS = {"location", "origin", "referer", "host", ":authority", ":path", ":scheme", ":method"}
URL_VALUE_HEADERS = {"location", "origin", "referer", ":path"}

STATIC_EXT = (
    ".js", ".mjs", ".css", ".map", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".avif", ".svg", ".ico",
    ".woff", ".woff2", ".ttf", ".otf", ".eot", ".mp3", ".mp4", ".m4a", ".wav", ".ogg", ".webm", ".wasm",
)
STATIC_MIME_PREFIX = ("image/", "font/", "audio/", "video/")
STATIC_MIME = {
    "text/css", "application/javascript", "text/javascript", "application/x-javascript", "application/wasm",
    "application/font-woff", "application/font-woff2", "application/vnd.ms-fontobject",
}
STATIC_RESOURCE_TYPES = {"image", "font", "media", "stylesheet", "script", "manifest", "texttrack"}

ENTRY_KEYS = ("pageref", "startedDateTime", "time", "request", "response", "timings")
REQUEST_KEYS = ("method", "httpVersion", "headersSize", "bodySize")
RESPONSE_KEYS = ("status", "statusText", "httpVersion", "headersSize", "bodySize")


# ---------------------------------------------------------------- helpers

def key_words(key):
    parts = re.findall(r"[A-Z]+(?![a-z])|[A-Z]?[a-z]+|\d+", key)
    return [p.lower() for p in parts]


def is_sensitive_key(key):
    words = key_words(str(key))
    joined = "".join(words)
    if any(w in SENSITIVE_WORDS for w in words):
        return True
    if any(c in joined for c in SENSITIVE_COMPOUNDS):
        return True
    return "code" in words and any(w in CODE_CONTEXT for w in words)


def redactable(value):
    """Booleans, numbers and null under a sensitive key carry shape, not secrets: keep them."""
    return isinstance(value, (str, dict, list))


def mime_of(value):
    return (value or "").split(";")[0].strip().lower()


def is_json_mime(mime):
    return mime in ("application/json", "text/json", "application/x-json") or mime.endswith("+json")


def url_path(url):
    return url.split("#", 1)[0].split("?", 1)[0]


def is_static_entry(entry):
    req = entry.get("request") or {}
    res = entry.get("response") or {}
    mime = mime_of((res.get("content") or {}).get("mimeType"))
    path = url_path(str(req.get("url") or "")).lower()
    return (
        path.endswith(STATIC_EXT)
        or mime in STATIC_MIME
        or mime.startswith(STATIC_MIME_PREFIX)
        or str(entry.get("_resourceType") or "").lower() in STATIC_RESOURCE_TYPES
    )


def dump_json(obj):
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":"))


# ---------------------------------------------------------------- scrubber

class Scrubber:
    def __init__(self, owner_email=(), owner_username=(), owner_name=(), max_items=5):
        self.owner = []
        for values, label in ((owner_email, "OWNER-EMAIL"), (owner_username, "OWNER-USERNAME"), (owner_name, "OWNER-NAME")):
            for v in values:
                self.owner.append((re.compile(re.escape(v), re.I), label))
        self.max_items = max_items
        self.maps = {"UUID": {}, "HEX": {}, "EMAIL": {}}
        self.stats = {
            "entries_in": 0, "entries_out": 0, "static_dropped": 0, "preflight_dropped": 0,
            "headers_dropped": 0, "headers_redacted": 0, "cookies_dropped": 0,
            "bodies_omitted": 0, "values_redacted": 0, "arrays_truncated": 0,
        }
        self.static_hosts = {}

    def placeholder(self, kind, value):
        table = self.maps[kind]
        key = value.lower()
        if key not in table:
            table[key] = "%s-%04d" % (kind, len(table) + 1)
        return table[key]

    def text(self, s):
        if not isinstance(s, str) or not s:
            return s
        for pattern, label in self.owner:
            s = pattern.sub(label, s)
        s = EMAIL_RE.sub(lambda m: self.placeholder("EMAIL", m.group(0)), s)
        s = JWT_RE.sub("JWT-REDACTED", s)
        s = BEARER_RE.sub(lambda m: m.group(0) if m.group(3) == REDACTED else "%s%s%s" % (m.group(1), m.group(2), REDACTED), s)
        s = UUID_RE.sub(lambda m: self.placeholder("UUID", m.group(0)), s)
        s = HEX_RE.sub(lambda m: self.placeholder("HEX", m.group(0)), s)
        return s

    def url(self, url):
        if not isinstance(url, str):
            return url
        base = url.split("#", 1)[0]  # fragments can carry tokens
        base = USERINFO_RE.sub(r"\1", base)  # drop user:password@ from the URL entirely
        if "?" not in base:
            return self.text(base)
        path, query = base.split("?", 1)
        items = []
        for pair in query.split("&"):
            if pair == "":
                continue
            k, _, v = pair.partition("=")
            if is_sensitive_key(unquote_plus(k)):
                items.append("%s=%s" % (k, REDACTED))
                self.stats["values_redacted"] += 1
                continue
            v_dec = unquote_plus(v)
            cleaned = self.text(v_dec)
            items.append(pair if cleaned == v_dec else "%s=%s" % (k, quote(cleaned, safe="")))
        return self.text(path) + "?" + "&".join(items)

    def json_value(self, node):
        if isinstance(node, dict):
            out = {}
            for k, v in node.items():
                nk = self.text(k)
                if is_sensitive_key(k) and redactable(v):
                    out[nk] = REDACTED
                    self.stats["values_redacted"] += 1
                else:
                    out[nk] = self.json_value(v)
            return out
        if isinstance(node, list):
            if len(node) > self.max_items:
                node = node[: self.max_items]
                self.stats["arrays_truncated"] += 1
            return [self.json_value(x) for x in node]
        if isinstance(node, str):
            return self.text(node)
        return node

    def named_pairs(self, pairs, url_values=False):
        out = []
        for p in pairs or []:
            if not isinstance(p, dict) or "name" not in p:
                continue
            name = str(p.get("name"))
            value = p.get("value", "")
            if is_sensitive_key(name):
                out.append({"name": self.text(name), "value": REDACTED})
                self.stats["values_redacted"] += 1
            else:
                out.append({"name": self.text(name), "value": self.text(value) if isinstance(value, str) else value})
        return out

    def headers(self, headers):
        out = []
        for h in headers or []:
            if not isinstance(h, dict):
                continue
            name = str(h.get("name") or "")
            low = name.lower()
            value = h.get("value", "")
            if low in URLISH_HEADERS:
                out.append({"name": name, "value": self.url(value) if low in URL_VALUE_HEADERS else self.text(value)})
            elif CRED_HEADER_RE.search(low):
                self.stats["headers_dropped"] += 1
            elif low in KEEP_VALUE_HEADERS:
                out.append({"name": name, "value": value})
            else:
                out.append({"name": name, "value": REDACTED})
                self.stats["headers_redacted"] += 1
        return out

    def post_data(self, pd):
        mime_raw = pd.get("mimeType")
        mime = mime_of(mime_raw)
        out = {"mimeType": mime_raw}
        if isinstance(pd.get("comment"), str) and pd["comment"]:
            out["comment"] = self.text(pd["comment"])  # keep notes from an earlier pass
        text = pd.get("text")
        if is_json_mime(mime) and isinstance(text, str):
            try:
                out["text"] = dump_json(self.json_value(json.loads(text)))
                return out
            except ValueError:
                pass
        elif mime == "application/x-www-form-urlencoded":
            params = pd.get("params")
            if not params and isinstance(text, str):
                params = [{"name": unquote_plus(k), "value": unquote_plus(v)} for k, _, v in (p.partition("=") for p in text.split("&") if p)]
            clean = self.named_pairs(params)
            out["params"] = clean
            out["text"] = "&".join("%s=%s" % (quote(str(p["name"]), safe=""), quote(str(p["value"]), safe="")) for p in clean)
            return out
        out["comment"] = "body omitted (%s)" % (mime or "unknown type")
        self.stats["bodies_omitted"] += 1
        return out

    def content(self, content):
        mime_raw = content.get("mimeType")
        mime = mime_of(mime_raw)
        out = {"size": content.get("size", 0), "mimeType": mime_raw}
        if isinstance(content.get("comment"), str) and content["comment"]:
            out["comment"] = self.text(content["comment"])  # keep notes from an earlier pass
        text = content.get("text")
        if text is None:
            return out
        if is_json_mime(mime) and isinstance(text, str) and content.get("encoding") != "base64":
            try:
                out["text"] = dump_json(self.json_value(json.loads(text)))
                return out
            except ValueError:
                pass
        out["comment"] = "body omitted (%s)" % (mime or "unknown type")
        self.stats["bodies_omitted"] += 1
        return out

    def entry(self, entry):
        before = self.stats["arrays_truncated"]
        req = entry.get("request") or {}
        res = entry.get("response") or {}
        out = {k: entry[k] for k in ENTRY_KEYS if k in entry and k not in ("request", "response")}
        out["cache"] = {}
        new_req = {k: req[k] for k in REQUEST_KEYS if k in req}
        new_req["url"] = self.url(req.get("url"))
        new_req["headers"] = self.headers(req.get("headers"))
        new_req["queryString"] = self.named_pairs(req.get("queryString"))
        new_req["cookies"] = []
        self.stats["cookies_dropped"] += len(req.get("cookies") or [])
        if isinstance(req.get("postData"), dict):
            new_req["postData"] = self.post_data(req["postData"])
        new_res = {k: res[k] for k in RESPONSE_KEYS if k in res}
        new_res["headers"] = self.headers(res.get("headers"))
        new_res["cookies"] = []
        self.stats["cookies_dropped"] += len(res.get("cookies") or [])
        new_res["content"] = self.content(res.get("content") or {})
        new_res["redirectURL"] = self.url(res.get("redirectURL") or "")
        out["request"] = new_req
        out["response"] = new_res
        if "_resourceType" in entry:
            out["_resourceType"] = entry["_resourceType"]
        cut = self.stats["arrays_truncated"] - before
        if cut:
            note = "%d long array(s) shortened to %d items" % (cut, self.max_items)
            prev = new_res["content"].get("comment")
            new_res["content"]["comment"] = (prev + "; " + note) if prev else note
        return out

    def har(self, har):
        log = har.get("log") or {}
        out_log = {"version": log.get("version", "1.2")}
        creator = log.get("creator")
        if isinstance(creator, dict):
            out_log["creator"] = {"name": creator.get("name"), "version": creator.get("version")}
        pages = []
        for p in log.get("pages") or []:
            if isinstance(p, dict):
                pages.append({"startedDateTime": p.get("startedDateTime"), "id": p.get("id"), "title": REDACTED,
                              "pageTimings": p.get("pageTimings") or {}})
        out_log["pages"] = pages
        entries = []
        for e in log.get("entries") or []:
            self.stats["entries_in"] += 1
            if not isinstance(e, dict):
                continue
            method = str((e.get("request") or {}).get("method") or "").upper()
            if method == "OPTIONS":
                self.stats["preflight_dropped"] += 1
                continue
            if is_static_entry(e):
                self.stats["static_dropped"] += 1
                host = re.sub(r"^[a-z]+://", "", self.url(str((e.get("request") or {}).get("url") or ""))).split("/", 1)[0]
                self.static_hosts[host] = self.static_hosts.get(host, 0) + 1
                continue
            entries.append(self.entry(e))
        self.stats["entries_out"] = len(entries)
        hosts = ", ".join("%s (%d)" % kv for kv in sorted(self.static_hosts.items(), key=lambda kv: -kv[1])[:10])
        out_log["comment"] = MARKER + (" Static assets dropped from: " + hosts + "." if hosts else "")
        out_log["entries"] = entries
        return {"log": out_log}


# ---------------------------------------------------------------- checker

def url_problem(value):
    """Return a short kind if a URL string still carries a credential-looking query value or a fragment."""
    if not isinstance(value, str):
        return None
    if "#" in value:
        return "url-fragment"
    if "?" in value:
        for pair in value.split("?", 1)[1].split("&"):
            k, _, v = pair.partition("=")
            if is_sensitive_key(unquote_plus(k)) and v != REDACTED:
                return "sensitive-value-in-url"
    return None


def check_har(har, raw_text, owner_terms):
    """Return a list of (kind, location). Never includes the offending value itself."""
    findings = []

    def add(kind, path):
        if (kind, path) not in findings:
            findings.append((kind, path))

    low = raw_text.lower()
    for label, term in owner_terms:
        if term.lower() in low:
            add("owner-identifier-present (%s)" % label, "file")

    def strings(s, path):
        if EMAIL_RE.search(s):
            add("email-address", path)
        if JWT_RE.search(s):
            add("jwt", path)
        for m in BEARER_RE.finditer(s):
            if m.group(3) != REDACTED:
                add("bearer-token", path)
        if UUID_RE.search(s):
            add("uuid", path)
        if HEX_RE.search(s):
            add("long-hex-id", path)
        if USERINFO_RE.search(s):
            add("credentials-in-url", path)

    def walk(node, path, ctx=None):
        if isinstance(node, dict):
            if ctx in ("headers", "queryString", "params") and "name" in node and "value" in node:
                name, value = str(node["name"]), node["value"]
                low_name = name.lower()
                if ctx == "headers" and low_name in URL_VALUE_HEADERS:
                    kind = url_problem(value)
                    if kind:
                        add(kind, path)
                if ctx == "headers" and low_name not in URLISH_HEADERS:
                    if CRED_HEADER_RE.search(low_name):
                        add("credential-header", path)
                    elif low_name not in KEEP_VALUE_HEADERS and value != REDACTED:
                        add("header-value-kept", path)
                elif ctx != "headers" and is_sensitive_key(name) and value != REDACTED:
                    add("sensitive-value", path)
            for k, v in node.items():
                p = "%s.%s" % (path, k)
                strings(str(k), p + " (key)")
                if is_sensitive_key(k) and redactable(v) and v != REDACTED and k not in ("headers", "queryString", "params", "cookies"):
                    add("sensitive-value", p)
                walk(v, p, k if k in ("headers", "queryString", "params", "cookies") else None)
        elif isinstance(node, list):
            if ctx == "cookies" and node:
                add("cookies-present", path)
            for i, x in enumerate(node):
                walk(x, "%s[%d]" % (path, i), ctx)
        elif isinstance(node, str):
            strings(node, path)
            t = node.strip()
            if t[:1] in "{[" and len(t) > 1:
                try:
                    walk(json.loads(t), path + "(json)")
                except ValueError:
                    pass

    walk(har, "$")
    for i, e in enumerate((har.get("log") or {}).get("entries") or []):
        base = "$.log.entries[%d]" % i
        req, res = e.get("request") or {}, e.get("response") or {}
        for label, value in (("request.url", req.get("url")), ("response.redirectURL", res.get("redirectURL"))):
            kind = url_problem(value)
            if kind:
                add(kind, "%s.%s" % (base, label))
        if str(req.get("method") or "").upper() == "OPTIONS":
            add("preflight-entry", base)
        if is_static_entry(e):
            add("static-asset-entry", base)
        c = res.get("content") or {}
        if c.get("encoding") == "base64":
            add("binary-body", base + ".response.content")
        if c.get("text") is not None and not is_json_mime(mime_of(c.get("mimeType"))):
            add("non-json-response-body", base + ".response.content")
        pd = req.get("postData") or {}
        pmime = mime_of(pd.get("mimeType"))
        if pd.get("text") is not None and not (is_json_mime(pmime) or pmime == "application/x-www-form-urlencoded"):
            add("non-json-request-body", base + ".request.postData")
    return findings


# ---------------------------------------------------------------- CLI

def die(message):
    print(message, file=sys.stderr)
    sys.exit(2)


def load_har(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            raw = fh.read()
    except OSError as err:
        die("error: cannot read %s: %s" % (path, err.strerror or err))
    try:
        data = json.loads(raw)
    except ValueError as err:
        die("error: %s is not valid JSON: %s" % (path, err))
    if not isinstance(data, dict) or not isinstance((data.get("log") or {}).get("entries"), list):
        die("error: %s does not look like a HAR file (no log.entries list)" % path)
    return data, raw


def owner_terms(args):
    terms = []
    for label, values in (("--email", args.email), ("--username", args.username), ("--name", args.name)):
        for v in values:
            terms.append((label, v))
    return terms


def print_findings(findings, out=sys.stdout):
    for kind, where in findings[:25]:
        print("  FAIL  %-34s %s" % (kind, where), file=out)
    if len(findings) > 25:
        print("  ... and %d more" % (len(findings) - 25), file=out)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Scrub a HAR capture, or check that one is clean. See the module docstring.")
    ap.add_argument("input", help="the HAR file to scrub (or to check, with --check)")
    ap.add_argument("-o", "--output", help="where to write the scrubbed file (default: <input>.scrubbed.har)")
    ap.add_argument("--check", action="store_true", help="only check the file for leaks; write nothing")
    ap.add_argument("--force", action="store_true", help="allow overwriting an existing output file")
    ap.add_argument("--email", action="append", default=[], help="your email address (repeatable)")
    ap.add_argument("--username", action="append", default=[], help="your BandLab username (repeatable)")
    ap.add_argument("--name", action="append", default=[], help="your real name (repeatable)")
    ap.add_argument("--max-items", type=int, default=5, help="keep at most this many items of a long JSON array (default 5)")
    args = ap.parse_args(argv)

    for v in args.email:
        if "@" not in v:
            ap.error("--email %r does not look like an email address" % v)
    for label, values in (("--username", args.username), ("--name", args.name)):
        for v in values:
            if len(v) < 3:
                ap.error("%s %r is too short to replace safely (3 characters minimum)" % (label, v))
    if args.max_items < 1:
        ap.error("--max-items must be at least 1")

    har, raw = load_har(args.input)
    terms = owner_terms(args)

    if args.check:
        findings = check_har(har, raw, terms)
        if findings:
            print("CHECK FAILED: %d problem(s) in %s" % (len(findings), args.input))
            print_findings(findings)
            print("Do not share this file. Values are never printed; open the file at the locations above.")
            return 1
        print("CHECK PASSED: %s (still skim it yourself; the check is not proof)" % args.input)
        return 0

    out_path = args.output or (os.path.splitext(args.input)[0] + ".scrubbed.har")
    if os.path.realpath(out_path) == os.path.realpath(args.input):
        die("error: the output path is the input file; the original is never modified")
    if os.path.exists(out_path) and not args.force:
        die("error: %s already exists (use --force to overwrite)" % out_path)

    s = Scrubber(args.email, args.username, args.name, args.max_items)
    scrubbed = s.har(har)
    text = json.dumps(scrubbed, indent=2, ensure_ascii=False) + "\n"
    out_dir = os.path.dirname(os.path.abspath(out_path))
    os.makedirs(out_dir, exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as fh:
        fh.write(text)

    findings = check_har(scrubbed, text, terms)
    if findings:
        os.remove(out_path)
        print("SCRUB FAILED the self-check, so the output was deleted (%d problem(s)):" % len(findings))
        print_findings(findings)
        return 1

    st = s.stats
    print("Wrote %s" % out_path)
    print("  entries: %d in, %d kept   | dropped: %d static assets, %d preflights" % (st["entries_in"], st["entries_out"], st["static_dropped"], st["preflight_dropped"]))
    print("  headers: %d credential headers dropped, %d values redacted, %d cookies dropped" % (st["headers_dropped"], st["headers_redacted"], st["cookies_dropped"]))
    print("  bodies : %d omitted | %d sensitive values redacted | %d long arrays shortened" % (st["bodies_omitted"], st["values_redacted"], st["arrays_truncated"]))
    print("  ids    : %d UUIDs, %d long hex ids, %d email addresses replaced" % (len(s.maps["UUID"]), len(s.maps["HEX"]), len(s.maps["EMAIL"])))
    print("Self-check passed. Now skim the file yourself, then check it once more with --check before sharing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
