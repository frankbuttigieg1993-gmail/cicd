#!/usr/bin/env python3
import argparse
import html
import json
from collections import Counter, defaultdict
from pathlib import Path

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "UNKNOWN": 4}

CSS = """
*{box-sizing:border-box}body{margin:0;background:#f6f8fb;color:#172033;font-family:Inter,Segoe UI,Arial,sans-serif}
.wrap{max-width:1500px;margin:28px auto;padding:0 24px}.hero,.section{background:#fff;border:1px solid #dfe5ee;border-radius:16px;box-shadow:0 1px 2px rgba(16,24,40,.04)}
.hero{padding:28px 30px;margin-bottom:22px}.hero h1{margin:0 0 10px;font-size:30px}.muted{color:#667085}
.badges{display:flex;gap:10px;flex-wrap:wrap;margin-top:22px}.badge{padding:7px 12px;border-radius:999px;font-weight:700;font-size:13px;background:#edf1f6}
.b-CRITICAL{background:#b42318;color:#fff}.b-HIGH{background:#e85d04;color:#fff}.b-MEDIUM{background:#f4b400;color:#172033}.b-LOW{background:#2e7d32;color:#fff}.b-UNKNOWN{background:#667085;color:#fff}
.section{overflow:hidden;margin:18px 0}.section-head{padding:18px 22px;background:#eef4fb;border-bottom:1px solid #dfe5ee}
.section-head h2{margin:0;font-size:20px}.section-head .meta{margin-top:5px;font-size:13px;color:#667085}
table{width:100%;border-collapse:collapse}th{text-align:left;background:#f8fafc;color:#475467;font-size:12px;text-transform:uppercase;letter-spacing:.04em;padding:12px 14px;border-bottom:1px solid #e4e7ec}
td{padding:14px;border-bottom:1px solid #eef1f5;vertical-align:top;font-size:14px}tr:last-child td{border-bottom:0}
.id{font-weight:800;white-space:nowrap}.title{font-weight:700;margin-bottom:5px}.message{color:#475467}.resolution{color:#344054}.sev{display:inline-block;border-radius:999px;padding:5px 9px;font-size:12px;font-weight:800}
a{color:#0969da;text-decoration:none}a:hover{text-decoration:underline}.target{font-family:ui-monospace,SFMono-Regular,Consolas,monospace}
.empty{padding:22px;color:#667085}
"""

def esc(value):
    return html.escape(str(value or ""))

def render_configuration(data, title):
    findings = []
    targets = defaultdict(list)

    for result in data.get("Results", []):
        target = result.get("Target", "Unknown")
        config_type = result.get("Type", "config")
        for finding in result.get("Misconfigurations") or []:
            item = {
                "target": target,
                "type": config_type,
                "id": finding.get("ID", ""),
                "title": finding.get("Title", ""),
                "severity": (finding.get("Severity") or "UNKNOWN").upper(),
                "message": finding.get("Message", ""),
                "resolution": finding.get("Resolution", ""),
                "url": finding.get("PrimaryURL", ""),
            }
            findings.append(item)
            targets[(target, config_type)].append(item)

    counts = Counter(item["severity"] for item in findings)
    trivy_version = data.get("Trivy", {}).get("Version", "unknown")

    parts = [
        "<!doctype html><html><head><meta charset=\"utf-8\">",
        f"<title>{esc(title)}</title><style>{CSS}</style></head><body><div class=\"wrap\">",
        f"<div class=\"hero\"><h1>{esc(title)}</h1>",
        f"<div class=\"muted\">Configuration and infrastructure-as-code findings from Trivy {esc(trivy_version)} · Repository scan</div>",
        "<div class=\"badges\">",
        f"<span class=\"badge\">Misconfigurations: {len(findings)}</span>",
        f"<span class=\"badge b-CRITICAL\">CRITICAL: {counts['CRITICAL']}</span>",
        f"<span class=\"badge b-HIGH\">HIGH: {counts['HIGH']}</span>",
        f"<span class=\"badge b-MEDIUM\">MEDIUM: {counts['MEDIUM']}</span>",
        f"<span class=\"badge b-LOW\">LOW: {counts['LOW']}</span>",
        "</div></div>",
    ]

    if not targets:
        parts.append('<div class="section"><div class="empty">No configuration misconfigurations were detected.</div></div>')

    for (target, config_type), items in targets.items():
        items = sorted(items, key=lambda x: (SEVERITY_ORDER.get(x["severity"], 9), x["id"]))
        parts.append(
            f'<div class="section"><div class="section-head">'
            f'<h2 class="target">{esc(target)}</h2>'
            f'<div class="meta">{esc(config_type)} · {len(items)} finding(s)</div></div>'
        )
        parts.append(
            "<table><thead><tr>"
            "<th>Check</th><th>Severity</th><th>Finding</th><th>Recommended remediation</th>"
            "</tr></thead><tbody>"
        )

        for item in items:
            if item["url"]:
                check = f'<a href="{esc(item["url"])}" target="_blank" rel="noopener noreferrer">{esc(item["id"])}</a>'
            else:
                check = esc(item["id"])

            resolution = esc(item["resolution"] or "No remediation supplied by Trivy.")
            parts.append(
                f'<tr><td class="id">{check}</td>'
                f'<td><span class="sev b-{esc(item["severity"])}">{esc(item["severity"])}</span></td>'
                f'<td><div class="title">{esc(item["title"])}</div><div class="message">{esc(item["message"])}</div></td>'
                f'<td><div class="resolution">{resolution}</div></td></tr>'
            )

        parts.append("</tbody></table></div>")

    parts.append("</div></body></html>")
    return "".join(parts)

def main():
    parser = argparse.ArgumentParser(description="Generate modern HTML from Trivy configuration JSON.")
    parser.add_argument("--trivy", required=True, help="Trivy JSON report")
    parser.add_argument("--output", required=True, help="HTML output path")
    parser.add_argument("--title", default="Trivy Configuration Security Report")
    args = parser.parse_args()

    input_path = Path(args.trivy)
    output_path = Path(args.output)

    with input_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_configuration(data, args.title), encoding="utf-8")

if __name__ == "__main__":
    main()
