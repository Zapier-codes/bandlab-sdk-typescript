# HANDOVER — READ THIS FIRST

> Every session (human or AI) that clones this repo **must read this file before doing anything else**,
> then follow the pointer below. This file is the single source of truth for project state.
> **The owner's rules override everything in this repo.** If the owner states a new rule, update §2 in the same session.

---

## 1. NEXT SESSION POINTER  (the previous session updates this block last)

```yaml
NEXT_SESSION: S01
NEXT_SESSION_TITLE: Baseline + coverage tooling
NEXT_SESSION_BRIEF: docs/handover/TASKS.md  ->  section "S01"
LAST_COMPLETED: S00C
LAST_COMPLETED_MARKER_COMMIT_SUBJECT: "handover: complete S00C"
LAST_PATCH_NAME: s00c-sdk-coverage-handover.patch
STATUS: READY
BLOCKERS: none for S01. S03 is blocked until the owner supplies evidence (captures / spec / confirmation) for the missing endpoints.
```

**Sanity check at session start:**
```bash
git log --oneline | grep "handover: complete S00C"   # must find the marker commit
```
If the marker for `LAST_COMPLETED` is **not** in `git log`, the previous patch was never applied/pushed.
**Stop and tell the owner** — do not continue on top of a missing session.

---

## 2. What this project is, and the rules

**Update the existing BandLab TypeScript SDK so it covers every BandLab API capability**, including those it is missing today
(messaging, audio/samples, mix/effects, and a handful of missing operations — see `docs/handover/COVERAGE.md`).
This is **not** an MCP server and **not** a restructure.

| # | Rule |
|---|------|
| D1 | **This is the owner's own project. Everything is editable, including `src/`.** |
| D2 | **Keep the existing tree. Extend it.** No relocating, renaming or splitting existing files; no new top-level directories. New code goes beside its neighbours (`ARCHITECTURE.md` "Where new things go"). |
| D3 | **Scope is SDK API coverage only.** Do not build an MCP server, tools, workflows, permission layers, bulk automation or any registry. Those were in the first plan and are cancelled. |
| D4 | **Additive only.** Every existing `client.*` call keeps working unchanged. |
| D5 | Python is allowed only in `scripts/research/` for evidence tooling. It is never shipped and never imported by `src/`. |
| D6 | **Never invent an endpoint or response shape.** Every new endpoint needs evidence (capture, spec, or owner confirmation) and a status (`spec` / `captured` / `unverified` / `live-ok` / `missing`). |
| D7 | **Sessions cannot reach `bandlab.com`** from the sandbox. Evidence comes from the owner. Never claim an endpoint is live-verified. |
| D8 | Stainless/release scaffolding is left untouched. Do not run or merge codegen (it would overwrite hand edits). |
| D9 | Wire paths stay exactly as the server expects; follow existing naming conventions in neighbouring files. |
| D10 | **Combined patch rule:** the patch is always built from `origin/main`, so it contains every commit not yet pushed. The owner applies one patch. |

---

## 3. Documents map

| File | Purpose |
|------|---------|
| `HANDOVER.md` | This file. Pointer + rules. |
| `docs/handover/ARCHITECTURE.md` | Existing tree (kept), where new code goes, the per-endpoint recipe, constraints. |
| `docs/handover/COVERAGE.md` | 17-domain coverage matrix + register of missing capabilities (G01…). |
| `docs/handover/endpoint-inventory.tsv` | Snapshot of the 123 existing endpoints (verb, path, accessor). |
| `docs/handover/TASKS.md` | Session chunks S01–S10, status board, implementation recipe. |
| `docs/handover/PROTOCOL.md` | Session start/finish checklist, combined-patch rule, git am commands. |
| `docs/handover/ORIGINAL-PLAN-TREE.md` | Original MCP plan, kept as a domain checklist only. Layout is cancelled. |
| `docs/handover/sessions/` | One audit file per completed session. |
| `scripts/handover/make-patch.sh` | Builds the combined `.patch`. |

---

## 4. Session audit index  (append one line per session)

| Session | Title | Status | Audit |
|---------|-------|--------|-------|
| S00 | Handover framework | DONE (superseded by S00C) | [session-S00.md](docs/handover/sessions/session-S00.md) |
| S00B | In-place revamp rules | DONE (superseded by S00C) | [session-S00B.md](docs/handover/sessions/session-S00B.md) |
| S00C | Rescope: SDK coverage only, extend existing tree | DONE | [session-S00C.md](docs/handover/sessions/session-S00C.md) |

Latest combined patch: `s00c-sdk-coverage-handover.patch` (contains S00, S00B, S00C).

---

## 5. Rules for every session (summary — full version in PROTOCOL.md)

1. Do **only** the session named in the pointer.
2. One logical change = one commit.
3. Never rewrite pushed history; no force-push.
4. Finish by: audit file, pointer (§1), audit index (§4), TASKS status board, COVERAGE.md if changed, commit `handover: complete SNN`, then `scripts/handover/make-patch.sh`.
5. Give the owner the single combined `.patch` and the three apply commands.
6. If you cannot finish, set `STATUS: PARTIAL`, say what is left, and still produce a patch.
