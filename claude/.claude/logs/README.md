# Run logs
<!-- TEMPLATE. Copy to run-log-<date>.md per working day or night with parallel sessions. -->

One place for what happened while the owner was not watching: decisions taken under delegation, stops, incidents, and open questions. Read the newest log first when you start a session that continues earlier work.

## Files
- `run-log-<date>.md`: one per working day or night with parallel sessions.
- `README.md`: this file.

## Who writes what
- Child sessions do not write here. Each writes its bugs and delegated decisions in its own reports and sends them to the orchestrator.
- The orchestrator copies them into the day's run log, bugs into `.claude/reports/bugs.md`, lasting decisions into `.claude/docs/decision-logs.md`, and reports them to the owner.

## Run log layout
1. Ground rules and scope (sessions, branches, base).
2. Decisions table: time, item, decision, why, reversible by. Mark each row with its source (orchestrator or session name).
3. Incidents: stops under the time-limit rule, stale locks, leftover resources, hangs.
4. Open questions for the owner, answered or not.
5. Summary for the owner: verified, merged, not done.
