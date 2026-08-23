#!/usr/bin/env python3
import argparse
import html
import os
from pathlib import Path


def env_int(name):
    try:
        return int(os.environ.get(name, "0"))
    except ValueError:
        return 0


def esc(value):
    return html.escape(str(value), quote=True)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a self-contained HTML summary for Trivy secret scans."
    )
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    fs_count = env_int("FS_COUNT")
    jar_count = env_int("JAR_COUNT")
    image_count = env_int("IMAGE_COUNT")
    total = env_int("TOTAL_COUNT")

    fs_error = os.environ.get("FS_ERROR", "0") == "1"
    jar_error = os.environ.get("JAR_ERROR", "0") == "1"
    image_error = os.environ.get("IMAGE_ERROR", "0") == "1"
    scan_error = fs_error or jar_error or image_error

    if total > 0:
        status = "BLOCKED"
        status_class = "fail"
        message = (
            "One or more potential secrets were detected by Trivy. "
            "Investigate and rotate any genuine credentials before merging."
        )
    elif scan_error:
        status = "SCAN ERROR"
        status_class = "warning"
        message = (
            "One or more enabled Trivy secret scans failed. "
            "Do not treat the repository as clean until the scan error is resolved."
        )
    else:
        status = "PASSED"
        status_class = "pass"
        message = "No secrets were detected by the enabled Trivy secret scans."

    rows = [
        ("Source filesystem", fs_count, "BLOCK if findings are detected", fs_error),
        ("Packaged JAR", jar_count, "BLOCK if findings are detected", jar_error),
        ("Container image", image_count, "BLOCK if findings are detected", image_error),
    ]

    table_rows = []
    for stage, count, policy, error in rows:
        stage_status = "SCAN ERROR" if error else ("FINDINGS" if count > 0 else "CLEAN")
        table_rows.append(
            "<tr>"
            f"<td>{esc(stage)}</td>"
            f"<td>{count}</td>"
            f"<td>{esc(stage_status)}</td>"
            f"<td>{esc(policy)}</td>"
            "</tr>"
        )

    document = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Trivy Secret Security Report</title>
<style>
body{{font-family:Arial,Helvetica,sans-serif;margin:0;background:#f5f6f8;color:#202124}}
main{{max-width:1100px;margin:32px auto;padding:0 24px}}
.card{{background:#fff;border:1px solid #dfe1e5;border-radius:8px;padding:20px;margin:18px 0}}
.metrics{{display:flex;flex-wrap:wrap;gap:12px}}
.metric{{background:#fff;border:1px solid #dfe1e5;border-radius:8px;padding:14px 18px;min-width:145px}}
.metric strong{{display:block;font-size:1.5rem;margin-top:6px}}
.pass{{color:#137333}}.fail{{color:#b3261e}}.warning{{color:#b06000}}
table{{width:100%;border-collapse:collapse;background:#fff;font-size:14px}}
th,td{{border:1px solid #dfe1e5;padding:9px;text-align:left;vertical-align:top}}
th{{background:#f1f3f4}}tr:nth-child(even){{background:#fafafa}}
.notice{{font-size:13px;color:#5f6368}}
</style>
</head>
<body>
<main>
<h1>Trivy Secret Security Report</h1>
<p class="{status_class}"><strong>Secrets Gate: {esc(status)}</strong></p>
<p>{esc(message)}</p>

<div class="metrics">
  <div class="metric">Filesystem<strong>{fs_count}</strong></div>
  <div class="metric">Packaged JAR<strong>{jar_count}</strong></div>
  <div class="metric">Container image<strong>{image_count}</strong></div>
  <div class="metric">Total<strong>{total}</strong></div>
</div>

<div class="card">
<h2>Scan summary</h2>
<table>
<thead>
<tr><th>Scan stage</th><th>Findings</th><th>Status</th><th>Policy</th></tr>
</thead>
<tbody>
{''.join(table_rows)}
<tr><td><strong>Total</strong></td><td><strong>{total}</strong></td><td><strong>{esc(status)}</strong></td><td></td></tr>
</tbody>
</table>
</div>

<div class="card notice">
<strong>No secret values are included in this report.</strong>
Detailed findings remain available in GitHub Code Scanning and the Trivy secret report artifacts.
</div>
</main>
</body>
</html>
"""

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    print(f"Trivy secret HTML report written to: {output}")


if __name__ == "__main__":
    main()
