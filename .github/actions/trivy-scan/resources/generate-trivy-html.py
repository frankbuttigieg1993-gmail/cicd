#!/usr/bin/env python3
"""Generate a dependency-aware Trivy HTML report for Gradle/Java projects.

Inputs:
  * Trivy JSON report (`trivy fs --format json`)
  * CycloneDX JSON SBOM containing `components` and `dependencies`

The CycloneDX root component's immediate `dependsOn` entries are Direct.
Any other reachable components are Transitive. Trivy remains the source of
vulnerability data; CycloneDX is the source of dependency relationship data.
"""

import argparse
import html
import json
import re
import sys
from collections import defaultdict, deque
from pathlib import Path
from urllib.parse import unquote

SEVERITY_ORDER = {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3, "UNKNOWN": 4}


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def find_sbom(search_root: Path) -> Path:
    candidates = []
    for pattern in ("**/bom.json", "**/*cyclonedx*.json"):
        candidates.extend(search_root.glob(pattern))
    seen = set()
    for path in candidates:
        path = path.resolve()
        if path in seen or "trivy" in path.name.lower():
            continue
        seen.add(path)
        try:
            data = load_json(path)
        except Exception:
            continue
        if isinstance(data, dict) and data.get("bomFormat") == "CycloneDX" and data.get("components") is not None:
            return path
    raise FileNotFoundError(f"No CycloneDX JSON SBOM found below {search_root}")


def purl_to_ga(purl: str):
    # pkg:maven/org.springframework/spring-core@6.1.0?... -> (group, artifact)
    if not purl or not purl.startswith("pkg:maven/"):
        return None
    body = purl[len("pkg:maven/"):].split("?", 1)[0].split("#", 1)[0]
    body = body.split("@", 1)[0]
    parts = body.split("/")
    if len(parts) < 2:
        return None
    return unquote("/".join(parts[:-1])), unquote(parts[-1])


def component_ga(component):
    group = component.get("group") or ""
    name = component.get("name") or ""
    if group and name:
        return group, name
    return purl_to_ga(component.get("purl", ""))


def normalize_ref(ref: str):
    return ref or ""


def dependency_relationships(sbom):
    components = sbom.get("components") or []
    by_ref = {normalize_ref(c.get("bom-ref")): c for c in components if c.get("bom-ref")}
    graph = {normalize_ref(d.get("ref")): list(d.get("dependsOn") or []) for d in (sbom.get("dependencies") or [])}

    root = (sbom.get("metadata") or {}).get("component") or {}
    root_ref = normalize_ref(root.get("bom-ref"))

    direct_refs = set(graph.get(root_ref, [])) if root_ref else set()

    # Some generators represent a project with a dependency node not identical to
    # metadata.component. Fall back to the dependency node whose children cover the
    # largest number of known components.
    if not direct_refs and graph:
        known = set(by_ref)
        root_candidates = [(len(set(children) & known), ref, children) for ref, children in graph.items()]
        root_candidates.sort(reverse=True)
        if root_candidates and root_candidates[0][0] > 0:
            direct_refs = set(root_candidates[0][2])

    reachable = set()
    q = deque(direct_refs)
    while q:
        ref = q.popleft()
        if ref in reachable:
            continue
        reachable.add(ref)
        q.extend(graph.get(ref, []))

    relation_by_ga = {}
    version_by_ga = defaultdict(set)
    for ref, comp in by_ref.items():
        ga = component_ga(comp)
        if not ga:
            continue
        if comp.get("version"):
            version_by_ga[ga].add(str(comp["version"]))
        if ref in direct_refs:
            relation_by_ga[ga] = "Direct"
        elif ref in reachable:
            relation_by_ga.setdefault(ga, "Transitive")
        else:
            relation_by_ga.setdefault(ga, "Unknown")
    return relation_by_ga, version_by_ga


def split_java_package(pkg_name: str):
    # Trivy commonly reports Maven packages as group:artifact. Avoid splitting
    # ecosystems where ':' has another meaning unless it resembles a Maven GA.
    if pkg_name and pkg_name.count(":") >= 1:
        group, artifact = pkg_name.rsplit(":", 1)
        if "." in group and artifact:
            return group, artifact
    return "", pkg_name or ""


def infer_ga(vuln, relation_by_ga):
    pkg = vuln.get("PkgName") or ""
    group, artifact = split_java_package(pkg)
    if (group, artifact) in relation_by_ga:
        return group, artifact

    # Match artifact-only names only when unambiguous in the SBOM.
    matches = [ga for ga in relation_by_ga if ga[1] == pkg or ga[1] == artifact]
    if len(matches) == 1:
        return matches[0]
    return group, artifact


def severity(v):
    return str(v.get("Severity") or (v.get("Vulnerability") or {}).get("Severity") or "UNKNOWN").upper()


def references(v):
    refs = v.get("References") or (v.get("Vulnerability") or {}).get("References") or []
    return [str(x) for x in refs]


def esc(value):
    return html.escape("" if value is None else str(value), quote=True)


def render(trivy, sbom, sbom_path: Path):
    relation_by_ga, _ = dependency_relationships(sbom)
    rows = []
    licenses = []

    for result in trivy.get("Results") or []:
        target = result.get("Target") or ""
        rtype = result.get("Type") or ""
        for v in result.get("Vulnerabilities") or []:
            group, package = infer_ga(v, relation_by_ga)
            relation = relation_by_ga.get((group, package), "Unknown")
            rows.append({
                "group": group or "(non-Maven / unknown)",
                "package": package or v.get("PkgName") or "Unknown",
                "relationship": relation,
                "id": v.get("VulnerabilityID") or "",
                "severity": severity(v),
                "installed": v.get("InstalledVersion") or "",
                "fixed": v.get("FixedVersion") or "",
                "title": v.get("Title") or "",
                "target": target,
                "type": rtype,
                "refs": references(v),
            })
        for lic in result.get("Licenses") or []:
            licenses.append((target, lic))

    rows.sort(key=lambda r: (r["group"].lower(), r["package"].lower(), SEVERITY_ORDER.get(r["severity"], 99), r["id"]))
    grouped = defaultdict(lambda: defaultdict(list))
    for row in rows:
        grouped[row["group"]][row["package"]].append(row)

    counts = defaultdict(int)
    for r in rows:
        counts[r["severity"]] += 1

    css = r"""
:root{font-family:Inter,Arial,Helvetica,sans-serif;color:#172033;background:#f5f7fb}*{box-sizing:border-box}
body{margin:0}.wrap{max-width:1500px;margin:0 auto;padding:28px}.hero{background:#fff;border:1px solid #dfe5ef;border-radius:14px;padding:24px;margin-bottom:18px}.hero h1{margin:0 0 8px;font-size:28px}.muted{color:#68758a}.summary{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}.pill,.relationship{display:inline-block;border-radius:999px;padding:5px 10px;font-size:12px;font-weight:700}.pill{background:#edf1f7}.critical{background:#b42318;color:#fff}.high{background:#e85d04;color:#fff}.medium{background:#f4b400;color:#222}.low{background:#2e7d32;color:#fff}.unknown{background:#667085;color:#fff}.direct{background:#d1fadf;color:#05603a}.transitive{background:#e0e7ff;color:#3730a3}.rel-unknown{background:#eaecf0;color:#344054}
.group{background:#fff;border:1px solid #dfe5ef;border-radius:14px;margin:16px 0;overflow:hidden}.group-title{padding:16px 20px;background:#eef3fa;font-size:20px;font-weight:800}.package{border-top:1px solid #e5e9f0}.package-title{padding:12px 20px;font-weight:700;display:flex;align-items:center;gap:10px}.table-wrap{overflow-x:auto}table{width:100%;border-collapse:collapse;background:#fff}th,td{padding:10px 12px;border-top:1px solid #e7ebf1;text-align:left;vertical-align:top}th{font-size:12px;text-transform:uppercase;letter-spacing:.04em;color:#58667a;background:#fafbfc}td{font-size:13px}.sev{font-weight:800}.refs a{display:block;max-width:440px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.empty{padding:28px;text-align:center;background:#fff;border:1px solid #dfe5ef;border-radius:14px}.meta{font-size:12px;margin-top:6px}.section-title{margin-top:28px}
"""

    out = ["<!doctype html><html><head><meta charset='utf-8'>", f"<style>{css}</style>", "<title>Trivy dependency report</title></head><body><div class='wrap'>"]
    out.append("<section class='hero'><h1>Trivy Dependency &amp; Vulnerability Report</h1>")
    out.append(f"<div class='muted'>Dependency relationship source: CycloneDX SBOM <code>{esc(sbom_path)}</code></div>")
    out.append("<div class='summary'>")
    out.append(f"<span class='pill'>Vulnerabilities: {len(rows)}</span>")
    for sev in ("CRITICAL", "HIGH", "MEDIUM", "LOW", "UNKNOWN"):
        if counts[sev]: out.append(f"<span class='pill {sev.lower()}'>{sev}: {counts[sev]}</span>")
    out.append("</div></section>")

    if not rows:
        out.append("<div class='empty'>No vulnerabilities found.</div>")
    else:
        for group, packages in grouped.items():
            out.append(f"<section class='group'><div class='group-title'>{esc(group)}</div>")
            for package, prows in packages.items():
                rels = {r['relationship'] for r in prows}
                rel = "Direct" if "Direct" in rels else ("Transitive" if "Transitive" in rels else "Unknown")
                rel_class = "direct" if rel == "Direct" else ("transitive" if rel == "Transitive" else "rel-unknown")
                out.append(f"<div class='package'><div class='package-title'>{esc(package)} <span class='relationship {rel_class}'>{esc(rel)}</span></div><div class='table-wrap'>")
                out.append("<table><thead><tr><th>Vulnerability</th><th>Severity</th><th>Installed</th><th>Fixed</th><th>Target / Type</th><th>Title</th><th>Links</th></tr></thead><tbody>")
                for r in prows:
                    refs = "".join(f"<a href='{esc(u)}'>{esc(u)}</a>" for u in r["refs"][:5])
                    out.append("<tr>" +
                        f"<td><strong>{esc(r['id'])}</strong></td>" +
                        f"<td><span class='pill {esc(r['severity'].lower())}'>{esc(r['severity'])}</span></td>" +
                        f"<td>{esc(r['installed'])}</td><td>{esc(r['fixed'])}</td>" +
                        f"<td>{esc(r['target'])}<div class='meta muted'>{esc(r['type'])}</div></td>" +
                        f"<td>{esc(r['title'])}</td><td class='refs'>{refs}</td></tr>")
                out.append("</tbody></table></div></div>")
            out.append("</section>")

    out.append("<h2 class='section-title'>Relationship classification</h2><section class='hero'><div class='muted'>")
    out.append("<strong>Direct</strong> = component referenced immediately by the CycloneDX root component. ")
    out.append("<strong>Transitive</strong> = component reachable below a direct component. ")
    out.append("<strong>Unknown</strong> = Trivy package could not be matched unambiguously to the CycloneDX dependency graph.")
    out.append("</div></section></div></body></html>")
    return "".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--trivy", required=True, type=Path)
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("--sbom", type=Path)
    group.add_argument("--sbom-search-root", type=Path)
    ap.add_argument("--output", required=True, type=Path)
    args = ap.parse_args()

    sbom_path = args.sbom if args.sbom else find_sbom(args.sbom_search_root)
    trivy = load_json(args.trivy)
    sbom = load_json(sbom_path)
    if sbom.get("bomFormat") != "CycloneDX":
        raise ValueError(f"{sbom_path} is not a CycloneDX JSON SBOM")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(render(trivy, sbom, sbom_path), encoding="utf-8")
    print(f"Generated {args.output} using CycloneDX SBOM {sbom_path}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(1)
