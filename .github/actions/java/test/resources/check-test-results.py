#!/usr/bin/env python3
import glob
import os
import sys
import xml.etree.ElementTree as ET

pattern = "build/test-results/test/TEST-*.xml"
files = sorted(glob.glob(pattern))

tests = failures = errors = skipped = 0

for path in files:
    try:
        root = ET.parse(path).getroot()
    except (OSError, ET.ParseError) as exc:
        print(f"::error::Unable to parse JUnit report {path}: {exc}")
        with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as out:
            out.write("tests=0\npassed=0\nfailed-tests=1\nskipped=0\n")
        sys.exit(0)
    tests += int(root.attrib.get("tests", "0") or "0")
    failures += int(root.attrib.get("failures", "0") or "0")
    errors += int(root.attrib.get("errors", "0") or "0")
    skipped += int(root.attrib.get("skipped", "0") or "0")

failed = failures + errors
passed = tests - failed - skipped

print(f"JUnit files: {len(files)}")
print(f"Tests: {tests}")
print(f"Passed: {max(passed, 0)}")
print(f"Failed: {failed}")
print(f"Skipped: {skipped}")

with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as out:
    out.write(f"tests={tests}\n")
    out.write(f"passed={max(passed, 0)}\n")
    out.write(f"failed-tests={failed}\n")
    out.write(f"skipped={skipped}\n")

sys.exit(0)