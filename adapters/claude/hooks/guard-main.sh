#!/bin/bash
# TEMPLATE. PreToolUse hook for Bash: agents may commit, push their own branch and open pull requests,
# but anything that changes the protected branch asks the owner first.
# Change PROTECTED if your main branch has another name. Not a hard stop: it only reads the plain command
# text (not quoted strings, scripts or eval), and bypassPermissions mode skips every prompt.
# The hard stop is branch protection on the Git host (require a PR, block force pushes).
PROTECTED="main"

input=$(cat)
cmd=$(printf '%s' "$input" | sed -nE 's/.*"command"[[:space:]]*:[[:space:]]*"(([^"\\]|\\.)*)".*/\1/p')
cmd=${cmd:-$input}
branch=$(git -C "${CLAUDE_PROJECT_DIR:-.}" symbolic-ref --short -q HEAD 2>/dev/null)
reason=""

if printf '%s' "$cmd" | grep -Eq "gh[[:space:]]+pr[[:space:]]+merge|pulls/[0-9]+/merge"; then
  reason="Merging a pull request."
elif printf '%s' "$cmd" | grep -Eq "git[^;&|]*[[:space:]]push"; then
  if printf '%s' "$cmd" | grep -Eq "(^|[[:space:]])(-f|--force[a-z-]*|--all|--mirror)([[:space:]]|$)|[[:space:]]\+"; then
    reason="A force or mass push."
  elif printf '%s' "$cmd" | grep -Eq "(^|[[:space:]:/])$PROTECTED([[:space:]]|$)"; then
    reason="A push to $PROTECTED."
  elif [ "$branch" = "$PROTECTED" ]; then
    reason="A push while the checkout is on $PROTECTED."
  fi
elif [ "$branch" = "$PROTECTED" ] && printf '%s' "$cmd" | grep -Eq "git[^;&|]*[[:space:]](commit|merge|pull|rebase|cherry-pick|revert|am|reset)"; then
  reason="A git write while the checkout is on $PROTECTED."
fi

[ -z "$reason" ] && exit 0
printf '{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"ask","permissionDecisionReason":"%s Only the owner changes %s."}}\n' "$reason" "$PROTECTED"
