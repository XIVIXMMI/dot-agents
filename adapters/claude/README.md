# Claude Code adapter

- `CLAUDE.md`: imports `AGENTS.md` (`@AGENTS.md`), so Claude reads the same instructions and rules block as every other tool, plus a few Claude-only notes.
- `settings.json`: git-safe permissions and a `SessionStart` (compact) hook that reprints `.agents/docs/compact-keep.md`.
- `tools/token-report.sh`: token use per session and per agent from local Claude transcripts.
- Agents: `install.py` renders `.agents/agents/*.md` to `.claude/agents/`, mapping `tier: strong` to `opus` and `fast` to `sonnet`.
- Skills: `.claude/skills` is a symlink to `.agents/skills`, because Claude Code reads skills only from `.claude/skills/`.
