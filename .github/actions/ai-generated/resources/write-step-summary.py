#!/usr/bin/env python3
import os
from pathlib import Path
import sys
import xml.etree.ElementTree as ET


def markdown_cell(value: str) -> str:
    return value.replace("\\", "\\\\").replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def collect_test_results(results_dir: Path) -> tuple[int, int, int, int, int, int]:
    files = sorted(results_dir.rglob("TEST-*.xml")) if results_dir.is_dir() else []
    tests = failures = errors = skipped = parse_errors = 0

    for path in files:
        try:
            root = ET.parse(path).getroot()
        except (OSError, ET.ParseError) as exc:
            print(f"::error::Unable to parse JUnit report {path.name}: {exc}")
            parse_errors += 1
            continue

        suites = list(root.iter("testsuite"))
        for suite in suites:
            tests += int(suite.attrib.get("tests", "0") or "0")
            failures += int(suite.attrib.get("failures", "0") or "0")
            errors += int(suite.attrib.get("errors", "0") or "0")
            skipped += int(suite.attrib.get("skipped", "0") or "0")

    return len(files), tests, failures, errors, skipped, parse_errors


def main() -> int:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not summary_path or not output_path:
        print("::error::GITHUB_STEP_SUMMARY and GITHUB_OUTPUT must be set.")
        return 1

    workspace = Path(os.environ.get("GITHUB_WORKSPACE", "."))
    working_directory = Path(os.environ.get("WORKING_DIRECTORY", "."))
    project_dir = working_directory if working_directory.is_absolute() else workspace / working_directory
    report_dir = project_dir / "build" / "test-results"
    file_count, tests, failures, errors, skipped, parse_errors = collect_test_results(report_dir)

    if parse_errors or failures or errors:
        test_status = "failed"
    elif tests:
        test_status = "passed"
    else:
        test_status = "not-reported"

    artifact_enabled = os.environ.get("UPLOAD_TEST_RESULTS", "true").lower() == "true"
    artifact_status = os.environ.get("ARTIFACT_STATUS", "")
    artifact_url = os.environ.get("ARTIFACT_URL", "")
    workflow_run_url = os.environ.get("WORKFLOW_RUN_URL", "")
    artifact_name = markdown_cell(os.environ.get("ARTIFACT_NAME", "gradle-test-results"))
    retention = markdown_cell(os.environ.get("ARTIFACT_RETENTION_DAYS", "7"))
    if not artifact_enabled:
        artifact_summary = "Not requested"
    elif artifact_status != "success":
        artifact_summary = f"Upload step status: {markdown_cell(artifact_status or 'unknown')}"
    elif file_count == 0:
        artifact_summary = f"No JUnit XML files found; upload configured to warn when missing ({artifact_name})"
    elif artifact_url.startswith("https://") and not any(char in artifact_url for char in "\r\n|<>"):
        artifact_summary = f"[{artifact_name}]({artifact_url}) (retention: {retention} days)"
    else:
        artifact_summary = f"{artifact_name} (retention: {retention} days)"

    gradle_status = os.environ.get("GRADLE_STATUS", "") or "not run"
    setup_status = os.environ.get("SETUP_STATUS", "") or "not run"
    tasks = markdown_cell(os.environ.get("GRADLE_TASKS", "clean build"))
    java_version = markdown_cell(os.environ.get("JAVA_VERSION", "21"))

    lines = [
        "## Gradle build and unit tests",
        "",
        "| Check | Result |",
        "| --- | --- |",
        f"| Java version | {java_version} (Temurin) |",
        f"| Gradle tasks | `{tasks}` |",
        f"| Java setup | {markdown_cell(setup_status)} |",
        f"| Build | {markdown_cell(gradle_status)} |",
        f"| Unit tests | {test_status} |",
        f"| Test results | {tests} total; {max(tests - failures - errors - skipped, 0)} passed; {failures} failed; {errors} errors; {skipped} skipped; {file_count} XML file(s) |",
        f"| Test-result artifact | {artifact_summary} |",
        "",
    ]
    if parse_errors:
        lines.extend(["JUnit XML parsing failed for one or more files. Inspect the Gradle logs and uploaded reports.", ""])
    if failures or errors:
        lines.extend([f"JUnit reports contain {failures} failure(s) and {errors} error(s). Inspect the test output in the Gradle step logs.", ""])
    if gradle_status != "success":
        if workflow_run_url.startswith("https://") and not any(char in workflow_run_url for char in "\r\n|<>"):
            lines.extend([f"Gradle did not complete successfully. See the [workflow run logs]({workflow_run_url}) for failure details.", ""])
        else:
            lines.extend(["Gradle did not complete successfully. See the Gradle step logs for the failure details.", ""])
    if test_status == "not-reported":
        lines.extend(["No JUnit XML results were found. If test-result upload is enabled, the artifact step warns when files are missing.", ""])

    Path(summary_path).write_text("\n".join(lines), encoding="utf-8")
    with Path(output_path).open("a", encoding="utf-8") as output:
        output.write(f"unit-test-status={test_status}\n")
        output.write(f"test-count={tests}\n")
        output.write(f"test-failures={failures}\n")
        output.write(f"test-errors={errors + parse_errors}\n")

    return 0


if __name__ == "__main__":
    sys.exit(main())
