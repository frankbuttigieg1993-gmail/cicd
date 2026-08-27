#!/usr/bin/env bash
set -euo pipefail

SARIF_DIR="${SARIF_DIR:?SARIF_DIR is required}"

mapfile -t SARIF_FILES < <(find "$SARIF_DIR" -maxdepth 1 -type f -name '*.sarif' -print | sort)

if (( ${#SARIF_FILES[@]} == 0 )); then
  {
    echo "## CodeQL Security Analysis"
    echo
    echo "### Security gate: SCAN ERROR"
    echo
    echo "CodeQL did not generate a SARIF report."
  } >> "$GITHUB_STEP_SUMMARY"
  exit 0
fi

TOTAL=0
ERRORS=0
WARNINGS=0
NOTES=0

for sarif in "${SARIF_FILES[@]}"; do
  TOTAL=$((TOTAL + $(jq '[.runs[]?.results[]?] | length' "$sarif")))
  ERRORS=$((ERRORS + $(jq '[.runs[]?.results[]? | select((.level // "") == "error")] | length' "$sarif")))
  WARNINGS=$((WARNINGS + $(jq '[.runs[]?.results[]? | select((.level // "") == "warning")] | length' "$sarif")))
  NOTES=$((NOTES + $(jq '[.runs[]?.results[]? | select((.level // "") == "note")] | length' "$sarif")))
done

if (( TOTAL > 0 )); then
  STATUS="BLOCKED"
else
  STATUS="PASSED"
fi

{
  echo "## CodeQL Security Analysis"
  echo
  echo "| SARIF level | Findings |"
  echo "|---|---:|"
  echo "| Error | ${ERRORS} |"
  echo "| Warning | ${WARNINGS} |"
  echo "| Note | ${NOTES} |"
  echo "| **Total** | **${TOTAL}** |"
  echo
  echo "### Security gate: ${STATUS}"
  echo

  if (( TOTAL > 0 )); then
    echo "CodeQL detected security finding(s)."
    echo
    echo "| Rule | Level | Location |"
    echo "|---|---|---|"

    for sarif in "${SARIF_FILES[@]}"; do
      jq -r '
        .runs[]?.results[]? |
        [
          (.ruleId // "N/A"),
          (.level // "N/A"),
          (
            (.locations[0].physicalLocation.artifactLocation.uri // "N/A")
            + ":"
            + ((.locations[0].physicalLocation.region.startLine // 0) | tostring)
          )
        ] |
        @tsv
      ' "$sarif"
    done |
    while IFS=$'\t' read -r rule level location; do
      printf '| `%s` | %s | `%s` |\n' "$rule" "$level" "$location"
    done
  else
    echo "No CodeQL security findings were detected."
  fi
} >> "$GITHUB_STEP_SUMMARY"
