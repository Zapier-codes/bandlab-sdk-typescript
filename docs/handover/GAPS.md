# Coverage Gaps — Plan vs. Generated SDK

Audit date: S00. Source: `api.md` (123 SDK methods). Re-verify with `scripts/compare-sdk-api/` once built (S15).

## A. Planned in the architecture, NOT in the SDK  → needs research / `raw-request`

| Planned tool(s) | Domain | Finding | Handling |
|-----------------|--------|---------|----------|
| `messaging/*` (conversations, messages, send-message, message-history, bulk-message) | 11 Messaging | **No messaging endpoints in SDK.** | Research (S15). Until verified, tools return `NOT_IMPLEMENTED` with status `unverified`. Bulk-message is blocked on this. |
| `production/*` (get-mix, edit-mix, effects CRUD, tracks, track-settings, project-structure) | 06 Production | **No mix/effects/track endpoints.** Only `revisions` get/patch/create/plays/forks exist. | Research (S15). Add to `research/endpoints/effects.json`. |
| `audio/*` (upload-audio, upload-sample, get-sample, audio-metadata) | 07 Audio | **No audio upload / sample endpoints.** SDK has image/video *post* creation only. | Research (S15) + `scripts/upload-audio/`. |
| `revisions/delete-revision` | 05 | No `DELETE /revisions/{id}`. | Research; may not exist. |
| `songs/create` (implicit) | 04 | No `POST /songs`; creation appears to be via `POST /revisions`. | Confirm in S04. |
| `collaborators/add-collaborator` | 08 | Only list + delete collaborator; adding is via **song invites** (`POST /song/{id}/invites`). | Map add-collaborator → song invite in S05. |
| `social/feed/user-feed` | 09 | Only `users/{id}/following/posts` (following feed) + `GET /posts`. | Map in S05; user-feed = `users/{id}/posts`. |
| `account/delete-account` | 01 | No delete-account endpoint (only `passwords`, `emails`, `logins`, `me`). | Research; mark `unverified`. |
| `media/media-posts` | 17 | Covered by `POST /images/{id}/posts`, `POST /videos/{id}/posts`; no list. | Fine; document. |

## B. In the SDK, NOT in the plan  → add tools

| SDK area | Endpoints | Suggested home |
|----------|-----------|----------------|
| Blocks | `users/{id}/blocks/users` list/post/delete | `tools/followers/` (block-user, unblock-user, list-blocked) — **Privileged** |
| Contacts | `users/{id}/contacts/users`, `/contacts/bands` | `tools/users/user-contacts.ts` |
| Access keys | `POST users/{id}/keys` | `tools/account/create-access-key.ts` — **Privileged** |
| Reports | `POST /reports` | `tools/developer/` or `tools/social/` — **Privileged** (affects other users) |
| Feedback | `POST /feedback` | `tools/developer/` |
| Push registrations | `POST/DELETE /push/registrations` | `tools/account/` — **Privileged** |
| Notification settings | `settings/notifications/email|push` get/patch | `tools/account/notification-settings.ts` |
| Video views / revision plays | `POST /videos/{id}/views`, `POST /revisions/{id}/plays` | `tools/media/`, `tools/revisions/play-revision.ts` |
| Authorizations | `POST /authorizations` | `bandlab/auth/` (login/token exchange) |
| Versions | `GET /versions/{clientId}`, `/valid` | `tools/developer/api-version.ts` |
| Validation | `GET /validation/{entityType}` | `tools/developer/validate.ts` |

## C. Inconsistent SDK path forms (watch out)

The SDK mixes singular/plural prefixes: `/song/{id}/invites`, `/song/{id}/posts`, `/community/{id}/invites|posts`
vs `/songs/{id}`, `/communities/{id}`. These come from the generated spec — **do not "fix" them**; wrap them.

## D. Status vocabulary used in `docs/endpoint-status.md`

`verified` (works against live API) · `sdk-only` (in SDK, untested live) · `unverified` (inferred) · `missing` (not found) · `blocked`.
