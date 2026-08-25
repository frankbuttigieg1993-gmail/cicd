#!/usr/bin/env python3
import argparse
import json
import urllib.request

MARKER = "<!-- semgrep-security-report -->"

def request_json(url, token, method="GET", body=None):
    data = None if body is None else json.dumps(body).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
        },
    )
    with urllib.request.urlopen(request) as response:
        raw = response.read()
        return json.loads(raw) if raw else None

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr", required=True)
    parser.add_argument("--body-file", required=True)
    parser.add_argument("--token", required=True)
    args = parser.parse_args()

    with open(args.body_file, encoding="utf-8") as fh:
        body = fh.read()

    if MARKER not in body:
        body = f"{MARKER}\n{body}"

    comments_url = f"https://api.github.com/repos/{args.repo}/issues/{args.pr}/comments"
    comments = request_json(f"{comments_url}?per_page=100", args.token) or []
    existing = next((c for c in comments if MARKER in c.get("body", "")), None)

    if existing:
        print(f"Updating existing Semgrep PR comment {existing['id']}.")
        request_json(
            f"https://api.github.com/repos/{args.repo}/issues/comments/{existing['id']}",
            args.token,
            method="PATCH",
            body={"body": body},
        )
    else:
        print("Creating Semgrep PR comment.")
        request_json(comments_url, args.token, method="POST", body={"body": body})

if __name__ == "__main__":
    main()
