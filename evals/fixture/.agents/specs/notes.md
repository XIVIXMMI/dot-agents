# Notes - UX Spec - [Accepted] - 2026-11-01

## Goal & linked decision
- D-001. Note titles and word count. Export is out of scope (see D-002).

## Acceptance criteria
Key: NOTE
- NOTE-1: A plain title is kept as typed.
- NOTE-2: Leading and trailing spaces are removed from the title.
- NOTE-3: Word count counts words separated by any whitespace.
- NOTE-4: An empty or blank title is rejected with ValueError("Title is required").
