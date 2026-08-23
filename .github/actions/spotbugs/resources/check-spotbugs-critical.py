#!/usr/bin/env python3
import argparse,json
from pathlib import Path
ap=argparse.ArgumentParser(); ap.add_argument('--sarif',required=True); ap.add_argument('--github-output',required=True); ap.add_argument('--summary',required=True); a=ap.parse_args()
data=json.loads(Path(a.sarif).read_text(encoding='utf-8')); rs=[]
for run in data.get('runs',[]): rs += run.get('results',[]) or []
critical=[r for r in rs if int((r.get('properties') or {}).get('priority',3))==1]
lines=['## SpotBugs / FindSecBugs Security Report','',f'**Total findings:** {len(rs)}  ',f'**Critical findings:** {len(critical)}  ','**Critical policy:** FAIL when SpotBugs priority = 1','']
if critical:
    lines += ['### Critical findings','','| Rule | File | Line | Category |','|---|---|---:|---|']
    for r in critical:
        p=(r.get('locations') or [{}])[0].get('physicalLocation') or {}; al=p.get('artifactLocation') or {}; rg=p.get('region') or {}; pr=r.get('properties') or {}
        lines.append(f"| `{r.get('ruleId','unknown')}` | `{al.get('uri','unknown')}` | {rg.get('startLine','')} | {pr.get('category','')} |")
else: lines.append('No critical SpotBugs / FindSecBugs findings were detected.')
Path(a.summary).write_text('\n'.join(lines)+'\n',encoding='utf-8')
with Path(a.github_output).open('a',encoding='utf-8') as f: f.write(f'critical-count={len(critical)}\n'); f.write(f'finding-count={len(rs)}\n')