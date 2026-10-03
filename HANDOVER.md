# HANDOVER — READ THIS FIRST

> Every session (human or AI) that clones this repo **must read this file before doing anything else**, then work **the one leaf** named in "Current position".
> This file is the single source of truth for sequencing. **The owner's rules override everything here.** If the owner states a new rule, update Section 2 in the same session.

---

## 0. How this file works

Work follows a fixed hierarchy (adapted from the D-Store handover; see `docs/handover/FORMULA.md` for what was adopted and what was not):

```
Phase        1, 2, 3, 4, 5
 └─ Track     a, b, c, d, e
     └─ Milestone   i, ii, iii, iv, v
         └─ Leaf        zi, zo
```

- A **leaf** is exactly **one task**. It is never bundled with another and never left partial. Its path is e.g. `3.c.i.zi`; use it in commit subjects, patch names, ledger lines and status updates.
- In this project `zi` is the **build** half of a milestone and `zo` is the **prove-and-record** half (tests, status docs, coverage rows).
- **Every session does exactly one leaf**, then hands off. Never start a second leaf, even if time remains.
- **Phase 0** is the handover setup (the sessions before the formula existed). It is history and is **not counted** in N of M.

### The splitting rule
1. A session that finds its leaf is bigger than one task **splits it before writing any code**. The split itself (docs only) is that session's one task.
2. The parent is kept and marked `[-]` (superseded) so its ID stays addressable. It no longer counts toward M.
3. The children get **new paths**: the next unused milestone numerals in the same track, one `zi`/`zo` pair per milestone. Their checklist numbers are the parent's number plus a letter (`29` becomes `29a`, `29b`, …).
4. M changes accordingly (children added, parent removed). The session reports the new total and updates the history line under "Done so far", so the count never changes meaning quietly.
5. Likely splits are flagged in advance: `3.b.i` (mix and effects), `3.b.ii` (audio upload), `3.c.i` (messaging). New G-items found by `2.b.i.zi` add leaves and raise M the same way.

### Status markers
`[ ]` open · `[~]` in progress (a session started but could not finish; commit as `WIP:`) · `[x]` done and handed off by patch · `[-]` superseded or split; never pick it up.

---

## 1. Focus run — the 47 leaves of the SDK full-coverage program

*Active until "47 done ✅ of 47". Owner directive, 2026-10-03. Scope and rules: Section 2. Leaf specs: `docs/handover/TASKS.md`. Coverage matrix and the G-item register: `docs/handover/COVERAGE.md`.*


**Phase 1 — Baseline and coverage tooling**

- [ ] 1 — `1.a.i.zi` Record the build baseline
- [ ] 2 — `1.a.i.zo` Record which tests need the Prism mock or the network, and report the base-URL finding
- [ ] 3 — `1.a.ii.zi` `scripts/utils/coverage-report.cjs`
- [ ] 4 — `1.a.ii.zo` Generate `docs/endpoint-status.md` and verify every `COVERAGE.md` row against the code

**Phase 2 — Evidence for the missing endpoints**

- [ ] 5 — `2.a.i.zi` `docs/research/CAPTURE-GUIDE.md`
- [ ] 6 — `2.a.i.zo` Evidence hand-back format
- [ ] 7 — `2.a.ii.zi` `scripts/research/scrub-har.py` and a synthetic fixture
- [ ] 8 — `2.a.ii.zo` `scripts/research/har-to-endpoints.py` and a fixture
- [ ] 9 — `2.b.i.zi` Run the tools on the owner's evidence and set a status per G-item *(owner's leaf)*
- [ ] 10 — `2.b.i.zo` Record the final resource design *(owner's leaf)*

**Phase 3 — Implementation by gap**

- [ ] 11 — `3.a.i.zi` G04 create song and list songs: implement
- [ ] 12 — `3.a.i.zo` G04 create song and list songs: tests and records
- [ ] 13 — `3.a.ii.zi` G05 delete revision: implement
- [ ] 14 — `3.a.ii.zo` G05 delete revision: tests and records
- [ ] 15 — `3.a.iii.zi` G11 add and update collaborator: implement
- [ ] 16 — `3.a.iii.zo` G11 add and update collaborator: tests and records
- [ ] 17 — `3.b.i.zi` G02 mix, effects, tracks, project structure (likely split): implement
- [ ] 18 — `3.b.i.zo` G02 mix, effects, tracks, project structure (likely split): tests and records
- [ ] 19 — `3.b.ii.zi` G03 audio upload, samples, audio metadata (likely split): implement
- [ ] 20 — `3.b.ii.zo` G03 audio upload, samples, audio metadata (likely split): tests and records
- [ ] 21 — `3.c.i.zi` G01 conversations, messages, send, history (likely split): implement
- [ ] 22 — `3.c.i.zo` G01 conversations, messages, send, history (likely split): tests and records
- [ ] 23 — `3.d.i.zi` G06 create post: implement
- [ ] 24 — `3.d.i.zo` G06 create post: tests and records
- [ ] 25 — `3.d.ii.zi` G07 get and update comment: implement
- [ ] 26 — `3.d.ii.zo` G07 get and update comment: tests and records
- [ ] 27 — `3.d.iii.zi` G08 search posts: implement
- [ ] 28 — `3.d.iii.zo` G08 search posts: tests and records
- [ ] 29 — `3.d.iv.zi` G12 image and video get and upload: implement
- [ ] 30 — `3.d.iv.zo` G12 image and video get and upload: tests and records
- [ ] 31 — `3.d.v.zi` G14 share and repost: implement
- [ ] 32 — `3.d.v.zo` G14 share and repost: tests and records
- [ ] 33 — `3.e.i.zi` G09 change email: implement
- [ ] 34 — `3.e.i.zo` G09 change email: tests and records
- [ ] 35 — `3.e.ii.zi` G10 delete account (JSDoc marks it destructive): implement
- [ ] 36 — `3.e.ii.zo` G10 delete account (JSDoc marks it destructive): tests and records

**Phase 4 — Consistency and final audit**

- [ ] 37 — `4.a.i.zi` Tighten types where captures gave real shapes
- [ ] 38 — `4.a.i.zo` JSDoc statuses, naming consistency, `api.md` complete
- [ ] 39 — `4.a.ii.zi` README: new resources and one example per new domain
- [ ] 40 — `4.a.ii.zo` Final coverage audit

**Phase 5 — Container image on GHCR (if possible)**

- [ ] 41 — `5.a.i.zi` Multi-stage `Dockerfile` and `.dockerignore`
- [ ] 42 — `5.a.i.zo` `scripts/container-smoke`
- [ ] 43 — `5.a.ii.zi` README container section
- [ ] 44 — `5.a.ii.zo` Default command
- [ ] 45 — `5.b.i.zi` `.github/workflows/container.yml`
- [ ] 46 — `5.b.i.zo` Owner steps document
- [ ] 47 — `5.b.ii.zi` Owner confirms the first CI run published the image and it pulls and runs *(owner's leaf)*

**Done so far: 0 of 47.** History of M: set at 47 on 2026-10-03 (no splits yet).

**Reporting rule:** a session that completes a leaf ends its final message with `N done ✅ of M`, read off this checklist **after** the session. One that completes none says `No new leaf completed — still N done of M`, with the reason. The tick, the count, Current position and the ledger line go in the leaf's own final commit, so the patch and the count can never disagree.

---

## 1a. Current position

```yaml
CURRENT_LEAF: 1.a.i.zi
CURRENT_LEAF_TITLE: Record the build baseline
CURRENT_LEAF_SPEC: docs/handover/TASKS.md  ->  "1.a.i.zi"
FOCUS_RUN: "0 done of 47"
LAST_COMPLETED_LEAF: 0.a.ii.zo        # Phase 0 setup, not counted
MARKER_COMMIT_SUBJECT_PREFIX: "0.a.ii.zo:"
LAST_PATCH_NAME: 0001-0.a.ii.zo-adopt-splitting-formula-and-container-phase.patch
NEXT_PATCH_NUMBER: "0002"
STATUS: READY
BLOCKERS: none for Phase 1. Phase 2 leaves 2.b.i.zi and 2.b.i.zo are the owner's evidence gate; every Phase 3 leaf waits behind them. 5.b.ii.zi is the owner's.
```

**Sanity check at session start:**
```bash
git fetch origin
git log --oneline | grep "0.a.ii.zo:"      # the previous leaf's marker commit must be present
```
If the marker is **not** in `git log`, the previous patch was never applied or pushed. **Stop and tell the owner.**

---

## 2. What this project is, and the rules

**Update the existing BandLab TypeScript SDK so it covers every BandLab API capability**, including the ones it is missing today (messaging, audio and samples, mix and effects, and a set of missing operations; see `COVERAGE.md`). Then **bake it as a container image on `ghcr.io`, if possible** (Phase 5). It is **not** an MCP server and **not** a restructure.

| # | Rule |
|---|------|
| D1 | **This is the owner's own project. Everything is editable, including `src/`.** |
| D2 | **Keep the existing tree. Extend it.** No relocating, renaming or splitting existing files; no new top-level directories. New code goes beside its neighbours (`ARCHITECTURE.md`, "Where new things go"). Files that must sit at the repo root (`Dockerfile`, `.dockerignore`) are files, not directories. |
| D3 | **Scope is SDK API coverage plus the container image.** No MCP server, tools, workflows, permission layers, bulk automation or registries. |
| D4 | **Additive only.** Every existing `client.*` call keeps working unchanged. |
| D5 | Python is allowed only in `scripts/research/` for evidence tooling. Never shipped, never imported by `src/`. |
| D6 | **Never invent an endpoint or a response shape.** Every new endpoint needs evidence (capture, spec or owner confirmation) and a status: `spec` / `captured` / `unverified` / `live-ok` / `missing`. |
| D7 | **Sessions cannot reach `bandlab.com`, `ghcr.io` or Docker Hub** from the sandbox (checked), and there is no container runtime. Evidence and live checks come from the owner. Never claim an endpoint is live-verified or an image is built when it was not. |
| D8 | Stainless and release scaffolding is left untouched. Do not run or merge codegen (it would overwrite hand edits). |
| D9 | Wire paths stay exactly as the server expects; follow the naming of neighbouring files. |
| D10 | **Combined patch rule:** the patch is always built from `origin/main`, so it carries every commit not yet pushed. The owner applies one patch. |
| D11 | **Never bake secrets into an image.** Tokens are supplied at runtime only. |

---

## 3. Standing handoff process (every session)

0. **Check upstream:** `git fetch origin`. If origin moved, rebase local work onto `origin/main` before starting. Check whether the previous patch reached GitHub (`git log origin/main | grep "<previous leaf path>:"`).
1. **Do the one leaf** named in Current position, and nothing else. If it is bigger than one task, split it first (Section 0) and hand off the split as the session's one task.
2. **One diff = one commit** (`git add <paths>`, `git commit`). Every commit subject starts with the leaf path.
3. **The leaf's final commit** carries, together: the work's last change, the checklist tick `[x]`, the "Done so far" count, Current position moved to the next open leaf (path order: `zi` before `zo`, then the next milestone, track, phase), one line appended to `docs/handover/LEDGER.md`, and the Done note `docs/handover/sessions/<leaf path>.md`. Its subject is `<leaf path>: <title>; <what was and was not run>; N done of M`.
4. **Build the patch:** `./scripts/handover/make-patch.sh NNNN-<leaf-path>-<description>` where `NNNN` is `NEXT_PATCH_NUMBER`. It always builds from `origin/main`, so it is the combined patch whenever earlier work is not yet pushed, and says which leaves it carries.
5. **Hand the owner exactly one patch file** and the commands (below). Delete older `.patch` files from the outputs folder.
6. Reply: which leaf, what was and was not run, the commands, then `N done ✅ of M`.

```bash
cd ~/bandlab-sdk-typescript
git am ~/storage/downloads/<patch-name>.patch
git push
```
If the owner applied an older patch locally without pushing: `git fetch origin && git reset --hard origin/main` first. If `git am` conflicts: `git am --abort` and report the base mismatch.

If a leaf cannot finish: mark it `[~]`, commit what exists with a `WIP:` prefix, say exactly what is left, and still hand off a patch. The next session resumes that leaf first.

---

## 4. Documents map

| File | Purpose |
|------|---------|
| `HANDOVER.md` | This file: formula, checklist (N of M), Current position, rules, process. |
| `docs/handover/TASKS.md` | The spec for every leaf (generated from the same table as the checklist). |
| `docs/handover/FORMULA.md` | The splitting formula: what was adopted from D-Store, what was changed, a worked split. |
| `docs/handover/ARCHITECTURE.md` | Existing tree, where new code goes, constraints. |
| `docs/handover/COVERAGE.md` | 17-domain matrix and the G-item register. |
| `docs/handover/endpoint-inventory.tsv` | Snapshot of the 123 existing endpoints. |
| `docs/handover/PROTOCOL.md` | Detailed session checklist and the Done-note template. |
| `docs/handover/LEDGER.md` | Append-only: one line per leaf. |
| `docs/handover/ORIGINAL-PLAN-TREE.md` | The cancelled MCP plan, kept as a domain checklist only. |
| `docs/handover/sessions/` | Done notes: `S00`, `S00B`, `S00C` (history) and one `<leaf path>.md` per leaf. |
| `scripts/handover/make-patch.sh` | Builds the combined patch. |
