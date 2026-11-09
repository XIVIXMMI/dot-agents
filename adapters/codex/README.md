# Codex adapter

Codex reads `AGENTS.md` (with the rules block) and `.agents/skills/` natively, so `install.py` only renders the subagents.

- Agents: `.agents/agents/*.md` -> `.codex/agents/<name>.toml` (`name`, `description`, `developer_instructions`). Codex keeps the session's model; `tier: strong` sets `model_reasoning_effort = "high"`, `fast` sets `"medium"`.
- Trust: Codex (checked on 0.145) reads the project's `.codex/` folder, agents included, only after you trust the project (Codex asks on first run). Until then the subagents are not available; `AGENTS.md` and skills still work.
- Skills: `new-feature` and `review-agents` have `agents/openai.yaml` with `allow_implicit_invocation: false`, so they run only when called: `$new-feature <idea>`. `$ARGUMENTS` is not substituted in Codex; the skill reads your request from the message.
- Not ported from Claude: per-command git confirmations (Codex uses `sandbox_mode` and `approval_policy` for the whole session, not per agent) and the compact hook.
