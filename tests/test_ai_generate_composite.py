from pathlib import Path
import re
import subprocess
import tempfile
import unittest


ACTION_FILE = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "actions"
    / "ai-generate-composite"
    / "action.yml"
)
ACTION_TEXT = ACTION_FILE.read_text(encoding="utf-8")
LIST_COMMAND = "find . -maxdepth 1 -type f -print | LC_ALL=C sort"


class CompositeActionTests(unittest.TestCase):
    def test_action_contains_only_a_single_file_listing_step(self):
        run_commands = re.findall(r"^\s+run:\s*(.+)$", ACTION_TEXT, re.MULTILINE)

        self.assertIn("name: ai-generate-composite", ACTION_TEXT)
        self.assertIn("using: composite", ACTION_TEXT)
        self.assertEqual(run_commands, [LIST_COMMAND])
        self.assertEqual(ACTION_TEXT.count("      uses:"), 0)

    def test_listing_command_outputs_only_top_level_files_in_order(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "z-last.txt").write_text("", encoding="utf-8")
            (root / "a-first.txt").write_text("", encoding="utf-8")
            nested = root / "nested"
            nested.mkdir()
            (nested / "nested-file.txt").write_text("", encoding="utf-8")

            result = subprocess.run(
                ["bash", "-c", LIST_COMMAND],
                cwd=root,
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ["./a-first.txt", "./z-last.txt"])


if __name__ == "__main__":
    unittest.main()
