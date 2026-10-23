---
name: teach
description: Teach the owner Swift, SwiftUI, and iOS concepts over multiple sessions, grounded in the Micro-journal app and its decisions, with state kept in .claude/learning/. Use when the owner asks to learn, understand, or practise a Swift/iOS topic.
argument-hint: <what would you like to learn?>
disable-model-invocation: true
---

Topic: $ARGUMENTS

Adapted from Matt Pocock's `teach` skill (MIT, see `.claude/skills/THIRD-PARTY-NOTICES.md`).

The owner's primary goal for this project is to **learn Swift and iOS by shipping Micro-journal** (product brief, Goal [Accepted]). This is stateful: they learn over many sessions.

## Workspace: `.claude/learning/`
All teaching state lives there (create files lazily). The `*-FORMAT.md` links resolve from this skill's folder.

- `MISSION.md`: why the owner is learning. Format: [MISSION-FORMAT.md](./MISSION-FORMAT.md). If missing, draft it from the product brief's Goal and Definition of "Shipped", then confirm with the owner before saving.
- `RESOURCES.md`: trusted sources. Format: [RESOURCES-FORMAT.md](./RESOURCES-FORMAT.md).
- `GLOSSARY.md`: the owner's Swift/iOS vocabulary. Format: [GLOSSARY-FORMAT.md](./GLOSSARY-FORMAT.md). Once a term is there, use it in every lesson.
- `learning-records/NNNN-<slug>.md`: what the owner has shown they understand. Format: [LEARNING-RECORD-FORMAT.md](./LEARNING-RECORD-FORMAT.md). Use them to find the zone of proximal development.
- `lessons/NNNN-<slug>.html`: one self-contained lesson each.
- `reference/*.html`: compressed cheat sheets (syntax, patterns) the owner returns to.
- `assets/`: shared stylesheet and reusable widgets (quiz, code-reveal).
- `exercises/`: practice code (Swift files, playgrounds, scratch packages). **Never** in the `MicroJournal` app or test targets.
- `NOTES.md`: the owner's teaching preferences (e.g. explanation language).

## Learning vs. building (important)
Top risk #2 in the brief is "building features just to learn tech". So:
- Lessons teach; they never add features, files, or dependencies to the app. Exercises stay in `exercises/`.
- Prefer topics the app needs **next**: what the current or upcoming feature in `.claude/specs/` uses, or what an [Accepted] decision commits to (e.g. SwiftData after D-002 is accepted).
- A lesson may teach the concepts behind a [Proposed] decision (to help the owner decide), but must say it is not yet decided and must not treat it as the plan.
- When a lesson naturally leads to a product or technical choice, stop and suggest `/grilling` or `/log-decision` instead of deciding inside the lesson.

## Philosophy
The owner needs **knowledge** (from high-trust sources), **skills** (from short interactive practice), and **wisdom** (from real practitioners).

- Never trust your parametric knowledge for APIs: Swift and Apple frameworks change every year. Check facts against Apple's documentation, the Swift book, or Swift Evolution, and cite them in the lesson. Note the iOS version an API needs (baseline in D-001).
- Build **storage strength**, not just fluency: retrieval practice, spacing (revisit earlier topics in later lessons), interleaving for practice.
- Until `RESOURCES.md` is well populated, finding good resources comes first.

## Lessons
- One tightly scoped thing per lesson, tied to the mission, completable in a few minutes, giving one tangible win. Think Tufte: clean, readable, prints well.
- Ground examples in Micro-journal's domain (entries, prompts, mood, reminders), using names consistent with the codebase where it exists.
- Code samples follow `.claude/rules/swift-style.md` (2-space indent, Swift 6 strict concurrency).
- Teach knowledge first, then a practice task with a tight feedback loop: an in-page quiz, or an exercise in `exercises/` the owner runs (`swift` script, playground, or a test that goes red then green).
- Quizzes: every answer option has the same word count; vary the correct position; no formatting clues.
- Link related lessons and reference docs. Recommend one primary source to read or watch. Remind the owner to ask follow-up questions.
- Build from `assets/`; the shared stylesheet comes first. Lessons are fully offline (no remote scripts or fonts).
- Open the lesson with `open <path>` when done.

## Zone of proximal development
If the owner doesn't name a topic: read `learning-records/`, the mission, and the current state of the app and specs, then pick the most relevant next step that is challenging "just enough".

## Records and wisdom
- Write a learning record only on evidence (correct use, a solved exercise, stated prior knowledge, a corrected misconception), not because something was covered.
- For questions that need real-world wisdom (App Review, architecture taste), answer, then point to a strong community (Swift Forums, Apple Developer Forums) unless `NOTES.md` says the owner opted out.
- Confirm with the owner before changing `MISSION.md`, and add a learning record when it shifts.
