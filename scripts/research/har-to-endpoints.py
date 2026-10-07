#!/usr/bin/env python3
"""Turn SCRUBBED HAR captures into endpoint descriptions, and flag the ones the SDK does not have.

Input : scrubbed .har files (see scrub-har.py and docs/research/HAND-BACK.md); default: docs/research/captures/
Output: docs/research/endpoints/<domain>.json, one file per domain that has endpoints
Compares each endpoint with the SDK table in docs/endpoint-status.md and marks it "inSdk": true / false.
Standard library only (Python 3.8+).

  python3 scripts/research/har-to-endpoints.py                       # all captures -> docs/research/endpoints/
  python3 scripts/research/har-to-endpoints.py FILE.har DIR --dry-run

What is recorded: method, host, path template, query KEYS, header NAMES, status codes, and the SHAPE (types only,
never values) of JSON request and response bodies, merged across every capture of the same endpoint.
Safety: every input is run through the scrubber's own leak check first. A file that fails it is refused, nothing is
written, and the exit code is 1. Output files are generated; do not edit them by hand.

Exit codes: 0 ok, 1 an input failed the leak check, 2 bad input or usage.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
DEFAULT_IN = os.path.join(REPO, "docs", "research", "captures")
DEFAULT_OUT = os.path.join(REPO, "docs", "research", "endpoints")
DEFAULT_STATUS = os.path.join(REPO, "docs", "endpoint-status.md")

API_PREFIX_RE = re.compile(r"^/api/v\d+(?:\.\d+)*(?=/|$)")
ID_SEGMENT_RE = re.compile(r"^(?:UUID|HEX)-\d{4}$")
EMAIL_SEGMENT_RE = re.compile(r"^(?:EMAIL-\d{4}|OWNER-EMAIL)$")
G_ITEM_RE = re.compile(r"^(G\d{2})-")
STATUS_ROW_RE = re.compile(r"^\| `(\w+)` \| ([A-Z]+) \| `([^`]+)` \| `([^`]+)` \| `([^`]+)` \|$")

# Which domain file an endpoint goes to: the LAST path segment that appears here wins.
SEGMENT_DOMAIN = {}
for _domain, _segments in {
    "account": "me passwords emails logins authorizations keys",
    "users": "users contacts recommendations blocks",
    "search": "search",
    "songs": "songs song",
    "revisions": "revisions forks",
    "collaborators": "collaborators",
    "posts": "posts post",
    "comments": "comments",
    "likes": "likes",
    "followers": "followers following",
    "bands": "bands band",
    "communities": "communities community",
    "collections": "collections",
    "notifications": "notifications",
    "invitations": "invites invitations",
    "media": "media",
    "audio": "audio samples sample",
    "videos": "videos",
    "images": "images",
    "effects": "effects mix mixdown tracks",
    "genres": "genres",
    "skills": "skills",
    "labels": "labels",
    "badges": "badges",
    "settings": "settings push",
    "messaging": "conversations messages message inbox chat",
}.items():
    for _s in _segments.split():
        SEGMENT_DOMAIN[_s] = _domain


def load_scrubber():
    spec = importlib.util.spec_from_file_location("scrub_har", os.path.join(HERE, "scrub-har.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def die(message):
    print(message, file=sys.stderr)
    sys.exit(2)


# ---------------------------------------------------------------- shapes (types only, never values)

def string_kind(s):
    if re.match(r"^UUID-\d{4}$", s):
        return "uuid"
    if re.match(r"^HEX-\d{4}$", s):
        return "hex-id"
    if EMAIL_SEGMENT_RE.match(s):
        return "email"
    if s == "OWNER-USERNAME":
        return "username"
    if s == "OWNER-NAME":
        return "name"
    if s == "REDACTED":
        return "redacted"
    if re.match(r"^\d{4}-\d{2}-\d{2}T", s):
        return "datetime"
    return "string"


STRING_KINDS = {"string", "uuid", "hex-id", "email", "username", "name", "redacted", "datetime"}


def shape_of(value):
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, str):
        return string_kind(value)
    if isinstance(value, list):
        element = None
        for item in value:
            s = shape_of(item)
            element = s if element is None else merge(element, s)
        return [] if element is None else [element]
    if isinstance(value, dict):
        return {k: shape_of(v) for k, v in value.items()}
    return "string"


def _members(shape):
    """Split a shape into (set of primitive names, object shape or None, list shape or None)."""
    prims, obj, lst = set(), None, None
    parts = shape["$union"] if isinstance(shape, dict) and set(shape) == {"$union"} else [shape]
    for part in parts:
        if isinstance(part, str):
            prims.update(part.split("|"))
        elif isinstance(part, list):
            lst = part if lst is None else merge_lists(lst, part)
        elif isinstance(part, dict):
            obj = part if obj is None else merge_objects(obj, part)
    return prims, obj, lst


def _prim_string(prims):
    kinds = prims & STRING_KINDS
    if len(kinds) > 1:
        prims = (prims - STRING_KINDS) | {"string"}
    if "integer" in prims and "number" in prims:
        prims = prims - {"integer"}
    return "|".join(sorted(prims))


def merge_lists(a, b):
    if not a:
        return b
    if not b:
        return a
    return [merge(a[0], b[0])]


def merge_objects(a, b):
    def split(obj):
        return {(k[:-1] if k.endswith("?") else k): (v, k.endswith("?")) for k, v in obj.items()}

    sa, sb = split(a), split(b)
    out = {}
    for key in list(sa) + [k for k in sb if k not in sa]:
        if key in sa and key in sb:
            shape = merge(sa[key][0], sb[key][0])
            optional = sa[key][1] or sb[key][1]
        else:
            shape, optional = (sa.get(key) or sb.get(key))[0], True
        out[key + "?" if optional else key] = shape
    return out


def merge(a, b):
    if a == b:
        return a
    pa, oa, la = _members(a)
    pb, ob, lb = _members(b)
    prims = pa | pb
    obj = oa if ob is None else (ob if oa is None else merge_objects(oa, ob))
    lst = la if lb is None else (lb if la is None else merge_lists(la, lb))
    complex_parts = [p for p in (obj, lst) if p is not None]
    if not complex_parts:
        return _prim_string(prims)
    parts = ([_prim_string(prims)] if prims else []) + complex_parts
    return parts[0] if len(parts) == 1 else {"$union": parts}


# ---------------------------------------------------------------- endpoints

def base_mime(value):
    return (value or "").split(";")[0].strip().lower() or None


def is_json(mime):
    return bool(mime) and (mime in ("application/json", "text/json", "application/x-json") or mime.endswith("+json"))


def split_url(url):
    m = re.match(r"^[a-z][a-z0-9+.-]*://([^/?#]*)(/[^?#]*)?(?:\?([^#]*))?", url or "")
    if not m:
        return None, url or "", ""
    return m.group(1), m.group(2) or "/", m.group(3) or ""


def template_path(path):
    prefix = ""
    m = API_PREFIX_RE.match(path)
    if m:
        prefix, path = m.group(0), path[m.end():] or "/"
    out = []
    for seg in path.split("/"):
        if ID_SEGMENT_RE.match(seg) or seg.isdigit():
            out.append("{id}")
        elif EMAIL_SEGMENT_RE.match(seg):
            out.append("{email}")
        elif seg == "OWNER-USERNAME":
            out.append("{username}")
        else:
            out.append(seg)
    return prefix or None, "/".join(out) or "/"


def domain_of(path):
    for seg in reversed([s for s in path.split("/") if s and not s.startswith("{")]):
        if seg in SEGMENT_DOMAIN:
            return SEGMENT_DOMAIN[seg]
    return "unknown"


def normalise(verb, path):
    return (verb.lower(), re.sub(r"\{[^}]*\}", "{}", path))


def load_sdk_table(path):
    try:
        with open(path, encoding="utf-8") as fh:
            lines = fh.read().splitlines()
    except OSError as err:
        die("error: cannot read the SDK table %s: %s" % (path, err.strerror or err))
    table = {}
    for line in lines:
        m = STATUS_ROW_RE.match(line)
        if m:
            table[normalise(m.group(2), m.group(3))] = m.group(4)
    if not table:
        die("error: no endpoint rows found in %s (expected the table written by scripts/coverage --markdown)" % path)
    return table


def body_shape(mime, text, params=None):
    if is_json(mime) and isinstance(text, str):
        try:
            return shape_of(json.loads(text))
        except ValueError:
            return None
    if mime == "application/x-www-form-urlencoded" and params:
        return {p["name"]: string_kind(str(p.get("value", ""))) for p in params if isinstance(p, dict) and "name" in p}
    return None


class Collector:
    def __init__(self):
        self.records = {}

    def add(self, entry, source):
        req, res = entry.get("request") or {}, entry.get("response") or {}
        host, path, _ = split_url(req.get("url") or "")
        prefix, template = template_path(path)
        method = str(req.get("method") or "GET").upper()
        key = (method, host, prefix, template)
        rec = self.records.setdefault(key, {
            "method": method, "host": host, "apiPrefix": prefix, "path": template, "samples": 0,
            "query": set(), "headers": set(), "gItems": set(), "sources": set(),
            "request": {"contentType": None, "shape": None, "note": None}, "responses": {},
        })
        rec["samples"] += 1
        rec["sources"].add(source)
        m = G_ITEM_RE.match(source)
        if m:
            rec["gItems"].add(m.group(1))
        for q in req.get("queryString") or []:
            if isinstance(q, dict) and q.get("name"):
                rec["query"].add(str(q["name"]))
        for h in (req.get("headers") or []) + (res.get("headers") or []):
            if isinstance(h, dict) and h.get("name"):
                rec["headers"].add(str(h["name"]))
        pd = req.get("postData")
        if isinstance(pd, dict):
            mime = base_mime(pd.get("mimeType"))
            rec["request"]["contentType"] = rec["request"]["contentType"] or mime
            shape = body_shape(mime, pd.get("text"), pd.get("params"))
            if shape is not None:
                prev = rec["request"]["shape"]
                rec["request"]["shape"] = shape if prev is None else merge(prev, shape)
            elif pd.get("comment"):
                rec["request"]["note"] = pd["comment"]
        status = str(res.get("status", 0))
        out = rec["responses"].setdefault(status, {"contentType": None, "shape": None})
        content = res.get("content") or {}
        mime = base_mime(content.get("mimeType"))
        out["contentType"] = out["contentType"] or mime
        shape = body_shape(mime, content.get("text"))
        if shape is not None:
            out["shape"] = shape if out["shape"] is None else merge(out["shape"], shape)

    def finish(self, sdk_table):
        by_domain = {}
        for rec in self.records.values():
            sdk_call = sdk_table.get(normalise(rec["method"], rec["path"]))
            record = {
                "method": rec["method"], "host": rec["host"], "apiPrefix": rec["apiPrefix"], "path": rec["path"],
                "inSdk": sdk_call is not None, "sdkCall": sdk_call,
                "gItems": sorted(rec["gItems"]), "samples": rec["samples"], "sources": sorted(rec["sources"]),
                "query": sorted(rec["query"]), "headerNames": sorted(rec["headers"]),
                "request": rec["request"],
                "responses": {k: rec["responses"][k] for k in sorted(rec["responses"])},
            }
            by_domain.setdefault(domain_of(rec["path"]), []).append(record)
        for records in by_domain.values():
            records.sort(key=lambda r: (r["path"], r["method"], r["host"] or ""))
        return by_domain


def gather_files(inputs):
    files = []
    for item in inputs:
        if os.path.isdir(item):
            files += [os.path.join(item, f) for f in sorted(os.listdir(item)) if f.lower().endswith(".har")]
        elif os.path.isfile(item):
            files.append(item)
        else:
            die("error: %s is not a file or a directory" % item)
    return files


def main(argv=None):
    ap = argparse.ArgumentParser(description="Extract endpoint descriptions from scrubbed HAR captures. See the module docstring.")
    ap.add_argument("inputs", nargs="*", help="scrubbed .har files or directories (default: docs/research/captures)")
    ap.add_argument("--out", default=DEFAULT_OUT, help="output directory (default: docs/research/endpoints)")
    ap.add_argument("--status-file", default=DEFAULT_STATUS, help="SDK table to compare against (default: docs/endpoint-status.md)")
    ap.add_argument("--dry-run", action="store_true", help="print the summary and write nothing")
    args = ap.parse_args(argv)

    files = gather_files(args.inputs or [DEFAULT_IN])
    if not files:
        die("error: no .har files found (looked in %s)" % (", ".join(args.inputs) if args.inputs else DEFAULT_IN))
    sdk_table = load_sdk_table(args.status_file)
    scrubber = load_scrubber()

    collector = Collector()
    refused = []
    for path in files:
        har, raw = scrubber.load_har(path)
        findings = scrubber.check_har(har, raw, [])
        if findings:
            refused.append((path, findings))
            continue
        source = os.path.basename(path)
        for entry in har["log"]["entries"]:
            if isinstance(entry, dict):
                collector.add(entry, source)
    if refused:
        print("REFUSED: %d input file(s) did not pass the leak check, so nothing was written." % len(refused))
        for path, findings in refused:
            print("  %s: %d problem(s); run scrub-har.py on it, then --check" % (path, len(findings)))
            scrubber.print_findings(findings[:5])
        return 1

    by_domain = collector.finish(sdk_table)
    total = sum(len(v) for v in by_domain.values())
    new = sum(1 for v in by_domain.values() for r in v if not r["inSdk"])
    if not args.dry_run:
        os.makedirs(args.out, exist_ok=True)
        for domain, records in by_domain.items():
            doc = {"domain": domain, "generatedBy": "scripts/research/har-to-endpoints.py (do not edit by hand)",
                   "captures": sorted({s for r in records for s in r["sources"]}), "endpoints": records}
            with open(os.path.join(args.out, domain + ".json"), "w", encoding="utf-8") as fh:
                json.dump(doc, fh, indent=2, ensure_ascii=False)
                fh.write("\n")
    print("%s%d capture file(s), %d endpoint(s): %d already in the SDK, %d NOT in the SDK" % ("(dry run) " if args.dry_run else "", len(files), total, total - new, new))
    for domain in sorted(by_domain):
        records = by_domain[domain]
        flagged = [r for r in records if not r["inSdk"]]
        print("  %-14s %3d endpoint(s), %d not in the SDK" % (domain + ".json", len(records), len(flagged)))
        for r in flagged:
            print("      NEW  %-6s %s%s  %s" % (r["method"], r["apiPrefix"] or "", r["path"], ("[" + ",".join(r["gItems"]) + "]") if r["gItems"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
