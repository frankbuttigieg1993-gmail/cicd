#!/usr/bin/env python3
import argparse
import html
import json
import os
from pathlib import Path

def env_int(name, default=0):
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default

def esc(value):
    return html.escape(str(value), quote=True)

def load_findings(path, stage):
    p = Path(path)
    if not path or not p.is_file() or p.stat().st_size == 0:
        return []
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return []

    findings = []
    for result in data.get("Results") or []:
        target = result.get("Target") or ""
        for secret in result.get("Secrets") or []:
            # Deliberately exclude Match, Code and other fields that can contain
            # the actual secret or surrounding source code.
            findings.append({
                "stage": stage,
                "target": target,
                "rule_id": secret.get("RuleID") or secret.get("RuleId") or "Unknown",
                "category": secret.get("Category") or "Secret",
                "severity": secret.get("Severity") or "UNKNOWN",
                "title": secret.get("Title") or "Potential secret",
                "start_line": secret.get("StartLine"),
                "end_line": secret.get("EndLine"),
            })
    return findings

def line_text(finding):
    start = finding.get("start_line")
    end = finding.get("end_line")
    if start is None:
        return "—"
    if end is None or end == start:
        return str(start)
    return f"{start}–{end}"

def remediation(finding):
    text = f"{finding.get('rule_id','')} {finding.get('title','')}".lower()
    if "password" in text:
        return "Remove the hard-coded password, rotate it if genuine, and load it from GitHub Secrets or an approved secrets manager."
    if "api" in text and "key" in text:
        return "Remove the hard-coded API key, rotate it if genuine, and inject it from GitHub Secrets or an approved secrets manager."
    if "token" in text:
        return "Revoke or rotate the token if genuine and inject it at runtime from GitHub Secrets or an approved secrets manager."
    if "private" in text and "key" in text:
        return "Revoke or replace the exposed private key if genuine and store key material in an approved secrets manager."
    return "Investigate the finding. If genuine, rotate or revoke the credential and replace the hard-coded value with a secure runtime secret."

parser = argparse.ArgumentParser()
parser.add_argument("--filesystem", default="")
parser.add_argument("--jar", default="")
parser.add_argument("--image", default="")
parser.add_argument("--output", required=True)
args = parser.parse_args()

fs_count = env_int("FS_COUNT")
jar_count = env_int("JAR_COUNT")
image_count = env_int("IMAGE_COUNT")
total_count = env_int("TOTAL_COUNT", fs_count + jar_count + image_count)
fs_error = os.getenv("FS_ERROR", "0") == "1"
jar_error = os.getenv("JAR_ERROR", "0") == "1"
image_error = os.getenv("IMAGE_ERROR", "0") == "1"
scan_error = fs_error or jar_error or image_error

findings = (
    load_findings(args.filesystem, "Source filesystem")
    + load_findings(args.jar, "Packaged JAR")
    + load_findings(args.image, "Container image")
)

if total_count > 0:
    gate, gate_class = "BLOCKED", "bad"
    gate_message = "One or more potential secrets were detected by Trivy. Investigate and rotate any genuine credentials before merging."
elif scan_error:
    gate, gate_class = "SCAN ERROR", "warn"
    gate_message = "One or more enabled Trivy secret scans failed. Do not treat the repository as clean until the scan error is resolved."
else:
    gate, gate_class = "PASSED", "good"
    gate_message = "No potential secrets were detected by the enabled Trivy secret scans."

def status(count, error):
    if error:
        return "SCAN ERROR"
    return "FINDINGS" if count else "CLEAN"

scan_rows = [
    ("Source filesystem", fs_count, status(fs_count, fs_error)),
    ("Packaged JAR", jar_count, status(jar_count, jar_error)),
    ("Container image", image_count, status(image_count, image_error)),
]
summary_rows = "".join(
    f"<tr><td>{esc(name)}</td><td>{count}</td><td>{esc(state)}</td><td>BLOCK if findings are detected</td></tr>"
    for name, count, state in scan_rows
)

table_rows = []
cards = []
for index, finding in enumerate(findings, 1):
    table_rows.append(f"""
<tr>
<td>{index}</td><td>{esc(finding['severity'])}</td><td>{esc(finding['title'])}</td>
<td><code>{esc(finding['rule_id'])}</code></td><td>{esc(finding['category'])}</td>
<td>{esc(finding['stage'])}</td><td><code>{esc(finding['target'] or '—')}</code></td>
<td>{esc(line_text(finding))}</td>
</tr>""")
    cards.append(f"""
<details>
<summary>#{index} {esc(finding['title'])} — {esc(finding['target'] or 'unknown target')}:{esc(line_text(finding))}</summary>
<div class="grid">
<div><strong>Severity</strong><br>{esc(finding['severity'])}</div>
<div><strong>Rule</strong><br><code>{esc(finding['rule_id'])}</code></div>
<div><strong>Category</strong><br>{esc(finding['category'])}</div>
<div><strong>Scan stage</strong><br>{esc(finding['stage'])}</div>
<div><strong>File / target</strong><br><code>{esc(finding['target'] or '—')}</code></div>
<div><strong>Line(s)</strong><br>{esc(line_text(finding))}</div>
</div>
<p><strong>Matched value:</strong> <span class="redacted">[REDACTED]</span></p>
<p><strong>Recommendation:</strong> {esc(remediation(finding))}</p>
</details>""")

if findings:
    details = f"""
<div class="table-wrap"><table>
<thead><tr><th>#</th><th>Severity</th><th>Finding</th><th>Rule</th><th>Category</th><th>Scan</th><th>File / target</th><th>Line(s)</th></tr></thead>
<tbody>{''.join(table_rows)}</tbody>
</table></div>
<h3>Investigation details</h3>
{''.join(cards)}
"""
elif total_count > 0:
    details = '<div class="notice">Trivy reported findings, but detailed JSON records could not be parsed. Inspect the JSON/SARIF files and error logs in the artifact.</div>'
else:
    details = "<p>No secret findings to display.</p>"

document = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Trivy Secret Security Report</title>
<style>
:root{{font-family:Inter,ui-sans-serif,system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;color:#202124;background:#f5f6f8}}
body{{margin:0;padding:28px 3.5%}} h1{{font-size:42px;margin:0 0 24px}} h2{{font-size:28px;margin:0 0 20px}}
.gate{{font-size:22px;font-weight:700}} .bad{{color:#b42318}} .warn{{color:#b65c00}} .good{{color:#067647}}
.cards{{display:flex;gap:16px;flex-wrap:wrap;margin:22px 0}} .card{{min-width:190px;background:white;border:1px solid #dfe3e8;border-radius:12px;padding:18px 22px}}
.card .n{{font-size:30px;font-weight:700;margin-top:6px}} .panel{{background:white;border:1px solid #dfe3e8;border-radius:12px;padding:28px;margin-top:24px}}
table{{width:100%;border-collapse:collapse}} th,td{{border:1px solid #dfe3e8;padding:12px;text-align:left;vertical-align:top}} th{{background:#eef0f2}}
.table-wrap{{overflow-x:auto}} code{{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;word-break:break-all}}
.muted{{color:#667085}} details{{border:1px solid #dfe3e8;border-radius:8px;margin:12px 0;padding:14px 16px}} summary{{cursor:pointer;font-weight:700}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:14px;margin:18px 0}} .redacted{{font-family:ui-monospace,monospace;background:#f2f4f7;padding:3px 7px;border-radius:5px}}
.notice{{padding:16px;border-radius:8px;background:#fff7ed;border:1px solid #fed7aa}}
</style></head><body>
<h1>Trivy Secret Security Report</h1>
<div class="gate {gate_class}">Secrets Gate: {gate}</div><p>{esc(gate_message)}</p>
<div class="cards">
<div class="card">Filesystem<div class="n">{fs_count}</div></div>
<div class="card">Packaged JAR<div class="n">{jar_count}</div></div>
<div class="card">Container image<div class="n">{image_count}</div></div>
<div class="card">Total<div class="n">{total_count}</div></div>
</div>
<section class="panel"><h2>Scan summary</h2><div class="table-wrap"><table>
<thead><tr><th>Scan stage</th><th>Findings</th><th>Status</th><th>Policy</th></tr></thead>
<tbody>{summary_rows}<tr><td><strong>Total</strong></td><td><strong>{total_count}</strong></td><td><strong>{gate}</strong></td><td></td></tr></tbody>
</table></div></section>
<section class="panel"><h2>Detailed findings</h2>
<p class="muted">Secret values and matching source-code excerpts are intentionally omitted from this HTML report.</p>
{details}</section>
<section class="panel"><strong>No secret values are included in this HTML report.</strong>
The raw Trivy JSON and SARIF files remain in the workflow artifact for investigation and Code Scanning integration. Treat raw scanner output as security-sensitive because it may contain matched content.</section>
</body></html>"""

Path(args.output).parent.mkdir(parents=True, exist_ok=True)
Path(args.output).write_text(document, encoding="utf-8")
print(f"Wrote detailed Trivy secret HTML report to {args.output} with {len(findings)} parsed finding(s).")
