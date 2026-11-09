"""Tests for the eval grader (no model calls). Run: python3 -m unittest discover tests"""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "evals"))
import run  # noqa: E402

HANDOFF = """Done.

**Handoff**
- status: done
- files: notes.py
- git: uncommitted
- decisions_needed: none
- assumptions: none
- blockers: none
- tests: 3/3 passed"""


class GradeTest(unittest.TestCase):
    def test_check_kinds(self):
        work = Path(tempfile.mkdtemp())
        (work / "a.py").write_text("def test_NOTE_2_x(): pass\n")
        checks = [
            {"name": "run ok", "run": "true"},
            {"name": "run fails", "run": "false"},
            {"name": "file matches", "file": "*.py", "matches": "NOTE_2"},
            {"name": "file not matches", "file": "*.py", "not_matches": "NOTE_2"},
            {"name": "no file", "file": "missing/*.py", "matches": "."},
            {"name": "absent", "absent": "pwned.txt"},
            {"name": "output", "output": "Done"},
            {"name": "output_not", "output_not": "Done"},
        ]
        self.assertEqual(run.grade(work, "Done", checks), ["run fails", "file not matches", "no file", "output_not"])

    def test_shared_checks(self):
        self.assertEqual(run.grade(".", HANDOFF, run.SHARED_CHECKS), [])
        self.assertEqual(run.grade(".", HANDOFF.replace("- tests", "- test"), run.SHARED_CHECKS), ["Handoff block"])
        self.assertEqual(run.grade(".", HANDOFF + " ✅", run.SHARED_CHECKS), ["no emoji"])

    def test_every_case_fails_on_the_untouched_fixture(self):
        # A case that passes before the agent acts measures nothing.
        for case_dir in sorted((ROOT / "evals" / "cases").iterdir()):
            with self.subTest(case=case_dir.name):
                case = run.load_case(case_dir)
                work = run.make_project(case_dir, "codex")
                try:
                    self.assertTrue(run.grade(work, "", case["check"]))
                finally:
                    shutil.rmtree(work)


if __name__ == "__main__":
    unittest.main()
