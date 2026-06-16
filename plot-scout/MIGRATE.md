# Moving plot-scout into its own private repo

The project currently lives **inside the `ccalitt/ccalitt` profile repo**, on the
branch `claude/plot-scout-bhubaneswar-xsnbwo`, under `plot-scout/`. The goal is
its own repo: **`ccalitt/plot-scout-engine`** (private), with the project at the
repository root.

## Why it isn't already moved
The cloud build environment's GitHub integration is scoped to `ccalitt/ccalitt`
and is **not permitted to create new repositories** (the API returns
`403 Resource not accessible by integration`). Creating a repo therefore has to
happen from a machine where you're authenticated — e.g. the M2 mini. It's a
one-liner.

## Option A — one command (recommended)
On the mini, with the GitHub CLI (`gh`) authenticated:

```bash
# 1. Get the code that's on the branch
git clone <your ccalitt/ccalitt remote> ccalitt && cd ccalitt
git checkout claude/plot-scout-bhubaneswar-xsnbwo

# 2. Run the migration helper from inside plot-scout/
cd plot-scout
./scripts/migrate_to_own_repo.sh            # -> ccalitt/plot-scout-engine (private)
```

This copies the project (minus the local SQLite DB and caches) into a fresh
root-level git repo and pushes it to a new private `ccalitt/plot-scout-engine`.

## Option B — manual
```bash
cd plot-scout
mkdir /tmp/plot-scout-engine
cp -R ./. /tmp/plot-scout-engine/
cd /tmp/plot-scout-engine
rm -rf .git data/*.db* **/__pycache__
git init -b main && git add . && git commit -m "initial import"
gh repo create ccalitt/plot-scout-engine --private --source=. --remote=origin --push
```

## Option C — let me do it in a re-scoped session
In Claude Code on the web, add `ccalitt/plot-scout-engine` to this session's
repo scope (after you've created the empty repo), or start a session scoped to
it. Then I can push the project directly.

## After the move
Once `ccalitt/plot-scout-engine` exists and has the code, remove the copy from
the profile repo so it's truly "moved":

```bash
# in a ccalitt/ccalitt checkout, on the feature branch
git rm -r plot-scout && git commit -m "Remove plot-scout (moved to ccalitt/plot-scout-engine)"
git push
```

(I left it in place for now so it isn't lost — it's the only persisted copy
until you publish the new repo.)
