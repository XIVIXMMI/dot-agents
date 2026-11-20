# Claude Code adapter

- `CLAUDE.md`: imports `AGENTS.md` (`@AGENTS.md`), so Claude reads the same instructions and rules block as every other tool, plus a few Claude-only notes.
- `settings.json`: agents go up to a PR, only the owner merges; a `SessionStart` (compact) hook reprints `.agents/docs/compact-keep.md`.
- `hooks/guard-main.sh`: `PreToolUse` hook that asks before anything changes the protected branch (merge, force push, push to `main`, writes while on `main`).
- `hooks/stop-check.py`: `Stop` hook. When code under `CODE_PATHS` changed since the last green run, it runs `CHECK_CMD` and keeps Claude working until it passes (at most `MAX_BLOCKS` failed runs in a row, then it lets Claude stop and tells the owner), then reminds Claude once to run `sec-perf-reviewer` and the `tester` feature run or say in the Handoff why not. Off until you set `CHECK_CMD` at the top of the file. It cannot prove a review happened.
- `tools/token-report.sh`: token use per session and per agent from local Claude transcripts.
- Agents: `install.py` renders `.agents/agents/*.md` to `.claude/agents/`, mapping `tier: strong` to `opus` and `fast` to `sonnet`.
- Skills: `.claude/skills` is a symlink to `.agents/skills`, because Claude Code reads skills only from `.claude/skills/`. Where symlinks are not allowed (Windows without Developer Mode), `install.py` copies the folder instead, marks it with `.dot-agents-copy` and refreshes it on every rerun.
