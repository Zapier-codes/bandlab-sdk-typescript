# Session Protocol & Patch Hand-off Process

Applies to **every** session. Read `HANDOVER.md` first, then this file.

## 1. Session START checklist

```bash
git clone https://github.com/Zapier-codes/bandlab-sdk-typescript.git
cd bandlab-sdk-typescript
git config user.name  "Claude Session"            # only if not already set
git config user.email "claude-session@users.noreply.github.com"
cat HANDOVER.md                                    # read the NEXT SESSION POINTER
```

1. Read `HANDOVER.md` §1 and confirm the previous marker commit exists: `git log --oneline | grep "handover: complete <LAST_COMPLETED>"`.
2. Read your section in `docs/handover/TASKS.md`, then `ARCHITECTURE.md`, `COVERAGE.md`, and the previous audit file in `docs/handover/sessions/`.
3. Stay inside your chunk.

## 2. During the session

- **One diff = one commit.** `git add <paths>` then `git commit -m "<type>(<scope>): <subject>"`.
  Types: `feat`, `fix`, `docs`, `chore`, `test`, `refactor`, `research`, `handover`. Review `git status` before adding; no blind `git add -A`.
- Existing files are never moved, renamed or split (HANDOVER D2). Existing public API stays working (D4).
- Never invent an endpoint or response shape (D6). No evidence → no implementation.
- Sessions cannot reach BandLab from the sandbox (D7). Never claim an endpoint is live-verified.
- Run `yarn build && yarn lint && yarn test` before finishing; do not regress the S01 baseline.
- Never commit secrets, tokens, cookies or unscrubbed captures.

## 3. Session FINISH checklist (in this order)

1. Create `docs/handover/sessions/session-SNN.md` (template §5).
2. Update `HANDOVER.md`: §1 pointer (`NEXT_SESSION`, `NEXT_SESSION_TITLE`, `LAST_COMPLETED`, `LAST_COMPLETED_MARKER_COMMIT_SUBJECT`, `LAST_PATCH_NAME`, `STATUS`, `BLOCKERS`) and §4 audit index row.
3. Update the status board in `docs/handover/TASKS.md` and the matrix/register in `COVERAGE.md` if coverage changed.
4. Commit all of it as one commit with the exact subject **`handover: complete SNN`**.
5. Check whether earlier patches reached GitHub: `git fetch origin && git log origin/main --format=%s | grep "handover: complete"`.
6. Build the patch: `./scripts/handover/make-patch.sh sNN-short-slug`.
7. Present the patch and the owner commands (§4) with the real filename.

### The combined-patch rule
The patch is **always built from `origin/main`**, so it automatically contains **every commit not yet on GitHub**, from all earlier sessions plus this one.
The owner therefore only ever applies **one** patch: the newest. The script prints which sessions it contains.
Do not use any other base. Remove older `.patch` files from the outputs folder so only the newest remains.

## 4. Owner apply commands (Termux)

```bash
cd ~/bandlab-sdk-typescript
git am ~/storage/downloads/<patch-name>.patch
git push
```

If the owner already applied an older patch locally but did **not** push it, the combined patch will conflict. Fix, before applying:
```bash
cd ~/bandlab-sdk-typescript
git fetch origin && git reset --hard origin/main     # discards only the unpushed local copy of the older patch
```
If `git am` stops with a conflict: `git am --abort`, and report that the local repo was not at the expected base.

## 5. Audit file template (`docs/handover/sessions/session-SNN.md`)

```markdown
# Session SNN — <title>
- Date / Status (DONE | PARTIAL) / Patch name / Sessions contained in the patch
- Commits: (paste `git log --oneline origin/main..HEAD`)
## What was done
## Decisions made   (mark any that need owner approval)
## Verification     (build / lint / test results vs the S01 baseline)
## Evidence used    (captures / spec / owner confirmation, or "none")
## Deviations from the plan
## Known issues / blockers
## Next session     (ID, title, first 3 actions, files likely touched)
```

## 6. Failure modes

| Situation | Action |
|-----------|--------|
| Previous marker commit missing | Stop; tell the owner the previous patch was not applied/pushed. |
| Ran out of time mid-chunk | `STATUS: PARTIAL`, list what is left, still produce a patch. |
| Needed endpoint has no evidence | Leave it `missing` in `COVERAGE.md`; list in BLOCKERS what evidence is needed. Never guess. |
| Existing code looks odd | Fix it in place, additively; don't relocate. |
| Owner states a new rule | Owner wins. Update `HANDOVER.md` §2 in the same session and note it in the audit. |
