#!/usr/bin/env bash
# Install a preset into a project: ./install.sh <preset> <project-dir> [--force]
# Copies each component's agents/rules/skills/specs/reports/docs into <project>/.claude/,
# and the preset's CLAUDE.md / settings.json. Existing files are skipped unless --force.
set -euo pipefail

root="$(cd "$(dirname "$0")" && pwd)"
preset="${1:?usage: install.sh <preset> <project-dir> [--force]}"
target="${2:?usage: install.sh <preset> <project-dir> [--force]}"
force="${3:-}"
pdir="$root/presets/$preset"

[ -d "$pdir" ] || { echo "unknown preset: $preset" >&2; exit 1; }
[ -d "$target" ] || { echo "no such project dir: $target" >&2; exit 1; }

copy() { # copy <src> <dst>
  if [ -e "$2" ] && [ "$force" != "--force" ]; then echo "skip   $2"; else mkdir -p "$(dirname "$2")"; cp "$1" "$2"; echo "copy   $2"; fi
}

while read -r comp; do
  case "$comp" in ''|\#*) continue ;; esac
  [ -d "$root/$comp" ] || { echo "missing component: $comp" >&2; exit 1; }
  while IFS= read -r -d '' f; do
    rel="${f#"$root/$comp/"}"
    [ "$rel" = "README.md" ] && continue # component docs are not installed
    copy "$f" "$target/.claude/$rel"
  done < <(find "$root/$comp" -type f ! -name .DS_Store -print0)
done < "$pdir/components"

if [ -f "$pdir/CLAUDE.md" ]; then copy "$pdir/CLAUDE.md" "$target/CLAUDE.md"; fi
if [ -f "$pdir/settings.json" ]; then copy "$pdir/settings.json" "$target/.claude/settings.json"; fi
