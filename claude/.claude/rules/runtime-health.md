# Runtime Health Rules (always apply)

Keeps runs from starving the machine and catches hangs early. Applies to the orchestrator, every session it starts, and every agent. Put machine limits (RAM, cores, simulators, ports, parallel runs) in `CLAUDE.md`.

## The 1-hour rule
Anything still going after 1 hour (a test run, a build, a background shell, an agent, a whole session) is checked at once. If it is making progress, leave it and note it. If it is stuck or looping, stop it and report what was stopped and why. A child session with work left and no activity for 30 minutes is asked directly by the orchestrator.

## Background tasks
Every background task ends on its own: lock waits give up after 90 minutes, no `sleep` over 60 minutes, every watcher loop has an end time, and you stop your own background tasks before ending a turn or a session's work. Log every stop (run log on a delegated night, otherwise the report or final message).

## Shared resources
- Take a lock before using a shared resource (test device, port, database). Only the owner of a lock removes it; a lock whose owner process is gone is removed by the next run.
- Start a heavy resource (emulator, simulator, container) only to run something right away and stop it when the run ends. Anyone who sees one that no running command names stops it.
- After a usage-limit reset, check for stale locks and leftover resources from stopped runs before starting again.

## Load and flaky failures
A failure in a run that overlapped with other heavy work, or one that looks like load (timeouts, timing tests over their limit), is unconfirmed until it is rerun alone while the machine is idle. One load reading is no signal. Record both runs in the report.
