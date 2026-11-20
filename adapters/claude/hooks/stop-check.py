#!/usr/bin/env python3
"""TEMPLATE. Stop hook: when code changed since the last green check, run the project's check command and
keep Claude working until it passes, then remind it once to run the review and test steps of the workflow.

Set CHECK_CMD and CODE_PATHS for the project; an empty CHECK_CMD turns the hook off.
- Runs only when the code under CODE_PATHS (index, working tree and untracked files) differs from the state
  of the last green run, so chat-only turns, commits and docs-only edits cost nothing.
- Not a hard stop: after MAX_BLOCKS failed runs in a row it lets Claude stop and tells the owner.
- It cannot prove a review happened; the reminder asks Claude to run it or say in the Handoff why not.
State lives in the git dir (dot-agents-stop-check.json), never in the repo.
"""
import hashlib
import json
import os
import subprocess
import sys
from pathlib import Path

CHECK_CMD = ""         # e.g. "just check", "pytest -q", "cargo nextest run"
CODE_PATHS = ["."]     # changes under these paths need a check; list only code to skip docs-only edits
MAX_BLOCKS = 3         # failed runs in a row before Claude may stop anyway
REVIEW_REMINDER = True
TIMEOUT = 540          # seconds; keep below the hook timeout in .claude/settings.json (600)
TAIL_LINES = 30


def git(root, *args):
    r = subprocess.run(["git", "-C", str(root), *args], capture_output=True)
    return r.stdout if r.returncode == 0 else None


def fingerprint(root):
    """Hash of the working-tree content under CODE_PATHS (path -> blob id), so staging or committing the
    same content does not change it. None when CODE_PATHS holds no files."""
    blobs = {}
    for line in (git(root, "ls-files", "-s", "-z", "--", *CODE_PATHS) or b"").split(b"\0"):
        if line:
            meta, path = line.split(b"\t", 1)
            blobs[path] = meta.split()[1]
    # Modified, deleted and untracked files: hash what is on disk now (unchanged files reuse the index).
    changed = [p for p in (git(root, "ls-files", "-m", "-o", "--exclude-standard", "-z", "--", *CODE_PATHS)
                           or b"").split(b"\0") if p]
    on_disk = [p for p in dict.fromkeys(changed) if (Path(root) / p.decode()).is_file()]
    for p in changed:
        blobs.pop(p, None)
    if on_disk:
        r = subprocess.run(["git", "-C", str(root), "hash-object", "--stdin-paths"],
                           input=b"\n".join(on_disk) + b"\n", capture_output=True)
        blobs.update(zip(on_disk, r.stdout.split()))
    if not blobs:
        return None
    return hashlib.sha256(b"\0".join(p + b" " + blobs[p] for p in sorted(blobs))).hexdigest()


def run_check(root):
    try:
        r = subprocess.run(CHECK_CMD, shell=True, cwd=root, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return False, f"timed out after {TIMEOUT} s"
    out = (r.stdout + r.stderr).strip().splitlines()
    return r.returncode == 0, "\n".join(out[-TAIL_LINES:])


def decide(raw):
    """Return the hook output as a dict, or None to let Claude stop."""
    if not CHECK_CMD:
        return None
    try:
        data = json.loads(raw or "{}")
    except ValueError:
        data = {}
    root = os.environ.get("CLAUDE_PROJECT_DIR") or data.get("cwd") or "."
    gitdir = git(root, "rev-parse", "--absolute-git-dir")
    if not gitdir:
        return None
    fp = fingerprint(root)
    if fp is None:
        return None
    state_file = Path(gitdir.decode().strip()) / "dot-agents-stop-check.json"
    try:
        state = json.loads(state_file.read_text())
    except (OSError, ValueError):
        state = {}
    if state.get("green") == fp:
        return None

    def save(**kw):
        state.update(kw)
        state_file.write_text(json.dumps(state))

    if state.get("blocks", 0) >= MAX_BLOCKS:
        save(blocks=0)
        return {"systemMessage": f"stop-check: `{CHECK_CMD}` still fails after {MAX_BLOCKS} tries; Claude stopped anyway."}
    ok, tail = run_check(root)
    if not ok:
        n = state.get("blocks", 0) + 1
        save(blocks=n)
        return {"decision": "block", "reason": (
            f"`{CHECK_CMD}` failed (try {n}/{MAX_BLOCKS}). Fix the cause; never weaken, delete or skip a test. "
            f"If you cannot fix it, report it to the owner.\n{tail}")}
    save(green=fp, blocks=0)
    if not REVIEW_REMINDER:
        return None
    return {"decision": "block", "reason": (
        f"`{CHECK_CMD}` passed on the changed code. Before you finish (.agents/rules/workflow.md): run "
        "`sec-perf-reviewer` if the change is in its review scope, and the `tester` feature run if this is a feature. "
        "If they already ran on this code or do not apply, say which and why in the Handoff, then stop.")}


if __name__ == "__main__":
    out = decide(sys.stdin.read())
    if out:
        print(json.dumps(out))
