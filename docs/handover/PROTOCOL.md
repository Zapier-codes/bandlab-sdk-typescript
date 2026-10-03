# Session Protocol & Patch Hand-off Process

Applies to **every** session. Read `HANDOVER.md` first, then this file.

---

## 1. Session START checklist

```bash
git clone https://github.com/Zapier-codes/bandlab-sdk-typescript.git
cd bandlab-sdk-typescript
git config user.name  "Claude Session"            # only if not already set
git config user.email "claude-session@users.noreply.github.com"
cat HANDOVER.md                                    # read the NEXT SESSION POINTER
```

1. Read `HANDOVER.md` §1 (pointer) and confirm the previous marker commit exists:
   `git log --oneline | grep "handover: complete <LAST_COMPLETED>"`.
2. Read your section in `docs/handover/TASKS.md`.
3. Read the previous audit file in `docs/handover/sessions/`.
4. Read `docs/handover/EXISTING-VS-PLAN.md` (what exists / moves / is new) and `docs/handover/GAPS.md` if your chunk touches a gap.
5. Do not touch anything outside your chunk's scope.

## 2. During the session

- **One diff = one commit.** After each logical change: `git add <paths>` then `git commit -m "<type>(<scope>): <subject>"`.
  - Types: `feat`, `fix`, `docs`, `chore`, `test`, `refactor`, `research`, `handover`.
  - Never `git add -A` blindly; review `git status` first.
- Everything in this repo is ours, including `src/` (HANDOVER D1). Edit freely, but keep refactors disciplined:
  - **Moves and edits are separate commits.** Use `git mv` so history follows the file; a move commit changes only import paths.
  - Keep the build green after each move commit.
  - Wire paths to the BandLab server must not change when renaming internal code.
- Run `yarn lint && yarn build && yarn test` at the repo root before finishing (record the baseline in S01; later sessions must not regress it). Do not hand over a red build;
  if something is unavoidably red, record it under BLOCKERS.
- Never commit secrets, tokens, cookies or captured credentials. `research/captures/` must be scrubbed.

## 3. Session FINISH checklist (in this order)

1. Create `docs/handover/sessions/session-SNN.md` using the template in §5.
2. Update `HANDOVER.md`:
   - §1 pointer: `NEXT_SESSION`, `NEXT_SESSION_TITLE`, `LAST_COMPLETED`, `LAST_COMPLETED_MARKER_COMMIT_SUBJECT`, `LAST_PATCH_NAME`, `STATUS`, `BLOCKERS`.
   - §4 audit index: append your row.
3. Update the task status table at the top of `docs/handover/TASKS.md`.
4. Commit all of the above as one commit with the exact subject: **`handover: complete SNN`**.
5. Build the patch:
   ```bash
   ./scripts/handover/make-patch.sh sNN-short-slug
   ```
   This produces `/mnt/user-data/outputs/sNN-short-slug.patch` (or `./patches/` if that path is missing).
   The name is chosen **dynamically by the session**: `sNN-<kebab-case-summary>.patch` (a correction session may use a letter suffix, e.g. `s00b-...`).
   If your commits sit on top of a previous session that is not yet on `origin/main`, set `PATCH_BASE=<ref>` (the previous marker commit) so the patch contains only your commits.
6. Present the patch to the owner and give them the exact commands in §4 with the real patch name filled in.

## 4. Owner apply commands (Termux)

The session must print these with the real patch filename substituted:

```bash
cd ~/bandlab-sdk-typescript
git am ~/storage/downloads/<patch-name>.patch
git push
```

Notes for the session to include when relevant:
- `git am` replays every commit from the session with its original message and author, so history stays one-commit-per-diff.
- If `git am` stops with a conflict: `git am --abort`, then tell the next session / owner the local repo was not at the expected base.
- Patches must be applied in order (S00, then S00B, then S01 …). Skip any you already applied.
- The patch is built against `origin/main` **as cloned at session start**. The owner must have pushed the previous session's patch
  before the next session clones; otherwise the marker-commit check (§1) fails and the next session must stop.
- To check before applying: `git apply --check ~/storage/downloads/<patch-name>.patch` is NOT sufficient for mbox patches;
  use `git am --3way` if a plain `git am` fails on a slightly diverged tree.

## 5. Audit file template  (`docs/handover/sessions/session-SNN.md`)

```markdown
# Session SNN — <title>
- Date: YYYY-MM-DD
- Status: DONE | PARTIAL
- Patch: sNN-<slug>.patch
- Commits: (paste `git log --oneline origin/main..HEAD`)

## What was done
(bullets, with file paths)

## Decisions made
(anything not already in HANDOVER D1–D6; mark if it needs owner approval)

## Verification
(commands run and their results: lint / build / test)

## Deviations from the plan
(or "none")

## Known issues / blockers

## Next session
- ID + title
- Exact first 3 things to do
- Files it will most likely touch
```

## 6. Failure modes and what to do

| Situation | Action |
|-----------|--------|
| Marker commit for previous session missing | Stop. Tell owner the previous patch was not applied/pushed. |
| Session ran out of time mid-chunk | `STATUS: PARTIAL`, list remaining items in the audit file and in TASKS.md, still produce a patch. |
| Chunk needs a decision from the owner | Put it in BLOCKERS, finish what is unblocked. |
| A needed endpoint is not in the SDK | Add to `GAPS.md`; never fake it. Use `developer/raw-request` once built (S13). |
| Existing code looks "generated" or odd | It is ours now. Fix or relocate it, per `EXISTING-VS-PLAN.md`. |
| Owner states a new rule mid-session | Owner's rule wins. Update `HANDOVER.md` rules in the same session and note it in the audit file. |
