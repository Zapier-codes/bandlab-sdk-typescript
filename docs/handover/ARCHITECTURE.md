# Target Architecture — Private BandLab MCP

> Saved verbatim from the owner's plan. **The tree below IS the repo root** — there is no `mcp/` folder (owner ruling, S00B).
> The existing SDK code is revamped in place: moved into these paths, extended, and the missing layers added.
> See `EXISTING-VS-PLAN.md` for exactly what exists, what moves, and what is new.
> Documented additions to the plan: `src/core/` + `src/internal/` (HTTP runtime kept), `api/messaging/`, `api/reports/`, `api/feedback/`, blocks/contacts under `api/users/`.
> The root label `bandlab-mcp/` in the tree means "repo root".
## 1. Full target tree

```text
bandlab-mcp/
│
├── README.md
├── LICENSE
├── package.json
├── tsconfig.json
├── tsconfig.build.json
├── eslint.config.js
├── prettier.config.js
├── .gitignore
├── .env.example
│
├── docs/
│   ├── architecture.md
│   ├── capabilities.md
│   ├── authentication.md
│   ├── permissions.md
│   ├── api-coverage.md
│   ├── endpoint-status.md
│   ├── workflows.md
│   ├── reverse-engineering.md
│   └── security.md
│
├── research/
│   │
│   ├── README.md
│   │
│   ├── endpoints/
│   │   ├── account.json
│   │   ├── users.json
│   │   ├── search.json
│   │   ├── songs.json
│   │   ├── revisions.json
│   │   ├── collaborators.json
│   │   ├── posts.json
│   │   ├── comments.json
│   │   ├── likes.json
│   │   ├── followers.json
│   │   ├── bands.json
│   │   ├── communities.json
│   │   ├── collections.json
│   │   ├── notifications.json
│   │   ├── invitations.json
│   │   ├── media.json
│   │   ├── audio.json
│   │   ├── videos.json
│   │   ├── images.json
│   │   ├── effects.json
│   │   ├── genres.json
│   │   ├── skills.json
│   │   ├── labels.json
│   │   ├── badges.json
│   │   ├── settings.json
│   │   └── unknown.json
│   │
│   ├── schemas/
│   │   ├── users/
│   │   ├── songs/
│   │   ├── revisions/
│   │   ├── posts/
│   │   ├── comments/
│   │   ├── collections/
│   │   ├── bands/
│   │   ├── communities/
│   │   └── media/
│   │
│   ├── captures/
│   │   ├── requests/
│   │   └── responses/
│   │
│   ├── experiments/
│   │   ├── authentication/
│   │   ├── songs/
│   │   ├── revisions/
│   │   ├── uploads/
│   │   ├── social/
│   │   └── account/
│   │
│   └── api-map.json
│
├── src/
│   │
│   ├── index.ts
│   ├── server.ts
│   ├── config.ts
│   ├── constants.ts
│   │
│   ├── bandlab/
│   │   │
│   │   ├── client/
│   │   │   ├── client.ts
│   │   │   ├── authenticated-client.ts
│   │   │   ├── raw-client.ts
│   │   │   ├── request.ts
│   │   │   ├── response.ts
│   │   │   ├── errors.ts
│   │   │   ├── retry.ts
│   │   │   ├── rate-limit.ts
│   │   │   └── headers.ts
│   │   │
│   │   ├── auth/
│   │   │   ├── session.ts
│   │   │   ├── tokens.ts
│   │   │   ├── refresh.ts
│   │   │   ├── credentials.ts
│   │   │   └── auth-state.ts
│   │   │
│   │   ├── api/
│   │   │   │
│   │   │   ├── account/
│   │   │   ├── users/
│   │   │   ├── search/
│   │   │   ├── songs/
│   │   │   ├── revisions/
│   │   │   ├── collaborators/
│   │   │   ├── posts/
│   │   │   ├── comments/
│   │   │   ├── likes/
│   │   │   ├── followers/
│   │   │   ├── following/
│   │   │   ├── bands/
│   │   │   ├── communities/
│   │   │   ├── collections/
│   │   │   ├── notifications/
│   │   │   ├── invitations/
│   │   │   ├── audio/
│   │   │   ├── samples/
│   │   │   ├── videos/
│   │   │   ├── images/
│   │   │   ├── effects/
│   │   │   ├── genres/
│   │   │   ├── skills/
│   │   │   ├── labels/
│   │   │   ├── badges/
│   │   │   ├── settings/
│   │   │   ├── push/
│   │   │   ├── validation/
│   │   │   └── versions/
│   │   │
│   │   ├── types/
│   │   │   ├── account.ts
│   │   │   ├── user.ts
│   │   │   ├── song.ts
│   │   │   ├── revision.ts
│   │   │   ├── collaborator.ts
│   │   │   ├── post.ts
│   │   │   ├── comment.ts
│   │   │   ├── like.ts
│   │   │   ├── follower.ts
│   │   │   ├── band.ts
│   │   │   ├── community.ts
│   │   │   ├── collection.ts
│   │   │   ├── notification.ts
│   │   │   ├── invitation.ts
│   │   │   ├── media.ts
│   │   │   ├── audio.ts
│   │   │   ├── effect.ts
│   │   │   └── common.ts
│   │   │
│   │   └── index.ts
│   │
│   ├── tools/
│   │   │
│   │   ├── account/
│   │   │   ├── whoami.ts
│   │   │   ├── get-me.ts
│   │   │   ├── update-profile.ts
│   │   │   ├── change-password.ts
│   │   │   ├── change-email.ts
│   │   │   ├── confirm-email.ts
│   │   │   ├── delete-account.ts
│   │   │   ├── login-providers.ts
│   │   │   ├── add-login-provider.ts
│   │   │   ├── change-login-provider.ts
│   │   │   └── remove-login-provider.ts
│   │   │
│   │   ├── users/
│   │   │   ├── get-user.ts
│   │   │   ├── search-users.ts
│   │   │   ├── user-songs.ts
│   │   │   ├── user-posts.ts
│   │   │   ├── user-followers.ts
│   │   │   ├── user-following.ts
│   │   │   ├── user-bands.ts
│   │   │   ├── user-collections.ts
│   │   │   ├── user-communities.ts
│   │   │   └── user-recommendations.ts
│   │   │
│   │   ├── search/
│   │   │   ├── search.ts
│   │   │   ├── search-users.ts
│   │   │   ├── search-songs.ts
│   │   │   ├── search-posts.ts
│   │   │   ├── search-bands.ts
│   │   │   └── search-collections.ts
│   │   │
│   │   ├── songs/
│   │   │   ├── list-songs.ts
│   │   │   ├── get-song.ts
│   │   │   ├── update-song.ts
│   │   │   ├── delete-song.ts
│   │   │   ├── song-posts.ts
│   │   │   ├── song-collaborators.ts
│   │   │   └── song-revisions.ts
│   │   │
│   │   ├── revisions/
│   │   │   ├── list-revisions.ts
│   │   │   ├── get-revision.ts
│   │   │   ├── create-revision.ts
│   │   │   ├── update-revision.ts
│   │   │   ├── delete-revision.ts
│   │   │   ├── fork-revision.ts
│   │   │   └── play-revision.ts
│   │   │
│   │   ├── production/
│   │   │   ├── get-mix.ts
│   │   │   ├── edit-mix.ts
│   │   │   ├── list-effects.ts
│   │   │   ├── get-effect.ts
│   │   │   ├── add-effect.ts
│   │   │   ├── update-effect.ts
│   │   │   ├── remove-effect.ts
│   │   │   ├── tracks.ts
│   │   │   ├── track-settings.ts
│   │   │   └── project-structure.ts
│   │   │
│   │   ├── audio/
│   │   │   ├── upload-audio.ts
│   │   │   ├── upload-sample.ts
│   │   │   ├── get-sample.ts
│   │   │   └── audio-metadata.ts
│   │   │
│   │   ├── collaborators/
│   │   │   ├── list-collaborators.ts
│   │   │   ├── add-collaborator.ts
│   │   │   ├── remove-collaborator.ts
│   │   │   └── collaboration-invites.ts
│   │   │
│   │   ├── social/
│   │   │   ├── posts/
│   │   │   │   ├── get-post.ts
│   │   │   │   ├── search-posts.ts
│   │   │   │   ├── create-post.ts
│   │   │   │   ├── update-post.ts
│   │   │   │   └── delete-post.ts
│   │   │   │
│   │   │   ├── comments/
│   │   │   │   ├── list-comments.ts
│   │   │   │   ├── get-comment.ts
│   │   │   │   ├── create-comment.ts
│   │   │   │   └── delete-comment.ts
│   │   │   │
│   │   │   ├── likes/
│   │   │   │   ├── list-likes.ts
│   │   │   │   ├── like-post.ts
│   │   │   │   └── unlike-post.ts
│   │   │   │
│   │   │   └── feed/
│   │   │       ├── user-feed.ts
│   │   │       └── following-feed.ts
│   │   │
│   │   ├── followers/
│   │   │   ├── followers.ts
│   │   │   ├── following.ts
│   │   │   ├── follow-user.ts
│   │   │   └── unfollow-user.ts
│   │   │
│   │   ├── messaging/
│   │   │   ├── conversations.ts
│   │   │   ├── messages.ts
│   │   │   ├── send-message.ts
│   │   │   └── message-history.ts
│   │   │
│   │   ├── bands/
│   │   │   ├── create-band.ts
│   │   │   ├── get-band.ts
│   │   │   ├── update-band.ts
│   │   │   ├── delete-band.ts
│   │   │   ├── members.ts
│   │   │   ├── add-member.ts
│   │   │   ├── update-member.ts
│   │   │   ├── remove-member.ts
│   │   │   ├── band-songs.ts
│   │   │   └── band-posts.ts
│   │   │
│   │   ├── communities/
│   │   │   ├── create-community.ts
│   │   │   ├── get-community.ts
│   │   │   ├── update-community.ts
│   │   │   ├── delete-community.ts
│   │   │   ├── members.ts
│   │   │   ├── posts.ts
│   │   │   └── invitations.ts
│   │   │
│   │   ├── collections/
│   │   │   ├── create-collection.ts
│   │   │   ├── get-collection.ts
│   │   │   ├── update-collection.ts
│   │   │   ├── delete-collection.ts
│   │   │   ├── collection-posts.ts
│   │   │   ├── add-post.ts
│   │   │   ├── remove-post.ts
│   │   │   ├── reorder-post.ts
│   │   │   └── collection-likes.ts
│   │   │
│   │   ├── notifications/
│   │   │   ├── list-notifications.ts
│   │   │   ├── notification-count.ts
│   │   │   ├── following-notifications.ts
│   │   │   ├── mark-read.ts
│   │   │   └── mark-all-read.ts
│   │   │
│   │   ├── invitations/
│   │   │   ├── get-invite.ts
│   │   │   ├── create-invite.ts
│   │   │   ├── accept-invite.ts
│   │   │   ├── decline-invite.ts
│   │   │   └── delete-invite.ts
│   │   │
│   │   ├── media/
│   │   │   ├── videos.ts
│   │   │   ├── images.ts
│   │   │   └── media-posts.ts
│   │   │
│   │   ├── discovery/
│   │   │   ├── recommendations.ts
│   │   │   ├── genres.ts
│   │   │   ├── skills.ts
│   │   │   ├── labels.ts
│   │   │   └── badges.ts
│   │   │
│   │   ├── bulk/
│   │   │   ├── bulk-follow.ts
│   │   │   ├── bulk-unfollow.ts
│   │   │   ├── bulk-like.ts
│   │   │   ├── bulk-unlike.ts
│   │   │   ├── bulk-comment.ts
│   │   │   ├── bulk-message.ts
│   │   │   ├── bulk-invite.ts
│   │   │   ├── batch-executor.ts
│   │   │   ├── dry-run.ts
│   │   │   ├── progress.ts
│   │   │   └── results.ts
│   │   │
│   │   └── developer/
│   │       ├── capabilities.ts
│   │       ├── raw-request.ts
│   │       ├── validate.ts
│   │       ├── api-version.ts
│   │       └── endpoint-status.ts
│   │
│   ├── workflows/
│   │   │
│   │   ├── artist-research.ts
│   │   ├── artist-discovery.ts
│   │   ├── song-analysis.ts
│   │   ├── project-inspection.ts
│   │   ├── music-production.ts
│   │   ├── collaboration.ts
│   │   ├── social-management.ts
│   │   ├── collection-management.ts
│   │   ├── notification-summary.ts
│   │   ├── account-management.ts
│   │   └── bulk-campaign.ts
│   │
│   ├── permissions/
│   │   ├── permission-manager.ts
│   │   ├── capability-registry.ts
│   │   ├── confirmation-manager.ts
│   │   ├── privileged-actions.ts
│   │   ├── bulk-actions.ts
│   │   ├── destructive-actions.ts
│   │   └── policies.ts
│   │
│   ├── schemas/
│   │   ├── account.ts
│   │   ├── users.ts
│   │   ├── songs.ts
│   │   ├── revisions.ts
│   │   ├── production.ts
│   │   ├── social.ts
│   │   ├── collaboration.ts
│   │   ├── collections.ts
│   │   ├── notifications.ts
│   │   ├── invitations.ts
│   │   ├── bulk.ts
│   │   └── common.ts
│   │
│   ├── services/
│   │   ├── api-coverage.ts
│   │   ├── endpoint-registry.ts
│   │   ├── capability-discovery.ts
│   │   ├── response-normalizer.ts
│   │   ├── pagination.ts
│   │   ├── caching.ts
│   │   ├── logging.ts
│   │   ├── audit-log.ts
│   │   └── health-check.ts
│   │
│   ├── utils/
│   │   ├── ids.ts
│   │   ├── dates.ts
│   │   ├── validation.ts
│   │   ├── errors.ts
│   │   └── serialization.ts
│   │
│   └── registry/
│       ├── tool-registry.ts
│       ├── workflow-registry.ts
│       └── capability-registry.ts
│
├── scripts/
│   ├── discover-endpoints/
│   ├── compare-sdk-api/
│   ├── generate-api-map/
│   ├── validate-endpoints/
│   ├── inspect-responses/
│   └── upload-audio/
│
├── tests/
│   │
│   ├── unit/
│   │   ├── auth/
│   │   ├── client/
│   │   ├── permissions/
│   │   ├── schemas/
│   │   └── services/
│   │
│   ├── integration/
│   │   ├── account/
│   │   ├── users/
│   │   ├── songs/
│   │   ├── revisions/
│   │   ├── production/
│   │   ├── social/
│   │   ├── collaboration/
│   │   ├── collections/
│   │   ├── notifications/
│   │   └── media/
│   │
│   └── workflows/
│       ├── artist-research/
│       ├── song-analysis/
│       ├── production/
│       └── collaboration/
│
└── .github/
    └── workflows/
        ├── test.yml
        ├── lint.yml
        ├── build.yml
        └── release.yml
```

## 2. The architecture in one view

```text
                         BANDLAB
                            │
                            ▼
                ┌──────────────────────┐
                │  PRIVATE/UNOFFICIAL  │
                │       API            │
                └──────────┬───────────┘
                           │
             ┌─────────────┴─────────────┐
             │                           │
             ▼                           ▼
       TypeScript SDK              Python Research
       / API Client                / Discovery
             │                           │
             │                    ┌──────┴──────┐
             │                    │             │
             │               endpoint       schemas
             │               discovery      behavior
             │                    │             │
             │                    └──────┬──────┘
             │                           │
             ◄──────────── API MAP ──────┘
             │
             ▼
       BANDLAB API LAYER
             │
             ├── Account
             ├── Users
             ├── Search
             ├── Songs
             ├── Revisions
             ├── Production
             ├── Audio
             ├── Collaborators
             ├── Social
             ├── Followers
             ├── Messaging
             ├── Bands
             ├── Communities
             ├── Collections
             ├── Notifications
             ├── Invitations
             ├── Media
             ├── Discovery
             └── Developer/Raw
                     │
                     ▼
                MCP TOOLS
                     │
                     ▼
              MCP WORKFLOWS
                     │
                     ▼
          ┌─────────────────────┐
          │  PERMISSION LAYER   │
          ├─────────────────────┤
          │ Read                │
          │ Write               │
          │ Privileged          │
          │ Destructive         │
          │ Bulk                │
          └──────────┬──────────┘
                     │
                     ▼
             Claude / Cursor /
             Other MCP Client
```

## 3. Capability target — 17 major BandLab domains

```text
01. Account & Identity
02. Users & Artists
03. Search & Discovery
04. Songs
05. Projects & Revisions
06. Music Production / Mix / Effects
07. Audio / Samples / Uploads
08. Collaborators
09. Posts / Social
10. Followers / Following
11. Messaging
12. Bands
13. Communities
14. Collections
15. Notifications
16. Invitations
17. Media / Metadata / Developer APIs
```

## 4. Automation layer (sits across all domains)

```text
Individual Actions
        │
        ├── Read
        ├── Create
        ├── Update
        └── Delete
                │
                ▼
        Bulk Operations
                │
                ├── Follow
                ├── Unfollow
                ├── Like
                ├── Unlike
                ├── Comment
                ├── Message
                └── Invite
```

## 5. Key design decision

**Python is not part of the production MCP runtime.** It belongs in `research/` and `scripts/` for API discovery and
reverse-engineering. The **TypeScript SDK/API client is the production transport layer**; MCP tools/workflows sit above it.
This leaves room to discover additional private endpoints later without redesigning the MCP architecture.
