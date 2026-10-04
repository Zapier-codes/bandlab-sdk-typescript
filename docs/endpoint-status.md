# Endpoint Status

One row per endpoint the SDK exposes, sorted by SDK accessor. Seeded by `./scripts/coverage --markdown` from `api.md`;
after that the **Status** column is edited by hand as evidence arrives. Do not regenerate over a hand-edited file.
To check that `api.md` still matches the inventory snapshot, run `./scripts/coverage`.

| Status | Meaning |
|--------|---------|
| `spec` | in the original OpenAPI spec; never run against BandLab from this repo |
| `captured` | seen in a real request capture supplied by the owner |
| `unverified` | inferred or added without evidence |
| `live-ok` | the owner ran it successfully against BandLab |
| `missing` | looked for, not found |

**123 endpoints: 123 `spec`.**

| Status | Verb | Path | SDK call | Source |
|--------|------|------|----------|--------|
| `spec` | POST | `/authorizations` | `client.authorizations.createSessionKey()` | `src/resources/authorizations.ts` |
| `spec` | GET | `/badges` | `client.badges.list()` | `src/resources/badges.ts` |
| `spec` | POST | `/bands` | `client.bands.create()` | `src/resources/bands/bands.ts` |
| `spec` | DELETE | `/bands/{bandId}` | `client.bands.delete()` | `src/resources/bands/bands.ts` |
| `spec` | GET | `/bands/{bandId}` | `client.bands.retrieve()` | `src/resources/bands/bands.ts` |
| `spec` | PATCH | `/bands/{bandId}` | `client.bands.update()` | `src/resources/bands/bands.ts` |
| `spec` | GET | `/bands/{bandId}/posts` | `client.bands.listPosts()` | `src/resources/bands/bands.ts` |
| `spec` | GET | `/bands/{bandId}/songs` | `client.bands.listSongs()` | `src/resources/bands/bands.ts` |
| `spec` | GET | `/bands/{bandId}/invites` | `client.bands.invites.list()` | `src/resources/bands/invites.ts` |
| `spec` | POST | `/bands/{bandId}/invites` | `client.bands.invites.send()` | `src/resources/bands/invites.ts` |
| `spec` | GET | `/bands/{bandId}/members` | `client.bands.members.list()` | `src/resources/bands/members.ts` |
| `spec` | DELETE | `/bands/{bandId}/members/{userId}` | `client.bands.members.remove()` | `src/resources/bands/members.ts` |
| `spec` | GET | `/bands/{bandId}/members/{userId}` | `client.bands.members.retrieve()` | `src/resources/bands/members.ts` |
| `spec` | PATCH | `/bands/{bandId}/members/{userId}` | `client.bands.members.update()` | `src/resources/bands/members.ts` |
| `spec` | POST | `/collections` | `client.collections.create()` | `src/resources/collections/collections.ts` |
| `spec` | DELETE | `/collections/{collectionId}` | `client.collections.delete()` | `src/resources/collections/collections.ts` |
| `spec` | GET | `/collections/{collectionId}` | `client.collections.retrieve()` | `src/resources/collections/collections.ts` |
| `spec` | PATCH | `/collections/{collectionId}` | `client.collections.update()` | `src/resources/collections/collections.ts` |
| `spec` | DELETE | `/collections/{collectionId}/likes` | `client.collections.likes.remove()` | `src/resources/collections/likes.ts` |
| `spec` | GET | `/collections/{collectionId}/likes` | `client.collections.likes.list()` | `src/resources/collections/likes.ts` |
| `spec` | POST | `/collections/{collectionId}/likes` | `client.collections.likes.add()` | `src/resources/collections/likes.ts` |
| `spec` | DELETE | `/collections/{collectionId}/posts/{postId}` | `client.collections.posts.remove()` | `src/resources/collections/posts.ts` |
| `spec` | GET | `/collections/{collectionId}/posts/{postId}` | `client.collections.posts.retrieve()` | `src/resources/collections/posts.ts` |
| `spec` | PATCH | `/collections/{collectionId}/posts/{postId}` | `client.collections.posts.updatePosition()` | `src/resources/collections/posts.ts` |
| `spec` | POST | `/collections/{collectionId}/posts/{postId}` | `client.collections.posts.add()` | `src/resources/collections/posts.ts` |
| `spec` | POST | `/communities` | `client.communities.create()` | `src/resources/communities/communities.ts` |
| `spec` | DELETE | `/communities/{communityId}` | `client.communities.delete()` | `src/resources/communities/communities.ts` |
| `spec` | GET | `/communities/{communityId}` | `client.communities.retrieve()` | `src/resources/communities/communities.ts` |
| `spec` | PATCH | `/communities/{communityId}` | `client.communities.update()` | `src/resources/communities/communities.ts` |
| `spec` | GET | `/community/{communityId}/invites` | `client.communities.invites.list()` | `src/resources/communities/invites.ts` |
| `spec` | POST | `/community/{communityId}/invites` | `client.communities.invites.send()` | `src/resources/communities/invites.ts` |
| `spec` | GET | `/communities/{communityId}/members` | `client.communities.members.list()` | `src/resources/communities/members.ts` |
| `spec` | DELETE | `/communities/{communityId}/members/{userId}` | `client.communities.members.delete()` | `src/resources/communities/members.ts` |
| `spec` | GET | `/communities/{communityId}/members/{userId}` | `client.communities.members.retrieve()` | `src/resources/communities/members.ts` |
| `spec` | PATCH | `/communities/{communityId}/members/{userId}` | `client.communities.members.update()` | `src/resources/communities/members.ts` |
| `spec` | GET | `/community/{communityId}/posts` | `client.communities.posts.list()` | `src/resources/communities/posts.ts` |
| `spec` | POST | `/community/{communityId}/posts` | `client.communities.posts.create()` | `src/resources/communities/posts.ts` |
| `spec` | POST | `/emails/confirmations` | `client.emails.confirmations.resend()` | `src/resources/emails/confirmations.ts` |
| `spec` | PUT | `/emails/confirmations` | `client.emails.confirmations.confirm()` | `src/resources/emails/confirmations.ts` |
| `spec` | POST | `/feedback` | `client.feedback.create()` | `src/resources/feedback.ts` |
| `spec` | GET | `/genres` | `client.genres.list()` | `src/resources/genres.ts` |
| `spec` | POST | `/images/{imageId}/posts` | `client.images.createPost()` | `src/resources/images.ts` |
| `spec` | POST | `/invites` | `client.invites.send()` | `src/resources/invites.ts` |
| `spec` | DELETE | `/invites/{inviteId}` | `client.invites.delete()` | `src/resources/invites.ts` |
| `spec` | GET | `/invites/{inviteId}` | `client.invites.retrieve()` | `src/resources/invites.ts` |
| `spec` | PUT | `/invites/{inviteId}` | `client.invites.accept()` | `src/resources/invites.ts` |
| `spec` | GET | `/labels` | `client.labels.list()` | `src/resources/labels.ts` |
| `spec` | GET | `/logins` | `client.logins.list()` | `src/resources/logins.ts` |
| `spec` | POST | `/logins` | `client.logins.create()` | `src/resources/logins.ts` |
| `spec` | DELETE | `/logins/{providerType}` | `client.logins.delete()` | `src/resources/logins.ts` |
| `spec` | PUT | `/logins/{providerType}` | `client.logins.update()` | `src/resources/logins.ts` |
| `spec` | GET | `/me` | `client.me.retrieve()` | `src/resources/me.ts` |
| `spec` | PATCH | `/me` | `client.me.update()` | `src/resources/me.ts` |
| `spec` | DELETE | `/passwords` | `client.passwords.sendRestoreEmail()` | `src/resources/passwords.ts` |
| `spec` | POST | `/passwords` | `client.passwords.reset()` | `src/resources/passwords.ts` |
| `spec` | PUT | `/passwords` | `client.passwords.change()` | `src/resources/passwords.ts` |
| `spec` | GET | `/posts` | `client.posts.list()` | `src/resources/posts/posts.ts` |
| `spec` | DELETE | `/posts/{postId}` | `client.posts.delete()` | `src/resources/posts/posts.ts` |
| `spec` | GET | `/posts/{postId}` | `client.posts.retrieve()` | `src/resources/posts/posts.ts` |
| `spec` | PATCH | `/posts/{postId}` | `client.posts.update()` | `src/resources/posts/posts.ts` |
| `spec` | GET | `/posts/{postId}/comments` | `client.posts.comments.list()` | `src/resources/posts/comments.ts` |
| `spec` | POST | `/posts/{postId}/comments` | `client.posts.comments.create()` | `src/resources/posts/comments.ts` |
| `spec` | DELETE | `/posts/{postId}/comments/{commentId}` | `client.posts.comments.delete()` | `src/resources/posts/comments.ts` |
| `spec` | DELETE | `/posts/{postId}/likes` | `client.posts.likes.delete()` | `src/resources/posts/likes.ts` |
| `spec` | GET | `/posts/{postId}/likes` | `client.posts.likes.list()` | `src/resources/posts/likes.ts` |
| `spec` | POST | `/posts/{postId}/likes` | `client.posts.likes.create()` | `src/resources/posts/likes.ts` |
| `spec` | DELETE | `/push/registrations` | `client.push.registrations.delete()` | `src/resources/push/registrations.ts` |
| `spec` | POST | `/push/registrations` | `client.push.registrations.create()` | `src/resources/push/registrations.ts` |
| `spec` | POST | `/reports` | `client.reports.create()` | `src/resources/reports.ts` |
| `spec` | POST | `/revisions` | `client.revisions.create()` | `src/resources/revisions.ts` |
| `spec` | GET | `/revisions/{revisionId}` | `client.revisions.retrieve()` | `src/resources/revisions.ts` |
| `spec` | PATCH | `/revisions/{revisionId}` | `client.revisions.update()` | `src/resources/revisions.ts` |
| `spec` | POST | `/revisions/{revisionId}/plays` | `client.revisions.addPlay()` | `src/resources/revisions.ts` |
| `spec` | GET | `/search` | `client.search.globalSearch()` | `src/resources/search.ts` |
| `spec` | GET | `/search/bands` | `client.search.searchBands()` | `src/resources/search.ts` |
| `spec` | GET | `/search/collections` | `client.search.searchCollections()` | `src/resources/search.ts` |
| `spec` | GET | `/search/songs` | `client.search.searchSongs()` | `src/resources/search.ts` |
| `spec` | GET | `/search/users` | `client.search.searchUsers()` | `src/resources/search.ts` |
| `spec` | GET | `/settings/notifications/email` | `client.settings.notifications.email.retrieve()` | `src/resources/settings/notifications/email.ts` |
| `spec` | PATCH | `/settings/notifications/email` | `client.settings.notifications.email.update()` | `src/resources/settings/notifications/email.ts` |
| `spec` | GET | `/settings/notifications/push` | `client.settings.notifications.push.retrieve()` | `src/resources/settings/notifications/push.ts` |
| `spec` | PATCH | `/settings/notifications/push` | `client.settings.notifications.push.update()` | `src/resources/settings/notifications/push.ts` |
| `spec` | GET | `/skills` | `client.skills.list()` | `src/resources/skills.ts` |
| `spec` | GET | `/song/{songId}/posts` | `client.songs.listPosts()` | `src/resources/songs/songs.ts` |
| `spec` | DELETE | `/songs/{songId}` | `client.songs.delete()` | `src/resources/songs/songs.ts` |
| `spec` | GET | `/songs/{songId}` | `client.songs.retrieve()` | `src/resources/songs/songs.ts` |
| `spec` | PATCH | `/songs/{songId}` | `client.songs.update()` | `src/resources/songs/songs.ts` |
| `spec` | GET | `/songs/{songId}/collaborators` | `client.songs.collaborators.list()` | `src/resources/songs/collaborators.ts` |
| `spec` | DELETE | `/songs/{songId}/collaborators/{userId}` | `client.songs.collaborators.remove()` | `src/resources/songs/collaborators.ts` |
| `spec` | GET | `/song/{songId}/invites` | `client.songs.invites.listInvites()` | `src/resources/songs/invites.ts` |
| `spec` | POST | `/song/{songId}/invites` | `client.songs.invites.sendInvites()` | `src/resources/songs/invites.ts` |
| `spec` | GET | `/songs/{songId}/revisions` | `client.songs.revisions.list()` | `src/resources/songs/revisions.ts` |
| `spec` | POST | `/songs/{songId}/revisions/{revisonId}/forks` | `client.songs.revisions.forks()` | `src/resources/songs/revisions.ts` |
| `spec` | GET | `/users/{userId}` | `client.users.retrieve()` | `src/resources/users/users.ts` |
| `spec` | GET | `/users/{userId}/bands` | `client.users.listBands()` | `src/resources/users/users.ts` |
| `spec` | GET | `/users/{userId}/collections` | `client.users.listCollections()` | `src/resources/users/users.ts` |
| `spec` | GET | `/users/{userId}/communities` | `client.users.listCommunities()` | `src/resources/users/users.ts` |
| `spec` | POST | `/users/{userId}/keys` | `client.users.createAccessKey()` | `src/resources/users/users.ts` |
| `spec` | GET | `/users/{userId}/posts` | `client.users.listPosts()` | `src/resources/users/users.ts` |
| `spec` | GET | `/users/{userId}/songs` | `client.users.listSongs()` | `src/resources/users/users.ts` |
| `spec` | GET | `/users/{userId}/blocks/users` | `client.users.blocks.users.list()` | `src/resources/users/blocks/users.ts` |
| `spec` | DELETE | `/users/{userId}/blocks/users/{blockedUserId}` | `client.users.blocks.users.remove()` | `src/resources/users/blocks/users.ts` |
| `spec` | POST | `/users/{userId}/blocks/users/{blockedUserId}` | `client.users.blocks.users.add()` | `src/resources/users/blocks/users.ts` |
| `spec` | GET | `/users/{userId}/contacts/bands` | `client.users.contacts.listBands()` | `src/resources/users/contacts.ts` |
| `spec` | GET | `/users/{userId}/contacts/users` | `client.users.contacts.listUsers()` | `src/resources/users/contacts.ts` |
| `spec` | DELETE | `/users/{userId}/followers` | `client.users.followers.remove()` | `src/resources/users/followers.ts` |
| `spec` | GET | `/users/{userId}/followers` | `client.users.followers.list()` | `src/resources/users/followers.ts` |
| `spec` | POST | `/users/{userId}/followers` | `client.users.followers.add()` | `src/resources/users/followers.ts` |
| `spec` | GET | `/users/{userId}/following` | `client.users.following.list()` | `src/resources/users/following.ts` |
| `spec` | GET | `/users/{userId}/following/posts` | `client.users.following.listPosts()` | `src/resources/users/following.ts` |
| `spec` | GET | `/users/{userId}/invites` | `client.users.invites.list()` | `src/resources/users/invites.ts` |
| `spec` | POST | `/users/{userId}/invites` | `client.users.invites.send()` | `src/resources/users/invites.ts` |
| `spec` | GET | `/users/{userId}/notifications` | `client.users.notifications.list()` | `src/resources/users/notifications.ts` |
| `spec` | PATCH | `/users/{userId}/notifications` | `client.users.notifications.updateAll()` | `src/resources/users/notifications.ts` |
| `spec` | GET | `/users/{userId}/notifications/count` | `client.users.notifications.count()` | `src/resources/users/notifications.ts` |
| `spec` | GET | `/users/{userId}/notifications/following` | `client.users.notifications.listFollowing()` | `src/resources/users/notifications.ts` |
| `spec` | PATCH | `/users/{userId}/notifications/{notificationId}` | `client.users.notifications.update()` | `src/resources/users/notifications.ts` |
| `spec` | GET | `/users/{userId}/recommendations/users` | `client.users.recommendations.listUsers()` | `src/resources/users/recommendations.ts` |
| `spec` | GET | `/validation/{entityType}` | `client.validation.validate()` | `src/resources/validation.ts` |
| `spec` | GET | `/versions/{clientId}` | `client.versions.retrieve()` | `src/resources/versions.ts` |
| `spec` | GET | `/versions/{clientId}/{version}/valid` | `client.versions.validate()` | `src/resources/versions.ts` |
| `spec` | POST | `/videos/{videoId}/posts` | `client.videos.createPost()` | `src/resources/videos.ts` |
| `spec` | POST | `/videos/{videoId}/views` | `client.videos.addView()` | `src/resources/videos.ts` |
