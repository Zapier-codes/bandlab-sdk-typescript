"""Tests for har-to-endpoints.py. Captures are produced by running the scrubber on the synthetic fixture.

Run from the repo root:   python3 -m unittest discover -s scripts/research -p "test_*.py" -v
"""
import hashlib
import importlib.util
import json
import os
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
SCRUB = os.path.join(HERE, "scrub-har.py")
EXTRACT = os.path.join(HERE, "har-to-endpoints.py")
FIXTURE = os.path.join(HERE, "fixtures", "synthetic-capture.har")
STATUS = os.path.join(REPO, "docs", "endpoint-status.md")
OWNER = ["--email", "fake.owner@example.com", "--username", "fakeowner", "--name", "Fake Owner"]

spec = importlib.util.spec_from_file_location("har_to_endpoints", EXTRACT)
ex = importlib.util.module_from_spec(spec)
spec.loader.exec_module(ex)


def run(script, *args):
    return subprocess.run([sys.executable, script] + list(args), capture_output=True, text=True)


def read_all(directory):
    out = {}
    for name in sorted(os.listdir(directory)):
        with open(os.path.join(directory, name), encoding="utf-8") as fh:
            out[name] = fh.read()
    return out


class ShapeTest(unittest.TestCase):
    def test_primitives_and_kinds(self):
        self.assertEqual(ex.shape_of(None), "null")
        self.assertEqual(ex.shape_of(True), "boolean")
        self.assertEqual(ex.shape_of(3), "integer")
        self.assertEqual(ex.shape_of(3.5), "number")
        for value, kind in (("UUID-0001", "uuid"), ("HEX-0002", "hex-id"), ("OWNER-EMAIL", "email"), ("EMAIL-0003", "email"),
                            ("OWNER-USERNAME", "username"), ("OWNER-NAME", "name"), ("REDACTED", "redacted"),
                            ("2026-01-01T10:00:00Z", "datetime"), ("hello", "string")):
            self.assertEqual(ex.shape_of(value), kind, value)

    def test_shapes_never_contain_values(self):
        shape = ex.shape_of({"title": "A secret title", "tags": ["alpha", "beta"], "n": 42})
        self.assertEqual(shape, {"title": "string", "tags": ["string"], "n": "integer"})
        self.assertNotIn("secret", json.dumps(shape))

    def test_merging_primitives(self):
        self.assertEqual(ex.merge("integer", "number"), "number")
        self.assertEqual(ex.merge("uuid", "string"), "string")
        self.assertEqual(ex.merge("uuid", "null"), "null|uuid")
        self.assertEqual(ex.merge("email", "uuid"), "string")
        self.assertEqual(ex.merge("boolean", "boolean"), "boolean")

    def test_merging_objects_marks_optional_keys(self):
        merged = ex.merge({"a": "string"}, {"b": "integer"})
        self.assertEqual(merged, {"a?": "string", "b?": "integer"})
        again = ex.merge(merged, {"a": "string", "b": "integer"})
        self.assertEqual(again, {"a?": "string", "b?": "integer"})
        both = ex.merge({"a": "string", "c": "boolean"}, {"a": "null", "c": "boolean"})
        self.assertEqual(both, {"a": "null|string", "c": "boolean"})

    def test_merging_lists(self):
        self.assertEqual(ex.merge([], ["string"]), ["string"])
        self.assertEqual(ex.merge(["string"], []), ["string"])
        self.assertEqual(ex.merge([{"a": "string"}], [{"b": "integer"}]), [{"a?": "string", "b?": "integer"}])
        self.assertEqual(ex.shape_of([1, 2.5, None]), ["null|number"])
        self.assertEqual(ex.shape_of([]), [])

    def test_merging_mixed_kinds_makes_a_union(self):
        self.assertEqual(ex.merge("null", {"a": "string"}), {"$union": ["null", {"a": "string"}]})
        self.assertEqual(ex.merge({"a": "string"}, ["string"]), {"$union": [{"a": "string"}, ["string"]]})
        merged = ex.merge({"$union": ["null", {"a": "string"}]}, {"b": "integer"})
        self.assertEqual(merged, {"$union": ["null", {"a?": "string", "b?": "integer"}]})


class PathTest(unittest.TestCase):
    def test_template_path(self):
        cases = {
            "/api/v1.3/users/UUID-0001/followers": ("/api/v1.3", "/users/{id}/followers"),
            "/api/v1.3/objects/HEX-0004": ("/api/v1.3", "/objects/{id}"),
            "/songs/UUID-0001/revisions/UUID-0002/forks": (None, "/songs/{id}/revisions/{id}/forks"),
            "/posts/12345/likes": (None, "/posts/{id}/likes"),
            "/users/OWNER-USERNAME": (None, "/users/{username}"),
            "/search/EMAIL-0001": (None, "/search/{email}"),
            "/api/v1.3": ("/api/v1.3", "/"),
            "/me": (None, "/me"),
        }
        for path, expected in cases.items():
            self.assertEqual(ex.template_path(path), expected, path)

    def test_split_url(self):
        self.assertEqual(ex.split_url("https://api.example.test/api/v1.3/me?x=1"), ("api.example.test", "/api/v1.3/me", "x=1"))
        self.assertEqual(ex.split_url("https://api.example.test"), ("api.example.test", "/", ""))

    def test_domain_of(self):
        cases = {
            "/me": "account", "/passwords": "account", "/users/{id}": "users", "/users/{id}/followers": "followers",
            "/users/{id}/notifications": "notifications", "/songs/{id}/invites": "invitations", "/songs/{id}/collaborators": "collaborators",
            "/songs/{id}/revisions/{id}/forks": "revisions", "/posts/{id}/comments": "comments", "/posts/{id}/likes": "likes",
            "/bands/{id}/members": "bands", "/collections/{id}/posts": "posts", "/conversations/{id}/messages": "messaging",
            "/settings/notifications/push": "settings", "/forms/example": "unknown", "/": "unknown",
        }
        for path, domain in cases.items():
            self.assertEqual(ex.domain_of(path), domain, path)

    def test_sdk_table_matches_endpoint_status(self):
        table = ex.load_sdk_table(STATUS)
        self.assertEqual(len(table), 123)
        self.assertEqual(table[ex.normalise("get", "/users/{id}/followers")], "client.users.followers.list()")
        self.assertEqual(table[ex.normalise("PUT", "/passwords")], "client.passwords.change()")
        self.assertNotIn(ex.normalise("get", "/messages"), table)


class PipelineTest(unittest.TestCase):
    """fixture -> scrub-har.py -> har-to-endpoints.py"""

    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.caps = os.path.join(cls.tmp.name, "caps")
        os.makedirs(cls.caps)
        first = os.path.join(cls.caps, "G04-02-list-my-songs.har")
        assert run(SCRUB, FIXTURE, "-o", first, *OWNER).returncode == 0
        # a second capture of the same endpoints, with a different followers body, to test merging
        with open(first, encoding="utf-8") as fh:
            har = json.load(fh)
        for entry in har["log"]["entries"]:
            if entry["request"]["url"].endswith("followers?limit=20&q=guitar&userId=UUID-0001&access_token=REDACTED"):
                body = json.loads(entry["response"]["content"]["text"])
                for item in body["items"]:
                    item.pop("email")
                    item["badge"] = "gold"
                entry["response"]["content"]["text"] = json.dumps(body)
        with open(os.path.join(cls.caps, "G06-01-create-post.har"), "w", encoding="utf-8") as fh:
            json.dump(har, fh, indent=2)
        cls.out = os.path.join(cls.tmp.name, "out")
        cls.proc = run(EXTRACT, cls.caps, "--out", cls.out, "--status-file", STATUS)
        cls.files = read_all(cls.out)
        cls.docs = {name[:-5]: json.loads(text) for name, text in cls.files.items()}

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def endpoint(self, domain, method, path):
        matches = [e for e in self.docs[domain]["endpoints"] if (e["method"], e["path"]) == (method, path)]
        self.assertEqual(len(matches), 1, (domain, method, path))
        return matches[0]

    def test_runs_and_writes_one_file_per_domain(self):
        self.assertEqual(self.proc.returncode, 0, self.proc.stdout + self.proc.stderr)
        self.assertEqual(sorted(self.files), ["account.json", "comments.json", "followers.json", "search.json", "unknown.json"])
        self.assertIn("2 capture file(s), 11 endpoint(s): 5 already in the SDK, 6 NOT in the SDK", self.proc.stdout)

    def test_flags_endpoints_missing_from_the_sdk(self):
        new = sorted((e["method"], e["path"]) for d in self.docs.values() for e in d["endpoints"] if not e["inSdk"])
        self.assertEqual(new, [("GET", "/confirm"), ("GET", "/go"), ("GET", "/objects/{id}"), ("GET", "/ping"), ("POST", "/forms/example"), ("POST", "/upload")])
        known = self.endpoint("followers", "GET", "/users/{id}/followers")
        self.assertTrue(known["inSdk"])
        self.assertEqual(known["sdkCall"], "client.users.followers.list()")
        self.assertIsNone(self.endpoint("unknown", "GET", "/ping")["sdkCall"])

    def test_prefix_host_query_headers_statuses(self):
        e = self.endpoint("followers", "GET", "/users/{id}/followers")
        self.assertEqual((e["host"], e["apiPrefix"]), ("api.example.test", "/api/v1.3"))
        self.assertEqual(e["query"], ["access_token", "limit", "q", "userId"])
        self.assertIn("X-Client-Id", e["headerNames"])
        self.assertEqual(list(e["responses"]), ["200"])
        self.assertEqual(self.endpoint("account", "PUT", "/passwords")["responses"]["204"], {"contentType": None, "shape": None})
        self.assertIsNone(self.endpoint("unknown", "POST", "/upload")["apiPrefix"])

    def test_merges_samples_across_captures(self):
        e = self.endpoint("followers", "GET", "/users/{id}/followers")
        self.assertEqual(e["samples"], 2)
        self.assertEqual(e["sources"], ["G04-02-list-my-songs.har", "G06-01-create-post.har"])
        self.assertEqual(e["gItems"], ["G04", "G06"])
        item = e["responses"]["200"]["shape"]["items"][0]
        self.assertEqual(item["id"], "uuid")
        self.assertEqual(item["email?"], "email|null")
        self.assertEqual(item["badge?"], "string")
        self.assertEqual(item["tokenCount"], "integer")
        self.assertEqual(item["hasPassword"], "boolean")

    def test_request_shapes_and_notes(self):
        self.assertEqual(self.endpoint("account", "PUT", "/passwords")["request"]["shape"], {"oldPassword": "redacted", "newPassword": "redacted"})
        form = self.endpoint("unknown", "POST", "/forms/example")["request"]
        self.assertEqual((form["contentType"], form["shape"]), ("application/x-www-form-urlencoded", {"username": "username", "password": "redacted", "remember": "string"}))
        upload = self.endpoint("unknown", "POST", "/upload")["request"]
        self.assertEqual(upload["contentType"], "multipart/form-data")
        self.assertIsNone(upload["shape"])
        self.assertEqual(upload["note"], "body omitted (multipart/form-data)")

    def test_no_value_from_the_captures_reaches_the_output(self):
        blob = "\n".join(self.files.values()).lower()
        for value in ("nice track", "user0", "guitar", "processing", "gold", "hunter", "fake", "owner-", "uuid-0", "hex-0", "email-0", "correct horse", "dark"):
            self.assertNotIn(value, blob, value)

    def test_output_is_deterministic_and_dry_run_writes_nothing(self):
        again = os.path.join(self.tmp.name, "again")
        self.assertEqual(run(EXTRACT, self.caps, "--out", again, "--status-file", STATUS).returncode, 0)
        self.assertEqual(read_all(again), self.files)
        dry = os.path.join(self.tmp.name, "dry")
        r = run(EXTRACT, self.caps, "--out", dry, "--status-file", STATUS, "--dry-run")
        self.assertEqual(r.returncode, 0)
        self.assertIn("(dry run)", r.stdout)
        self.assertFalse(os.path.exists(dry))

    def test_accepts_single_files_as_well_as_directories(self):
        out = os.path.join(self.tmp.name, "single")
        r = run(EXTRACT, os.path.join(self.caps, "G04-02-list-my-songs.har"), "--out", out, "--status-file", STATUS)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(self.docs.keys(), {n[:-5] for n in os.listdir(out)})


class RefusalTest(unittest.TestCase):
    def test_unscrubbed_input_is_refused_and_nothing_is_written(self):
        with tempfile.TemporaryDirectory() as tmp:
            caps = os.path.join(tmp, "caps")
            os.makedirs(caps)
            good = os.path.join(caps, "G01-01-good.har")
            assert run(SCRUB, FIXTURE, "-o", good, *OWNER).returncode == 0
            with open(FIXTURE, "rb") as src, open(os.path.join(caps, "G01-02-raw.har"), "wb") as dst:
                dst.write(src.read())
            out = os.path.join(tmp, "out")
            r = run(EXTRACT, caps, "--out", out, "--status-file", STATUS)
            self.assertEqual(r.returncode, 1, r.stdout)
            self.assertIn("REFUSED", r.stdout)
            self.assertIn("G01-02-raw.har", r.stdout)
            self.assertNotIn("G01-01-good.har:", r.stdout)
            self.assertFalse(os.path.exists(out), "all-or-nothing: the good file must not be written either")
            for secret in ("hunter2", "FAKE-TOKEN", "fake.owner@example.com"):
                self.assertNotIn(secret, r.stdout + r.stderr)

    def test_bad_inputs_exit_2(self):
        with tempfile.TemporaryDirectory() as tmp:
            empty = os.path.join(tmp, "empty")
            os.makedirs(empty)
            not_json = os.path.join(tmp, "x.har")
            with open(not_json, "w") as fh:
                fh.write("{nope")
            bad_status = os.path.join(tmp, "status.md")
            with open(bad_status, "w") as fh:
                fh.write("no table here\n")
            cases = {
                "no har files in the directory": [empty, "--status-file", STATUS],
                "missing path": [os.path.join(tmp, "missing"), "--status-file", STATUS],
                "invalid json": [not_json, "--status-file", STATUS],
                "missing status file": [FIXTURE, "--status-file", os.path.join(tmp, "nope.md")],
                "status file without rows": [FIXTURE, "--status-file", bad_status],
            }
            for label, args in cases.items():
                with self.subTest(label):
                    self.assertEqual(run(EXTRACT, *args).returncode, 2, label)


if __name__ == "__main__":
    unittest.main()
