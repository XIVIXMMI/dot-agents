#!/usr/bin/env bash
# Lists Swift files over the line limit (default 200). This is a guideline, not a
# hard rule, so it always exits 0 — the caller reports the list, it doesn't fail the build.
limit="${1:-200}"
over=$(find . -name '*.swift' -not -path '*/.build/*' -not -path '*/DerivedData/*' -print0 \
  | xargs -0 wc -l 2>/dev/null \
  | awk -v max="$limit" '$2 != "total" && $1 > max { print $1 "\t" $2 }')
if [ -n "$over" ]; then
  echo "Files over $limit lines (worth a look, not an automatic split):"
  echo "$over"
else
  echo "All Swift files are within $limit lines."
fi
