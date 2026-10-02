# HANDOVER — READ THIS FIRST

> Every session (human or AI) that clones this repo **must read this file before doing anything else**,
> then follow the pointer below. This file is the single source of truth for project state.

---

## 1. NEXT SESSION POINTER  (the previous session updates this block last)

```yaml
NEXT_SESSION: S01
NEXT_SESSION_TITLE: Scaffold the mcp/ package
NEXT_SESSION_BRIEF: docs/handover/TASKS.md  ->  section "S01"
LAST_COMPLETED: S00
LAST_COMPLETED_MARKER_COMMIT_SUBJECT: "handover: complete S00"
LAST_PATCH_NAME: s00-handover-framework.patch
STATUS: READY
BLOCKERS: none
```

**Sanity check at session start:**
```bash
git log --oneline | grep "handover: complete S00"   # must find the marker commit
```
If the marker for `LAST_COMPLETED` is **not** in `git log`, the previous patch was never applied/pushed.
**Stop and tell the owner** — do not continue on top of a missing session.

---

## 2. What this project is

Fork of the Stainless-generated TypeScript SDK for BandLab (`Zapier-codes/bandlab-sdk-typescript`).
Goal: build a **private BandLab MCP server** on top of it, per the target architecture saved in
[`docs/handover/ARCHITECTURE.md`](docs/handover/ARCHITECTURE.md).

Key design decisions (do not change without owner approval):

| # | Decision |
|---|----------|
| D1 | **The SDK in `src/` is generated code. Do NOT hand-edit it** (except `src/lib/`, which is Stainless' safe custom-code zone). The MCP is a *consumer* of the SDK. |
| D2 | The MCP lives in a new top-level folder **`mcp/`** (the plan's `bandlab-mcp/` root maps to `mcp/`). Plan path `src/x` → repo path `mcp/src/x`. |
| D3 | **Python is never part of the production runtime.** It lives only in `research/` and `scripts/` for endpoint discovery. |
| D4 | The SDK is the production transport. `mcp/src/bandlab/client/` wraps it; raw-request goes through the same wrapper for undocumented endpoints. |
| D5 | Every tool is classified **Read / Write / Privileged / Destructive / Bulk** and goes through the permission layer. No tool bypasses it. |
| D6 | Bulk tools are **dry-run by default**, rate-limited, and audit-logged. |

---

## 3. Documents map

| File | Purpose |
|------|---------|
| `HANDOVER.md` | This file. Pointer + rules + protocol summary. |
| `docs/handover/ARCHITECTURE.md` | Full target tree and architecture diagrams (verbatim from the plan). |
| `docs/handover/TASKS.md` | All work divided into session-sized chunks (S01…S18) with acceptance criteria. |
| `docs/handover/PROTOCOL.md` | Session start/finish checklist and the **git am patch process**. |
| `docs/handover/GAPS.md` | Planned capabilities NOT covered by the SDK (need research). |
| `docs/handover/sessions/` | One audit file per completed session (`session-S00.md`, …). |
| `scripts/handover/make-patch.sh` | Builds the downloadable `.patch` file. |

---

## 4. Session audit index  (append one line per session)

| Session | Title | Status | Patch | Audit |
|---------|-------|--------|-------|-------|
| S00 | Handover framework + planning | DONE | `s00-handover-framework.patch` | [session-S00.md](docs/handover/sessions/session-S00.md) |

---

## 5. Rules for every session (summary — full version in PROTOCOL.md)

1. Do **only** the session you are assigned in the pointer. Do not start the next one.
2. One logical change = one commit (`git add` + `git commit` per diff). Conventional-style subjects.
3. Never rewrite history that was already pushed. No force-push, no rebase of published commits.
4. Finish by: writing the audit file, updating the pointer (section 1) and the audit index (section 4),
   committing with the subject `handover: complete SNN`, and producing the patch with `scripts/handover/make-patch.sh`.
5. Hand the owner the `.patch` file and the three commands to apply it (see PROTOCOL.md §4).
6. If you cannot finish, set `STATUS: PARTIAL` in the pointer, say exactly what is left, and still produce a patch.
