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

# CodeQL stores security severity on rule metadata rather than necessarily
# setting result.level. Resolve each result to its rule and normalize the
# numeric security-severity score into GitHub-style severity bands.
FINDINGS_JSON="$(
  jq -s '
    [
      .[] |
      .runs[]? as $run |
      $run.results[]? as $result |
      (
        if ($result.ruleIndex? != null) then
          $run.tool.driver.rules[$result.ruleIndex]
        else
          ($run.tool.driver.rules // [] | map(select(.id == $result.ruleId)) | first)
        end
      ) as $rule |
      (($rule.properties["security-severity"] // "0") | tonumber? // 0) as $score |
      {
        rule: ($result.ruleId // $rule.id // "N/A"),
        score: $score,
        severity:
          (if $score >= 9.0 then "Critical"
           elif $score >= 7.0 then "High"
           elif $score >= 4.0 then "Medium"
           elif $score > 0 then "Low"
           else "Other"
           end),
        location:
          (
            ($result.locations[0].physicalLocation.artifactLocation.uri // "N/A")
            + ":"
            + (($result.locations[0].physicalLocation.region.startLine // 0) | tostring)
          )
      }
    ]
  ' "${SARIF_FILES[@]}"
)"

TOTAL="$(jq 'length' <<< "$FINDINGS_JSON")"
CRITICAL="$(jq '[.[] | select(.severity == "Critical")] | length' <<< "$FINDINGS_JSON")"
HIGH="$(jq '[.[] | select(.severity == "High")] | length' <<< "$FINDINGS_JSON")"
MEDIUM="$(jq '[.[] | select(.severity == "Medium")] | length' <<< "$FINDINGS_JSON")"
LOW="$(jq '[.[] | select(.severity == "Low")] | length' <<< "$FINDINGS_JSON")"
OTHER="$(jq '[.[] | select(.severity == "Other")] | length' <<< "$FINDINGS_JSON")"

if (( TOTAL > 0 )); then
  STATUS="BLOCKED"
else
  STATUS="PASSED"
fi

{
  echo "## CodeQL Security Analysis"
  echo
  echo "| Security Severity | Findings |"
  echo "|---|---:|"
  echo "| Critical | ${CRITICAL} |"
  echo "| High | ${HIGH} |"
  echo "| Medium | ${MEDIUM} |"
  echo "| Low | ${LOW} |"
  echo "| Other | ${OTHER} |"
  echo "| **Total** | **${TOTAL}** |"
  echo
  echo "### Security gate: ${STATUS}"
  echo

  if (( TOTAL > 0 )); then
    echo "CodeQL detected security finding(s)."
    echo
    echo "| Rule | Security Severity | Score | Location |"
    echo "|---|---|---:|---|"

    jq -r '
      .[] |
      [
        .rule,
        .severity,
        (if .score > 0 then (.score | tostring) else "N/A" end),
        .location
      ] |
      @tsv
    ' <<< "$FINDINGS_JSON" |
    while IFS=$'\t' read -r rule severity score location; do
      printf '| `%s` | %s | %s | `%s` |\n' "$rule" "$severity" "$score" "$location"
    done
  else
    echo "No CodeQL security findings were detected."
  fi
} >> "$GITHUB_STEP_SUMMARY"