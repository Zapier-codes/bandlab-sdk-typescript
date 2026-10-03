# HANDOVER — READ THIS FIRST

> Every session (human or AI) that clones this repo **must read this file before doing anything else**,
> then follow the pointer below. This file is the single source of truth for project state.
> **The owner's rules override everything in this repo.** If the owner states a new rule, update §2 in the same session.

---

## 1. NEXT SESSION POINTER  (the previous session updates this block last)

```yaml
NEXT_SESSION: S01
NEXT_SESSION_TITLE: Detach from Stainless, package identity, tooling baseline, plan skeleton
NEXT_SESSION_BRIEF: docs/handover/TASKS.md  ->  section "S01"
LAST_COMPLETED: S00B
LAST_COMPLETED_MARKER_COMMIT_SUBJECT: "handover: complete S00B"
LAST_PATCH_NAME: s00b-in-place-revamp-rules.patch
STATUS: READY
BLOCKERS: none
```

**Sanity check at session start:**
```bash
git log --oneline | grep "handover: complete S00B"   # must find the marker commit
```
If the marker for `LAST_COMPLETED` is **not** in `git log`, the previous patch was never applied/pushed.
**Stop and tell the owner** — do not continue on top of a missing session.

---

## 2. What this project is, and the rules

This repo (`Zapier-codes/bandlab-sdk-typescript`, the owner's fork) is being **revamped in place** into a private BandLab MCP server,
following the target architecture in [`docs/handover/ARCHITECTURE.md`](docs/handover/ARCHITECTURE.md).
The architecture tree **is the repo root**. We move what already works into the plan's paths, extend what is partial, and add what is missing.

| # | Rule |
|---|------|
| D1 | **This is the owner's own project. Everything is editable, including `src/`.** The old "generated SDK is read-only" rule is void. |
| D2 | **No `mcp/` folder.** Work happens in the existing `src/` and repo root. |
| D3 | Revamp, don't rewrite: relocate working code with `git mv` into plan paths. **Moves and edits are separate commits.** Keep the build green. |
| D4 | **Python is never part of the production runtime.** It lives only in `research/` and `scripts/`. |
| D5 | Every tool is classified **Read / Write / Privileged / Destructive / Bulk** and all dispatch goes through the permission layer. |
| D6 | Bulk tools are **dry-run by default**, capped, rate-limited and audit-logged. |
| D7 | **Stainless is detached** (no regeneration). Remove its scaffolding in S01, but **only after the OpenAPI spec is snapshotted** into `research/` (the Prism mock reads its URL from `.stats.yml`). |
| D8 | `src/index.ts` stays the **library barrel** (existing public surface). The MCP stdio entry is `src/server.ts`, exposed via `package.json` `bin`. *(Deviation from the plan tree; owner may overrule.)* |
| D9 | Wire paths to BandLab stay exactly as the server expects. Internal names may be normalised freely. |
| D10 | Never invent endpoints. Unproven ones are flagged `unverified` and fail with a typed `NotImplementedError`. |

---

## 3. Documents map

| File | Purpose |
|------|---------|
| `HANDOVER.md` | This file. Pointer + rules + protocol summary. |
| `docs/handover/ARCHITECTURE.md` | Full target tree and diagrams (the repo root layout). |
| `docs/handover/EXISTING-VS-PLAN.md` | **What exists, what moves where, what is new.** |
| `docs/handover/TASKS.md` | All work divided into session-sized chunks (S01…S18) with acceptance criteria. |
| `docs/handover/PROTOCOL.md` | Session start/finish checklist and the **git am patch process**. |
| `docs/handover/GAPS.md` | Planned capabilities not covered by existing code (need research). |
| `docs/handover/sessions/` | One audit file per completed session. |
| `scripts/handover/make-patch.sh` | Builds the downloadable `.patch` file. |

---

## 4. Session audit index  (append one line per session)

| Session | Title | Status | Patch | Audit |
|---------|-------|--------|-------|-------|
| S00 | Handover framework + planning | DONE (rules superseded by S00B) | `s00-handover-framework.patch` | [session-S00.md](docs/handover/sessions/session-S00.md) |
| S00B | Rules correction: in-place revamp | DONE | `s00b-in-place-revamp-rules.patch` | [session-S00B.md](docs/handover/sessions/session-S00B.md) |

---

## 5. Rules for every session (summary — full version in PROTOCOL.md)

1. Do **only** the session named in the pointer. Do not start the next one.
2. One logical change = one commit (`git add` + `git commit` per diff). Moves and edits in separate commits.
3. Never rewrite history that was already pushed. No force-push.
4. Finish by: writing the audit file, updating the pointer (§1), the audit index (§4) and the TASKS status board,
   committing with the subject `handover: complete SNN`, and producing the patch with `scripts/handover/make-patch.sh`.
5. Hand the owner the `.patch` file and the three commands to apply it (PROTOCOL.md §4).
6. If you cannot finish, set `STATUS: PARTIAL`, say exactly what is left, and still produce a patch.
