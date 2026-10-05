# Hand-back — how captured evidence gets into the repo

`CAPTURE-GUIDE.md` says what to capture. This file says what happens to a capture afterwards: the layout, the file names, the checks, and the routes from your phone to a session. The tick-list is `CAPTURE-CHECKLIST.md`.

## 1. The one rule

**Only scrubbed files ever enter the repo. Raw captures stay on your device.** A raw HAR holds access tokens, cookies, your email and your ids. Scrub every capture with `scripts/research/scrub-har.py` (section 4) and run its check before you hand anything back. P0 (one line, no secrets) and your written notes need no scrubbing.

## 2. Layout

```text
docs/research/
├── CAPTURE-GUIDE.md        what to capture
├── CAPTURE-CHECKLIST.md    the 42 rows; sessions keep the "In repo" and "Result" columns current
├── HAND-BACK.md            this file
├── captures/               SCRUBBED evidence only; this is the only place evidence is committed
├── raw/                    optional, local only: if you keep raw HARs inside your clone, keep them here.
│                           Git ignores this folder, so a raw file cannot be committed from it by accident.
└── endpoints/              created later by leaf 2.a.ii.zo: extracted endpoint descriptions per domain
```

`.gitignore` also ignores any file named `*.raw.har`, so a raw file that is named as raw cannot be committed even outside `raw/`.

## 3. File names

`<ID>-<nn>-<slug>.har`, exactly as listed in `CAPTURE-CHECKLIST.md`: for example `G01-03-send-message.har`. This extends the plan's `<G-id>-<action>` with a two-digit step number so the files sort in the order you did them.

- **P0** is a plain text file: `P0-base-host.txt`.
- A small capture that you paste as text instead of attaching keeps the same name but ends in `.json` (or `.txt`).
- If a task has no matching file because **the app has no such action**, do not make an empty file. Say so in your hand-back message; the session records it in the checklist as `no-such-action`.

## 4. Scrub a file, then check it, before you send it

You need Python 3.8 or newer (`python3 --version`). The script uses only the standard library, so there is nothing to install. (In Termux, `pkg install python` provides it; that command is from memory, so check Termux's own instructions if it fails.)

From the repo root, with your raw file somewhere git ignores (`docs/research/raw/` is ignored):

```bash
python3 scripts/research/scrub-har.py docs/research/raw/my-raw-capture.har \
    -o docs/research/captures/G01-03-send-message.har \
    --email you@example.com --username yourname --name "Your Real Name"

python3 scripts/research/scrub-har.py --check docs/research/captures/G01-03-send-message.har \
    --email you@example.com --username yourname --name "Your Real Name"
```

- `-o` is the exact file name from `CAPTURE-CHECKLIST.md`. The original is never modified, an existing output is never overwritten without `--force`, and the scrubber **deletes its own output if its self-check fails**.
- Pass `--email`, `--username` and `--name` (each can be repeated). They are replaced everywhere and the check fails if any is still present. Any other email address is replaced automatically.
- `--check` must print `CHECK PASSED` (exit code 0). When it fails it lists *what* kind of problem and *where* (a path such as `$.log.entries[3].request.headers[1]`), and never prints the secret value itself.

**Why not just search the file for the word "password"?** Because the words legitimately appear: the profile response has a `hasPassword` field and one endpoint is `/passwords`. A word search raises false alarms and teaches you to ignore it. The scrubber and the check look at *values* of sensitive keys, not the words, and keep key names because key names are the evidence.

**What the scrubber keeps:** method, full URL (host and path), query keys, status, the shape of JSON request and response bodies, and the *names* of headers. **What it removes:** credential headers and cookies, header values, static assets, non-JSON bodies, URL fragments, and every email address, UUID, long hex id, JWT, bearer token and the values of keys like `password`, `token` and `secret`. Long JSON arrays are shortened to 5 items. See `python3 scripts/research/scrub-har.py --help`.

**It is best effort, not proof.** It cannot know a secret it does not recognise (a numeric PIN under an unusual key name, a name typed into a free-text comment). **Skim the scrubbed file before you send it:** search it for your name, your phone number and any long random-looking strings, and if anything personal is left, do not send it and tell me what was missed.

One optional extra check for credential header names (it must print `0`):

```bash
grep -ciE '"name": *"(authorization|cookie|set-cookie)"' docs/research/captures/G01-03-send-message.har
```

## 5. Three ways to hand files back

| Route | How | Good for | Limits |
|-------|-----|----------|--------|
| **1. Upload into a chat session** (recommended) | Attach the scrubbed files to a message in a session. The session checks them (section 7), copies them into `captures/`, updates the checklist and commits. | HAR files | I do not know this chat's upload size limit. Keep files small; the scrubber drops images, fonts and other static assets for that reason. |
| **2. Commit them yourself from the phone** | `git add docs/research/captures/<file>`, commit, `git push` from Termux, as you already do for patches. | You prefer to keep files out of chats | Files reach `origin/main` unreviewed, so run the section 4 checks first. A session must then `git fetch` before working (its start checklist already does this). |
| **3. Paste text into the message** | Paste the scrubbed request and response JSON, or the P0 line, straight into the chat. The session saves it as `<name>.json` or `.txt`. | P0 and very small captures; a phone-only workflow | Long HARs do not fit. |

### A message you can copy
```text
Evidence hand-back
Done: G01.01, G01.02, G01.03 (captured); G01.05 (no-such-action: the app has no mark-read); G05 (skipped: no throwaway song)
Accounts: own; second account received the message in G01.03
Client: <browser and version, or "phone browser through <tool>">
Files: attached, scrubbed, --check passed on each
Anything odd: <for example: the app asked me to log in again halfway through>
```

## 6. What the scrubber does (leaf `2.a.ii.zi`, built)

These were the requirements; `scripts/research/scrub-har.py` meets them, and `scripts/research/test_scrub_har.py` tests each one against a synthetic capture full of fake secrets:
- its output passes `--check` for any address and username you give it;
- credential headers and all cookies are dropped, other header values are replaced with `REDACTED`;
- tokens, your email and any other email, UUIDs, long hex ids and JWTs are replaced with stable placeholders (the same id gets the same placeholder inside a file, so a request and its response still line up): `UUID-0001`, `HEX-0001`, `EMAIL-0001`, `OWNER-EMAIL`, `OWNER-USERNAME`, `OWNER-NAME`;
- static assets (images, fonts, scripts, CSS, media), OPTIONS preflights and non-JSON bodies are dropped, and JSON bodies are kept;
- method, full URL (host and path), query keys, status, and request and response JSON shapes are kept, because they are the evidence;
- the original file is never modified; the result goes to a separate file with the checklist name.

## 7. What a session does when evidence arrives

1. Run `python3 scripts/research/scrub-har.py --check <file>` itself, with the owner's `--email`, `--username` and `--name` if they gave them. **If any file fails, do not commit it**; tell the owner which kind of problem and where. A scrubbed `.har` that passes still gets a quick skim.
2. Copy accepted files into `captures/` under the exact names in the checklist.
3. In `CAPTURE-CHECKLIST.md`, set *In repo* to `[x]` and fill *Result* and *Note* for each row the owner reported, including `no-such-action`, `not-capturable` and `skipped`.
4. Commit it as `<current leaf path>: evidence intake, <files>`, with one commit per logical set, and mention it in that leaf's Done note.
5. Evidence intake is **not a leaf**. It does not change N of M, and it does not triage anything. Triage (setting each G-item to captured, missing or blocked, and recording the resource design) stays in leaves `2.b.i.zi` and `2.b.i.zo`.
