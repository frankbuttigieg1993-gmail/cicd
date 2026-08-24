#!/usr/bin/env python3
import re
import sys
from pathlib import Path

path = Path(sys.argv[1])
data = path.read_bytes()

if data.startswith(b"\xef\xbb\xbf"):
    raise SystemExit("ERROR: trivy-secret.yaml contains a UTF-8 BOM")
if b"\x00" in data:
    raise SystemExit("ERROR: trivy-secret.yaml contains NUL bytes")

text = data.decode("utf-8")
if not text.startswith("rules:\n"):
    raise SystemExit("ERROR: trivy-secret.yaml must start with 'rules:'")

rule_count = len(re.findall(r"(?m)^  - id: \S+", text))
regex_count = len(re.findall(r"(?m)^    regex: .+", text))
if rule_count == 0 or regex_count != rule_count:
    raise SystemExit(
        f"ERROR: malformed Trivy secret config: rules={rule_count}, regexes={regex_count}"
    )

print(f"Trivy secret config structural validation passed: {rule_count} rules, UTF-8 without BOM.")
