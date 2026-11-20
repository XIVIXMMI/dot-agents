"""Tests for xcresult2junit.py. Run: python3 -I -m unittest discover -s .agents/tools -p 'test_*.py'"""
import json
import unittest

import xcresult2junit


def case(name, result, failure=None):
    children = [{"nodeType": "Failure Message", "name": failure}] if failure else []
    return {"nodeType": "Test Case", "name": name, "result": result, "children": children}


def convert(*cases):
    tree = {"testNodes": [{"nodeType": "Test Suite", "name": "Suite", "children": list(cases)}]}
    return xcresult2junit.to_junit(json.dumps(tree)).getroot().find("testsuite")


class ToJunitTests(unittest.TestCase):
    def test_counts_skipped_and_marks_the_case(self):
        suite = convert(case("a()", "Passed"), case("b()", "Skipped"))
        self.assertEqual(suite.get("skipped"), "1")
        self.assertEqual(suite.get("failures"), "0")
        self.assertIsNotNone(suite.findall("testcase")[1].find("skipped"))

    def test_an_unknown_result_is_a_failure_not_a_pass(self):
        suite = convert(case("a()", "unknown"), case("b()", "Passed"))
        self.assertEqual(suite.get("failures"), "1")
        self.assertIsNotNone(suite.findall("testcase")[0].find("failure"))

    def test_failed_case_keeps_its_message_and_expected_failure_passes(self):
        suite = convert(case("a()", "Failed", "x was not y"), case("b()", "Expected Failure"))
        self.assertEqual(suite.get("failures"), "1")
        self.assertEqual(suite.findall("testcase")[0].find("failure").get("message"), "x was not y")
        self.assertIsNone(suite.findall("testcase")[1].find("failure"))


if __name__ == "__main__":
    unittest.main()
