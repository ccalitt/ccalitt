#!/usr/bin/env bash
#
# Move plot-scout into its OWN private GitHub repo, with the project at the repo
# root (out of the ccalitt/ccalitt profile repo).
#
# Why this is a script you run (not done automatically): the cloud build
# environment's GitHub integration is scoped to ccalitt/ccalitt and is not
# permitted to create new repositories (create_repository -> HTTP 403). Run this
# on a machine where the `gh` CLI is authenticated (e.g. the M2 mini).
#
# Usage:
#   cd plot-scout
#   ./scripts/migrate_to_own_repo.sh [repo-name] [owner]
# Defaults: repo-name=plot-scout-engine  owner=ccalitt
#
set -euo pipefail

REPO="${1:-plot-scout-engine}"
OWNER="${2:-ccalitt}"

# Resolve the plot-scout/ project root (parent of this scripts/ dir).
PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

command -v gh   >/dev/null || { echo "error: GitHub CLI 'gh' not found"; exit 1; }
command -v git  >/dev/null || { echo "error: 'git' not found"; exit 1; }

STAGING="$(mktemp -d)/$REPO"
mkdir -p "$STAGING"

# Copy the project, excluding VCS, local DB, and caches.
if command -v rsync >/dev/null; then
  rsync -a --exclude='.git' --exclude='data/*.db' --exclude='data/*.db-*' \
        --exclude='__pycache__' --exclude='.pytest_cache' \
        "$PROJECT_DIR"/ "$STAGING"/
else
  cp -R "$PROJECT_DIR"/. "$STAGING"/
  rm -rf "$STAGING/.git" "$STAGING"/data/*.db "$STAGING"/data/*.db-* 2>/dev/null || true
  find "$STAGING" -name __pycache__ -type d -prune -exec rm -rf {} + 2>/dev/null || true
fi

cd "$STAGING"
git init -b main >/dev/null
git add .
git commit -q -m "plot-scout-engine: initial import (sourcing & scoring engine + browse UI)"

# Create the private repo and push main in one step.
gh repo create "$OWNER/$REPO" --private --source=. --remote=origin --push

echo
echo "Done → https://github.com/$OWNER/$REPO  (private, project at root)"
echo "Next: cd $STAGING ; python web/server.py --scan --open"
