import os
from pathlib import Path
import subprocess
import tempfile
import unittest


ACTION_DIR = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "actions"
    / "java"
    / "github-actions-ai-generated"
)


class GradleSonarActionTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.project_dir = Path(self.temp_dir.name)
        self.wrapper_args = self.project_dir / "wrapper-args.txt"
        wrapper = self.project_dir / "gradlew"
        wrapper.write_text(
            "#!/usr/bin/env bash\n"
            "printf '%s\\n' \"$@\" > \"$WRAPPER_ARGS_FILE\"\n"
            "exit \"${WRAPPER_EXIT_CODE:-0}\"\n",
            encoding="utf-8",
        )
        subprocess.run(["bash", "-c", "chmod +x ./gradlew"], cwd=self.project_dir, check=True)

    def tearDown(self):
        self.temp_dir.cleanup()

    def run_script(self, script_name, env):
        return subprocess.run(
            ["bash", str(ACTION_DIR / "resources" / script_name)],
            cwd=self.project_dir,
            env={**os.environ, "WRAPPER_ARGS_FILE": str(self.wrapper_args), **env},
            capture_output=True,
            text=True,
            check=False,
        )

    def test_build_tasks_are_passed_as_arguments_without_shell_evaluation(self):
        result = self.run_script(
            "run-gradle-tasks.sh",
            {"GRADLE_TASKS": "assemble; touch injected-file"},
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            self.wrapper_args.read_text(encoding="utf-8").splitlines(),
            ["--no-daemon", "--stacktrace", "assemble;", "touch", "injected-file"],
        )
        self.assertFalse((self.project_dir / "injected-file").exists())

    def test_build_failure_is_propagated(self):
        result = self.run_script(
            "run-gradle-tasks.sh",
            {"GRADLE_TASKS": "build", "WRAPPER_EXIT_CODE": "7"},
        )

        self.assertEqual(result.returncode, 7)

    def test_sonar_waits_for_quality_gate_and_supports_pull_requests(self):
        result = self.run_script(
            "run-sonar-analysis.sh",
            {
                "SONAR_TOKEN": "do-not-print-this",
                "SONAR_HOST_URL": "https://sonar.example.test",
                "SONAR_QUALITY_GATE_TIMEOUT": "120",
                "SONAR_PROJECT_KEY": "example-project",
                "SONAR_PULL_REQUEST_KEY": "42",
                "SONAR_PULL_REQUEST_BRANCH": "feature/example",
                "SONAR_PULL_REQUEST_BASE": "main",
            },
        )

        args = self.wrapper_args.read_text(encoding="utf-8").splitlines()
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("-Dsonar.qualitygate.wait=true", args)
        self.assertIn("-Dsonar.qualitygate.timeout=120", args)
        self.assertIn("-Dsonar.projectKey=example-project", args)
        self.assertIn("-Dsonar.pullrequest.key=42", args)
        self.assertIn("-Dsonar.pullrequest.branch=feature/example", args)
        self.assertIn("-Dsonar.pullrequest.base=main", args)
        self.assertNotIn("do-not-print-this", result.stdout + result.stderr)

    def test_partial_pull_request_configuration_is_rejected(self):
        result = self.run_script(
            "run-sonar-analysis.sh",
            {
                "SONAR_TOKEN": "token",
                "SONAR_HOST_URL": "https://sonar.example.test",
                "SONAR_QUALITY_GATE_TIMEOUT": "300",
                "SONAR_PULL_REQUEST_KEY": "42",
            },
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("Set all three SonarQube pull-request inputs", result.stdout)
        self.assertFalse(self.wrapper_args.exists())

    def test_sonar_failure_is_propagated(self):
        result = self.run_script(
            "run-sonar-analysis.sh",
            {
                "SONAR_TOKEN": "token",
                "SONAR_HOST_URL": "https://sonar.example.test",
                "SONAR_QUALITY_GATE_TIMEOUT": "300",
                "WRAPPER_EXIT_CODE": "9",
            },
        )

        self.assertEqual(result.returncode, 9)

    def test_summary_reports_check_results_and_report_link(self):
        summary = self.project_dir / "summary.md"
        result = self.run_script(
            "write-step-summary.sh",
            {
                "GITHUB_STEP_SUMMARY": str(summary),
                "SETUP_STATUS": "success",
                "BUILD_STATUS": "success",
                "TEST_STATUS": "failure",
                "SONAR_STATUS": "success",
                "QUALITY_GATE_STATUS": "PASSED",
                "REPORT_ARTIFACT_URL": "https://github.com/example/repo/actions/runs/123",
            },
        )

        report = summary.read_text(encoding="utf-8")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Gradle build", report)
        self.assertIn("Unit tests", report)
        self.assertIn("Quality gate", report)
        self.assertIn("PASSED", report)
        self.assertIn("❌ Failed", report)
        self.assertIn("[Download Gradle test and SonarQube reports]", report)
        self.assertIn("https://github.com/example/repo/actions/runs/123", report)


if __name__ == "__main__":
    unittest.main()
