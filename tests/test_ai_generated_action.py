import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ACTION_RESOURCES = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "actions"
    / "ai-generated"
    / "resources"
)


class GradleActionTests(unittest.TestCase):
    def test_gradle_tasks_are_passed_as_arguments_without_shell_evaluation(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            args_file = project / "args.txt"
            wrapper = project / "gradlew"
            wrapper.write_text(
                "#!/usr/bin/env bash\n"
                "printf '%s\\n' \"$@\" > \"$WRAPPER_ARGS_FILE\"\n"
                "exit \"${WRAPPER_EXIT_CODE:-0}\"\n",
                encoding="utf-8",
            )
            subprocess.run(["bash", "-c", "chmod +x ./gradlew"], cwd=project, check=True)
            result = subprocess.run(
                ["bash", str(ACTION_RESOURCES / "run-gradle.sh")],
                cwd=project,
                env={**os.environ, "GRADLE_TASKS": "clean build; touch injected-file", "WRAPPER_ARGS_FILE": str(args_file)},
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(
                args_file.read_text(encoding="utf-8").splitlines(),
                ["--no-daemon", "--stacktrace", "clean", "build;", "touch", "injected-file"],
            )
            self.assertFalse((project / "injected-file").exists())

    def test_gradle_failure_is_propagated(self):
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory)
            wrapper = project / "gradlew"
            wrapper.write_text("#!/usr/bin/env bash\nexit 9\n", encoding="utf-8")
            subprocess.run(["bash", "-c", "chmod +x ./gradlew"], cwd=project, check=True)
            result = subprocess.run(
                ["bash", str(ACTION_RESOURCES / "run-gradle.sh")],
                cwd=project,
                env={**os.environ, "GRADLE_TASKS": "clean build"},
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 9)

    def test_summary_counts_junit_results_and_reports_failure(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            results = root / "build" / "test-results" / "test"
            results.mkdir(parents=True)
            (results / "TEST-example.xml").write_text(
                '<testsuite tests="4" failures="1" errors="0" skipped="1"></testsuite>',
                encoding="utf-8",
            )
            summary = root / "summary.md"
            output = root / "output.txt"
            result = subprocess.run(
                ["python3", str(ACTION_RESOURCES / "write-step-summary.py")],
                cwd=root,
                env={
                    **os.environ,
                    "GITHUB_WORKSPACE": str(root),
                    "GITHUB_STEP_SUMMARY": str(summary),
                    "GITHUB_OUTPUT": str(output),
                    "JAVA_VERSION": "21",
                    "GRADLE_TASKS": "clean build",
                    "GRADLE_STATUS": "failure",
                    "SETUP_STATUS": "success",
                    "UPLOAD_TEST_RESULTS": "true",
                    "ARTIFACT_NAME": "test-results",
                    "ARTIFACT_RETENTION_DAYS": "7",
                    "ARTIFACT_STATUS": "success",
                    "ARTIFACT_URL": "https://github.com/example/repo/actions/runs/123",
                    "WORKFLOW_RUN_URL": "https://github.com/example/repo/actions/runs/123",
                },
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            rendered_summary = summary.read_text(encoding="utf-8")
            outputs = output.read_text(encoding="utf-8")

        self.assertIn("21 (Temurin)", rendered_summary)
        self.assertIn("1 failed", rendered_summary)
        self.assertIn("JUnit reports contain 1 failure(s)", rendered_summary)
        self.assertIn("https://github.com/example/repo/actions/runs/123", rendered_summary)
        self.assertIn("[workflow run logs]", rendered_summary)
        self.assertIn("unit-test-status=failed", outputs)
        self.assertIn("test-count=4", outputs)

    def test_summary_handles_missing_junit_results_without_success_claim(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            summary = root / "summary.md"
            output = root / "output.txt"
            result = subprocess.run(
                ["python3", str(ACTION_RESOURCES / "write-step-summary.py")],
                cwd=root,
                env={
                    **os.environ,
                    "GITHUB_WORKSPACE": str(root),
                    "GITHUB_STEP_SUMMARY": str(summary),
                    "GITHUB_OUTPUT": str(output),
                    "GRADLE_STATUS": "success",
                    "SETUP_STATUS": "success",
                    "UPLOAD_TEST_RESULTS": "true",
                    "ARTIFACT_STATUS": "success",
                },
                capture_output=True,
                text=True,
                check=False,
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            rendered_summary = summary.read_text(encoding="utf-8")
            outputs = output.read_text(encoding="utf-8")

        self.assertIn("No JUnit XML results were found", rendered_summary)
        self.assertIn("No JUnit XML files found", rendered_summary)
        self.assertIn("unit-test-status=not-reported", outputs)


if __name__ == "__main__":
    unittest.main()
