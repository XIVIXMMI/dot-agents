#!/usr/bin/env python3
"""Convert an xcodebuild .xcresult bundle to JUnit XML, so rtm.py can read app test results.

Usage: python3 .agents/tools/xcresult2junit.py RESULT.xcresult OUT.xml
"""
import json
import subprocess
import sys
import xml.etree.ElementTree as ET


# Anything else, including a result this script does not know, counts as a failure.
PASSING = {"Passed", "Expected Failure"}


def test_cases(node, suite=""):
    """Yield (suite, case node) for every test case below node."""
    if node.get("nodeType") == "Test Suite":
        suite = node["name"]
    if node.get("nodeType") == "Test Case":
        yield suite, node
    for child in node.get("children", []):
        yield from test_cases(child, suite)


def to_junit(raw):
    """Build the JUnit element tree from the JSON text of `xcresulttool get test-results tests`."""
    cases = [c for n in json.loads(raw)["testNodes"] for c in test_cases(n)]
    skipped = sum(case["result"] == "Skipped" for _, case in cases)
    failed = sum(case["result"] not in PASSING | {"Skipped"} for _, case in cases)
    root = ET.Element("testsuites")
    suite = ET.SubElement(root, "testsuite", name="XcodeTests", tests=str(len(cases)),
                          failures=str(failed), skipped=str(skipped))
    for suite_name, case in cases:
        name = case["name"].removesuffix("()")
        element = ET.SubElement(suite, "testcase", classname=suite_name, name=name)
        if case["result"] == "Skipped":
            ET.SubElement(element, "skipped")
        elif case["result"] not in PASSING:
            messages = [c["name"] for c in case.get("children", []) if c.get("nodeType") == "Failure Message"]
            message = "; ".join(messages) or f"result: {case['result']}"
            ET.SubElement(element, "failure", message=message[:500])
    return ET.ElementTree(root)


def main(bundle, out):
    raw = subprocess.run(["xcrun", "xcresulttool", "get", "test-results", "tests", "--path", bundle],
                         capture_output=True, text=True, check=True).stdout
    to_junit(raw).write(out, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    main(sys.argv[1], sys.argv[2])
