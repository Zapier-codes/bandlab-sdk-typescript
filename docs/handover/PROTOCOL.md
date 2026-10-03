# Session Protocol — detail

The rules and the checklist are in `HANDOVER.md` (Sections 0 to 3). This file holds the detail that would clutter it.

## 1. Session start
```bash
git clone https://github.com/Zapier-codes/bandlab-sdk-typescript.git
cd bandlab-sdk-typescript
git config user.name  "Claude Session"            # only if not already set
git config user.email "claude-session@users.noreply.github.com"
git fetch origin
cat HANDOVER.md                                    # Current position (Section 1a)
git log --oneline | grep "<MARKER_COMMIT_SUBJECT_PREFIX>"   # previous leaf must be present
```
Then read your leaf in `docs/handover/TASKS.md`, `ARCHITECTURE.md`, `COVERAGE.md`, and the previous Done note in `docs/handover/sessions/`.

## 2. During the leaf
- One diff, one commit. Every subject starts with the leaf path: `3.d.i.zi: add posts.create; ...`.
- Existing files are not moved, renamed or split (D2). Existing public API keeps working (D4).
- No invented endpoints or shapes (D6). No claim of live verification or of a built image unless it happened (D7).
- Run `yarn build && yarn lint && yarn test` and compare to the `1.a.i.zi` baseline. Say plainly what could not be run.
- No secrets, tokens, cookies or unscrubbed captures in commits (D11 for images).

## 3. Finishing the leaf
1. Write the Done note `docs/handover/sessions/<leaf path>.md` (template below).
2. In the **final commit**, together: tick `[x]` in `HANDOVER.md`, update "Done so far", move Current position (and `LAST_COMPLETED_LEAF`, `MARKER_COMMIT_SUBJECT_PREFIX`, `LAST_PATCH_NAME`, `NEXT_PATCH_NUMBER`, `BLOCKERS`), append one line to `docs/handover/LEDGER.md`, update `COVERAGE.md` if coverage changed.
3. Subject of the final commit: `<leaf path>: <title>; <what was and was not run>; N done of M`.
4. `git fetch origin`, then `./scripts/handover/make-patch.sh NNNN-<leaf-path>-<description>`.
5. Present the single patch, delete older ones, give the apply commands, end with `N done ✅ of M`.

### Combined-patch rule
The patch is built from `origin/main`, so it contains every commit not yet on GitHub. The owner applies one patch. The script lists the leaves it carries.

### If the leaf is split
Follow `HANDOVER.md` Section 0, "The splitting rule". Docs only. Update the checklist, M, the history line under "Done so far", and `TASKS.md` (regenerate the affected specs by hand). Commit as `<leaf path>: split into ...; docs-only, no code changed; still N done of M`.

## 4. Done-note template (`docs/handover/sessions/<leaf path>.md`)
```markdown
# <leaf path> — <title>
- Date / Status (DONE | PARTIAL) / Patch name / Leaves carried by the patch / Focus run count after this leaf
- Commits: (paste `git log --oneline origin/main..HEAD`)
## What was done
## Decisions made   (mark any needing owner approval)
## Verification     (build / lint / test vs baseline; what was NOT run)
## Evidence used    (captures / spec / owner confirmation, or "none")
## Deviations
## Known issues / blockers
## Next leaf        (path, title, first 3 actions, files likely touched)
```

## 5. Failure modes
| Situation | Action |
|-----------|--------|
| Previous marker commit missing | Stop; tell the owner the previous patch was not applied or pushed. |
| Leaf bigger than one task | Split first (docs only); that is the session's task. |
| Ran out of time mid-leaf | `[~]`, `WIP:` commit, say what is left, still hand off a patch. |
| No evidence for a G-item | Leave it `missing`; name the needed evidence under BLOCKERS. Never guess. |
| Owner states a new rule | Owner wins. Update `HANDOVER.md` Section 2 in the same leaf and note it in the Done note. |
