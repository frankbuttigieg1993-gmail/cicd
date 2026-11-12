import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SUMMARY_SCRIPT = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "actions"
    / "ai-generate-composite"
    / "resources"
    / "write-step-summary.py"
)


class CompositeSummaryTests(unittest.TestCase):
    def run_summary(self, root, extra_env=None):
        summary = root / "summary.md"
        env_file = root / "env.txt"
        result = subprocess.run(
            ["python", str(SUMMARY_SCRIPT)],
            cwd=root,
            env={
                **os.environ,
                "GITHUB_STEP_SUMMARY": str(summary),
                "GITHUB_ENV": str(env_file),
                "JAVA_STATUS": "success",
                "BUILD_STATUS": "success",
                "TEST_STATUS": "success",
                "FILE_LIST_STATUS": "success",
                "ARTIFACT_STATUS": "success",
                "ARTIFACT_URL": "https://github.com/example/repo/actions/runs/42/artifacts/3",
                "WORKFLOW_RUN_URL": "https://github.com/example/repo/actions/runs/42",
                **(extra_env or {}),
            },
            capture_output=True,
            text=True,
            check=False,
        )
        return result, summary.read_text(encoding="utf-8"), env_file.read_text(encoding="utf-8")

    def test_summary_counts_junit_and_links_uploaded_artifact(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result_file = root / "build" / "test-results" / "test" / "TEST-example.xml"
            result_file.parent.mkdir(parents=True)
            result_file.write_text(
                '<testsuite><testcase/><testcase><failure/></testcase><testcase><skipped/></testcase></testsuite>',
                encoding="utf-8",
            )

            result, summary, env_file = self.run_summary(
                root, {"TEST_STATUS": "failure"}
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("3 total; 1 passed; 1 failed; 0 errors; 1 skipped", summary)
        self.assertIn("| Unit test status | failure |", summary)
        self.assertIn("Download test results", summary)
        self.assertIn("Gradle failure details", summary)
        self.assertIn("JUNIT_REPORT_STATUS=success", env_file)

    def test_missing_junit_results_are_reported_without_claiming_results_exist(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result, summary, env_file = self.run_summary(root)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("No JUnit XML files found", summary)
        self.assertIn("No JUnit XML files were available", summary)
        self.assertIn("JUNIT_REPORT_STATUS=success", env_file)

    def test_invalid_junit_xml_is_reported_for_final_enforcement(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            result_file = root / "build" / "test-results" / "test" / "TEST-invalid.xml"
            result_file.parent.mkdir(parents=True)
            result_file.write_text("<testsuite>", encoding="utf-8")

            result, summary, env_file = self.run_summary(root)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("JUnit XML parsing errors", summary)
        self.assertIn("JUNIT_REPORT_STATUS=failed", env_file)


if __name__ == "__main__":
    unittest.main()
