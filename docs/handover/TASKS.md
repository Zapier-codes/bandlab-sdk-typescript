# Session Task Chunks

Each chunk is sized for **one session**. Do them in order unless "Depends on" says otherwise.
All paths are relative to `mcp/` unless they start with `/` or say "repo root". Plan paths: see `ARCHITECTURE.md`.

## Status board  (update at the end of every session)

| ID | Title | Depends on | Status |
|----|-------|-----------|--------|
| S00 | Handover framework + planning | — | DONE |
| S01 | Scaffold `mcp/` package | S00 | TODO |
| S02 | BandLab client + auth layer (wraps SDK) | S01 | TODO |
| S03 | Shared infrastructure: utils, services, schemas/common, registry | S01 | TODO |
| S04 | Permission layer | S03 | TODO |
| S05 | API layer A: account, users, search, songs, revisions + types | S02, S03 | TODO |
| S06 | API layer B: collaborators, posts, comments, likes, followers, following | S05 | TODO |
| S07 | API layer C: bands, communities, collections, notifications, invitations | S05 | TODO |
| S08 | API layer D: media, genres, skills, labels, badges, settings, push, validation, versions (+ stubs for gaps) | S05 | TODO |
| S09 | Tools A: account, users, search | S04, S05 | TODO |
| S10 | Tools B: songs, revisions, collaborators | S06, S09 | TODO |
| S11 | Tools C: social (posts/comments/likes/feed), followers | S06, S09 | TODO |
| S12 | Tools D: bands, communities, collections, notifications, invitations | S07, S09 | TODO |
| S13 | Tools E: media, discovery, production/audio/messaging gap stubs | S08, S09 | TODO |
| S14 | Bulk operations | S11, S12 | TODO |
| S15 | Developer tools + capability/endpoint-status services | S13 | TODO |
| S16 | Research layer + Python discovery scripts + api-map | S02 | TODO (can run in parallel after S02) |
| S17 | Workflows | S10–S15 | TODO |
| S18 | Tests (unit + integration + workflow) | S17 | TODO |
| S19 | Docs, CI, README, release | S18 | TODO |

Rule: a session that discovers a previously-missing endpoint (S16) must update `GAPS.md` and the affected API/tool chunks.

---

## S01 — Scaffold `mcp/` package
**Goal:** buildable, lintable empty MCP server wired to the SDK.
- Create `mcp/` with `package.json`, `tsconfig.json`, `tsconfig.build.json`, `eslint.config.js`, `prettier.config.js`, `.gitignore`, `.env.example`, `README.md`, `LICENSE` (Apache-2.0 copy).
- Dependency on the SDK: `"bandlab-sdk": "file:.."` (or workspace); make sure the SDK builds first (`yarn build` at repo root). Document in README how to build both.
- Add `@modelcontextprotocol/sdk` and `zod`. Node ≥ 18, ESM or CJS — pick one and record it in the audit file.
- `src/index.ts` (stdio entry), `src/server.ts` (creates MCP server, registers nothing yet), `src/config.ts` (env: `BANDLAB_*`), `src/constants.ts`.
- Create **empty directory skeleton** (with `.gitkeep`) for the whole `mcp/` tree from ARCHITECTURE.md §1 so later sessions only fill files.
- Add `yarn dev|build|lint|test` scripts. Add one smoke test (server boots, lists zero tools).
- **Accept:** `cd mcp && yarn build && yarn lint && yarn test` green; repo-root SDK build unaffected.

## S02 — Client + auth layer
**Goal:** `src/bandlab/client/*` and `src/bandlab/auth/*`.
- `client.ts` constructs the SDK client; `authenticated-client.ts` injects tokens; `raw-client.ts` does arbitrary `GET/POST/...` through the same transport (for undocumented endpoints, HANDOVER D4).
- `request.ts`, `response.ts`, `errors.ts` (typed error hierarchy mapping SDK errors), `retry.ts` (backoff, honour `Retry-After`), `rate-limit.ts` (token bucket, configurable), `headers.ts`.
- Auth: `credentials.ts` (env/secure source; never log), `session.ts`, `tokens.ts`, `refresh.ts`, `auth-state.ts`. Use SDK `authorizations` resource.
- **Accept:** unit tests with mocked fetch for retry, rate-limit, refresh-on-401, redaction of secrets in logs.

## S03 — Shared infrastructure
- `utils/{ids,dates,validation,errors,serialization}.ts`
- `services/{logging,audit-log,caching,pagination,response-normalizer}.ts` (audit-log: append-only JSONL, secrets redacted).
- `schemas/common.ts` (zod: ids, pagination, cursor, error shape).
- `registry/{tool-registry,workflow-registry,capability-registry}.ts` — a tool declares `{name, domain, risk: read|write|privileged|destructive|bulk, inputSchema, handler, endpoints[]}`.
- **Accept:** unit tests; registry can register/list tools by domain and risk.

## S04 — Permission layer
- `permissions/{permission-manager,capability-registry,confirmation-manager,privileged-actions,destructive-actions,bulk-actions,policies}.ts`.
- Policy: Read = allowed; Write = allowed with audit; Privileged = requires `confirm:true` token; Destructive = two-step confirmation (preview → confirm with returned nonce); Bulk = dry-run default, hard caps, delay between ops.
- Config switch to run in **read-only mode**.
- Wrap tool dispatch in `server.ts` so no tool bypasses it (HANDOVER D5).
- **Accept:** unit tests for each risk class incl. nonce expiry.

## S05 — API layer A (account, users, search, songs, revisions)
- `bandlab/api/{account,users,search,songs,revisions}/` + `bandlab/types/{account,user,song,revision,common}.ts`.
- Thin typed functions over the SDK. Resolve open questions in GAPS.md §A (song creation via `POST /revisions`).
- Account = `me`, `passwords`, `emails`, `logins`. Include `users/{id}/keys`.
- **Accept:** each function has a mocked-SDK unit test; `docs/endpoint-status.md` created with these endpoints as `sdk-only`.

## S06 — API layer B (collaborators, posts, comments, likes, followers, following)
- Map add-collaborator → song invites; user-feed → `users/{id}/posts`; following-feed → `users/{id}/following/posts`.
- Include blocks and contacts (GAPS §B).
- types: `collaborator, post, comment, like, follower`.

## S07 — API layer C (bands, communities, collections, notifications, invitations)
- Honour singular/plural path quirks (GAPS §C). Notifications: list/count/following/mark-read/mark-all-read (`PATCH users/{id}/notifications`).
- types: `band, community, collection, notification, invitation`.

## S08 — API layer D (media, genres, skills, labels, badges, settings, push, validation, versions)
- `images`, `videos` (posts + views), `settings/notifications/*`, `push/registrations`, `validation`, `versions`, `reports`, `feedback`.
- Create **stub modules** for gaps (`audio/`, `samples/`, `effects/`, messaging) that throw `NotImplementedError` with status `unverified` and link to GAPS.md.
- types: `media, audio, effect`.

## S09 — Tools A: account, users, search
- All tools under `tools/account/`, `tools/users/`, `tools/search/` using plan filenames; each registered with correct risk class.
- `change-password`, `change-email`, login-provider changes = **Privileged**. `delete-account` = **Destructive** + `unverified` stub.
- zod schemas in `schemas/{account,users}.ts`. Normalise outputs via `response-normalizer`.
- **Accept:** tools list correctly via MCP `tools/list`; unit tests per tool with mocks.

## S10 — Tools B: songs, revisions, collaborators
- `tools/songs/*`, `tools/revisions/*`, `tools/collaborators/*`. `delete-song` = Destructive. `create-revision`/`fork-revision` = Write.
- schemas: `songs, revisions, collaboration`.

## S11 — Tools C: social + followers
- `tools/social/{posts,comments,likes,feed}/*`, `tools/followers/*` (+ block/unblock as Privileged).
- schemas: `social`.

## S12 — Tools D: bands, communities, collections, notifications, invitations
- Plan filenames. Deletes = Destructive. Invites create/accept/decline = Write/Privileged as appropriate.
- schemas: `collections, notifications, invitations`.

## S13 — Tools E: media, discovery, gap stubs
- `tools/media/*`, `tools/discovery/*`; `tools/production/*`, `tools/audio/*`, `tools/messaging/*` registered as **stubs** returning `NOT_IMPLEMENTED/unverified` (real impl after S16 finds endpoints).
- schemas: `production`.

## S14 — Bulk operations
- `tools/bulk/*`: `batch-executor` (concurrency 1–3, jittered delay, stop-on-error option), `dry-run`, `progress`, `results`; bulk follow/unfollow/like/unlike/comment/invite. `bulk-message` stub until messaging is verified.
- Defaults: dry-run on, max items per call (e.g. 25), global daily cap in config, full audit log. Make spam-like behaviour hard (dedupe, no identical comment spam without `allowDuplicate`).
- schemas: `bulk`.

## S15 — Developer tools + capability services
- `tools/developer/{capabilities,raw-request,validate,api-version,endpoint-status}.ts`; `raw-request` is **Privileged**, path allow-list for host.
- `services/{api-coverage,endpoint-registry,capability-discovery,health-check}.ts`.
- Generate `docs/endpoint-status.md` from the registry.

## S16 — Research layer + discovery scripts (can start after S02)
- `research/` tree + README; `research/endpoints/*.json` seeded from the SDK (`api.md`) including `unknown.json`.
- `scripts/compare-sdk-api`, `generate-api-map`, `validate-endpoints`, `inspect-responses` (TypeScript or **Python in `scripts/` only**, HANDOVER D3), `discover-endpoints`, `upload-audio`.
- Only against the owner's **own** account, polite rate limits; scrub all captures (no tokens/cookies) before commit.
- Goal: resolve GAPS §A (messaging, production, audio). Update `GAPS.md` and statuses.

## S17 — Workflows
- `workflows/*` (11 files) composing tools: artist-research, artist-discovery, song-analysis, project-inspection, music-production, collaboration, social-management, collection-management, notification-summary, account-management, bulk-campaign.
- Register in `workflow-registry`; expose as MCP prompts and/or composite tools.

## S18 — Tests
- Fill `tests/unit/*`, `tests/integration/*` (live tests gated by env `BANDLAB_LIVE=1`, skipped by default), `tests/workflows/*`.
- Coverage report; fix gaps found.

## S19 — Docs, CI, release
- `mcp/docs/*` (9 files), root `mcp/README.md`, `.github/workflows/{test,lint,build,release}.yml` (mind the existing Stainless workflows — don't break them).
- Final audit: every plan-tree file exists or is explicitly listed as deferred.
