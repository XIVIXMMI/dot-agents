---
name: grilling
description: Interview the owner relentlessly about a project plan, feature idea, or open decision until every branch is resolved, then turn the outcomes into [Proposed] decision-log entries. Use when the owner wants to stress-test their thinking, says "grill me", or before a feature enters the /new-feature pipeline with unclear scope.
argument-hint: <plan, feature idea, or decision ID to grill>
---

Topic: $ARGUMENTS

Adapted from Matt Pocock's `grilling` skill (MIT, see `THIRD-PARTY-NOTICES.md`).

Interview the owner  until you reach a shared understanding. Map the topic as a **design tree**: every decision branches into the decisions that hang off it.

## Before the first round
- Read `.claude/docs/product-brief.md` and `.claude/docs/decision-logs.md`.
- **[Accepted] decisions are settled.** Treat them as the trunk of the tree, not as questions. Only reopen one if the owner asks, or if the topic directly contradicts it; then say which decision and why.
- [Proposed], [Hypothesis], and [Open] items that the topic depends on are fair game: put them on the frontier.

## Rounds
The **frontier** is every decision whose prerequisites are already settled: the questions you can ask _now_ without guessing at answers you haven't heard yet. Ask the whole frontier in one round, numbered, each with your recommendation **and its trade-offs** (the owner decides, so every recommendation states its cost). Then wait for answers.

```
**Q1** - **<question title>**: <question body; list the options when there are several>

Recommendation: <recommended answer> — Trade-offs: <what it costs, what it rules out>

---

**Q2** - ...
```

Word each question so "yes" accepts your recommendation.

Each round of answers reshapes the tree: settled decisions push the frontier outward. Recompute it and ask the next round. A question that depends on another question still open in this round belongs to a _later_ round.

Keep questions inside the Product Rules in `CLAUDE.md`. If an answer would break one, say which rule and ask whether the owner really means to change it.

## Facts vs. decisions
Finding _facts_ is your job, never the owner's. When a question needs a fact from the codebase or docs, dispatch an `Explore` sub-agent; for a framework or API fact, use `solution-architect` or a web search. Don't block on it: only the questions downstream of a running lookup wait; ask the rest of the frontier now.

The _decisions_ are the owner's: put each to them and wait.

## Finishing
The session is done when the frontier is empty: every branch visited, nothing silently assumed.

1. Summarize the settled tree in a short list, and ask the owner to confirm it is the shared understanding. Do nothing else until they confirm.
2. For each outcome that is a lasting product or technical decision, use the `log-decision` skill to add a **[Proposed]** entry (or update an existing one's fields). Put the alternatives you discussed under "Options considered".
3. An owner answer in this session is **not** acceptance of the log entry. Mark an entry [Accepted] only if the owner explicitly says so (e.g. "accept D-007"), quoting their words, as `log-decision` requires.
4. Outcomes that only sharpen the brief (assumptions, scope notes) go into `product-brief.md` with the right tag; ask before editing it.

Don't start implementing. If the topic is a feature, end by pointing to `/new-feature`.
