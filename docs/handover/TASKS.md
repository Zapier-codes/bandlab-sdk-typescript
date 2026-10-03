# Session Task Chunks  (rewritten in S00B for the in-place revamp)

Each chunk is sized for **one session**. Do them in order unless "Depends on" says otherwise.
All paths are relative to the **repo root** (the architecture tree is the repo root; no `mcp/` folder). What exists / moves / is new: `EXISTING-VS-PLAN.md`.

Refactor discipline (applies to S01–S05): **moves and edits are separate commits.** Use `git mv` so history follows files. Run `yarn build && yarn lint && yarn test` after each move commit.
A moved file's only change in its move commit is import paths.

## Status board  (update at the end of every session)

| ID | Title | Depends on | Status |
|----|-------|-----------|--------|
| S00 | Handover framework + planning | — | DONE |
| S00B | Rules correction: in-place revamp, no `mcp/`, existing-vs-plan audit | S00 | DONE |
| S01 | Detach from Stainless, package identity, tooling baseline, plan skeleton | S00B | TODO |
| S02 | Relocate client + shared types → `src/bandlab/client`, `src/bandlab/types` | S01 | TODO |
| S03 | Relocate resources A → account, users, search, songs, revisions, collaborators | S02 | TODO |
| S04 | Relocate resources B → everything else in `api/` | S03 | TODO |
| S05 | Extend client + build auth layer (retry, rate-limit, raw/authenticated client, session/refresh) | S04 | TODO |
| S06 | Shared infrastructure: utils, services, `schemas/common`, registry | S05 | TODO |
| S07 | Permission layer + `server.ts`/`config.ts`/`constants.ts` MCP wiring | S06 | TODO |
| S08 | Research layer + discovery scripts + api-map (resolve GAPS §A) | S05 | TODO |
| S09 | New API modules for missing domains (audio, samples, effects, messaging, reports/feedback tidy) | S08, S06 | TODO |
| S10 | Tools A: account, users, search | S07, S04 | TODO |
| S11 | Tools B: songs, revisions, production, audio, collaborators | S09, S10 | TODO |
| S12 | Tools C: social (posts/comments/likes/feed), followers, messaging | S09, S10 | TODO |
| S13 | Tools D: bands, communities, collections, notifications, invitations, media, discovery | S10 | TODO |
| S14 | Bulk operations | S12, S13 | TODO |
| S15 | Developer tools + capability/endpoint-status services | S13 | TODO |
| S16 | Workflows | S11–S15 | TODO |
| S17 | Tests (unit + integration + workflow) | S16 | TODO |
| S18 | Docs, CI, README, release | S17 | TODO |

If S08 discovers new endpoints, update `GAPS.md` and the affected chunks.

---

## S01 — Detach from Stainless, identity, tooling baseline, skeleton
- First run `yarn install && yarn build && yarn test` and record the baseline (note which tests need the Prism mock).
- **Snapshot the OpenAPI spec** referenced in `.stats.yml` into `research/openapi-snapshot.yml` (try `curl`; if the sandbox blocks `storage.googleapis.com`, record that as a BLOCKER and ask the owner to supply the file). Repoint `scripts/mock` to the snapshot. Only then remove `.stats.yml`.
- Remove Stainless/release scaffolding listed in `EXISTING-VS-PLAN.md` §7 (`release-please*`, `bin/*`, auto-CHANGELOG, `release-doctor`/`publish-npm` workflows, `prepare` git-install hook). Keep `scripts/{build,lint,format,test,mock}`.
- Rewrite `package.json`: name, description, repository (`Zapier-codes/bandlab-sdk-typescript`), author, license (keep Apache-2.0 unless owner says otherwise), add `bin` placeholder for `src/server.ts`.
- Add: `.env.example`, `prettier.config.js` (migrate from `.prettierrc.json`), plan root files (`README.md` rewrite, `tsconfig.build.json` already exists).
- Create the **empty directory skeleton** (`.gitkeep`) for every NEW path in `EXISTING-VS-PLAN.md` §4.
- **Accept:** build/lint/test results equal the baseline; no references to Stainless codegen remain except historical CHANGELOG.

## S02 — Relocate client + shared types
- `git mv src/client.ts src/bandlab/client/client.ts`; merge errors into `client/errors.ts`; move `internal/headers.ts` → `client/headers.ts`. Fix imports everywhere (`src/index.ts` stays the barrel, D8).
- Split `src/resources/shared.ts` and per-resource type exports into `src/bandlab/types/*` (plan filenames). Re-export so `src/index.ts` public surface is unchanged.
- Check the base-URL finding (EXISTING-VS-PLAN §8): fix `production` default if it truly points at a test host; keep the old value reachable as an explicit environment.
- Support both `BANDLAB_*` and legacy `BANDLAB_SDK_*` env vars.
- **Accept:** zero behaviour change except the two items above; all baseline tests green.

## S03 — Relocate resources A
- Move per mapping table: `me/passwords/emails/logins` → `api/account/`; `users/*` core → `api/users/`; `search` → `api/search/`; `songs` → `api/songs/`; `songs/revisions` + `revisions` → `api/revisions/`; `songs/collaborators` → `api/collaborators/`.
- Update `BandlabSDK` resource wiring and `tests/api-resources/**` imports; keep public client API (`client.me`, `client.songs…`) working.
- Resolve GAPS: song creation via `POST /revisions`; add-collaborator via song invites.
- **Accept:** tests green; `api.md` regenerated by hand or script to match new paths (it is now our doc, not generated).

## S04 — Relocate resources B
- Everything else per mapping: followers, following, notifications, invitations (merge the five `invites` modules), posts, comments, likes, bands, communities, collections, images, videos, genres, skills, labels, badges, settings, push, validation, versions, reports, feedback, authorizations → `auth/`.
- Blocks, contacts, recommendations stay under `api/users/`.
- **Accept:** `src/resources/` is empty/removed; tests green.

## S05 — Extend client + auth layer
- Split out of `client.ts`: `retry.ts` (honour `Retry-After`), `request.ts`, `response.ts`; add `rate-limit.ts` (token bucket, configurable), `authenticated-client.ts`, `raw-client.ts` (arbitrary method/path through the same transport; used for undocumented endpoints).
- Typed error hierarchy.
- Auth: `credentials.ts` (env/secure source; never log), `session.ts`, `tokens.ts`, `refresh.ts`, `auth-state.ts`, built on the existing `authorizations.createSessionKey`.
- **Accept:** unit tests (mock fetch) for retry, rate-limit, refresh-on-401, and secret redaction in logs.

## S06 — Shared infrastructure
- `utils/{ids,dates,validation,errors,serialization}.ts`; `services/{logging,audit-log,caching,pagination,response-normalizer}.ts` (audit-log = append-only JSONL, secrets redacted); `schemas/common.ts` (zod).
- `registry/{tool-registry,workflow-registry,capability-registry}.ts`; a tool declares `{name, domain, risk: read|write|privileged|destructive|bulk, inputSchema, handler, endpoints[]}`.
- **Accept:** unit tests; registry lists tools by domain and risk.

## S07 — Permission layer + server wiring
- `permissions/*` (all 7 files). Policy: Read allowed; Write allowed + audited; Privileged needs explicit confirm; Destructive two-step (preview → confirm nonce, expiring); Bulk dry-run by default with caps. Config switch for read-only mode.
- `src/server.ts` (MCP stdio server; **all dispatch goes through the permission layer, D5**), `src/config.ts`, `src/constants.ts`; `package.json` `bin`.
- Add `@modelcontextprotocol/sdk` and `zod`.
- **Accept:** server boots, `tools/list` works with zero tools; unit tests for every risk class.

## S08 — Research layer + discovery
- Create `research/` tree and README; seed `research/endpoints/*.json` from the existing resources (`unknown.json` for the rest); `schemas/`, `captures/`, `experiments/`, `api-map.json`.
- Scripts: `discover-endpoints`, `compare-sdk-api`, `generate-api-map`, `validate-endpoints`, `inspect-responses`, `upload-audio` (Python allowed here only, D4).
- Own account only, polite rate limits, **scrub all captures** (no tokens/cookies) before commit.
- Goal: resolve GAPS §A (messaging, production/mix/effects, audio/samples, delete-account, delete-revision). Update `GAPS.md`.
- **Accept:** `api-map.json` generated; each GAPS §A item marked verified / missing / blocked.

## S09 — New API modules for missing domains
- Implement `api/audio/`, `api/samples/`, `api/effects/`, `api/messaging/` using S08 findings. Anything not proven live is flagged `unverified` and throws a typed `NotImplementedError` rather than guessing.
- Types: `audio.ts`, `effect.ts`, messaging types.
- **Accept:** mocked unit tests; `docs/endpoint-status.md` created with a status per endpoint.

## S10 — Tools A: account, users, search
- Plan filenames. `change-password`, `change-email`, login-provider changes = Privileged; `delete-account` = Destructive (stub if unverified).
- `schemas/{account,users}.ts`; add tools for blocks/contacts/access-keys (GAPS §B).

## S11 — Tools B: songs, revisions, production, audio, collaborators
- `delete-song` = Destructive. `schemas/{songs,revisions,production,collaboration}.ts`. Production/audio tools real only where S09 verified, else `NOT_IMPLEMENTED/unverified`.

## S12 — Tools C: social, followers, messaging
- `social/{posts,comments,likes,feed}`, `followers/*` (+ block/unblock Privileged), `messaging/*` per S09. `schemas/social.ts`.

## S13 — Tools D: bands, communities, collections, notifications, invitations, media, discovery
- Plan filenames; deletes = Destructive. `schemas/{collections,notifications,invitations}.ts`.

## S14 — Bulk operations
- `tools/bulk/*`: `batch-executor` (concurrency 1–3, jittered delay, stop-on-error), `dry-run`, `progress`, `results`; follow/unfollow/like/unlike/comment/invite; `bulk-message` only if messaging verified.
- Defaults: dry-run on, per-call cap (e.g. 25), daily cap in config, full audit log, dedupe, no identical-comment spam without explicit `allowDuplicate`. `schemas/bulk.ts`.

## S15 — Developer tools + capability services
- `tools/developer/*` (`raw-request` Privileged, host allow-list); `services/{api-coverage,endpoint-registry,capability-discovery,health-check}.ts`; generate `docs/endpoint-status.md` from the registry.

## S16 — Workflows
- All 11 `workflows/*` files; register in `workflow-registry`; expose as MCP prompts and/or composite tools.

## S17 — Tests
- `tests/unit/*`, `tests/integration/*` (live tests gated by `BANDLAB_LIVE=1`, skipped by default), `tests/workflows/*`; coverage report.

## S18 — Docs, CI, release
- Plan `docs/*` (9 files), final `README.md`, `.github/workflows/{test,lint,build,release}.yml`.
- Final audit: every file in the plan tree exists or is explicitly listed as deferred.
