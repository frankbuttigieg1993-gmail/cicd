#!/usr/bin/env python3
import json
import os
from pathlib import Path

sarif_path = Path("build/reports/semgrep/semgrep.sarif")
data = json.loads(sarif_path.read_text(encoding="utf-8"))

counts = {"error": 0, "warning": 0, "note": 0, "total": 0}
for run in data.get("runs", []):
    for result in run.get("results", []):
        level = result.get("level", "none")
        counts["total"] += 1
        if level in counts:
            counts[level] += 1

with Path(os.environ["GITHUB_OUTPUT"]).open("a", encoding="utf-8") as f:
    f.write(f"error-count={counts['error']}\n")
    f.write(f"warning-count={counts['warning']}\n")
    f.write(f"note-count={counts['note']}\n")
    f.write(f"total-findings={counts['total']}\n")

print("Semgrep findings:")
print(f"  error:   {counts['error']}")
print(f"  warning: {counts['warning']}")
print(f"  note:    {counts['note']}")
print(f"  total:   {counts['total']}")