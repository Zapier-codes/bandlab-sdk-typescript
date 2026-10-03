# Architecture — Extend the existing SDK for full API coverage

## Goal
Update the existing BandLab TypeScript SDK so it covers **every BandLab API capability**, including the ones it is missing today.
It is **not** an MCP server, and nothing MCP-related is built. It is **not** a restructure.

## Principles (owner rules)
1. **Keep the existing tree.** No relocating, renaming or splitting existing files. No new top-level directories.
2. **Extend in place.** Existing resources get new methods where an endpoint is missing from that resource; missing domains become new resource files next to the existing ones.
3. **Additive only.** Every existing `client.*` call keeps working unchanged.
4. **Follow the existing conventions** exactly (below). New code should look like the code beside it.
5. **No invented endpoints.** Every new endpoint is backed by evidence (a captured request, an OpenAPI spec, or the owner's confirmation) and carries a status.

## The existing tree (kept as is)

```text
repo root
├── src/
│   ├── index.ts            public barrel
│   ├── client.ts           class BandlabSDK: options, auth header, retries, timeout, logging, resource wiring,
│   │                       and generic client.get/post/patch/put/delete(path, opts) for any endpoint
│   ├── core/               runtime: api-promise, error, resource, uploads
│   ├── internal/           runtime: headers, parse, request-options, shims, to-file, uploads, utils/*
│   ├── lib/                empty; allowed home for hand-written helpers
│   └── resources/          one file (or folder with index.ts) per API resource  ← main extension point
│       ├── index.ts        re-exports every resource
│       ├── shared.ts       shared types
│       └── …               me, users/*, songs/*, revisions, posts/*, bands/*, communities/*, collections/*, invites,
│                           search, images, videos, settings/*, push/*, emails/*, logins, passwords, authorizations,
│                           genres, skills, labels, badges, validation, versions, reports, feedback
├── tests/
│   ├── api-resources/      one test file per resource, written for a Prism mock; all 185 tests are currently `test.skip`
│   └── *.test.ts           runtime tests (custom fetch mock pattern lives in tests/index.test.ts)
├── api.md                  method list; hand-maintained from now on
├── scripts/                build, lint, format, test, mock, utils/
└── docs/handover/          handover system (ours)
```

## Where new things go

| Need | Location | Notes |
|------|----------|-------|
| New endpoint on an existing resource | the resource's existing file | add method + params/response types in the same file, as the neighbours do |
| New resource that is a sub-resource of an existing **folder** resource (e.g. under `songs/`, `users/`, `posts/`) | new file in that folder + register in that folder's `index.ts` and parent class | mirror `songs/collaborators.ts` |
| New top-level resource (messaging, audio, samples, effects…) | new file `src/resources/<name>.ts` | do **not** convert existing flat files into folders |
| Wiring | `src/client.ts` (property + static + type exports) and `src/resources/index.ts` | mirror how `Collections` is wired |
| Types | in the resource file; shared ones in `src/resources/shared.ts` | |
| Docs of the method | `api.md` entry | keep the same line format |
| Tests | `tests/api-resources/<name>.test.ts` | **see testing note** |
| Hand-written helpers (pagination, upload convenience, only if needed) | `src/lib/` | keep minimal |
| Research tooling (Python allowed) | `scripts/research/` | never shipped, never imported by `src/` |
| Research findings | `docs/research/` | scrubbed of secrets |

Not touched: Stainless/release scaffolding (`release-please-config.json`, `bin/`, `.github/workflows/*`, `scripts/utils/*`). Left as is.

### Testing note
The 46 resource test files are written for a Prism mock server built from the OpenAPI spec (`http://127.0.0.1:4010`), but **every one of their 185 tests is declared `test.skip` ("Prism tests are disabled"), so today they assert nothing.** The 7 runtime suites in `tests/*.test.ts` need neither a mock nor the network (verified in a network-less namespace). Details: `sessions/1.a.i.zo.md`.
**New endpoints are not in the spec, so Prism could not serve them even if the tests were enabled.**
New-endpoint tests must use a **custom `fetch` mock** (pattern in `tests/index.test.ts`) and assert method, path, query, body and response parsing.
Keep them in `tests/api-resources/`, named like the resource.

### Known constraints
- **The sandbox sessions cannot reach `bandlab.com`** (not on the network allow-list). Sessions cannot discover or live-verify endpoints themselves.
  Evidence must come from the owner: HAR/curl captures from their own account, an OpenAPI spec, or confirmation. Sessions produce the tools to capture and the code to consume it.
- **Stainless regeneration would overwrite hand-edits** in `src/`. Do not merge codegen PRs or regenerate. (Scaffolding is untouched; this is a standing risk the owner owns.)
- The spec has a typo: path param `revisonId` in `POST /songs/{songId}/revisions/{revisonId}/forks`. Parameters are positional in TS, so it is harmless; leave it unless touched for another reason.

## Coverage targets
The 17 BandLab domains from the original plan are the coverage checklist. Status per domain and the register of missing capabilities live in `COVERAGE.md`.
