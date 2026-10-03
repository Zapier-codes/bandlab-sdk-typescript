# Session S00 — Handover framework + planning
> **Superseded in part by S00B:** decisions D1 (src read-only) and D2 (`mcp/` folder) below are void. See `session-S00B.md`.
- Date: 2026-10-02
- Status: DONE
- Patch: s00-handover-framework.patch

## What was done
- Cloned `Zapier-codes/bandlab-sdk-typescript` (main @ `6cf63b8`, SDK v0.0.2, Stainless-generated, Yarn 1, 123 endpoints).
- Saved the full target architecture verbatim: `docs/handover/ARCHITECTURE.md`.
- Audited SDK vs plan: `docs/handover/GAPS.md` (messaging, production/mix/effects, audio upload, delete-account not in SDK; blocks/contacts/keys/reports/push etc. in SDK but not in plan).
- Split all work into 19 session chunks with dependencies and acceptance criteria: `docs/handover/TASKS.md`.
- Defined session protocol and the git-am patch process: `docs/handover/PROTOCOL.md`.
- Added `scripts/handover/make-patch.sh` (builds one mbox `.patch`, verifies it applies cleanly on origin/main in a throwaway worktree).
- Wrote `HANDOVER.md` with the next-session pointer.

## Decisions made
- D1–D6 in HANDOVER.md. Notably: MCP lives in `mcp/`; generated SDK in `src/` is never hand-edited.
- Patch naming: `sNN-kebab-slug.patch`, chosen by each session.
- Next-session marker is a commit *subject* (`handover: complete SNN`), not a hash, because `git am` rewrites hashes.

## Verification
- `make-patch.sh` verified the patch applies cleanly to origin/main in a temp worktree.
- No code was changed, so no build/test run was needed.

## Deviations from the plan
- None. (Plan root `bandlab-mcp/` mapped to `mcp/`, flagged for owner awareness.)

## Known issues / blockers
- Git identity is a placeholder (`Claude Session`); owner may prefer their own — only affects commit author metadata.
- Owner must push this patch before S01 clones, or S01 will stop at the marker check.

## Next session
- **S01 — Scaffold `mcp/` package**
- First 3 things: (1) build the root SDK (`yarn install && yarn build`) to confirm it compiles; (2) create `mcp/package.json` + tsconfigs + eslint/prettier; (3) create the full empty directory skeleton with `.gitkeep`.
- Touches: `mcp/**` only (plus `HANDOVER.md`, `docs/handover/**` at finish).
