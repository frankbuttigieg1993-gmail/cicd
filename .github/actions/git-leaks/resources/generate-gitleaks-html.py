#!/usr/bin/env python3
import argparse
import html
import json
from pathlib import Path


def esc(value):
    return html.escape("" if value is None else str(value), quote=True)


def location_for(result):
    locations = result.get("locations") or []
    if not locations:
        return ("Unknown", "", "")
    physical = (locations[0].get("physicalLocation") or {})
    artifact = (physical.get("artifactLocation") or {})
    region = physical.get("region") or {}
    return (
        artifact.get("uri") or "Unknown",
        region.get("startLine") or "",
        region.get("startColumn") or "",
    )


def property_value(result, *names):
    props = result.get("properties") or {}
    for name in names:
        value = props.get(name)
        if value not in (None, ""):
            return value
    return ""


def main():
    parser = argparse.ArgumentParser(description="Generate a self-contained HTML report from Gitleaks SARIF.")
    parser.add_argument("--sarif", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    sarif_path = Path(args.sarif)
    output_path = Path(args.output)
    data = json.loads(sarif_path.read_text(encoding="utf-8"))

    findings = []
    for run in data.get("runs", []):
        driver = ((run.get("tool") or {}).get("driver") or {})
        rules = {rule.get("id"): rule for rule in driver.get("rules", []) if rule.get("id")}
        for result in run.get("results", []) or []:
            rule_id = result.get("ruleId") or "Unknown"
            rule = rules.get(rule_id) or {}
            path, line, column = location_for(result)
            message = ((result.get("message") or {}).get("text") or "")
            findings.append({
                "rule": rule_id,
                "description": ((rule.get("shortDescription") or {}).get("text") or message or rule_id),
                "file": path,
                "line": line,
                "column": column,
                "level": result.get("level") or "warning",
                "commit": property_value(result, "commit", "Commit"),
                "author": property_value(result, "author", "Author"),
            })

    status = "BLOCKED" if findings else "PASSED"
    status_class = "fail" if findings else "pass"

    rows = []
    for f in findings:
        rows.append(
            "<tr>"
            f"<td><code>{esc(f['rule'])}</code></td>"
            f"<td>{esc(f['description'])}</td>"
            f"<td><code>{esc(f['file'])}</code></td>"
            f"<td>{esc(f['line'])}</td>"
            f"<td>{esc(f['level'])}</td>"
            f"<td><code>{esc(f['commit'])}</code></td>"
            f"<td>{esc(f['author'])}</td>"
            "</tr>"
        )

    table = (
        '<div class="overflow"><table><thead><tr>'
        '<th>Rule</th><th>Description</th><th>File</th><th>Line</th>'
        '<th>Level</th><th>Commit</th><th>Author</th>'
        '</tr></thead><tbody>' + "".join(rows) + "</tbody></table></div>"
        if findings
        else "<p>No Gitleaks findings were reported.</p>"
    )

    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Gitleaks Secret Security Report</title>
<style>
body{{font-family:Arial,Helvetica,sans-serif;margin:0;background:#f5f6f8;color:#202124}}
main{{max-width:1400px;margin:32px auto;padding:0 24px}}
.card{{background:#fff;border:1px solid #dfe1e5;border-radius:8px;padding:20px;margin:18px 0}}
.metric{{display:inline-block;background:#fff;border:1px solid #dfe1e5;border-radius:8px;padding:14px 18px;min-width:150px}}
.metric strong{{display:block;font-size:1.5rem;margin-top:6px}}
.pass{{color:#137333}}.fail{{color:#b3261e}}
table{{width:100%;border-collapse:collapse;background:#fff;font-size:14px}}
th,td{{border:1px solid #dfe1e5;padding:9px;text-align:left;vertical-align:top}}
th{{background:#f1f3f4}}tr:nth-child(even){{background:#fafafa}}
code{{font-family:Consolas,Monaco,monospace}}.overflow{{overflow-x:auto}}
.notice{{font-size:13px;color:#5f6368}}
</style>
</head>
<body>
<main>
<h1>Gitleaks Secret Security Report</h1>
<p class="{status_class}"><strong>Security Gate: {status}</strong></p>
<div class="metric">Findings<strong>{len(findings)}</strong></div>
<div class="card">
<h2>Findings</h2>
{table}
</div>
<div class="card notice">
<strong>Secret values are intentionally excluded.</strong>
This report is generated from the redacted Gitleaks SARIF output.
</div>
</main>
</body>
</html>
"""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(document, encoding="utf-8")


if __name__ == "__main__":
    main()