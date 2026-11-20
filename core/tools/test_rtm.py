"""Tests for rtm.py. Run: python3 -I -m unittest discover -s .agents/tools -p 'test_*.py'"""
import tempfile
import unittest
from pathlib import Path

import rtm


def specs(**files):
    d = tempfile.TemporaryDirectory()
    for name, text in files.items():
        (Path(d.name) / f"{name}.md").write_text(text, encoding="utf-8")
    return d


class UnreadRequirementLinesTests(unittest.TestCase):
    def test_a_tag_before_the_colon_is_reported_not_silently_dropped(self):
        with specs(a="- INDEX-1: read\n- INDEX-2 (D-1): tagged before the colon\n") as d:
            reqs, _ = rtm.load_requirements(d)
            self.assertEqual(list(reqs), ["INDEX-1"])
            self.assertEqual(rtm.find_unread(d, reqs), [("a.md", 2, "INDEX-2")])

    def test_notes_about_known_ids_or_other_prefixes_are_not_reported(self):
        text = "- INDEX-1: read\n  - INDEX-1 fixture: a note\n- BUG-001 (D-018): a bug note\n"
        with specs(a=text) as d:
            reqs, _ = rtm.load_requirements(d)
            self.assertEqual(rtm.find_unread(d, reqs), [])

    def test_gaps_list_unread_lines(self):
        gaps = rtm.gaps_markdown([], [], [], 0, unread=[("a.md", 2, "INDEX-2")])
        self.assertIn("## Requirement-like lines not read", gaps)
        self.assertIn("- INDEX-2 (a.md:2)", gaps)


if __name__ == "__main__":
    unittest.main()
