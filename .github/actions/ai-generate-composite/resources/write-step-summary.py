#!/usr/bin/env python3
import os
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


def collect_junit_results(results_dir: Path) -> tuple[list[Path], int, int, int, int, list[str]]:
    reports = sorted(results_dir.rglob("*.xml")) if results_dir.is_dir() else []
    tests = failures = errors = skipped = 0
    parse_errors = []

    for report in reports:
        try:
            root = ET.parse(report).getroot()
        except (OSError, ET.ParseError) as exc:
            parse_errors.append(f"{report.as_posix()}: {exc}")
            continue

        test_cases = root.findall(".//testcase")
        if test_cases:
            tests += len(test_cases)
            for case in test_cases:
                failures += case.find("failure") is not None
                errors += case.find("error") is not None
                skipped += case.find("skipped") is not None
            continue

        suites = [root] if root.tag == "testsuite" else root.findall(".//testsuite")
        for suite in suites:
            tests += int(suite.attrib.get("tests", "0") or "0")
            failures += int(suite.attrib.get("failures", "0") or "0")
            errors += int(suite.attrib.get("errors", "0") or "0")
            skipped += int(suite.attrib.get("skipped", "0") or "0")

    return reports, tests, failures, errors, skipped, parse_errors


def markdown_cell(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def main() -> int:
    summary_file = os.environ.get("GITHUB_STEP_SUMMARY")
    env_file = os.environ.get("GITHUB_ENV")
    if not summary_file or not env_file:
        print("::error::GITHUB_STEP_SUMMARY and GITHUB_ENV must be set.")
        return 1

    reports, tests, failures, errors, skipped, parse_errors = collect_junit_results(
        Path("build/test-results")
    )
    with Path(env_file).open("a", encoding="utf-8") as environment:
        environment.write(f"JUNIT_REPORT_STATUS={'failed' if parse_errors else 'success'}\n")

    artifact_status = os.environ.get("ARTIFACT_STATUS", "")
    artifact_url = os.environ.get("ARTIFACT_URL", "")
    if not reports:
        artifact_result = "No JUnit XML files found; upload step is configured to warn when missing."
    elif artifact_status != "success":
        artifact_result = f"Upload failed (step status: {markdown_cell(artifact_status or 'unknown')})."
    elif artifact_url.startswith("https://") and not any(char in artifact_url for char in "\r\n|<>"):
        artifact_result = f"[Download test results]({artifact_url}) (retention: 1 day)"
    else:
        artifact_result = f"Uploaded as `gradle-test-results` (retention: 1 day)"

    java_status = os.environ.get("JAVA_STATUS", "") or "not run"
    build_status = os.environ.get("BUILD_STATUS", "") or "not run"
    test_status = os.environ.get("TEST_STATUS", "") or "not run"
    file_list_status = os.environ.get("FILE_LIST_STATUS", "") or "not run"
    workflow_url = os.environ.get("WORKFLOW_RUN_URL", "")

    lines = [
        "## Gradle Build, Unit Tests, and File Listing",
        "",
        "| Check | Result |",
        "| --- | --- |",
        "| Java version | 21 (Temurin) |",
        f"| Java setup | {markdown_cell(java_status)} |",
        "| Gradle build command | `./gradlew clean build -x test --info --stacktrace` |",
        f"| Gradle build status | {markdown_cell(build_status)} |",
        "| Unit test command | `./gradlew test --info --stacktrace` |",
        f"| Unit test status | {markdown_cell(test_status)} |",
        f"| JUnit results | {tests} total; {max(tests - failures - errors - skipped, 0)} passed; {failures} failed; {errors} errors; {skipped} skipped; {len(reports)} XML file(s) |",
        f"| Workspace file listing | {markdown_cell(file_list_status)} |",
        f"| Test-result artifact | {artifact_result} |",
        "",
    ]

    if parse_errors:
        lines.extend(["JUnit XML parsing errors:", *[f"- `{markdown_cell(error)}`" for error in parse_errors], ""])
    if failures or errors:
        lines.extend([f"JUnit reports contain {failures} failure(s) and {errors} error(s). Inspect the Gradle unit-test step logs.", ""])
    if build_status != "success" or test_status != "success":
        if workflow_url.startswith("https://") and not any(char in workflow_url for char in "\r\n|<>"):
            lines.extend([f"Gradle failure details are available in the [workflow run logs]({workflow_url}).", ""])
        else:
            lines.extend(["Gradle failure details are available in the corresponding step logs.", ""])
    if not reports:
        lines.extend(["No JUnit XML files were available for the test-result summary.", ""])

    with Path(summary_file).open("a", encoding="utf-8") as summary:
        summary.write("\n".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main())
