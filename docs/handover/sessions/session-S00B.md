# Session S00B — Rules correction: in-place revamp
- Date: 2026-10-03
- Status: DONE
- Patch: s00b-in-place-revamp-rules.patch (stacked on S00; apply S00 first if not already applied)

## Why
S00 invented a rule (D1 "generated SDK in `src/` is read-only") and put the MCP in `mcp/`. The owner ruled both void: it is their own project,
the existing code is being revamped, and the missing layers are added inside `src/`.

## What was done
- Audited existing code against the architecture tree: `docs/handover/EXISTING-VS-PLAN.md` (move / split / keep / new for every area).
- Rewrote the rules (HANDOVER D1–D10), removed `mcp/` everywhere.
- Rewrote `TASKS.md` into 18 chunks: S01 detach, S02–S04 relocate (client/types, resources A, resources B), S05 client+auth, S06 infra, S07 permissions+server, S08 research, S09 new API modules, S10–S13 tools, S14 bulk, S15 developer, S16 workflows, S17 tests, S18 docs/CI.
- Updated ARCHITECTURE header, GAPS (session refs, path-quirk rule), PROTOCOL (src editable, move/edit discipline, patch stacking), `make-patch.sh` (`PATCH_BASE`, `sNNx` names).

## Findings from the audit
- Auth today is one static bearer token; the whole auth layer is new.
- `environments.production` points at `https://test.bandlab.com/api/v1.3`; `bandlab.com` is the second environment. Verify and fix in S02.
- `tests/api-resources` depend on a Prism mock fed from the spec URL in `.stats.yml`; snapshot the spec before removing Stainless files (S01).
- Plan tree lacks `api/messaging/`, `api/reports/`, `api/feedback/`, and a home for blocks/contacts; added as documented additions.
- `src/index.ts` clashes with the plan's MCP entry; resolved as D8.

## Decisions made (owner may overrule)
- D8 (index.ts barrel, server.ts entry), keep `src/core` + `src/internal` as the HTTP runtime, relocate via `git mv` rather than leaving two parallel structures.

## Verification
- Docs and one shell script only; no build/test run needed. Patch verified to apply on the S00 marker commit.

## Deviations from the plan
- The additions listed above.

## Known issues / blockers
- Sandbox may not reach `storage.googleapis.com` (not on the network allow-list) to download the spec in S01; if so the owner must supply the spec file.

## Next session
- **S01 — Detach from Stainless, package identity, tooling baseline, plan skeleton**
- First 3 things: (1) `yarn install && yarn build && yarn test`, record baseline; (2) snapshot the OpenAPI spec into `research/openapi-snapshot.yml`; (3) rewrite `package.json` identity.
- Touches: `package.json`, `scripts/`, `.github/`, root config files, new empty skeleton dirs.
