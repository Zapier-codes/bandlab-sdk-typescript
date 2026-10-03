#!/usr/bin/env bash
# Build a single git-am-compatible .patch from every commit made since origin/main.
# Usage: scripts/handover/make-patch.sh NNNN-<leaf-path>-<description>
#   e.g.  0002-1.a.i.zi-record-build-baseline
# Always builds the COMBINED patch: every commit not yet on origin/main (all unpushed sessions + this one).
set -euo pipefail

NAME="${1:-}"
if [[ -z "$NAME" ]]; then
  echo "usage: $0 NNNN-<leaf-path>-<description>" >&2; exit 1
fi
NAME="${NAME%.patch}"
if [[ ! "$NAME" =~ ^[0-9]{4}-[0-9a-z.]+-[a-z0-9-]+$ ]]; then
  echo "error: name must look like NNNN-<leaf-path>-<description> (got '$NAME')" >&2; exit 1
fi

cd "$(git rev-parse --show-toplevel)"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "error: working tree not clean — git add/commit everything first." >&2
  git status --short >&2; exit 1
fi

git fetch origin -q 2>/dev/null || echo "warning: could not fetch origin; using last known origin/main" >&2
BASE="origin/main"
git rev-parse --verify -q "$BASE" >/dev/null || { echo "error: $BASE not found (git fetch origin)" >&2; exit 1; }
COUNT="$(git rev-list --count "$BASE"..HEAD)"
if [[ "$COUNT" -eq 0 ]]; then echo "error: no commits ahead of $BASE" >&2; exit 1; fi

SUBJECTS="$(git log "$BASE"..HEAD --format=%s)"
if ! grep -qE '^[0-9]+\.[a-z]\.[ivx]+\.z[io]:' <<<"$SUBJECTS"; then
  echo "warning: no commit subject starting with a leaf path (e.g. 1.a.i.zi:) found — did you finish the leaf's final commit?" >&2
fi

OUTDIR="/mnt/user-data/outputs"
[[ -d "$OUTDIR" ]] || { OUTDIR="./patches"; mkdir -p "$OUTDIR"; }
OUT="$OUTDIR/$NAME.patch"

git format-patch --stdout "$BASE"..HEAD > "$OUT"

# Verify it applies cleanly on a throwaway worktree of origin/main
TMP="$(mktemp -d)"
git worktree add -q --detach "$TMP" "$BASE"
if ( cd "$TMP" && git am -q "$OUT" ); then
  echo "verify: patch applies cleanly on $BASE ($COUNT commits)"
else
  echo "error: patch does NOT apply cleanly on $BASE" >&2
  ( cd "$TMP" && git am --abort ) || true
  git worktree remove --force "$TMP"; rm -f "$OUT"; exit 1
fi
git worktree remove --force "$TMP"

echo
echo "Leaves carried by this combined patch (commit subjects that start with a leaf path or a legacy marker):"
git log --reverse "$BASE"..HEAD --format=%s | grep -E "^([0-9]+\.[a-z]\.[ivx]+\.z[io]:|handover: complete)" | cut -c1-110 | sed "s/^/  - /"
echo
echo "Patch: $OUT"
echo "(Apply ONLY this one. Delete older .patch files.)"
echo
echo "Run on the phone:"
echo "  cd ~/bandlab-sdk-typescript"
echo "  git am ~/storage/downloads/$NAME.patch"
echo "  git push"
