#!/usr/bin/env python3
import json
import os
from pathlib import Path

path = Path("build/reports/semgrep/semgrep.sarif")
counts = {"error": 0, "warning": 0, "note": 0}

if path.exists():
    data = json.loads(path.read_text(encoding="utf-8"))
    for run in data.get("runs", []):
        for result in run.get("results", []):
            level = result.get("level", "warning")
            if level not in counts:
                level = "warning"
            counts[level] += 1

total = sum(counts.values())
print(f"Semgrep SARIF: errors={counts['error']}, warnings={counts['warning']}, notes={counts['note']}, total={total}")

with open(os.environ["GITHUB_OUTPUT"], "a", encoding="utf-8") as out:
    out.write(f"error-count={counts['error']}\n")
    out.write(f"warning-count={counts['warning']}\n")
    out.write(f"note-count={counts['note']}\n")
    out.write(f"total-findings={total}\n")
