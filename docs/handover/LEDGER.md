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
- 1.a.ii.zo — generated docs/endpoint-status.md (123 endpoints, all spec), added --markdown to the coverage script, verified COVERAGE.md against the code (123 calls = 123 api.md rows) and corrected it (7 Covered, 8 Partial, 2 Missing); Phase 1 complete; 4 done of 47
- 2.a.i.zi — wrote docs/research/CAPTURE-GUIDE.md (capture tasks for G01 to G14 plus the base-host check P0, HAR export steps, safety rules; written from memory without BandLab access); 5 done of 47
- 2.a.i.zo — wrote docs/research/HAND-BACK.md and the 42-row CAPTURE-CHECKLIST.md, git-ignored raw captures, defined the three hand-back routes and the scrubber requirements; 6 done of 47
- 2.a.ii.zi — added scripts/research/scrub-har.py (scrubber plus structured --check, stdlib only), a synthetic fixture and 24 tests; replaced the false-alarm keyword check in HAND-BACK.md; 7 done of 47
- 2.a.ii.zo — added scripts/research/har-to-endpoints.py (endpoint shapes from scrubbed captures, flags what the SDK lacks, refuses unscrubbed input) and 20 mutation-checked tests; 44 python tests total; next leaf is blocked on owner evidence; 8 done of 47
