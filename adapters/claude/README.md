# Claude Code adapter

- `CLAUDE.md`: imports `AGENTS.md` (`@AGENTS.md`), so Claude reads the same instructions and rules block as every other tool, plus a few Claude-only notes.
- `settings.json`: agents go up to a PR, only the owner merges; a `SessionStart` (compact) hook reprints `.agents/docs/compact-keep.md`.
- `hooks/guard-main.sh`: `PreToolUse` hook that asks before anything changes the protected branch (merge, force push, push to `main`, writes while on `main`).
- `tools/token-report.sh`: token use per session and per agent from local Claude transcripts.
- Agents: `install.py` renders `.agents/agents/*.md` to `.claude/agents/`, mapping `tier: strong` to `opus` and `fast` to `sonnet`.
- Skills: `.claude/skills` is a symlink to `.agents/skills`, because Claude Code reads skills only from `.claude/skills/`.
