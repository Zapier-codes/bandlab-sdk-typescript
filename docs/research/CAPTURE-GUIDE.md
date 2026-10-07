# Capture Guide — how to record BandLab's own requests from your own account

**Why this exists.** The SDK is missing some BandLab capabilities (`docs/handover/COVERAGE.md`, register G01 to G14). The sessions that build them cannot reach BandLab and will not guess how an endpoint looks. The only reliable source is what BandLab's own website or app sends when you use it. This guide tells you what to do and what to record.

**What you are producing:** a *capture* is a recording of the network requests your browser or phone makes while you do one action in BandLab. The standard file format is **HAR**.

> **What this guide could not check.** Written without web access and without access to BandLab. Button names, menu locations and tool menus below are from memory and may differ in the current BandLab app or your browser version. If something is not where this says, do the action in your own words; what matters is the request it sends. If BandLab has no such action, **say so**. That is useful evidence too.

---

## 1. Rules (read these first)

1. **Your own account only.** Never capture while viewing other people's private messages or data. For anything that needs a second person (messages, collaborators), use **a second account that you also own**.
2. **Start recording after you log in.** The login request contains your password. Never capture it, and never share a capture that contains it.
3. **A raw HAR contains your secrets** (access tokens, cookies, your email, your ids). **Do not send a raw HAR to anyone, including me, and do not commit one.** Scrub every capture with `scripts/research/scrub-har.py` and check it (`docs/research/HAND-BACK.md`, section 4) before it goes anywhere.
4. **Destructive actions: use a throwaway.** For G05 (delete revision), G09 (change email) and G10 (delete account), use a throwaway account or throwaway content. **Do not delete your real account to produce a capture.** If you have no throwaway account, skip G10 and say so.
5. **One action per capture file.** Small, focused files are far easier to use than one long recording. Clear the log between actions.
6. **No payments or subscriptions.** Do not capture purchase or billing screens.
7. **Terms of service.** I cannot check BandLab's terms from here. Recording your own account's traffic for your own use is the intended scope; do not automate anything against other people's accounts.

---

## 2. Choose a method

| Method | What you need | Works for | Limits |
|--------|---------------|-----------|--------|
| **A. Desktop browser DevTools** (recommended) | A computer with Chrome, Edge, Firefox or Safari, and BandLab's website | Everything the **website** can do, including the web Studio | Only what the website does. A feature that exists only in the phone app will not appear. |
| **B. Phone browser through a capture tool** | A phone and a capture/proxy app that can decrypt HTTPS for the browser | Website features, from the phone | Setup is fiddly: the tool's own certificate must be installed and trusted. Same coverage as A (website only). |
| **C. The BandLab phone app** | A capture tool and the app | App-only features | **Often not possible.** Modern Android apps usually refuse user-installed certificates, and iOS apps may pin certificates, so the traffic cannot be read without rooting or modifying the phone. Do not root or patch your phone for this. If method C fails, say "app traffic not capturable" and move on. |

**If you can only use a phone:** try B. If that is too much, tell me, and we will agree a smaller set of captures; the leaf `2.b.i.zi` triage records what could not be captured.

---

## 3. How to record a HAR (method A, desktop browser)

Menu names change between versions; look for the equivalents.

**Chrome or Edge**
1. Log in to BandLab in a normal tab.
2. Open DevTools (F12, or Ctrl+Shift+I / Cmd+Option+I) and go to the **Network** tab.
3. Tick **Preserve log**. Click the **Clear** (circle with a line) button so the list is empty.
4. Tick the **Fetch/XHR** filter. These are the API calls. (Uploads may also show under **Other**; clear the filter for upload captures.)
5. Do **one action** (see section 4). Wait until it visibly finishes.
6. In the Network list, right-click any row and choose **Save all as HAR with content** (or use the download arrow in the toolbar).
7. Clear the list and do the next action.

**Firefox:** Network tab, gear icon, **Save All As HAR**. **Safari:** enable the Develop menu first, then Web Inspector, Network tab, **Export**.

**Check each capture quickly (10 seconds):** open the Network list and click the key request. You should see the **method**, the **full URL**, a **request body** (for writes), a **response body** (JSON), and a **2xx status**. If the action only produced image or font requests, the capture missed it; redo it.

**Always note the API host** for any capture: the part of the URL before `/api/...`. See P0 below.

---

## 4. What to capture

Do these in any order. For each one: clear the log, start from a normal page, do the action, save the HAR, write down one line (what you did and whether anything unexpected happened). Item **IDs are the register IDs** in `COVERAGE.md`.

### P0 — Which host does BandLab call? (do this first, takes 2 minutes)
**Why:** the SDK's default is `https://test.bandlab.com/api/v1.3` and its alternative is `https://bandlab.com/api/v1.3`; nobody knows which is right (`docs/handover/sessions/1.a.i.zo.md`, Part 2).
**Do:** with the Network tab open, load your own profile page. Write down the **host name and path prefix** of the API requests (for example `.../api/v1.3/...`) and **whether `test.bandlab.com` appears at all**. No HAR needed; one line is enough.

### Capture tasks

| ID | Do this | Look for | Safety |
|----|---------|----------|--------|
| **G01** Messaging | Open messages. (1) Load the conversation list. (2) Open an existing conversation. (3) Send one message to your **second account**. (4) Scroll up in a conversation to load older messages. (5) Mark as read, if the app has such an action. One capture per step. | requests that list conversations, fetch messages, send a message, load older messages | Only converse with your own second account. |
| **G02** Studio mix, tracks, effects | Open one of **your own** projects in the web Studio. (1) Capture just **opening** it. (2) Change one track's volume or pan. (3) Add or change one effect on a track or channel. (4) Let it save (or save manually). | what loads the project; what the save sends; whether tracks, channels and effects travel inside one request or separate ones. The SDK's revision type already has `tracks`, `samples`, `auxChannels` with `effects` (`slug`, `bypass`, `params`), `mixdown` and `mastering`; compare. | Use a project you do not mind changing, or undo afterwards. The Studio may autosave constantly: clear the log right before the change and stop right after. |
| **G03** Audio / samples / uploads | Upload a **very short audio file you own** (a few seconds) into a project, or as a sample, whichever the app offers. Capture from choosing the file until it shows as processed. If a sample library is browsable, open one sample too. | the whole sequence: create, upload (possibly to a separate storage host), status polling, final object; any audio metadata in a response | Clear the filter to **All** so uploads to other hosts are included. Use a tiny file: large HARs are unwieldy. |
| **G04** Create song / list songs | (1) Create a **brand-new empty song or project** and capture the first save. (2) Open your list of songs ("my songs" or library) and capture the load. | which request first creates the song, and whether it is `POST /revisions` with a `song` object (as the SDK's types suggest) or something else; how the list of songs is fetched | The new song can be deleted afterwards. |
| **G05** Delete revision | In a **throwaway song that has two or more revisions**, delete one revision, if the app lets you. | a `DELETE` request for a revision, or whatever the app uses | If the app has **no way to delete a revision, write that down**. That settles G05 as missing. |
| **G06** Create post | Create a **plain post** (text or a track post) from the feed or profile, using whichever "create post" or "share" entry the app offers. | the request that creates a post; its body shape; how it differs from posting an image or video (those already exist in the SDK) | Delete the post afterwards. |
| **G07** Get / update a comment | On **your own post**: (1) write a comment, (2) **edit** it, if the app allows, (3) open the comment on its own (a permalink or reply view), if the app has one. | a `PATCH`/`PUT` for editing; a single-comment `GET` | If the app cannot edit comments, say so. |
| **G08** Search posts | Use the search box with a word you know appears in posts. Switch between any result tabs (users, songs, posts, and so on). | whether there is a posts tab, and the request it sends | If no posts tab exists, say so. |
| **G09** Change email | **Throwaway account, or a second address you control.** Start the change-email flow in settings and finish it, then confirm via the email. | the request that changes the email. The SDK's `me.update` (`PATCH /me`) already has an `email` field, so check whether the app uses exactly that or a separate endpoint; also the confirmation request | Change it back afterwards. Do not do this on an account whose email you cannot recover. |
| **G10** Delete account | **Throwaway account only.** Walk through account deletion and capture the final confirm request. | the request that deletes or deactivates | **Never on your real account.** No throwaway account: skip and write "skipped". |
| **G11** Collaborators | With your **second account**: (1) invite it as a collaborator on a song, (2) accept the invite on the second account, (3) change its role or permission if the app allows, (4) remove it. One capture per step. | invite, accept, role change, removal. The SDK has list and remove only, plus `songs.invites`. | Use a throwaway song. |
| **G12** Image / video get + upload | (1) Upload one small **image** as a post. (2) Upload one very short **video** as a post. (3) Open an image or video post on its own page. | the upload sequence for each; the single-item `GET` | Clear the filter to **All** for uploads. Small files only. |
| **G13** Unknown extras | Do a **read-only tour**: with the log running, open each main section of the app once (feed/explore, library, notifications, collections, bands, communities, anything for releases/distribution, contests/challenges, playlists/albums, stats). **Change nothing.** Save one HAR per section. | any requests that have no match in `docs/endpoint-status.md`. Anything BandLab offers that nobody listed. | Read-only. Close the tab on anything that asks for payment. |
| **G14** Share / repost | On a track post, use the app's **share** or **repost** action. Distinguish a **repost inside BandLab** from sharing out to another app. Undo it afterwards. | a request that creates a repost or share. "Copy link" does not send anything to BandLab and does not count. | Use your own post or your second account's post, not a stranger's. |

---

## 5. After you have captures

1. Keep the files on your device. **Do not send raw HARs** (rule 3).
2. For each capture keep your one-line note: what you did, the date, what happened.
3. The hand-back format (folder layout, file names, and a checklist you tick) is in `HAND-BACK.md` and `CAPTURE-CHECKLIST.md`. The scrubbing script that removes tokens and personal data is `scripts/research/scrub-har.py`; the extractor `scripts/research/har-to-endpoints.py` turns scrubbed captures into endpoint descriptions. Do the captures any time, scrub and check each one, and send only the scrubbed files.
4. The session that triages them (`2.b.i.zi`) will mark each G-item as captured, missing or blocked. **"The app has no such action" is a valid and useful result.**
