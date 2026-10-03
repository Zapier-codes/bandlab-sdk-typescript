# The Splitting Formula — adopted from D-Store, adapted for this repo

Source read: `github.com/Zapier-codes/D-Store`, `HANDOVER.md` (Sections 0, 1 and 3, the Focus run 3 checklist, and the 13h4 split), at its `master` head `c4e3711`. Only the method is borrowed; none of D-Store's content applies here.

## What the formula is
1. **Hierarchy** Phase › Track › Milestone › Leaf (`zi`, `zo`). A leaf has a full path such as `3.c.i.zi`, used everywhere (commits, patches, ledger).
2. **One leaf = one task.** Never bundled, never partial. **One leaf per session.**
3. **Split before coding** when a leaf is bigger than one task. The split is itself the session's one task and changes no code.
4. **Counted checklist.** Every leaf is a numbered checkbox. The session reports `N done ✅ of M` after each leaf, so the whole program's progress is one number.
5. **Honest count.** When a leaf splits, the parent becomes `[-]` (kept, addressable, no longer counted), children are added, and M's history is written down.
6. **Current position** pointer, advanced in the same commit that ticks the leaf.
7. **Handoff** by exactly one patch; combined when origin lacks earlier work.

## What was changed for this repo

| D-Store | Here | Why |
|---|---|---|
| Branch `master` | `main` | This repo's default branch. |
| Patch name `000X-<leaf>-<desc>.patch` | `NNNN-<leaf-path>-<description>.patch`, `NNNN` from `NEXT_PATCH_NUMBER` | Same idea, explicit counter. |
| One commit per leaf | **One commit per diff**, all subjects prefixed with the leaf path; the final one is the marker and carries tick, count, position, ledger and Done note | The owner's original rule is a commit for every diff; the marker keeps D-Store's "count and code cannot disagree". |
| `zi`/`zo` loosely defined | `zi` = build, `zo` = prove and record | Gives every milestone the same shape. |
| Done notes inside `HANDOVER.md` (it reached 1.1 MB) | One file per leaf: `docs/handover/sessions/<leaf path>.md` | Keeps `HANDOVER.md` readable. |
| `CHANGELOG.md` ledger | `docs/handover/LEDGER.md` | `CHANGELOG.md` here is owned by the release tooling. |
| Phase 0 for the UI revamp, counted | Phase 0 = handover setup, **not counted** | It is history, not program work. |

## Not adopted
- **"Stop running tests and builds"** — D-Store's operator instruction for D-Store only. Here sessions build, lint and test where the sandbox allows, and say plainly when they could not.
- **Cross-repo rules** (clone Zealot, Storeapp, distr every session) — this program is one repo.
- **Held / blocked taxonomies** — replaced by D-Store's simpler marker set plus an "owner's leaf" flag for work only the owner can do (evidence, first image publish).

## Worked split (how a session would split `3.c.i.zi`, messaging, checklist number 21)
Suppose the evidence shows messaging is four independent parts: conversations, messages, send, history.
1. The session stops before any code and marks `21` as `[-]` *(split, DATE, into 21a to 21d; kept so the ID stays addressable)*.
2. It adds four children as new milestones in track `3.c`, one task each. After a split, `zi` and `zo` are just positions in a milestone, exactly as in D-Store's `13h4a` to `13h4d`:
   - `21a` `3.c.ii.zi` implement conversations
   - `21b` `3.c.ii.zo` implement messages
   - `21c` `3.c.iii.zi` implement send
   - `21d` `3.c.iii.zo` implement history
   Leaf `22` (`3.c.i.zo`, tests and records) stays and now proves all four. It may split too.
3. M goes from 47 to 50 (4 added, 1 removed). The session writes: "Leaf 21 (`3.c.i.zi`) was split on DATE into 21a to 21d, which moves the total from 47 to 50."
4. It commits docs only, `3.c.i.zi: split into 21a to 21d because it bundled ...; docs-only, no code changed; still N done of 50`, and hands off the patch. That is the session's one task.
