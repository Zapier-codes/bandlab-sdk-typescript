# Session Task Chunks — SDK full-coverage project

Scope: extend the existing SDK for full BandLab API coverage (`COVERAGE.md`). **No MCP, no restructure.** Rules: `HANDOVER.md` §2, layout/recipe: `ARCHITECTURE.md`.

## Status board  (update at the end of every session)

| ID | Title | Depends on | Status |
|----|-------|-----------|--------|
| S00 | Handover framework | — | DONE (superseded) |
| S00B | In-place revamp rules | S00 | DONE (superseded) |
| S00C | Rescope: SDK coverage only, extend existing tree, combined-patch rule | S00B | DONE |
| S01 | Baseline + coverage tooling | S00C | TODO |
| S02 | Research kit (capture guide + scrub/extract scripts) | S01 | TODO |
| S03 | Evidence triage (needs owner captures) | S02 + owner input | TODO — BLOCKED until owner supplies evidence |
| S04 | Implement: songs / revisions / production gaps (G02, G04, G05, G11) | S03 | TODO |
| S05 | Implement: audio / samples / uploads (G03) | S03 | TODO |
| S06 | Implement: messaging (G01) | S03 | TODO |
| S07 | Implement: social + media gaps (G06, G07, G08, G12) | S03 | TODO |
| S08 | Implement: account + any discovered extras (G09, G10, G13) | S03 | TODO |
| S09 | Consistency + types + docs pass | S04–S08 | TODO |
| S10 | Final coverage audit + README | S09 | TODO |

S04–S08 can run in any order once S03 has produced evidence for their items. An item with no evidence is **not implemented** — it stays in the register as `missing`.

## Implementation recipe (S04–S08; every new endpoint)
1. Pick the home in `ARCHITECTURE.md` "Where new things go". Never move/rename/split existing files.
2. Add the method with params/response types, JSDoc (include the path and the evidence status), matching neighbouring files.
3. Wire it: `src/client.ts` + `src/resources/index.ts` (new resources) or the parent resource/index (sub-resources).
4. Add the `api.md` line.
5. Add a test in `tests/api-resources/` using a **custom fetch mock** (new endpoints are not in the Prism spec): assert method, path, query, body, parsing.
6. Update `docs/endpoint-status.md` and `COVERAGE.md` (domain status + register row).
7. `yarn build && yarn lint && yarn test` must match or beat the S01 baseline.
8. Commit: one logical change per commit (`feat(<resource>): add <method>`, then `test(...)`, `docs(...)`).

---

## S01 — Baseline + coverage tooling
- `yarn install && yarn build && yarn lint && yarn test`; record results (and which tests need the Prism mock / network) in the audit file. If the mock cannot run in the sandbox, record which tests are skipped.
- Add `scripts/utils/coverage-report.cjs`: parses `api.md` into the inventory (verb, path, accessor), diffs against `docs/handover/endpoint-inventory.tsv`, and writes `docs/endpoint-status.md` (every endpoint = `spec`). Wire as `scripts/coverage`.
- Verify each domain row in `COVERAGE.md` against the code; correct anything wrong (e.g. whether `songs` has a list/create, whether `search` covers posts, what `emails.ts` exposes).
- Check the base-URL finding: `environments.production` = `https://test.bandlab.com/api/v1.3`, `environment_1` = `https://bandlab.com/api/v1.3`. **Report it; do not change defaults without the owner's decision.**
- **Accept:** baseline recorded; coverage script runs; `endpoint-status.md` exists; COVERAGE.md verified.

## S02 — Research kit
Because sessions cannot reach BandLab, build everything the owner needs to produce evidence and everything sessions need to consume it.
- `docs/research/CAPTURE-GUIDE.md`: step-by-step for capturing the owner's **own** traffic (browser HAR export from the BandLab web app; optionally a proxy on a phone). Say exactly which actions to perform for G01–G12 (send a message, upload an audio file, create a post, delete a revision, edit a comment, change email, open mix/effects, etc.).
- `scripts/research/scrub-har.py`: removes tokens, cookies, auth headers, emails, personal ids (replaces with placeholders). Python allowed here only.
- `scripts/research/har-to-endpoints.py`: extracts method, path template, query keys, request/response JSON shapes into `docs/research/endpoints/<domain>.json` (+ `unknown.json`), and flags endpoints not in the inventory.
- `scripts/research/README.md`; tests/fixtures with a tiny synthetic HAR.
- **Accept:** running the scripts on the synthetic HAR yields the expected JSON; guide is complete.

## S03 — Evidence triage  (BLOCKED until the owner supplies captures, a spec, or confirmations)
- Run the S02 tools on supplied evidence. For each G-item: status `captured` / `missing` / `blocked`; record the shapes.
- Decide the final resource design for S04–S08 (file names, methods, types) and write it into `COVERAGE.md`.
- Add any newly found endpoints as G13+ rows.
- If the owner supplies nothing, stop with `STATUS: PARTIAL` and BLOCKERS naming exactly what is needed. **Do not guess shapes.**

## S04 — Songs / revisions / production (G02, G04, G05, G11)
Create song, list songs, delete revision, add/update collaborator, mix/effects/tracks/project structure — whichever have evidence. Follow the recipe.

## S05 — Audio / samples / uploads (G03)
New `audio.ts` / `samples.ts` (names per S03). Use the existing `core/uploads` and `internal/uploads` for multipart/binary bodies; do not duplicate upload logic.

## S06 — Messaging (G01)
New `messaging.ts` (conversations, messages, send, history) per S03 design.

## S07 — Social + media gaps (G06, G07, G08, G12)
Generic create post, get/update comment, search posts, image/video get + upload.

## S08 — Account + extras (G09, G10, G13+)
Change email, delete account (flag destructive in JSDoc), plus anything discovered in S03.

## S09 — Consistency + types + docs pass
- Tighten types where captures gave real shapes; JSDoc statuses; consistent naming with neighbours; `api.md` complete; `CHANGELOG`-style notes in the audit file.
- Optionally fix the `revisonId` typo if touched.

## S10 — Final coverage audit + README
- Regenerate `endpoint-status.md`; every endpoint has a status; COVERAGE.md domain rows all Covered or explicitly `missing/blocked` with reasons.
- Update `README.md` with the new resources and a short usage example for each new domain.
