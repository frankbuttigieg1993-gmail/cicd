#!/usr/bin/env python3
import argparse, json, xml.etree.ElementTree as ET
from pathlib import Path

def iv(v,d=3):
    try: return int(v)
    except (TypeError,ValueError): return d

ap=argparse.ArgumentParser(); ap.add_argument('--xml',required=True); ap.add_argument('--output',required=True); a=ap.parse_args()
r=ET.parse(a.xml).getroot(); ns_uri=r.tag.split('}',1)[0].strip('{') if r.tag.startswith('{') else ''
ns={'b':ns_uri} if ns_uri else {}
findings=[]
for b in r.findall('.//b:BugInstance',ns):
    src=b.find('b:SourceLine',ns); src=src if src is not None else b.find('b:SourceLine',ns)
    file_name=(src.attrib.get('sourcepath') or src.attrib.get('classname') or '') if src is not None else ''
    start=iv(src.attrib.get('start'),1) if src is not None else 1
    end=iv(src.attrib.get('end'),start) if src is not None else start
    priority=iv(b.attrib.get('priority'),3); rank=iv(b.attrib.get('rank'),20)
    short=b.findtext('b:ShortMessage','',ns)
    longm=b.findtext('b:LongMessage','',ns)
    findings.append({'ruleId':b.attrib.get('type','SPOTBUGS_UNKNOWN'),'level':'error' if priority==1 else ('warning' if priority==2 else 'note'),'message':{'text':short or longm or b.attrib.get('type','')},'locations':[{'physicalLocation':{'artifactLocation':{'uri':file_name.replace('\\','/')},'region':{'startLine':start,'endLine':end}}}], 'properties':{'priority':priority,'rank':rank,'category':b.attrib.get('category','CORRECTNESS')}})
sarif={'$schema':'https://json.schemastore.org/sarif-2.1.0.json','version':'2.1.0','runs':[{'tool':{'driver':{'name':'SpotBugs + FindSecBugs','informationUri':'https://spotbugs.github.io/'}},'results':findings}]}
out=Path(a.output); out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(sarif,indent=2),encoding='utf-8')