# <Project name> (<stack>)
<!-- SAMPLE. Copy this preset to presets/<your-project>/ and fill in. Keep it short: details live in .claude/. -->

## Context
<What the product is, who it is for, the goal.>
Owner: <name>, who makes all final decisions — every proposal must state its trade-offs.

## Product Rules
- <3-5 principles every agent must follow, e.g. minimalism, privacy by default, no new dependency without a decision.>

## Docs
Read the decision index before proposing or building anything.
- `.claude/docs/product-brief.md` — vision, scope, assumptions, risks.
- `.claude/docs/decision-logs.md` — decision index and open entries; closed ones in `decision-archive.md`. Only **[Accepted]** decisions are binding.
- Agents: `.claude/agents/`. Rules: `.claude/rules/`. Skills: `.claude/skills/` (start features with `/new-feature`).
- Specs: `.claude/specs/<feature>[-tech|-tests].md`; reports and audits: `.claude/reports/`.
- When the owner corrects how you work, add one line to `.claude/docs/owner-feedback.md`; lasting rules go to `.claude/rules/` or `/log-decision`.

## Project Structure
<Folder map of the source tree, one line per folder.>

## Commands
- Build: `<command>`
- Test (all / one suite / fast loop): `<commands>`
- Lint / format: `<command>`

## Workflow
**IMPORTANT:** <Your definition of done, e.g. the full test suite runs after every feature; never call a feature done while tests fail.>
