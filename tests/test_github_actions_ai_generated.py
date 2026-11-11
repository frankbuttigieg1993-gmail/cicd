import os
from pathlib import Path
import subprocess
import tempfile
import unittest


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / ".github"
    / "actions"
    / "java"
    / "github-actions-ai-generated"
    / "resources"
    / "list-files.sh"
)


class ListWorkspaceFilesTests(unittest.TestCase):
    def test_lists_nested_hidden_and_space_containing_files_in_sorted_order(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for name in ("z.txt", ".hidden", "nested/a file.txt", "nested/b.txt"):
                path = root / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("test", encoding="utf-8")

            result = subprocess.run(
                ["bash", str(SCRIPT)],
                cwd=root,
                env=os.environ.copy(),
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(
            result.stdout.splitlines(),
            ["./.hidden", "./nested/a file.txt", "./nested/b.txt", "./z.txt"],
        )

    def test_excludes_git_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / ".git" / "objects").mkdir(parents=True)
            (root / ".git" / "config").write_text("git metadata", encoding="utf-8")
            (root / "README.md").write_text("project file", encoding="utf-8")

            result = subprocess.run(
                ["bash", str(SCRIPT)],
                cwd=root,
                env=os.environ.copy(),
                capture_output=True,
                text=True,
                check=False,
            )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.splitlines(), ["./README.md"])


if __name__ == "__main__":
    unittest.main()
