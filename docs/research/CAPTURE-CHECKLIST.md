# Capture Checklist

One row per capture the guide asks for (`CAPTURE-GUIDE.md`, section 4). **42 rows**: P0 plus 41 captures for G01 to G14.
The file names are fixed so the extractor and the triage session can find things. Format and routes: `HAND-BACK.md`.

**How this is used.** While capturing, keep a private copy of this table (a notes app is fine) and tick as you go. When you hand files back, tell the session which rows are done and the result for each. **Sessions update this repo copy** (the *In repo* and *Result* columns); you never have to edit it.

**Result values** (also used by the triage leaf `2.b.i.zi`):
`captured` the file is usable ·
`no-such-action` the app has no such action (a valid, useful result) ·
`not-capturable` tried, but the traffic could not be read (for example phone-app traffic) ·
`skipped` not done, with the reason in *Note*.

**Account column of your private copy:** write `own`, `second` or `throwaway` so a later reader knows whose data the capture holds.

| Row | Capture | File name | Done | In repo | Result | Note |
|-----|---------|-----------|------|---------|--------|------|
| P0 | Note which API host the BandLab site calls, and whether test.bandlab.com appears at all | `P0-base-host.txt` | [ ] | [ ] | | |
| G01.01 | Load the conversation list | `G01-01-list-conversations.har` | [ ] | [ ] | | |
| G01.02 | Open an existing conversation | `G01-02-open-conversation.har` | [ ] | [ ] | | |
| G01.03 | Send one message to your second account | `G01-03-send-message.har` | [ ] | [ ] | | |
| G01.04 | Scroll up to load older messages | `G01-04-load-older.har` | [ ] | [ ] | | |
| G01.05 | Mark as read, if the app has that action | `G01-05-mark-read.har` | [ ] | [ ] | | |
| G02.01 | Open one of your own projects in the web Studio | `G02-01-open-project.har` | [ ] | [ ] | | |
| G02.02 | Change one track's volume or pan | `G02-02-change-volume-pan.har` | [ ] | [ ] | | |
| G02.03 | Add or change one effect | `G02-03-change-effect.har` | [ ] | [ ] | | |
| G02.04 | Let it save, or save manually | `G02-04-save.har` | [ ] | [ ] | | |
| G03.01 | Upload a very short audio file you own, from choosing the file until it shows as processed | `G03-01-upload-audio.har` | [ ] | [ ] | | |
| G03.02 | Open one sample, if a sample library is browsable | `G03-02-open-sample.har` | [ ] | [ ] | | |
| G04.01 | Create a brand-new empty song or project; capture the first save | `G04-01-create-song.har` | [ ] | [ ] | | |
| G04.02 | Open your list of songs | `G04-02-list-my-songs.har` | [ ] | [ ] | | |
| G05.01 | In a throwaway song with two or more revisions, delete one revision | `G05-01-delete-revision.har` | [ ] | [ ] | | |
| G06.01 | Create a plain post (text or a track post) | `G06-01-create-post.har` | [ ] | [ ] | | |
| G07.01 | Write a comment on your own post | `G07-01-write-comment.har` | [ ] | [ ] | | |
| G07.02 | Edit that comment, if the app allows | `G07-02-edit-comment.har` | [ ] | [ ] | | |
| G07.03 | Open the comment on its own, if the app has such a view | `G07-03-open-single-comment.har` | [ ] | [ ] | | |
| G08.01 | Search for a word that appears in posts; switch between result tabs | `G08-01-search-posts.har` | [ ] | [ ] | | |
| G09.01 | Throwaway account or a second address: start and finish the change-email flow | `G09-01-change-email.har` | [ ] | [ ] | | |
| G09.02 | Confirm the new address through the email link | `G09-02-confirm-email.har` | [ ] | [ ] | | |
| G10.01 | THROWAWAY ACCOUNT ONLY: walk through account deletion to the final confirm | `G10-01-delete-account.har` | [ ] | [ ] | | |
| G11.01 | Invite your second account as a collaborator on a throwaway song | `G11-01-invite.har` | [ ] | [ ] | | |
| G11.02 | Accept the invite on the second account | `G11-02-accept-invite.har` | [ ] | [ ] | | |
| G11.03 | Change its role or permission, if the app allows | `G11-03-change-role.har` | [ ] | [ ] | | |
| G11.04 | Remove the collaborator | `G11-04-remove-collaborator.har` | [ ] | [ ] | | |
| G12.01 | Upload one small image as a post | `G12-01-upload-image.har` | [ ] | [ ] | | |
| G12.02 | Upload one very short video as a post | `G12-02-upload-video.har` | [ ] | [ ] | | |
| G12.03 | Open an image or video post on its own page | `G12-03-open-media.har` | [ ] | [ ] | | |
| G13.01 | Read-only tour: feed / explore | `G13-01-feed-explore.har` | [ ] | [ ] | | |
| G13.02 | Read-only tour: library | `G13-02-library.har` | [ ] | [ ] | | |
| G13.03 | Read-only tour: notifications | `G13-03-notifications.har` | [ ] | [ ] | | |
| G13.04 | Read-only tour: collections | `G13-04-collections.har` | [ ] | [ ] | | |
| G13.05 | Read-only tour: bands | `G13-05-bands.har` | [ ] | [ ] | | |
| G13.06 | Read-only tour: communities | `G13-06-communities.har` | [ ] | [ ] | | |
| G13.07 | Read-only tour: releases / distribution, if the app has it | `G13-07-releases-distribution.har` | [ ] | [ ] | | |
| G13.08 | Read-only tour: contests / challenges, if the app has them | `G13-08-contests-challenges.har` | [ ] | [ ] | | |
| G13.09 | Read-only tour: playlists / albums, if the app has them | `G13-09-playlists-albums.har` | [ ] | [ ] | | |
| G13.10 | Read-only tour: stats | `G13-10-stats.har` | [ ] | [ ] | | |
| G14.01 | Share or repost a track post (inside BandLab, not sharing out to another app) | `G14-01-share-repost.har` | [ ] | [ ] | | |
| G14.02 | (optional) Undo it afterwards | `G14-02-undo-repost.har` | [ ] | [ ] | | |
