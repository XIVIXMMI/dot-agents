@AGENTS.md

## Claude Code
- Subagents in `.claude/agents/` are generated from `.agents/agents/` by `install.py`: edit the source, then rerun it.
- `.claude/skills` links to `.agents/skills`. Start features with `/new-feature`.
- Token use per session and per agent: `bash .claude/tools/token-report.sh` (on demand, numbers only).
- A `Stop` hook (`.claude/hooks/stop-check.py`) runs the project check when code changed and asks for review and tests before you finish. Fix failures; never weaken a test to pass it.
