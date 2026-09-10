#!/bin/sh
# new-lane.sh <name> — one worktree per lane. Run from repo root.
# Usage: sh scripts/new-lane.sh api
set -e
test -n "$1" || { echo "usage: new-lane.sh <lane>"; exit 2; }
git worktree add "../$(basename "$PWD")-$1" -b "lane/$1"
echo "lane $1 ready — claim it in LANES.md before touching code"
