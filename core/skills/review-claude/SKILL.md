---
name: review-claude
description: Review a change to the Micro-journal workflow files (CLAUDE.md, .claude/agents, rules, skills, docs, specs) for broken decision IDs, missing files, conflicting rules, claims that tools do not support, and extra always-loaded text. Read-only. Use after editing .claude/ or CLAUDE.md, before committing them, or when the owner says "review claude".
argument-hint: [git range, default: uncommitted changes and the last commit]
disable-model-invocation: true
---

Review target: $ARGUMENTS. With no argument, use `git diff HEAD` plus untracked files under `.claude/`. Read only; never edit, commit, or mark a decision [Accepted]. The author of the change must not be the only reviewer, so run this in a fresh session or subagent when you can.

Read the changed files and only what each check needs. Do not trust the author's summary; check against the files and tool output.

## Checks
1. **Decisions.** Every `D-NNN` named in the diff exists in `.claude/docs/decision-logs.md` (index, body or archive) and means what the text says. IDs are unique, the Index table has no blank row, and nothing the owner has not accepted is marked [Accepted].
2. **Paths and names.** Every backticked path, script, skill, agent, scheme, test suite or test name in the diff exists (`ls`, `grep`). Renamed or moved files have no stale references (`grep -rn <old>`).
3. **Conflicts.** The same rule must not appear in two places with different numbers or words: file length (200), spec length (about 150), fix rounds (3), release-build tries (2), who runs which suite, commit and push rules. Grep the key phrase across `CLAUDE.md`, `.claude/rules`, agents and skills.
4. **Claims versus evidence.** Statements such as "all cases are built", "tests pass", counts, or "resolved" match the code, test names or reports they cite.
5. **Cost.** Text added to always-loaded files (`CLAUDE.md`, rules without `paths`) is worth loading in every session. Agents are not told to read what is already loaded, or long files whole.
6. **Project rules.** English only in files; no emoji; Handoff block rule intact; decisions only by the owner; privacy and copy-tone rules not weakened; each proposal states its trade-off.

## Report
Findings first, most serious first, each as `file:line - problem - suggested fix`, with a severity (High = a rule or ID is wrong or a file is missing; Medium = conflict or unsupported claim; Low = cost or wording). Then what you did not check. Under 40 lines. End with the `Handoff` block from `.claude/rules/workflow.md`.
