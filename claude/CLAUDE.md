# <Project name>
<!-- TEMPLATE. Fill the <placeholders>. Keep this file short: it is loaded in every session. Details live in .claude/. -->

## Context
<What the product is, who it is for, the goal.>

## Owner
<Name>, who makes all final decisions. Every proposal must state its trade-offs.
Reply language: <e.g. English / Vietnamese>.

## Product Rules
- <3-5 principles every agent must follow, e.g. minimalism, privacy by default, no new dependency without an owner-approved decision.>

## Docs
Read the decision index before proposing or building anything.
- `.claude/docs/product-brief.md` - vision, scope, assumptions, risks.
- `.claude/docs/decision-logs.md` - decision index and open entries; closed ones in `decision-archive.md`. Only **[Accepted]** decisions are binding.
- Agents: `.claude/agents/`. Rules: `.claude/rules/` (`workflow`, `communication`, `testing`). Skills: `.claude/skills/` (start features with `/new-feature`).
- Specs: `.claude/specs/`. Reports, audits, bugs: `.claude/reports/`. Both have `_template-*.md` files and a README.
- Owner corrections and repeated preferences: `.claude/docs/owner-feedback.md`.

## Project Structure
<Folder map of the source tree, one line per folder.>

## Commands
Keep output quiet; read summaries, not raw logs.
- Build: `<command>`
- Test, all: `<command>`
- Test, one suite / feature run / critical set: `<commands>`
- Lint / format: `<command>`

## Limits
- Child sessions in parallel: 2. Machine limits (RAM, cores, devices, ports): <fill in>. Hot files shared by features: <fill in later>.
- Paths that skip test runs (optional): <e.g. docs/, site/>. Protected branch: <main>.

## Workflow
**IMPORTANT:** <Your definition of done, e.g. the full test suite runs once at the end of every feature; never call a feature done while tests fail.>
