#!/usr/bin/env python3
import json
import os
import urllib.request
from pathlib import Path

token = os.environ["GH_TOKEN"]
repository = os.environ["REPOSITORY"]
pr_number = os.environ["PR_NUMBER"]
api_root = f"https://api.github.com/repos/{repository}"

headers = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {token}",
    "X-GitHub-Api-Version": "2022-11-28",
    "User-Agent": "semgrep-composite-action",
}

def request(url, method="GET", body=None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as response:
        payload = response.read()
        return response.status, json.loads(payload) if payload else None

comments = []
page = 1
while True:
    url = f"{api_root}/issues/{pr_number}/comments?per_page=100&page={page}"
    _, page_data = request(url)
    comments.extend(page_data or [])
    if not page_data or len(page_data) < 100:
        break
    page += 1

marker = "<!-- semgrep-security-report -->"
existing = next((c for c in comments if marker in c.get("body", "")), None)
body = Path("semgrep-comment.md").read_text(encoding="utf-8")

if existing:
    url = f"{api_root}/issues/comments/{existing['id']}"
    request(url, method="PATCH", body={"body": body})
    print(f"Updated Semgrep PR comment {existing['id']}.")
else:
    url = f"{api_root}/issues/{pr_number}/comments"
    _, created = request(url, method="POST", body={"body": body})
    print(f"Created Semgrep PR comment {created['id']}.")