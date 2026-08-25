#!/usr/bin/env python3

import argparse
import json
import urllib.error
import urllib.request


MARKER = "<!-- semgrep-appsec-summary -->"


def github_request(url, token, method="GET", body=None):
    data = None

    if body is not None:
        data = json.dumps(body).encode("utf-8")

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
        return json.load(response)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--repo", required=True)
    parser.add_argument("--pr", required=True)
    parser.add_argument("--body-file", required=True)
    parser.add_argument("--token", required=True)

    args = parser.parse_args()

    with open(args.body_file, encoding="utf-8") as file:
        body = file.read()

    if MARKER not in body:
        body = f"{MARKER}\n{body}"

    comments_url = (
        f"https://api.github.com/repos/{args.repo}"
        f"/issues/{args.pr}/comments"
    )

    comments = github_request(
        comments_url,
        args.token,
    )

    existing = next(
        (
            comment
            for comment in comments
            if MARKER in comment.get("body", "")
        ),
        None,
    )

    if existing:
        print(
            f"Updating existing Semgrep PR comment "
            f"{existing['id']}."
        )

        github_request(
            f"https://api.github.com/repos/{args.repo}"
            f"/issues/comments/{existing['id']}",
            args.token,
            method="PATCH",
            body={"body": body},
        )

    else:
        print("Creating Semgrep PR comment.")

        github_request(
            comments_url,
            args.token,
            method="POST",
            body={"body": body},
        )


if __name__ == "__main__":
    main()