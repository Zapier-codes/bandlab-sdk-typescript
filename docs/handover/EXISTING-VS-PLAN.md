# Existing Code vs. Target Architecture (audit done in S00B)

The architecture tree in `ARCHITECTURE.md` is the **repo root**. There is no `mcp/` folder.
We revamp the existing code in place: **move** what already works into the plan's paths, **extend** where partial, **add** what is missing.

Legend: MOVE = `git mv` into plan path (no behaviour change) · SPLIT = break one file into several plan files · KEEP = stays where it is · NEW = does not exist yet · EXT = exists, needs extending.

## 1. Transport / client layer

| Existing | Disposition | Plan target |
|----------|-------------|-------------|
| `src/client.ts` (1066 lines, class `BandlabSDK`: options, base URL, retries, timeout, logging, auth header, resource wiring) | MOVE then SPLIT | `src/bandlab/client/client.ts`; retry logic → `retry.ts`; header building → `headers.ts`; request build/dispatch → `request.ts`; response parsing → `response.ts` |
| `src/core/error.ts`, `src/internal/errors.ts`, `src/error.ts` | MOVE/merge | `src/bandlab/client/errors.ts` (+ `src/utils/errors.ts` for non-HTTP errors) |
| `src/internal/headers.ts` | MOVE | `src/bandlab/client/headers.ts` |
| `src/core/api-promise.ts`, `src/api-promise.ts`, `src/core/resource.ts`, `src/resource.ts`, `src/core/uploads.ts`, `src/internal/*` (parse, request-options, shims, to-file, uploads, utils/*) | KEEP | HTTP runtime used by the client. Stays at `src/core/` and `src/internal/` (documented addition to the plan). Plan `src/utils/` is for MCP-level helpers. |
| `src/lib/` | KEEP | Free custom-code area; unused so far. |
| Rate limiting | NEW | `client/rate-limit.ts` (only retry exists today, `maxRetries` default 2) |
| Authenticated wrapper / raw client | NEW | `client/authenticated-client.ts`, `client/raw-client.ts` |

## 2. Auth layer — almost entirely missing

Today: a single static bearer token (`BANDLAB_SDK_BEARER_TOKEN`) set on the client; header `Authorization: Bearer …`. No refresh, no session state.
`src/resources/authorizations.ts` has `createSessionKey` (`POST /authorizations`).

| Plan file | Status |
|-----------|--------|
| `auth/credentials.ts`, `session.ts`, `tokens.ts`, `refresh.ts`, `auth-state.ts` | NEW (build on `authorizations` resource) |

## 3. API layer (`src/resources/*` → `src/bandlab/api/*`)

| Existing resource | Plan target | Notes |
|-------------------|-------------|-------|
| `me.ts`, `passwords.ts`, `emails/*`, `logins.ts` | `api/account/` | MOVE |
| `users/users.ts` (+ `keys`, bands, collections, communities, posts, songs) | `api/users/` | MOVE |
| `users/blocks/*`, `users/contacts.ts`, `users/recommendations.ts` | `api/users/` | MOVE (blocks/contacts are **not in the plan** — added) |
| `users/followers.ts` | `api/followers/` | MOVE |
| `users/following.ts` | `api/following/` | MOVE |
| `users/notifications.ts` | `api/notifications/` | MOVE |
| `users/invites.ts`, `invites.ts`, `songs/invites.ts`, `bands/invites.ts`, `communities/invites.ts` | `api/invitations/` | MOVE/merge |
| `search.ts` | `api/search/` | MOVE |
| `songs/songs.ts` | `api/songs/` | MOVE |
| `songs/revisions.ts`, `revisions.ts` | `api/revisions/` | MOVE/merge |
| `songs/collaborators.ts` | `api/collaborators/` | MOVE |
| `posts/posts.ts` | `api/posts/` | MOVE |
| `posts/comments.ts` | `api/comments/` | MOVE |
| `posts/likes.ts` | `api/likes/` | MOVE |
| `bands/bands.ts`, `bands/members.ts` | `api/bands/` | MOVE |
| `communities/communities.ts`, `members.ts`, `posts.ts` | `api/communities/` | MOVE |
| `collections/collections.ts`, `posts.ts`, `likes.ts` | `api/collections/` | MOVE |
| `images.ts`, `videos.ts` | `api/images/`, `api/videos/` | MOVE |
| `genres.ts`, `skills.ts`, `labels.ts`, `badges.ts` | `api/genres|skills|labels|badges/` | MOVE |
| `settings/*` | `api/settings/` | MOVE |
| `push/*` | `api/push/` | MOVE |
| `validation.ts`, `versions.ts` | `api/validation/`, `api/versions/` | MOVE |
| `reports.ts`, `feedback.ts` | `api/reports/`, `api/feedback/` | MOVE (**not in plan** — added dirs) |
| `authorizations.ts` | `auth/` | MOVE/merge into auth layer |
| `shared.ts` (+ per-resource type exports) | `bandlab/types/*` | SPLIT by domain; `common.ts` gets shared |
| Missing: `api/audio/`, `api/samples/`, `api/effects/` | NEW | no SDK endpoints exist (GAPS §A) |
| Missing: messaging API | NEW | plan has `tools/messaging/` but **no `api/messaging/`** — we add `api/messaging/` (plan addition) |

Wire paths (`/song/{id}/invites` vs `/songs/{id}`) must stay exactly as the server expects. Our *internal names* may be normalised.

## 4. Everything else in the plan — NEW (nothing exists)

`src/server.ts`, `src/config.ts`, `src/constants.ts`, `src/tools/**` (all ~170 tool files), `src/workflows/**`, `src/permissions/**`,
`src/schemas/**`, `src/services/**`, `src/utils/**`, `src/registry/**`, `research/**`, `scripts/{discover-endpoints,compare-sdk-api,generate-api-map,validate-endpoints,inspect-responses,upload-audio}`,
`tests/unit/**`, `tests/integration/**`, `tests/workflows/**`, plan `docs/*` (9 files), `.env.example`, `prettier.config.js`.

## 5. `src/index.ts` conflict (decision D8)

The plan lists `src/index.ts` as the MCP entry. Today it is the public library barrel (22 lines, exports client + errors + types) and tests import from it.
**Decision:** `src/index.ts` stays the library barrel (re-exporting `src/bandlab/*`). The MCP stdio entry is `src/server.ts`, exposed through `package.json` `bin`. Owner may overrule.

## 6. Tests

| Existing | Disposition |
|----------|-------------|
| `tests/api-resources/**` (one test per resource; run against a Prism mock built from the OpenAPI spec URL in `.stats.yml`) | KEEP, update import paths as resources move. **Do not delete `.stats.yml` until the spec is snapshotted into `research/` (D7)** — the mock script reads the URL from it. |
| `tests/{base64,buildHeaders,form,index,path,stringifyQuery,uploads}.test.ts` | KEEP, update imports |
| Plan `tests/unit|integration|workflows` | NEW |

## 7. Stainless / release scaffolding (detach in S01)

`.stats.yml`, `release-please-config.json`, `.release-please-manifest.json`, `CHANGELOG.md` (auto), `bin/check-release-environment`, `bin/publish-npm`,
`.github/workflows/{ci,publish-npm,release-doctor}.yml`, `scripts/utils/{git-swap,check-is-in-git-install,...}`, `package.json` `prepare` hook, branches `generated`/`next`.
Plan CI = `.github/workflows/{test,lint,build,release}.yml`.
`package.json`: name `bandlab-sdk`, description "official TypeScript library", repo `github:unityaisolutions/...`, author `Bandlab SDK` — all to be rewritten.

## 8. Findings to verify early

- `environments.production` = `https://test.bandlab.com/api/v1.3`, `environment_1` = `https://bandlab.com/api/v1.3`. The default points at a **test host**; confirm and correct in the client move (S02).
- Env vars are `BANDLAB_SDK_*`. Plan `config.ts` wants `BANDLAB_*`. Support both during transition.
