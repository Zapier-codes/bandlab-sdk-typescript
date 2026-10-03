# Session S00C — Rescope: SDK coverage only, extend the existing tree
- Date: 2026-10-03
- Status: DONE
- Patch: s00c-sdk-coverage-handover.patch — **combined**: contains S00, S00B and S00C (none had reached origin/main; verified by `git fetch`)

## Why
S00 and S00B built the wrong project (an MCP server in `mcp/`, then a relocation of the SDK into the MCP tree).
Owner ruling: the project is **updating the existing SDK for full API coverage**. No MCP, no relocating files, no new directories where the existing tree works.

## What was done
- Cancelled the MCP scope entirely (HANDOVER D3). The 170-file tool tree, workflows, permissions, bulk automation and registries are out.
- Kept the existing tree as-is; documented it and the rules for where new code goes: `ARCHITECTURE.md`.
- Moved the original plan tree to `ORIGINAL-PLAN-TREE.md` as a reference checklist only.
- Replaced `GAPS.md` + `EXISTING-VS-PLAN.md` with one `COVERAGE.md`: 17-domain status matrix and a register of 13 missing-capability items (G01–G13).
- Snapshotted the 123 existing endpoints: `endpoint-inventory.tsv`.
- Rewrote `TASKS.md` into 10 sessions (S01 baseline/tooling → S02 research kit → S03 evidence triage → S04–S08 implement by domain → S09 consistency → S10 audit).
- Rewrote `PROTOCOL.md` and `make-patch.sh`: patches are always built from `origin/main` (combined).

## Findings
- Missing entirely: messaging, mix/effects/tracks, audio/samples/uploads.
- Missing operations: create song, delete revision, generic create post, get/update comment, search posts, change email (`emails.ts` has no methods), delete account, image/video get+upload; add/update collaborator only via invites.
- `client.get/post/patch/put/delete(path, opts)` already exist, so unmodelled endpoints are always reachable.
- Existing tests use a Prism mock from the OpenAPI spec; new endpoints aren't in it, so new tests need a custom fetch mock.
- The sandbox cannot reach `bandlab.com`; endpoint discovery needs owner-supplied evidence (HAR captures, spec, or confirmation).
- `environments.production` points at `https://test.bandlab.com/api/v1.3`. Reported only; to be raised with the owner in S01.
- Spec typo `revisonId` in the fork path (harmless).

## Decisions made (owner may overrule)
- Research tooling lives in `scripts/research/` and findings in `docs/research/` (no new top-level dirs).
- Stainless scaffolding left untouched; regeneration must not be run (it would overwrite hand edits).

## Verification
- Docs and one shell script only. `make-patch.sh` verifies the combined patch applies cleanly on `origin/main`.

## Evidence used
- Repo itself (`api.md`, `src/`); no BandLab traffic.

## Deviations from the plan
- The original MCP plan is cancelled by the owner.

## Known issues / blockers
- S03 and everything after it is blocked on owner-supplied evidence.

## Next session
- **S01 — Baseline + coverage tooling**
- First 3 actions: (1) `yarn install && yarn build && yarn lint && yarn test`, record the baseline; (2) write `scripts/utils/coverage-report.cjs` and generate `docs/endpoint-status.md`; (3) verify each `COVERAGE.md` row against the code.
- Files likely touched: `scripts/`, `docs/endpoint-status.md`, `docs/handover/COVERAGE.md`.
