#!/usr/bin/env python3
import argparse
import xml.etree.ElementTree as ET
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument("--xml", required=True)
parser.add_argument("--github-output", required=True)
parser.add_argument("--summary", required=True)
args = parser.parse_args()

root = ET.parse(args.xml).getroot()
findings = root.findall("./BugInstance")

def priority_of(node):
    try:
        return int(node.get("priority", "3"))
    except ValueError:
        return 3

by_priority = {p: [f for f in findings if priority_of(f) == p] for p in (1, 2, 3, 4)}
critical = by_priority[1]

lines = [
    "## SpotBugs / FindSecBugs Security Report", "",
    f"**Total findings:** {len(findings)}  ",
    f"**Critical findings (P1):** {len(by_priority[1])}  ",
    f"**High findings (P2):** {len(by_priority[2])}  ",
    f"**Normal findings (P3):** {len(by_priority[3])}  ",
    f"**Experimental findings (P4):** {len(by_priority[4])}  ",
    "**Critical policy:** FAIL when SpotBugs priority = 1", "",
]

if critical:
    lines += ["### ❌ Critical policy failed", "",
              f"{len(critical)} Priority 1 SpotBugs / FindSecBugs finding(s) were detected.", "",
              "| Finding | CWE | Class | File | Line |",
              "|---|---|---|---|---:|"]
    for bug in critical:
        cwe = bug.get("cweid")
        cls = bug.find("./Class")
        source = bug.find('./SourceLine[@primary="true"]')
        if source is None:
            source = bug.find("./SourceLine")
        lines.append(
            f"| `{bug.get('type','unknown')}` | {f'CWE-{cwe}' if cwe else ''} | "
            f"`{cls.get('classname','unknown') if cls is not None else 'unknown'}` | "
            f"`{source.get('sourcefile','unknown') if source is not None else 'unknown'}` | "
            f"{source.get('start','') if source is not None else ''} |"
        )
else:
    lines += ["### ✅ Critical policy passed", "",
              "No Priority 1 SpotBugs / FindSecBugs findings were detected."]

Path(args.summary).write_text("\n".join(lines) + "\n", encoding="utf-8")
with Path(args.github_output).open("a", encoding="utf-8") as f:
    f.write(f"critical-count={len(critical)}\n")
    f.write(f"finding-count={len(findings)}\n")
    for p in (1, 2, 3, 4):
        f.write(f"priority-{p}-count={len(by_priority[p])}\n")