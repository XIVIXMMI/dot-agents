"""Tests for install.py and core/tools/rtm.py. Run: python3 -m unittest discover tests"""
import csv
import subprocess
import sys
import tempfile
import tomllib
import unittest
from unittest import mock
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "core" / "tools"))
import install  # noqa: E402
import rtm  # noqa: E402

SPEC = """# Notes
## Acceptance criteria
Key: AUTH
- AUTH-1: Rejects empty title
- AUTH-2: Trims spaces
- AUTH-3: Saves offline
- AUTH-30: Syncs later
- AUTH-4: Shows a hint
"""
JUNIT = """<testsuites><testsuite name="s">
  <testcase classname="tests.test_notes" name="test_AUTH_1_rejects_empty_title"/>
  <testcase classname="tests.test_notes" name="test_auth_2_trims_spaces"><failure message="x"/></testcase>
  <testcase classname="tests.test_notes" name="test_AUTH_2_keeps_inner_spaces"/>
  <testcase classname="tests.test_notes" name="test_AUTH_30_syncs_later"/>
  <testcase classname="tests.test_notes" name="test_AUTH_4_hint"><skipped/></testcase>
  <testcase classname="tests.test_notes" name="test_helper_parses_date"/>
</testsuite></testsuites>"""


class RtmTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        (self.tmp / "specs").mkdir()
        (self.tmp / "specs" / "notes.md").write_text(SPEC)
        (self.tmp / "specs" / "_template-feature.md").write_text("- FEAT-1: <criterion>\n")
        (self.tmp / "junit.xml").write_text(JUNIT)

    def run_rtm(self):
        rtm.main(["--junit", str(self.tmp / "*.xml"), "--specs", str(self.tmp / "specs"), "--out", str(self.tmp / "out")])
        with open(self.tmp / "out" / "rtm.csv", newline="") as f:
            return {r["req_id"]: r for r in csv.DictReader(f)}

    def test_statuses_and_id_matching(self):
        rows = self.run_rtm()
        self.assertEqual(list(rows), ["AUTH-1", "AUTH-2", "AUTH-3", "AUTH-4", "AUTH-30"])
        self.assertEqual(rows["AUTH-1"]["status"], "PASS")
        self.assertEqual(rows["AUTH-2"]["status"], "FAIL")  # lowercase id still matches
        self.assertEqual((rows["AUTH-2"]["passed"], rows["AUTH-2"]["failed"]), ("1", "1"))
        self.assertEqual(rows["AUTH-3"]["status"], "NO_TEST")  # AUTH_30 must not count for AUTH-3
        self.assertEqual(rows["AUTH-4"]["status"], "SKIP")
        self.assertEqual(rows["AUTH-30"]["status"], "PASS")
        self.assertNotIn("FEAT-1", rows)

    def test_gaps_file(self):
        self.run_rtm()
        gaps = (self.tmp / "out" / "rtm-gaps.md").read_text()
        self.assertIn("without a requirement ID: 1", gaps)
        self.assertIn("## Failing\n- AUTH-2", gaps)
        self.assertIn("## No test\n- AUTH-3", gaps)
        self.assertNotIn("AUTH-1 (", gaps)

    def test_missing_junit_is_an_error(self):
        with self.assertRaises(SystemExit) as cm:
            rtm.main(["--junit", str(self.tmp / "nothing*.xml"), "--specs", str(self.tmp / "specs")])
        self.assertIn("no JUnit XML matched", str(cm.exception))


class InstallTest(unittest.TestCase):
    def test_install_twice(self):
        target = Path(tempfile.mkdtemp())
        install.install(target, "python", ["claude", "codex"])
        (target / ".agents" / "docs" / "product-brief.md").write_text("owner edit")
        install.install(target, "python", ["claude", "codex"])

        agents_md = (target / "AGENTS.md").read_text()
        self.assertEqual(agents_md.count("dot-agents:rules:start"), 1)
        self.assertIn("## Stack: Python", agents_md)
        self.assertIn("## Testing Rules", agents_md)
        self.assertEqual((target / ".agents" / "docs" / "product-brief.md").read_text(), "owner edit")
        self.assertTrue((target / ".claude" / "skills").is_symlink())
        self.assertTrue((target / ".claude" / "hooks" / "guard-main.sh").exists())
        self.assertTrue((target / ".claude" / "skills" / "new-feature" / "SKILL.md").exists())
        self.assertIn("model: opus", (target / ".claude" / "agents" / "solution-architect.md").read_text())
        self.assertEqual((target / ".gitignore").read_text().count(".agents/logs/junit/"), 1)

        tomls = sorted((target / ".codex" / "agents").glob("*.toml"))
        self.assertEqual(len(tomls), 6)
        for t in tomls:
            data = tomllib.loads(t.read_text())
            self.assertEqual(data["name"], t.stem)
            self.assertIn(data["model_reasoning_effort"], ("high", "medium"))
            self.assertIn("Handoff", data["developer_instructions"] + agents_md)

    def test_existing_claude_md_gets_import_once(self):
        target = Path(tempfile.mkdtemp())
        (target / "CLAUDE.md").write_text("# Old notes\nkeep me\n")
        install.install(target, None, ["claude"])
        install.install(target, None, ["claude"])
        text = (target / "CLAUDE.md").read_text()
        self.assertTrue(text.startswith("@AGENTS.md\n"))
        self.assertEqual(text.count("@AGENTS.md"), 1)
        self.assertIn("keep me", text)

    def test_skills_copied_when_symlink_fails(self):
        target = Path(tempfile.mkdtemp())
        with mock.patch.object(Path, "symlink_to", side_effect=OSError("no privilege")):
            install.install(target, None, ["claude", "codex"])
            skills = target / ".claude" / "skills"
            self.assertFalse(skills.is_symlink())
            self.assertTrue((skills / "new-feature" / "SKILL.md").exists())
            self.assertTrue((target / ".codex" / "agents" / "tester.toml").exists())
            (skills / "stale").mkdir()
            install.install(target, None, ["claude"])
            self.assertFalse((skills / "stale").exists())
            self.assertTrue((skills / install.SKILLS_COPY_MARKER).exists())
        # A folder the owner made (no marker) is never deleted.
        own = Path(tempfile.mkdtemp())
        (own / ".claude" / "skills" / "mine").mkdir(parents=True)
        install.install(own, None, ["claude"])
        self.assertTrue((own / ".claude" / "skills" / "mine").exists())

    def test_cli_rejects_unknown_tool(self):
        r = subprocess.run([sys.executable, str(ROOT / "install.py"), tempfile.mkdtemp(), "--tools", "cursor"],
                           capture_output=True, text=True)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("unknown tools", r.stderr)


if __name__ == "__main__":
    unittest.main()
