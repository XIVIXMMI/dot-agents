# <Project name>
<!-- TEMPLATE. Fill the <placeholders>. Read by every agent tool (Codex, Kimi, OpenCode natively; Claude via CLAUDE.md). Keep it short. The block between the dot-agents markers at the end is generated from .agents/rules/: edit those files, then rerun install.py. -->

## Context
<What the product is, who it is for, the goal.>

## Owner
<Name>, who makes all final decisions. Every proposal must state its trade-offs.
Reply language: <e.g. English / Vietnamese>.

## Product Rules
- <3-5 principles every agent must follow, e.g. minimalism, privacy by default, no new dependency without an owner-approved decision.>

## Docs
Read the decision index before proposing or building anything.
- `.agents/docs/product-brief.md` - vision, scope, assumptions, risks.
- `.agents/docs/decision-logs.md` - decision index and open entries; closed ones in `decision-archive.md`. Only **[Accepted]** decisions are binding.
- Agents: `.agents/agents/`. Rules: `.agents/rules/`, already loaded below. Skills: `.agents/skills/` (start features with the `new-feature` skill).
- Specs: `.agents/specs/`. Reports, audits, bugs, RTM: `.agents/reports/`. Both have `_template-*.md` files and a README.
- Owner corrections and repeated preferences: `.agents/docs/owner-feedback.md`.

## Project Structure
<Folder map of the source tree, one line per folder.>

## Commands
Defaults are in the Stack section below, which exists only if a stack was chosen on the first install (`--stack` on a later install does not add it). Without it, fill in every command here before agents rely on them.
Keep output quiet; read summaries, not raw logs.
- Build: `<command>`
- Test, all: `<command>`
- Test, one suite / feature run / critical set: `<commands>`
- JUnit XML for the RTM: `<test command that writes JUnit XML>`; glob: `<JUnit XML glob>`
- Lint / format: `<command>`

## Limits
- Child sessions in parallel: 2. Machine limits (RAM, cores, devices, ports): <fill in>. Hot files shared by features: <fill in later>.
- Paths that skip test runs (optional): <e.g. docs/, site/>. Protected branch: <main>.

## Workflow
**IMPORTANT:** <Your definition of done, e.g. the full test suite runs once at the end of every feature; never call a feature done while tests fail.>
