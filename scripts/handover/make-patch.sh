#!/usr/bin/env bash
# Build a single git-am-compatible .patch from every commit made since origin/main.
# Usage: scripts/handover/make-patch.sh sNN-short-slug
set -euo pipefail

NAME="${1:-}"
if [[ -z "$NAME" ]]; then
  echo "usage: $0 sNN-short-slug   (e.g. s01-scaffold-mcp-package)" >&2; exit 1
fi
NAME="${NAME%.patch}"
if [[ ! "$NAME" =~ ^s[0-9]{2}-[a-z0-9-]+$ ]]; then
  echo "error: name must look like sNN-kebab-slug (got '$NAME')" >&2; exit 1
fi

cd "$(git rev-parse --show-toplevel)"

if [[ -n "$(git status --porcelain)" ]]; then
  echo "error: working tree not clean — git add/commit everything first." >&2
  git status --short >&2; exit 1
fi

BASE="origin/main"
git rev-parse --verify -q "$BASE" >/dev/null || { echo "error: $BASE not found (git fetch origin)" >&2; exit 1; }
COUNT="$(git rev-list --count "$BASE"..HEAD)"
if [[ "$COUNT" -eq 0 ]]; then echo "error: no commits ahead of $BASE" >&2; exit 1; fi

if ! git log "$BASE"..HEAD --format=%s | grep -q '^handover: complete S'; then
  echo "warning: no 'handover: complete SNN' commit found in this patch — did you finish the handover step?" >&2
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
echo "Patch: $OUT"
echo
echo "Run on the phone:"
echo "  cd ~/bandlab-sdk-typescript"
echo "  git am ~/storage/downloads/$NAME.patch"
echo "  git push"
