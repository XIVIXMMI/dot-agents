# Communication Rules (always apply)

How agents talk to the owner.

- Reply in the language set in `CLAUDE.md` (Owner section). Files in the repo stay in English unless `CLAUDE.md` says otherwise.
- Lead with the answer or the decision needed; then the reasons. Short bullets over long prose.
- Every proposal states its trade-offs and a recommendation. The owner decides.
- Ask only what changes the outcome. For minor gaps, make a reasonable reversible assumption, label it, and continue.
- Questions to the owner are numbered, each with your recommendation, worded so "yes" accepts it.
- Say plainly what was not done, not verified, or not run. Never claim "done" or "passing" without tool output to back it.
- Errors and warnings you show or write (including product text) must be clear in meaning and must not claim anything that may be untrue. If unsure, say less.
- When the owner corrects how you work or repeats a preference, add one line to `.claude/docs/owner-feedback.md` (date, feedback, how to apply). If it should become a lasting rule, propose it for `.claude/rules/`.

## Token economy
Spend tokens only where they add value.
- `CLAUDE.md` and `.claude/rules/` are already loaded; do not re-read them.
- Read files by path and section, not whole directories; do not read the same file twice in one task.
- Pass file paths between agents, not pasted contents. Link a decision or spec instead of repeating it.
- Keep command output quiet (quiet flags, `tail`, summaries). Never load a raw build or test log into context; read the summary and open details only for failures.
- Run the narrowest test that covers a change (see Test levels in `workflow.md`); do not re-run without a code change.
- To see where tokens went, run `bash .claude/tools/token-report.sh` (per session and per agent, numbers only). Run it on demand, not in the background.
- Keep specs about 150 lines, dev reports about 40, test reports about 80, decision entries about 8 lines. List failures, not passing cases.
