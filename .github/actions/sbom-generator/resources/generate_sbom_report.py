#!/usr/bin/env python3
"""
Generate a single HTML report from:
- CycloneDX SBOM JSON (all components + dependency depth)
- Trivy JSON output (vulnerabilities + licenses)

Usage:
  python3 generate_sbom_report.py --sbom bom.json --trivy trivy-sbom.json --output sbom-report.html

Features:
- Full component inventory
- Dependency type (root / direct / transitive / unmapped)
- Trivy vulnerabilities and license findings
- Colored severity badges
- Clickable CVE IDs
- DataTables search / sort / pagination
- Fix available column
- Publication date column
- Severity summaries under the findings tables
"""

from __future__ import annotations

import argparse
import html
import json
from collections import Counter, deque
from pathlib import Path
from typing import Any, Optional
from urllib.parse import quote


def load_json(path: str | Path) -> dict[str, Any]:
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def get_license_text(licenses: Optional[list[dict[str, Any]]]) -> str:
    values: list[str] = []

    for lic in licenses or []:
        if not isinstance(lic, dict):
            continue

        if "license" in lic and isinstance(lic["license"], dict):
            inner = lic["license"]
            values.append(inner.get("id") or inner.get("name") or "Unknown")
        else:
            values.append(lic.get("id") or lic.get("name") or "Unknown")

    return ", ".join(values) if values else "-"


def get_root_purl(sbom: dict[str, Any]) -> str:
    metadata_component = sbom.get("metadata", {}).get("component", {})
    if isinstance(metadata_component, dict):
        purl = metadata_component.get("purl")
        if purl:
            return str(purl)

    components = sbom.get("components", [])
    if components and isinstance(components[0], dict):
        purl = components[0].get("purl")
        if purl:
            return str(purl)

    raise ValueError("Could not determine the root component PURL from the SBOM.")


def build_dependency_graph(sbom: dict[str, Any]) -> dict[str, list[str]]:
    graph: dict[str, list[str]] = {}

    for dep in sbom.get("dependencies", []) or []:
        if not isinstance(dep, dict):
            continue
        ref = dep.get("ref")
        if not ref:
            continue
        depends_on = dep.get("dependsOn", [])
        graph[str(ref)] = [str(x) for x in depends_on if x]

    return graph


def build_depth_map(sbom: dict[str, Any]) -> dict[str, int]:
    graph = build_dependency_graph(sbom)
    root = get_root_purl(sbom)

    depth: dict[str, int] = {root: 0}
    queue: deque[str] = deque([root])

    while queue:
        current = queue.popleft()
        current_depth = depth[current]

        for child in graph.get(current, []):
            next_depth = current_depth + 1
            if child not in depth or next_depth < depth[child]:
                depth[child] = next_depth
                queue.append(child)

    return depth


def dependency_type(depth: Optional[int]) -> str:
    if depth is None:
        return "unmapped"
    if depth == 0:
        return "root"
    if depth == 1:
        return "direct"
    return "transitive"


def build_components(sbom: dict[str, Any]) -> list[dict[str, Any]]:
    components: list[dict[str, Any]] = []

    metadata_component = sbom.get("metadata", {}).get("component")
    if isinstance(metadata_component, dict):
        components.append(
            {
                "scope": "main component",
                "group": metadata_component.get("group", ""),
                "name": metadata_component.get("name", ""),
                "version": metadata_component.get("version", ""),
                "type": metadata_component.get("type", ""),
                "licenses": metadata_component.get("licenses", []),
                "purl": metadata_component.get("purl", ""),
            }
        )

    for component in sbom.get("components", []) or []:
        if not isinstance(component, dict):
            continue
        components.append(
            {
                "scope": "dependency",
                "group": component.get("group", ""),
                "name": component.get("name", ""),
                "version": component.get("version", ""),
                "type": component.get("type", ""),
                "licenses": component.get("licenses", []),
                "purl": component.get("purl", ""),
            }
        )

    return components


def extract_cvss(vuln: dict[str, Any]) -> tuple[str, str]:
    cvss = vuln.get("CVSS", {})
    if not isinstance(cvss, dict):
        return "-", "-"

    preferred_sources = (
        "nvd",
        "ghsa",
        "redhat",
        "ubuntu",
        "debian",
        "alpine",
        "oracle",
        "arch",
        "suse",
        "amazon",
        "chainguard",
        "cbl-mariner",
        "bitnami",
    )
    score_keys = ("V4Score", "V3Score", "V2Score", "Score", "score")

    def first_score(entry: dict[str, Any]) -> Optional[str]:
        for key in score_keys:
            value = entry.get(key)
            if value not in (None, ""):
                return str(value)
        return None

    for source in preferred_sources:
        entry = cvss.get(source)
        if isinstance(entry, dict):
            score = first_score(entry)
            if score is not None:
                return score, source

    for source, entry in cvss.items():
        if isinstance(entry, dict):
            score = first_score(entry)
            if score is not None:
                return score, str(source)

    return "-", "-"


def pick_advisory_url(vuln: dict[str, Any]) -> str:
    """
    Prefer NVD for CVE IDs, otherwise GitHub Advisory URL / primary URL.
    """
    vuln_id = str(vuln.get("VulnerabilityID", "")).strip()
    primary_url = str(vuln.get("PrimaryURL", "")).strip()

    if vuln_id.startswith("CVE-"):
        return f"https://nvd.nist.gov/vuln/detail/{quote(vuln_id)}"

    if primary_url:
        return primary_url

    for ref in vuln.get("References", []) or []:
        if isinstance(ref, str) and "github.com/advisories" in ref:
            return ref

    return ""


def build_vulnerability_list(trivy: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []

    for result in trivy.get("Results", []) or []:
        if not isinstance(result, dict):
            continue

        target = result.get("Target", result.get("Class", "SBOM"))

        for vuln in result.get("Vulnerabilities", []) or []:
            if not isinstance(vuln, dict):
                continue

            score, source = extract_cvss(vuln)
            pub_date = str(vuln.get("PublishedDate", "-")) if vuln.get("PublishedDate") else "-"
            fix_available = "Yes" if str(vuln.get("FixedVersion", "")).strip() not in ("", "-", "none", "null") else "No"

            findings.append(
                {
                    "target": target,
                    "package": vuln.get("PkgName", "-"),
                    "vuln_id": vuln.get("VulnerabilityID", "-"),
                    "severity": vuln.get("Severity", "-"),
                    "score": score,
                    "cvss_source": source,
                    "installed": vuln.get("InstalledVersion", "-"),
                    "fixed": vuln.get("FixedVersion", "-"),
                    "fix_available": fix_available,
                    "published_date": pub_date,
                    "advisory_url": pick_advisory_url(vuln),
                }
            )

    return findings


def build_license_list(trivy: dict[str, Any]) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []

    for result in trivy.get("Results", []) or []:
        if not isinstance(result, dict):
            continue

        target = result.get("Target", result.get("Class", "SBOM"))

        for lic in result.get("Licenses", []) or []:
            if not isinstance(lic, dict):
                continue

            findings.append(
                {
                    "target": target,
                    "package": lic.get("PkgName", lic.get("PkgID", "-")),
                    "license": lic.get("Name", lic.get("License", lic.get("ID", "-"))),
                    "severity": lic.get("Severity", "-"),
                    "category": lic.get("Category", "-"),
                }
            )

    return findings


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value))


def sev_class(severity: str) -> str:
    s = (severity or "").strip().lower()
    if s == "critical":
        return "sev-critical"
    if s == "high":
        return "sev-high"
    if s == "medium":
        return "sev-medium"
    if s == "low":
        return "sev-low"
    return "sev-unknown"


def sev_badge(severity: str) -> str:
    label = (severity or "-").strip() or "-"
    return f"<span class='sev {sev_class(label)}'>{esc(label)}</span>"


def summarize_severities(items: list[dict[str, Any]], key: str = "severity") -> str:
    counts = Counter(str(item.get(key, "-")).strip().title() or "-" for item in items)
    order = ["Critical", "High", "Medium", "Low", "-"]
    parts = []
    for sev in order:
        if counts.get(sev, 0):
            parts.append(f"{counts[sev]} {sev.lower()}")
    if not parts:
        return "No findings."
    return ", ".join(parts) + "."


def summarize_license_categories(items: list[dict[str, Any]]) -> str:
    counts = Counter(str(item.get("severity", "-")).strip().title() or "-" for item in items)
    order = ["Critical", "High", "Medium", "Low", "-"]
    parts = []
    for sev in order:
        if counts.get(sev, 0):
            parts.append(f"{counts[sev]} {sev.lower()}")
    if not parts:
        return "No license findings."
    return ", ".join(parts) + "."


def write_html(
    output: str | Path,
    components: list[dict[str, Any]],
    depth_map: dict[str, int],
    vulnerabilities: list[dict[str, Any]],
    licenses: list[dict[str, Any]],
    title: str,
) -> None:
    comp_rows: list[str] = []
    comp_dep_counts = Counter()

    for i, component in enumerate(components, 1):
        purl = str(component.get("purl", ""))
        depth = depth_map.get(purl) if purl else None
        dep_type = dependency_type(depth)
        comp_dep_counts[dep_type] += 1

        comp_rows.append(
            "<tr>"
            f"<td>{i}</td>"
            f"<td>{esc(component.get('scope', ''))}</td>"
            f"<td>{esc(component.get('group', ''))}</td>"
            f"<td>{esc(component.get('name', ''))}</td>"
            f"<td>{esc(component.get('version', ''))}</td>"
            f"<td>{esc(component.get('type', ''))}</td>"
            f"<td>{esc(dep_type)}</td>"
            f"<td>{esc(depth) if depth is not None else '-'}</td>"
            f"<td>{esc(get_license_text(component.get('licenses')))}</td>"
            f"<td><code>{esc(purl)}</code></td>"
            "</tr>"
        )

    vuln_rows = "".join(
        "<tr>"
        f"<td>{i}</td>"
        f"<td>{esc(v['target'])}</td>"
        f"<td>{esc(v['package'])}</td>"
        f"<td><a href='{esc(v['advisory_url'])}' target='_blank' rel='noopener noreferrer'>{esc(v['vuln_id'])}</a></td>"
        f"<td>{sev_badge(v['severity'])}</td>"
        f"<td>{esc(v['score'])}</td>"
        f"<td>{esc(v['cvss_source'])}</td>"
        f"<td>{esc(v['installed'])}</td>"
        f"<td>{esc(v['fixed'])}</td>"
        f"<td>{esc(v['fix_available'])}</td>"
        f"<td>{esc(v['published_date'])}</td>"
        "</tr>"
        for i, v in enumerate(vulnerabilities, 1)
    ) or "<tr><td colspan='11'>No vulnerabilities found.</td></tr>"

    lic_rows = "".join(
        "<tr>"
        f"<td>{i}</td>"
        f"<td>{esc(l['target'])}</td>"
        f"<td>{esc(l['package'])}</td>"
        f"<td>{esc(l['license'])}</td>"
        f"<td>{sev_badge(l['severity'])}</td>"
        f"<td>{esc(l['category'])}</td>"
        "</tr>"
        for i, l in enumerate(licenses, 1)
    ) or "<tr><td colspan='6'>No license findings were returned by Trivy.</td></tr>"

    vuln_summary = summarize_severities(vulnerabilities)
    lic_summary = summarize_license_categories(licenses)

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>{esc(title)}</title>
  <link rel="stylesheet" href="https://cdn.datatables.net/1.13.8/css/jquery.dataTables.min.css">
  <script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>
  <script src="https://cdn.datatables.net/1.13.8/js/jquery.dataTables.min.js"></script>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; background: #f7f7f7; color: #111; }}
    h1, h2 {{ margin-bottom: 0.25rem; }}
    .card {{ background: #fff; border: 1px solid #ddd; border-radius: 12px; padding: 16px; margin: 16px 0; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit,minmax(160px,1fr)); gap: 12px; }}
    .stat {{ border: 1px solid #e5e5e5; border-radius: 10px; padding: 12px; background: #fafafa; }}
    .stat b {{ display: block; font-size: 1.4rem; margin-top: 6px; }}
    table.dataTable {{ width: 100% !important; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; }}
    th, td {{ border: 1px solid #ddd; padding: 8px; vertical-align: top; text-align: left; }}
    th {{ background: #f0f0f0; }}
    .tablewrap {{ overflow: auto; border: 1px solid #ddd; border-radius: 10px; }}
    code {{ word-break: break-all; }}
    .muted {{ color: #666; }}
    .summary {{ margin-top: 10px; font-size: 0.95rem; }}
    .sev {{ display: inline-block; padding: 2px 9px; border-radius: 999px; font-size: 0.85rem; font-weight: 700; line-height: 1.4; }}
    .sev-critical {{ background: #7a0012; color: #fff; }}
    .sev-high {{ background: #c62828; color: #fff; }}
    .sev-medium {{ background: #ef6c00; color: #fff; }}
    .sev-low {{ background: #f9a825; color: #111; }}
    .sev-unknown {{ background: #607d8b; color: #fff; }}
    .badge-line {{ margin-top: 8px; }}
    a {{ color: inherit; }}
  </style>
</head>
<body>
  <h1>{esc(title)}</h1>
  <p class="muted">Full CycloneDX inventory plus Trivy vulnerability and license scan results.</p>

  <div class="card">
    <div class="grid">
      <div class="stat">Components<b>{len(components)}</b></div>
      <div class="stat">Vulnerabilities<b>{len(vulnerabilities)}</b></div>
      <div class="stat">License findings<b>{len(licenses)}</b></div>
    </div>
  </div>

  <div class="card">
    <h2>All components</h2>
    <div class="tablewrap">
      <table id="componentsTable" class="display">
        <thead>
          <tr>
            <th>#</th>
            <th>Scope</th>
            <th>Group</th>
            <th>Name</th>
            <th>Version</th>
            <th>Type</th>
            <th>Dependency type</th>
            <th>Depth</th>
            <th>Licenses</th>
            <th>PURL</th>
          </tr>
        </thead>
        <tbody>
          {''.join(comp_rows)}
        </tbody>
      </table>
    </div>
    <div class="summary muted">Dependency summary: {comp_dep_counts.get("root", 0)} root, {comp_dep_counts.get("direct", 0)} direct, {comp_dep_counts.get("transitive", 0)} transitive, {comp_dep_counts.get("unmapped", 0)} unmapped.</div>
  </div>

  <div class="card">
    <h2>Vulnerabilities</h2>
    <div class="tablewrap">
      <table id="vulnTable" class="display">
        <thead>
          <tr>
            <th>#</th>
            <th>Target</th>
            <th>Package</th>
            <th>Vulnerability ID</th>
            <th>Severity</th>
            <th>CVSS score</th>
            <th>CVSS source</th>
            <th>Installed</th>
            <th>Fixed</th>
            <th>Fix available</th>
            <th>Published date</th>
          </tr>
        </thead>
        <tbody>
          {vuln_rows}
        </tbody>
      </table>
    </div>
    <div class="summary muted">Severity summary: {vuln_summary}</div>
  </div>

  <div class="card">
    <h2>License findings</h2>
    <div class="tablewrap">
      <table id="licenseTable" class="display">
        <thead>
          <tr>
            <th>#</th>
            <th>Target</th>
            <th>Package</th>
            <th>License</th>
            <th>Severity</th>
            <th>Category</th>
          </tr>
        </thead>
        <tbody>
          {lic_rows}
        </tbody>
      </table>
    </div>
    <div class="summary muted">Severity summary: {lic_summary}</div>
  </div>

  <script>
    $(function() {{
      $('#componentsTable').DataTable({{
        pageLength: 25,
        order: [[3, 'asc']]
      }});
      $('#vulnTable').DataTable({{
        pageLength: 25,
        order: [[4, 'desc'], [10, 'desc']]
      }});
      $('#licenseTable').DataTable({{
        pageLength: 25,
        order: [[4, 'desc'], [3, 'asc']]
      }});
    }});
  </script>
</body>
</html>
"""

    Path(output).write_text(html_doc, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate an HTML SBOM report.")
    parser.add_argument("--sbom", required=True, help="Path to CycloneDX JSON SBOM file")
    parser.add_argument("--trivy", required=True, help="Path to Trivy JSON scan output")
    parser.add_argument("--output", required=True, help="Path to output HTML file")
    parser.add_argument(
        "--title",
        default="SBOM HTML Report",
        help="Title displayed in the generated HTML report",
    )
    args = parser.parse_args()

    sbom = load_json(args.sbom)
    trivy = load_json(args.trivy)

    components = build_components(sbom)
    depth_map = build_depth_map(sbom)
    vulnerabilities = build_vulnerability_list(trivy)
    licenses = build_license_list(trivy)

    write_html(args.output, components, depth_map, vulnerabilities, licenses, args.title)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()