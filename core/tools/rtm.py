#!/usr/bin/env python3
"""Build the requirement traceability matrix (RTM) from specs and JUnit XML.

Requirements: lines `- KEY-N: text` in .agents/specs/*.md (KEY is 2-10 capitals).
Tests: JUnit XML testcases whose name carries the ID (case and -/_ do not matter).
Writes .agents/reports/rtm.csv (for people) and rtm-gaps.md (for agents).

    python3 .agents/tools/rtm.py --junit '.agents/logs/junit/*.xml' [--junit ...] [--sheet SHEET_ID]

--sheet replaces the "RTM" tab of a Google Sheet with the CSV rows. It needs
`pip install gspread` and a service account key: the JSON text in RTM_SA_KEY_JSON (CI),
or a file at RTM_SA_KEY (default ~/.config/rtm/key.json). Share the sheet with the
service account's email as Editor.
"""
import argparse
import csv
import datetime
import glob
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

REQ_LINE = re.compile(r"^\s*[-*]\s*([A-Z][A-Z0-9]{1,9}-\d{1,4})\s*:\s*(.+?)\s*$")
ID_IN_NAME = re.compile(r"(?<![A-Za-z0-9])([A-Za-z][A-Za-z0-9]{1,9})[-_](\d{1,4})(?!\d)")
COLUMNS = ["req_id", "requirement", "spec", "status", "passed", "failed", "skipped", "tests", "last_run"]


def load_requirements(spec_dir):
    """Return ({id: (text, spec file)}, [duplicate ids])."""
    reqs, dups = {}, []
    for path in sorted(Path(spec_dir).glob("*.md")):
        if path.name.startswith("_template"):
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            m = REQ_LINE.match(line)
            if not m:
                continue
            if m[1] in reqs:
                dups.append(m[1])
            else:
                reqs[m[1]] = (m[2], path.name)
    return reqs, dups


def load_tests(patterns):
    """Return [(test name, PASS|FAIL|SKIP)] from every JUnit file matching the globs."""
    files = sorted({f for p in patterns for f in glob.glob(p, recursive=True)})
    if not files:
        raise SystemExit(f"rtm: no JUnit XML matched {patterns}; run the tests first")
    tests = []
    for f in files:
        try:
            root = ET.parse(f).getroot()
        except ET.ParseError as e:
            raise SystemExit(f"rtm: cannot parse {f}: {e}")
        for case in root.iter("testcase"):
            name = case.get("name", "")
            if case.get("classname"):
                name = f"{case.get('classname')}.{name}"
            if case.find("failure") is not None or case.find("error") is not None:
                status = "FAIL"
            elif case.find("skipped") is not None:
                status = "SKIP"
            else:
                status = "PASS"
            tests.append((name, status))
    return tests


def ids_in(name, known):
    found = {f"{k.upper()}-{n}" for k, n in ID_IN_NAME.findall(name)}
    return found & known


def build(reqs, tests):
    """Return (rows sorted by ID, names of tests that carry no known ID)."""
    known = set(reqs)
    by_req = {r: [] for r in reqs}
    orphans = []
    for name, status in tests:
        hits = ids_in(name, known)
        if not hits:
            orphans.append(name)
        for r in hits:
            by_req[r].append((name, status))
    now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    rows = []
    for r in sorted(reqs, key=lambda i: (i.rsplit("-", 1)[0], int(i.rsplit("-", 1)[1]))):
        cases = by_req[r]
        counts = {s: sum(1 for _, st in cases if st == s) for s in ("PASS", "FAIL", "SKIP")}
        if not cases:
            status = "NO_TEST"
        elif counts["FAIL"]:
            status = "FAIL"
        elif not counts["PASS"]:
            status = "SKIP"
        else:
            status = "PASS"
        text, spec = reqs[r]
        rows.append({
            "req_id": r, "requirement": text, "spec": spec, "status": status,
            "passed": counts["PASS"], "failed": counts["FAIL"], "skipped": counts["SKIP"],
            "tests": "; ".join(n for n, _ in cases), "last_run": now,
        })
    return rows, orphans


def gaps_markdown(rows, orphans, dups, total_tests):
    by = {s: [r for r in rows if r["status"] == s] for s in ("PASS", "FAIL", "NO_TEST", "SKIP")}
    out = [f"# RTM gaps - {rows[0]['last_run'] if rows else 'no requirements'}", "",
           f"Requirements: {len(rows)} (PASS {len(by['PASS'])}, FAIL {len(by['FAIL'])}, "
           f"NO_TEST {len(by['NO_TEST'])}, SKIP {len(by['SKIP'])}). "
           f"Tests: {total_tests}, without a requirement ID: {len(orphans)}."]
    sections = [
        ("Failing", [f"- {r['req_id']} ({r['spec']}): {r['tests']}" for r in by["FAIL"]]),
        ("No test", [f"- {r['req_id']} ({r['spec']}): {r['requirement']}" for r in by["NO_TEST"]]),
        ("Skipped only", [f"- {r['req_id']} ({r['spec']})" for r in by["SKIP"]]),
        ("Duplicate IDs in specs", [f"- {d}" for d in dups]),
    ]
    for title, lines in sections:
        if lines:
            out += ["", f"## {title}", *lines]
    if len(out) == 3:
        out += ["", "No gaps."]
    return "\n".join(out) + "\n"


def push_to_sheet(sheet_id, table):
    import gspread  # optional: only needed for --sheet

    key_json = os.environ.get("RTM_SA_KEY_JSON")
    if key_json:
        gc = gspread.service_account_from_dict(json.loads(key_json))
    else:
        key_file = os.path.expanduser(os.environ.get("RTM_SA_KEY", "~/.config/rtm/key.json"))
        gc = gspread.service_account(filename=key_file)
    sh = gc.open_by_key(sheet_id)
    try:
        ws = sh.worksheet("RTM")
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet("RTM", rows=len(table) + 10, cols=len(COLUMNS))
    ws.clear()
    # RAW: cell text that starts with "=" stays text, never a formula.
    ws.update(range_name="A1", values=table, value_input_option="RAW")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--junit", action="append", required=True, help="JUnit XML glob; repeat for more")
    ap.add_argument("--specs", default=".agents/specs")
    ap.add_argument("--out", default=".agents/reports")
    ap.add_argument("--sheet", help="Google Sheet ID to update (tab RTM)")
    args = ap.parse_args(argv)

    reqs, dups = load_requirements(args.specs)
    tests = load_tests(args.junit)
    rows, orphans = build(reqs, tests)

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "rtm.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    gaps = gaps_markdown(rows, orphans, dups, len(tests))
    (out / "rtm-gaps.md").write_text(gaps, encoding="utf-8")

    if args.sheet:
        push_to_sheet(args.sheet, [COLUMNS] + [[str(r[c]) for c in COLUMNS] for r in rows])
    print(gaps.splitlines()[2])
    return 0


if __name__ == "__main__":
    sys.exit(main())
