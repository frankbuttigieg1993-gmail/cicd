#!/usr/bin/env bash
set -euo pipefail

SUMMARY_FILE="build/reports/spotbugs/main/spotbugs-summary.md"

if [[ -f "$SUMMARY_FILE" ]]; then
  cat "$SUMMARY_FILE" >> "$GITHUB_STEP_SUMMARY"
else
  {
    echo "## SpotBugs / FindSecBugs Security Summary"
    echo
    echo "Report unavailable."
  } >> "$GITHUB_STEP_SUMMARY"
fi
