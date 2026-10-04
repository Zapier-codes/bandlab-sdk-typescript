# Hand-back — how captured evidence gets into the repo

`CAPTURE-GUIDE.md` says what to capture. This file says what happens to a capture afterwards: the layout, the file names, the checks, and the routes from your phone to a session. The tick-list is `CAPTURE-CHECKLIST.md`.

## 1. The one rule

**Only scrubbed files ever enter the repo. Raw captures stay on your device.** A raw HAR holds access tokens, cookies, your email and your ids. The scrubbing tool is built in leaf `2.a.ii.zi`. Until it exists, **the only things you can hand back are P0 (one line, no secrets) and your own written notes.** Capturing now is fine; just do not send the files yet.

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

## 4. Check a file before you send it

Run these on the **scrubbed** file (in Termux or on a computer). Every command must print **0**:

```bash
f=G01-03-send-message.har
grep -ciE 'authorization|cookie|bearer|password|access_token|refresh_token' "$f"
grep -ci 'your-email-address@example.com' "$f"     # put your real address here
grep -ci 'your-username' "$f"                      # and your BandLab username
```

(`grep -c` counts matching *lines*; a HAR can be one very long line, so only "0 or not 0" means anything.)

These checks lower the risk; they do not prove a file is clean. **Skim the file as well.** Search it for your name, phone number, and any long random-looking strings. If anything personal is left, do not send it, and tell me which scrubber step missed it.

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
Files: attached, scrubbed, section 4 checks all 0
Anything odd: <for example: the app asked me to log in again halfway through>
```

## 6. What this asks of the scrubber (leaf `2.a.ii.zi`)

The scrubber's output must pass the section 4 checks for **any** address and username, and must also:
- drop request and response headers that carry credentials, and all cookies;
- replace tokens, the owner's email, user ids and other personal ids with stable placeholders (the same id gets the same placeholder inside a file, so request and response still line up);
- drop static assets (images, fonts, scripts, CSS) and binary bodies, and keep JSON bodies;
- keep method, full URL (host and path), query keys, status, and request and response JSON shapes. These are the evidence.
- never modify the original file; write the scrubbed result to a separate file with the checklist name.

## 7. What a session does when evidence arrives

1. Run the section 4 checks itself. **If any file fails, do not commit it**; tell the owner which check failed.
2. Copy accepted files into `captures/` under the exact names in the checklist.
3. In `CAPTURE-CHECKLIST.md`, set *In repo* to `[x]` and fill *Result* and *Note* for each row the owner reported, including `no-such-action`, `not-capturable` and `skipped`.
4. Commit it as `<current leaf path>: evidence intake, <files>`, with one commit per logical set, and mention it in that leaf's Done note.
5. Evidence intake is **not a leaf**. It does not change N of M, and it does not triage anything. Triage (setting each G-item to captured, missing or blocked, and recording the resource design) stays in leaves `2.b.i.zi` and `2.b.i.zo`.
