# Leaf Specs — SDK full-coverage program (47 leaves)

Generated from the same table as the checklist in `HANDOVER.md` Section 1, so the two cannot disagree.
Rules: `HANDOVER.md` Section 2. A leaf is one task; if it is bigger, split it first (Section 0, "The splitting rule").
`zi` = build, `zo` = prove and record. Every Phase 3 leaf waits for `2.b.i.zo`.


---

## Phase 1 — Baseline and coverage tooling


### 1.a Baseline and tooling › 1.a.i Baseline

**1 · `1.a.i.zi` — Record the build baseline**

`yarn install && yarn build && yarn lint && yarn test`; record pass/fail counts and timings in the leaf's Done note. No code change.

**2 · `1.a.i.zo` — Record which tests need the Prism mock or the network, and report the base-URL finding**

List tests that cannot run without the mock or network. Report that `environments.production` is `https://test.bandlab.com/api/v1.3` and `environment_1` is `https://bandlab.com/api/v1.3` for the owner to decide. Do not change defaults. Docs only.


### 1.a Baseline and tooling › 1.a.ii Coverage tooling

**3 · `1.a.ii.zi` — `scripts/utils/coverage-report.cjs`**

Parse `api.md` into (verb, path, accessor), diff against `docs/handover/endpoint-inventory.tsv`, exit non-zero on drift. Wire as `scripts/coverage`.

**4 · `1.a.ii.zo` — Generate `docs/endpoint-status.md` and verify every `COVERAGE.md` row against the code**

Every existing endpoint gets status `spec`. Correct any wrong matrix rows (does `songs` have list/create, what `search` covers, what `emails.ts` exposes).


---

## Phase 2 — Evidence for the missing endpoints

Sessions cannot reach `bandlab.com` (HANDOVER D7), so the tooling is built first and the owner supplies the evidence.


### 2.a Research kit › 2.a.i Capture guide

**5 · `2.a.i.zi` — `docs/research/CAPTURE-GUIDE.md`**

Exact in-app actions for G01 to G14 (send a message, upload audio, create a post, delete a revision, edit a comment, change email, share or repost a track, open mix and effects, and so on) and how to export a HAR from the owner's own account.

**6 · `2.a.i.zo` — Evidence hand-back format**

Folder layout under `docs/research/`, file naming (`<G-id>-<action>.har`, scrubbed), and a checklist table the owner ticks as captures are made.


### 2.a Research kit › 2.a.ii Scripts

**7 · `2.a.ii.zi` — `scripts/research/scrub-har.py` and a synthetic fixture**

Removes tokens, cookies, auth headers, emails and personal ids, replacing them with placeholders. Python is allowed here only (D5).

**8 · `2.a.ii.zo` — `scripts/research/har-to-endpoints.py` and a fixture**

Extracts method, path template, query keys and JSON shapes into `docs/research/endpoints/<domain>.json`, and flags endpoints not in the inventory.


### 2.b Evidence triage › 2.b.i Triage

**9 · `2.b.i.zi` — Run the tools on the owner's evidence and set a status per G-item** — **owner's leaf**

**BLOCKED until the owner supplies captures, a spec, or confirmations.** Newly found endpoints become G15 onward and raise M (see the splitting rule). If nothing is supplied: `[~]`, BLOCKERS names exactly what is needed, no guessing.

**10 · `2.b.i.zo` — Record the final resource design** — **owner's leaf**

File names, methods and types per G-item in `COVERAGE.md`. Split any Phase 3 leaf that is bigger than one task, before any code.


---

## Phase 3 — Implementation by gap

Every leaf here depends on `2.b.i.zo`. An item with no evidence is not implemented; it stays `missing` in the register. Each milestone is one gap item: `zi` implements, `zo` proves and records.


### 3.a Songs and revisions › 3.a.i G04 create song and list songs

**11 · `3.a.i.zi` — G04 create song and list songs: implement**

Implement: the method(s), request/response types, JSDoc carrying the evidence status, wiring in `src/client.ts` / the resource index, and the `api.md` line. Home per ARCHITECTURE.md. Existing files are not moved, renamed or split.

**12 · `3.a.i.zo` — G04 create song and list songs: tests and records**

Prove and record: a custom-fetch-mock test in `tests/api-resources/` (method, path, query, body, parsing; Prism cannot serve new endpoints), the `docs/endpoint-status.md` row, and the `COVERAGE.md` domain and register rows.


### 3.a Songs and revisions › 3.a.ii G05 delete revision

**13 · `3.a.ii.zi` — G05 delete revision: implement**

Implement: the method(s), request/response types, JSDoc carrying the evidence status, wiring in `src/client.ts` / the resource index, and the `api.md` line. Home per ARCHITECTURE.md. Existing files are not moved, renamed or split.

**14 · `3.a.ii.zo` — G05 delete revision: tests and records**

Prove and record: a custom-fetch-mock test in `tests/api-resources/` (method, path, query, body, parsing; Prism cannot serve new endpoints), the `docs/endpoint-status.md` row, and the `COVERAGE.md` domain and register rows.


### 3.a Songs and revisions › 3.a.iii G11 add and update collaborator

**15 · `3.a.iii.zi` — G11 add and update collaborator: implement**

Implement: the method(s), request/response types, JSDoc carrying the evidence status, wiring in `src/client.ts` / the resource index, and the `api.md` line. Home per ARCHITECTURE.md. Existing files are not moved, renamed or split.

**16 · `3.a.iii.zo` — G11 add and update collaborator: tests and records**

Prove and record: a custom-fetch-mock test in `tests/api-resources/` (method, path, query, body, parsing; Prism cannot serve new endpoints), the `docs/endpoint-status.md` row, and the `COVERAGE.md` domain and register rows.


### 3.b Studio and audio › 3.b.i G02 mix, effects, tracks, project structure (likely split)

**17 · `3.b.i.zi` — G02 mix, effects, tracks, project structure (likely split): implement**

Implement: the method(s), request/response types, JSDoc carrying the evidence status, wiring in `src/client.ts` / the resource index, and the `api.md` line. Home per ARCHITECTURE.md. Existing files are not moved, renamed or split.

**18 · `3.b.i.zo` — G02 mix, effects, tracks, project structure (likely split): tests and records**

Prove and record: a custom-fetch-mock test in `tests/api-resources/` (method, path, query, body, parsing; Prism cannot serve new endpoints), the `docs/endpoint-status.md` row, and the `COVERAGE.md` domain and register rows.


### 3.b Studio and audio › 3.b.ii G03 audio upload, samples, audio metadata (likely split)

**19 · `3.b.ii.zi` — G03 audio upload, samples, audio metadata (likely split): implement**

Implement: the method(s), request/response types, JSDoc carrying the evidence status, wiring in `src/client.ts` / the resource index, and the `api.md` line. Home per ARCHITECTURE.md. Existing files are not moved, renamed or split.

**20 · `3.b.ii.zo` — G03 audio upload, samples, audio metadata (likely split): tests and records**

Prove and record: a custom-fetch-mock test in `tests/api-resources/` (method, path, query, body, parsing; Prism cannot serve new endpoints), the `docs/endpoint-status.md` row, and the `COVERAGE.md` domain and register rows.


### 3.c Messaging › 3.c.i G01 conversations, messages, send, history (likely split)

**21 · `3.c.i.zi` — G01 conversations, messages, send, history (likely split): implement**

Implement: the method(s), request/response types, JSDoc carrying the evidence status, wiring in `src/client.ts` / the resource index, and the `api.md` line. Home per ARCHITECTURE.md. Existing files are not moved, renamed or split.

**22 · `3.c.i.zo` — G01 conversations, messages, send, history (likely split): tests and records**

Prove and record: a custom-fetch-mock test in `tests/api-resources/` (method, path, query, body, parsing; Prism cannot serve new endpoints), the `docs/endpoint-status.md` row, and the `COVERAGE.md` domain and register rows.


### 3.d Social and media › 3.d.i G06 create post

**23 · `3.d.i.zi` — G06 create post: implement**

Implement: the method(s), request/response types, JSDoc carrying the evidence status, wiring in `src/client.ts` / the resource index, and the `api.md` line. Home per ARCHITECTURE.md. Existing files are not moved, renamed or split.

**24 · `3.d.i.zo` — G06 create post: tests and records**

Prove and record: a custom-fetch-mock test in `tests/api-resources/` (method, path, query, body, parsing; Prism cannot serve new endpoints), the `docs/endpoint-status.md` row, and the `COVERAGE.md` domain and register rows.


### 3.d Social and media › 3.d.ii G07 get and update comment

**25 · `3.d.ii.zi` — G07 get and update comment: implement**

Implement: the method(s), request/response types, JSDoc carrying the evidence status, wiring in `src/client.ts` / the resource index, and the `api.md` line. Home per ARCHITECTURE.md. Existing files are not moved, renamed or split.

**26 · `3.d.ii.zo` — G07 get and update comment: tests and records**

Prove and record: a custom-fetch-mock test in `tests/api-resources/` (method, path, query, body, parsing; Prism cannot serve new endpoints), the `docs/endpoint-status.md` row, and the `COVERAGE.md` domain and register rows.


### 3.d Social and media › 3.d.iii G08 search posts

**27 · `3.d.iii.zi` — G08 search posts: implement**

Implement: the method(s), request/response types, JSDoc carrying the evidence status, wiring in `src/client.ts` / the resource index, and the `api.md` line. Home per ARCHITECTURE.md. Existing files are not moved, renamed or split.

**28 · `3.d.iii.zo` — G08 search posts: tests and records**

Prove and record: a custom-fetch-mock test in `tests/api-resources/` (method, path, query, body, parsing; Prism cannot serve new endpoints), the `docs/endpoint-status.md` row, and the `COVERAGE.md` domain and register rows.


### 3.d Social and media › 3.d.iv G12 image and video get and upload

**29 · `3.d.iv.zi` — G12 image and video get and upload: implement**

Implement: the method(s), request/response types, JSDoc carrying the evidence status, wiring in `src/client.ts` / the resource index, and the `api.md` line. Home per ARCHITECTURE.md. Existing files are not moved, renamed or split.

**30 · `3.d.iv.zo` — G12 image and video get and upload: tests and records**

Prove and record: a custom-fetch-mock test in `tests/api-resources/` (method, path, query, body, parsing; Prism cannot serve new endpoints), the `docs/endpoint-status.md` row, and the `COVERAGE.md` domain and register rows.


### 3.d Social and media › 3.d.v G14 share and repost

**31 · `3.d.v.zi` — G14 share and repost: implement**

Implement: the method(s), request/response types, JSDoc carrying the evidence status, wiring in `src/client.ts` / the resource index, and the `api.md` line. Home per ARCHITECTURE.md. Existing files are not moved, renamed or split.

**32 · `3.d.v.zo` — G14 share and repost: tests and records**

Prove and record: a custom-fetch-mock test in `tests/api-resources/` (method, path, query, body, parsing; Prism cannot serve new endpoints), the `docs/endpoint-status.md` row, and the `COVERAGE.md` domain and register rows.


### 3.e Account › 3.e.i G09 change email

**33 · `3.e.i.zi` — G09 change email: implement**

Implement: the method(s), request/response types, JSDoc carrying the evidence status, wiring in `src/client.ts` / the resource index, and the `api.md` line. Home per ARCHITECTURE.md. Existing files are not moved, renamed or split.

**34 · `3.e.i.zo` — G09 change email: tests and records**

Prove and record: a custom-fetch-mock test in `tests/api-resources/` (method, path, query, body, parsing; Prism cannot serve new endpoints), the `docs/endpoint-status.md` row, and the `COVERAGE.md` domain and register rows.


### 3.e Account › 3.e.ii G10 delete account (JSDoc marks it destructive)

**35 · `3.e.ii.zi` — G10 delete account (JSDoc marks it destructive): implement**

Implement: the method(s), request/response types, JSDoc carrying the evidence status, wiring in `src/client.ts` / the resource index, and the `api.md` line. Home per ARCHITECTURE.md. Existing files are not moved, renamed or split.

**36 · `3.e.ii.zo` — G10 delete account (JSDoc marks it destructive): tests and records**

Prove and record: a custom-fetch-mock test in `tests/api-resources/` (method, path, query, body, parsing; Prism cannot serve new endpoints), the `docs/endpoint-status.md` row, and the `COVERAGE.md` domain and register rows.


---

## Phase 4 — Consistency and final audit


### 4.a Finish › 4.a.i Types and docs

**37 · `4.a.i.zi` — Tighten types where captures gave real shapes**

Replace loose types with the captured shapes; keep every existing type compatible.

**38 · `4.a.i.zo` — JSDoc statuses, naming consistency, `api.md` complete**

Every new method documented the same way as its neighbours; `api.md` lists every method.


### 4.a Finish › 4.a.ii README and audit

**39 · `4.a.ii.zi` — README: new resources and one example per new domain**

Short, runnable-looking examples; no claim that an endpoint is live-verified unless the owner confirmed it.

**40 · `4.a.ii.zo` — Final coverage audit**

Regenerate `endpoint-status.md`; every endpoint has a status; every domain row in `COVERAGE.md` is Covered or `missing`/`blocked` with a reason.


---

## Phase 5 — Container image on GHCR (if possible)

The SDK is a library, so the image is a runtime and base image that bundles the built SDK. It is not a service. **Feasibility, checked in 0.a.ii.zo:** the sandbox has no container runtime, and `ghcr.io` and Docker Hub both answer 403 from it, so a session can write the files but cannot build, push or test an image. GitHub Actions on the owner's fork does that. Until `5.b.ii.zi`, every Phase 5 leaf is *written, NOT built or run*. The registry host is `ghcr.io` (lowercase image name: `ghcr.io/zapier-codes/bandlab-sdk-typescript`).


### 5.a Image definition › 5.a.i Dockerfile

**41 · `5.a.i.zi` — Multi-stage `Dockerfile` and `.dockerignore`**

Build stage: Node 20, `yarn install --frozen-lockfile --ignore-scripts`, `./scripts/build` (the `prepare` hook is skipped on purpose). Final stage: Node slim with the `dist/` package installed. No tokens or `.env` copied in.

**42 · `5.a.i.zo` — `scripts/container-smoke`**

`docker run`s the image and checks the SDK loads and lists its resources. Written for the owner or CI to run; not run by sessions.


### 5.a Image definition › 5.a.ii Runtime contract

**43 · `5.a.ii.zi` — README container section**

How to run, `BANDLAB_SDK_BEARER_TOKEN` supplied at runtime only and never baked in, `NODE_PATH` use, how to use the image as a base.

**44 · `5.a.ii.zo` — Default command**

Prints the SDK version and resource names and exits 0, so `docker run <image>` is a smoke test.


### 5.b Publish to GHCR › 5.b.i Workflow

**45 · `5.b.i.zi` — `.github/workflows/container.yml`**

Build and push `ghcr.io/zapier-codes/bandlab-sdk-typescript` on pushes to `main` and `v*` tags, `linux/amd64` and `linux/arm64`, tags `latest`, `sha-<short>` and semver, `org.opencontainers.image.source` label, `packages: write` through `GITHUB_TOKEN`. Existing workflows untouched.

**46 · `5.b.i.zo` — Owner steps document**

Enable Actions on the fork, set package visibility, confirm the package is linked to the repo, `docker pull` command. Action versions are written from memory and must be checked on first run.


### 5.b Publish to GHCR › 5.b.ii First publish

**47 · `5.b.ii.zi` — Owner confirms the first CI run published the image and it pulls and runs** — **owner's leaf**

**The owner's leaf.** Tracked here for visibility; a session records the owner's confirmation or the failure log.


---

## Recipe reminders for Phase 3 leaves
- Home for new code: `ARCHITECTURE.md`. Sub-resources of a folder resource go in that folder; new top-level resources are new files in `src/resources/`; flat files are never converted into folders.
- Evidence first (D6). A leaf with no evidence for its item is not implemented; set `[~]` and name the evidence needed under BLOCKERS.
- `yarn build && yarn lint && yarn test` must match or beat the `1.a.i.zi` baseline.
