# Coverage Matrix and Missing-Capability Register

Source of truth for what the SDK covers. Baseline inventory (123 methods, snapshot of `api.md`): `endpoint-inventory.tsv`
(columns: HTTP verb, path, resource accessor). S01 builds a script that regenerates and diffs it.

Status vocabulary for endpoints (tracked in `docs/endpoint-status.md` from S01):
`spec` (in the original OpenAPI spec) · `captured` (seen in a real request capture) · `unverified` (inferred, no evidence yet) · `live-ok` (owner ran it successfully) · `missing`.

## 1. Domain matrix (the 17 domains)

| # | Domain | Status | Existing accessors | What is missing |
|---|--------|--------|--------------------|-----------------|
| 01 | Account & Identity | Partial | `me`, `passwords`, `emails.confirmations`, `logins`, `users.keys`, `authorizations`, `push.registrations`, `settings.notifications.{email,push}` | change-email (`emails.ts` has no methods) · delete-account |
| 02 | Users & Artists | Covered | `users` (retrieve, bands, collections, communities, posts, songs), `contacts`, `recommendations`, `blocks.users` | — |
| 03 | Search & Discovery | Partial | `search` (all, users, songs, bands, collections), `genres`, `skills`, `labels`, `badges` | search posts |
| 04 | Songs | Partial | `songs` (retrieve, update, delete, posts), `songs.revisions`, `songs.collaborators`, `songs.invites` | create song · list songs (only per-user) |
| 05 | Projects & Revisions | Partial | `revisions` (create, retrieve, update, addPlay), `songs.revisions` (list, fork) | delete revision |
| 06 | Production / Mix / Effects | **Missing** | none (revision types mention `AudioSample`, `Mastering`) | mix, effects, tracks, track settings, project structure |
| 07 | Audio / Samples / Uploads | **Missing** | none (`core/uploads` handles generic file bodies) | audio upload, sample upload/get, audio metadata |
| 08 | Collaborators | Partial | `songs.collaborators` (list, delete) | add/update collaborator (currently only via `songs.invites`; confirm) |
| 09 | Posts / Social | Partial | `posts` (list, retrieve, update, delete), `posts.comments` (list, create, delete), `posts.likes`, `images`, `videos` | create post (generic) · get/update comment |
| 10 | Followers / Following | Covered | `users.followers`, `users.following`, `users.blocks` | — |
| 11 | Messaging | **Missing** | none | conversations, messages, send, history |
| 12 | Bands | Covered | `bands` (CRUD, posts, songs), `bands.members`, `bands.invites` | — |
| 13 | Communities | Covered | `communities` (CRUD), `.members`, `.invites`, `.posts` | — |
| 14 | Collections | Covered | `collections` (CRUD), `.posts` (add, get, update, remove), `.likes` | — |
| 15 | Notifications | Covered | `users.notifications` (list, count, following, mark one, mark all), `settings.notifications.*` | — |
| 16 | Invitations | Covered | `invites` (get, create, update/accept, delete), `users|songs|bands|communities.invites` | — |
| 17 | Media / Metadata / Dev | Partial | `images.post`, `videos.post/views`, `validation`, `versions`, `reports`, `feedback` | get/upload image & video media |

## 2. Missing-capability register  (each needs evidence before implementation)

| ID | Capability | Domain | Likely home | Evidence status |
|----|-----------|--------|-------------|-----------------|
| G01 | Messaging (conversations, messages, send, history) | 11 | new `src/resources/messaging.ts` (+ sub-resources if needed) | none |
| G02 | Mix / effects / tracks / track settings / project structure | 06 | new `src/resources/` file(s); possibly extend `revisions.ts` | none |
| G03 | Audio upload, sample upload/get, audio metadata | 07 | new `src/resources/audio.ts`, `samples.ts` | none |
| G04 | Create song (may be `POST /revisions`); list songs | 04 | `songs/songs.ts` / `revisions.ts` | partial hint |
| G05 | Delete revision | 05 | `revisions.ts` | none |
| G06 | Create post (generic) | 09 | `posts/posts.ts` | none (image/video/band/community post creation exist) |
| G07 | Get / update single comment | 09 | `posts/comments.ts` | none |
| G08 | Search posts | 03 | `search.ts` | none |
| G09 | Change email | 01 | `emails/emails.ts` | none |
| G10 | Delete account | 01 | `me.ts` or new | none |
| G11 | Add / update collaborator | 08 | `songs/collaborators.ts` | partial hint (invites) |
| G12 | Image / video get + upload | 17 | `images.ts`, `videos.ts` | none |
| G13 | Unknown extras BandLab exposes that nobody listed (reposts, playlists, studio projects, etc.) | — | decided by research | n/a — discovered in S03 |

"none" means no request/response shape has been seen. Sessions must not guess shapes.

## 3. Escape hatch for anything not yet modelled
`client.get|post|patch|put|delete(path, opts)` already exist on `BandlabSDK`. Research scripts and unverified experiments use these,
so no endpoint is ever blocked by the SDK itself.
