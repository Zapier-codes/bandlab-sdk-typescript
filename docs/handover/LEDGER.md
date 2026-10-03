# Leaf Ledger

Append-only. One line per leaf, written in the leaf's own final commit, **without a hash** (a commit cannot know its own). Format: `leaf path — short title`. Counted leaves also show the running count. Full account of a leaf: `docs/handover/sessions/<leaf path>.md`.
Never rewrite or reorder lines.

## Phase 0 — handover setup (not counted)
- 0.a.i.zi — handover framework and planning (was S00; superseded)
- 0.a.i.zo — in-place revamp rules (was S00B; superseded)
- 0.a.ii.zi — rescope to SDK coverage, extend the existing tree (was S00C)
- 0.a.ii.zo — adopt the splitting formula with N of M, add the container phase; 0 done of 47

## Counted leaves
- 1.a.i.zi — recorded the build baseline (build 0, lint 0 with 1 warning, jest 217 passed / 185 skipped / 0 failed); 1 done of 47
- 1.a.i.zo — recorded which tests need the mock or network (7 runtime suites need neither; all 185 resource tests are skipped) and wrote the base-URL report; 2 done of 47
- 1.a.ii.zi — added scripts/utils/coverage-report.cjs and scripts/coverage (parses api.md, diffs against the inventory; 123 endpoints, no drift; 11 checks run); 3 done of 47
