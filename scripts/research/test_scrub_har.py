"""Tests for scrub-har.py, using only the synthetic fixture (every value in it is fake).

Run from the repo root:   python3 -m unittest discover -s scripts/research -p "test_*.py" -v
"""
import copy
import hashlib
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
SCRIPT = os.path.join(HERE, "scrub-har.py")
FIXTURE = os.path.join(HERE, "fixtures", "synthetic-capture.har")
OWNER = ["--email", "fake.owner@example.com", "--username", "fakeowner", "--name", "Fake Owner"]
FAKE_SECRETS = [
    "hunter2", "correct horse", "FAKE-TOKEN", "FAKE-SESSION", "FAKE-NEW", "FAKE-REFRESH", "FAKE-API-KEY",
    "FAKE-ACCESS", "FAKE-CONFIRM", "fake.owner@example.com", "fakeowner", "Fake Owner",
    "second.account@example.org", "eyJhbGciOiJub25lIn0", "11111111-1111", "0123456789abcdef01234567",
    "203.0.113.9", "theme=dark", "RIFFfakebytes",
]

spec = importlib.util.spec_from_file_location("scrub_har", SCRIPT)
sh = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sh)


def run(*args):
    return subprocess.run([sys.executable, SCRIPT] + list(args), capture_output=True, text=True)


def sha(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def body(entry):
    return json.loads(entry["response"]["content"]["text"])


class ScrubberTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.out = os.path.join(cls.tmp.name, "out.har")
        cls.fixture_hash = sha(FIXTURE)
        cls.proc = run(FIXTURE, "-o", cls.out, *OWNER)
        with open(cls.out, encoding="utf-8") as fh:
            cls.text = fh.read()
        cls.har = json.loads(cls.text)
        cls.entries = cls.har["log"]["entries"]

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def by_url(self, fragment):
        matches = [e for e in self.entries if fragment in e["request"]["url"]]
        self.assertEqual(len(matches), 1, fragment)
        return matches[0]

    # ----- the basics
    def test_scrub_succeeds_and_self_check_passes(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout + self.proc.stderr)
        self.assertIn("Self-check passed", self.proc.stdout)

    def test_check_passes_on_the_output(self):
        r = run("--check", self.out, *OWNER)
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_no_fake_secret_survives_anywhere(self):
        low = self.text.lower()
        for secret in FAKE_SECRETS:
            self.assertNotIn(secret.lower(), low, secret)

    def test_raw_fixture_fails_the_check_without_printing_values(self):
        r = run("--check", FIXTURE, *OWNER)
        self.assertEqual(r.returncode, 1)
        for secret in FAKE_SECRETS:
            self.assertNotIn(secret.lower(), (r.stdout + r.stderr).lower(), secret)

    # ----- headers and cookies
    def test_credential_headers_and_cookies_are_gone(self):
        for e in self.entries:
            for part in (e["request"], e["response"]):
                names = [h["name"].lower() for h in part["headers"]]
                for bad in ("authorization", "cookie", "set-cookie"):
                    self.assertNotIn(bad, names)
                self.assertEqual(part["cookies"], [])

    def test_other_header_names_are_kept_but_values_redacted(self):
        e = self.by_url("/followers")
        h = {x["name"]: x["value"] for x in e["request"]["headers"]}
        self.assertEqual(h["X-Client-Id"], "REDACTED")
        self.assertEqual(h["User-Agent"], "REDACTED")
        self.assertEqual(h["Accept"], "application/json")
        r = {x["name"]: x["value"] for x in e["response"]["headers"]}
        self.assertEqual(r["Content-Type"], "application/json")

    # ----- entries
    def test_static_assets_and_preflights_are_dropped(self):
        self.assertEqual(len(self.entries), 11)
        for e in self.entries:
            self.assertNotRegex(e["request"]["url"], r"\.(js|png)$")
            self.assertNotEqual(e["request"]["method"], "OPTIONS")
        self.assertIn("cdn.example.test (2)", self.har["log"]["comment"])

    def test_only_known_fields_are_kept(self):
        for e in self.entries:
            for key in e:
                self.assertIn(key, ("pageref", "startedDateTime", "time", "request", "response", "cache", "timings", "_resourceType"))
        self.assertEqual(self.har["log"]["pages"][0]["title"], "REDACTED")

    # ----- ids and identifiers
    def test_placeholders_are_stable_and_distinct(self):
        followers = self.by_url("/followers")
        me = self.by_url("/me")
        owner_in_path = re.search(r"/users/(UUID-\d{4})/", followers["request"]["url"]).group(1)
        self.assertEqual(body(me)["id"], owner_in_path)
        ids = {i["id"] for i in body(followers)["items"]}
        self.assertEqual(len(ids), 5)
        self.assertNotIn(owner_in_path, ids)
        self.assertRegex(self.by_url("/objects/")["request"]["url"], r"/objects/HEX-0001\?x=1$")

    def test_owner_identifiers_and_emails_are_replaced(self):
        m = body(self.by_url("/me"))
        self.assertEqual((m["username"], m["name"], m["email"]), ("OWNER-USERNAME", "OWNER-NAME", "OWNER-EMAIL"))
        self.assertEqual(m["bio"], "Contact me at OWNER-EMAIL")
        self.assertEqual(body(self.by_url("/followers"))["items"][1]["email"], "EMAIL-0001")

    # ----- bodies
    def test_sensitive_values_redacted_but_keys_and_shapes_kept(self):
        m = body(self.by_url("/me"))
        self.assertEqual(m["refresh_token"], "REDACTED")
        self.assertEqual(m["jwt"], "REDACTED")
        self.assertEqual(m["settings"], {"apiKey": "REDACTED", "theme": "dark"})
        self.assertIs(m["hasPassword"], True)
        item = body(self.by_url("/followers"))["items"][0]
        self.assertEqual(item["tokenCount"], 3)
        self.assertIs(item["hasPassword"], True)
        sent = json.loads(self.by_url("/passwords")["request"]["postData"]["text"])
        self.assertEqual(sent, {"oldPassword": "REDACTED", "newPassword": "REDACTED"})

    def test_long_arrays_are_shortened_with_a_note(self):
        e = self.by_url("/followers")
        data = body(e)
        self.assertEqual((len(data["items"]), data["total"]), (5, 8))
        self.assertEqual(e["response"]["content"]["comment"], "1 long array(s) shortened to 5 items")

    def test_non_json_bodies_are_omitted_and_json_bodies_kept(self):
        upload = self.by_url("/upload")
        self.assertNotIn("text", upload["request"]["postData"])
        self.assertIn("body omitted", upload["request"]["postData"]["comment"])
        self.assertEqual(body(upload)["status"], "processing")
        html = self.by_url("/confirm")
        self.assertNotIn("text", html["response"]["content"])
        for e in self.entries:
            text = e["response"]["content"].get("text")
            if text:
                json.loads(text)

    def test_form_bodies(self):
        pd = self.by_url("/forms/example")["request"]["postData"]
        params = {p["name"]: p["value"] for p in pd["params"]}
        self.assertEqual(params, {"username": "OWNER-USERNAME", "password": "REDACTED", "remember": "1"})
        self.assertEqual(pd["text"], "username=OWNER-USERNAME&password=REDACTED&remember=1")

    # ----- urls
    def test_urls(self):
        e = self.by_url("/followers")
        q = {p["name"]: p["value"] for p in e["request"]["queryString"]}
        self.assertEqual(q["access_token"], "REDACTED")
        self.assertEqual(q["q"], "guitar")
        self.assertIn("access_token=REDACTED", e["request"]["url"])
        self.assertIn("q=guitar", e["request"]["url"])
        self.assertEqual(self.by_url("/go")["response"]["redirectURL"], "https://www.example.test/home?access_token=REDACTED")
        self.assertEqual(self.by_url("/ping")["request"]["url"], "https://api.example.test/ping")
        self.assertIn("email=OWNER-EMAIL", self.by_url("/search")["request"]["url"])
        self.assertNotIn("#", "".join(e["request"]["url"] + e["response"]["redirectURL"] for e in self.entries))

    # ----- safety of the files themselves
    def test_input_unchanged_and_overwrite_protection(self):
        self.assertEqual(sha(FIXTURE), self.fixture_hash)
        r = run(FIXTURE, "-o", FIXTURE, *OWNER)
        self.assertEqual(r.returncode, 2)
        self.assertEqual(sha(FIXTURE), self.fixture_hash)
        again = run(FIXTURE, "-o", self.out, *OWNER)
        self.assertEqual(again.returncode, 2)
        self.assertEqual(run(FIXTURE, "-o", self.out, "--force", *OWNER).returncode, 0)

    def test_scrubbing_twice_changes_nothing(self):
        second = os.path.join(self.tmp.name, "second.har")
        self.assertEqual(run(self.out, "-o", second, *OWNER).returncode, 0, "second pass")
        with open(second, encoding="utf-8") as fh:
            again = json.load(fh)
        a, b = copy.deepcopy(self.har), again
        a["log"].pop("comment"), b["log"].pop("comment")
        self.assertEqual(a, b)

    def test_failed_self_check_deletes_the_output(self):
        # "REDACTED" is the scrubber's own placeholder, so a username equal to it can never pass the check.
        out = os.path.join(self.tmp.name, "never.har")
        r = run(FIXTURE, "-o", out, "--username", "REDACTED")
        self.assertEqual(r.returncode, 1, r.stdout)
        self.assertFalse(os.path.exists(out))


class CheckerTest(unittest.TestCase):
    """The checker must catch leaks planted into an otherwise clean file."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        out = os.path.join(cls.tmp.name, "clean.har")
        assert run(FIXTURE, "-o", out, *OWNER).returncode == 0
        with open(out, encoding="utf-8") as fh:
            cls.clean = json.load(fh)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def check(self, har):
        path = os.path.join(self.tmp.name, "planted.har")
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(har, fh, indent=2)
        return run("--check", path, *OWNER)

    def planted(self, mutate):
        har = copy.deepcopy(self.clean)
        mutate(har["log"]["entries"][0])
        return self.check(har)

    def test_clean_file_passes(self):
        self.assertEqual(self.check(self.clean).returncode, 0)

    def test_each_planted_leak_is_caught(self):
        leaks = {
            "authorization header": lambda e: e["request"]["headers"].append({"name": "Authorization", "value": "REDACTED"}),
            "cookie header": lambda e: e["request"]["headers"].append({"name": "Cookie", "value": "REDACTED"}),
            "cookie list": lambda e: e["request"]["cookies"].append({"name": "a", "value": "b"}),
            "header value kept": lambda e: e["request"]["headers"].append({"name": "X-Device", "value": "abc"}),
            "email in url": lambda e: e["request"].update(url=e["request"]["url"] + "&e=someone@example.org"),
            "uuid in url": lambda e: e["request"].update(url=e["request"]["url"] + "&id=22222222-2222-4222-8222-222222222222"),
            "long hex id": lambda e: e["request"].update(url=e["request"]["url"] + "&h=0123456789abcdef01234567"),
            "bearer token in a body": lambda e: e["response"]["content"].update(text=json.dumps({"note": "Bearer abcdefghijkl"})),
            "jwt in a body": lambda e: e["response"]["content"].update(text=json.dumps({"x": "eyJhbGciOiJub25lIn0.eyJmYWtlIjp0cnVlfQ.ZmFrZXNpZw"})),
            "sensitive key with a real value": lambda e: e["response"]["content"].update(text=json.dumps({"password": "hunter2"})),
            "sensitive query value": lambda e: e["request"]["queryString"].append({"name": "token", "value": "abc"}),
            "sensitive query value in the url": lambda e: e["request"].update(url=e["request"]["url"] + "&token=abc"),
            "sensitive query value in a :path header": lambda e: e["request"]["headers"].append({"name": ":path", "value": "/a?token=abc"}),
            "url fragment": lambda e: e["request"].update(url=e["request"]["url"] + "#access_token=abc"),
            "sensitive query value in a redirect": lambda e: e["response"].update(redirectURL="https://www.example.test/x?access_token=abc"),
            "owner username": lambda e: e["response"]["content"].update(text=json.dumps({"who": "fakeowner"})),
            "credentials in url": lambda e: e["request"].update(url="https://user:pw@api.example.test/x"),
            "binary body": lambda e: e["response"]["content"].update(encoding="base64", text="AAAA"),
            "html body": lambda e: e["response"]["content"].update(mimeType="text/html", text="<html></html>"),
            "static asset entry": lambda e: e["request"].update(url="https://cdn.example.test/a.js"),
            "preflight entry": lambda e: e["request"].update(method="OPTIONS"),
        }
        for label, mutate in leaks.items():
            with self.subTest(label):
                r = self.planted(mutate)
                self.assertEqual(r.returncode, 1, label + "\n" + r.stdout)
                self.assertNotIn("hunter2", r.stdout)


class HelpersTest(unittest.TestCase):
    def test_sensitive_key_detection(self):
        for key in ("password", "oldPassword", "refresh_token", "accessToken", "apiKey", "APIKey", "Authorization", "sessionId",
                    "verificationCode", "otp", "pin", "secret"):
            self.assertTrue(sh.is_sensitive_key(key), key)
        for key in ("username", "content", "tokenizer", "pinned", "mapping", "author", "authorId",
                    "code", "id", "email", "name"):
            self.assertFalse(sh.is_sensitive_key(key), key)

    def test_json_mime(self):
        for m in ("application/json", "application/vnd.api+json", "text/json"):
            self.assertTrue(sh.is_json_mime(m), m)
        self.assertFalse(sh.is_json_mime("text/html"))


class OddShapesTest(unittest.TestCase):
    """Real browser HARs are messier than the fixture: nothing may crash, and URL-like headers must be scrubbed."""

    def test_odd_shapes(self):
        odd = {"log": {"version": "1.2", "pages": [{"title": "x"}, "junk"], "entries": [
            {"request": {"method": "GET", "url": "https://api.example.test/a",
                         "headers": [{"name": ":authority", "value": "api.example.test"}, {"name": ":path", "value": "/a?token=zzz"},
                                     {"name": "Referer", "value": "https://www.example.test/p?access_token=abc#x"},
                                     {"name": "X-Null", "value": None}, {"name": "X-Num", "value": 5}]},
             "response": {"status": 200, "content": {"mimeType": "application/json", "text": "[]"}}},
            {"request": {"method": "POST", "url": "https://api.example.test/b",
                         "postData": {"mimeType": "application/x-www-form-urlencoded", "params": [{"name": "password", "value": "x"}, {"name": "a", "value": None}]}},
             "response": {"status": 204}},
            {"request": {"method": "GET", "url": "https://api.example.test/c"},
             "response": {"status": 200, "content": {"mimeType": "application/json", "text": "not json at all"}}},
            {"request": {"method": "GET", "url": "https://api.example.test/d"},
             "response": {"status": 200, "content": {"mimeType": "application/json",
                          "text": "{\"password\":null,\"token\":false,\"tokenValue\":12345,\"list\":[[1,2,3,4,5,6,7],{\"secret\":{\"a\":1}}]}"}}},
            "not-a-dict", 7, None, {"request": {}, "response": {}},
            {"request": {"method": "GET", "url": None}, "response": {"content": None}},
            {"request": {"method": "POST", "url": "https://api.example.test/e", "postData": {"mimeType": "application/json", "text": "{broken"}},
             "response": {"status": 500, "content": {"mimeType": "application/json; charset=utf-8", "text": "{\"ok\":true}"}}},
        ]}}
        with tempfile.TemporaryDirectory() as tmp:
            src, out = os.path.join(tmp, "odd.har"), os.path.join(tmp, "odd.out.har")
            with open(src, "w") as fh:
                json.dump(odd, fh)
            r = run(src, "-o", out)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            with open(out, encoding="utf-8") as fh:
                entries = json.load(fh)["log"]["entries"]
            headers = {h["name"]: h["value"] for h in entries[0]["request"]["headers"]}
            self.assertEqual(headers[":path"], "/a?token=REDACTED")
            self.assertEqual(headers["Referer"], "https://www.example.test/p?access_token=REDACTED")
            self.assertEqual(headers[":authority"], "api.example.test")
            d = json.loads(entries[3]["response"]["content"]["text"])
            self.assertEqual(d, {"password": None, "token": False, "tokenValue": 12345, "list": [[1, 2, 3, 4, 5], {"secret": "REDACTED"}]})
            self.assertEqual(run("--check", out).returncode, 0)


class CliErrorsTest(unittest.TestCase):
    def test_bad_inputs_exit_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            notjson = os.path.join(tmp, "a.har")
            nothar = os.path.join(tmp, "b.har")
            with open(notjson, "w") as fh:
                fh.write("{nope")
            with open(nothar, "w") as fh:
                fh.write('{"hello": 1}')
            cases = {
                "missing file": [os.path.join(tmp, "missing.har")],
                "invalid json": [notjson],
                "not a har": [nothar],
                "short username": [FIXTURE, "--username", "ab"],
                "bad email": [FIXTURE, "--email", "nope"],
                "bad max-items": [FIXTURE, "--max-items", "0"],
            }
            for label, args in cases.items():
                with self.subTest(label):
                    self.assertEqual(run(*args).returncode, 2, label)


if __name__ == "__main__":
    unittest.main()
