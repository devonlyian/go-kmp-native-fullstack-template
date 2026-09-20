"""Exercise the real Stop command in disposable Git repositories."""

import json
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


class StopHookChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="codex hook ")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.tools = self.root / "tools"
        self.tools.mkdir()
        for name in ("check-docs.py", "codex-stop.py"):
            shutil.copy(Path(__file__).with_name(name), self.tools / name)
        self.git("init", "-q")
        # Keep fixture infrastructure out of the changed-document selection.
        (self.root / ".git/info/exclude").write_text("tools/\n")

    def git(self, *args):
        return subprocess.run(["git", "-C", str(self.root), *args],
                              check=True, capture_output=True)

    def write_pair(self):
        (self.root / "Guide.md").write_text("# Guide\n", encoding="utf-8")
        (self.root / "Guide.ko.md").write_text("# 안내\n", encoding="utf-8")

    def record(self):
        subprocess.run([sys.executable, str(self.tools / "check-docs.py"),
                        "--record", "Guide.md"], cwd=self.root,
                       check=True, capture_output=True)

    def hook(self, event=None, raw=None):
        if raw is None:
            raw = json.dumps(event or {"hook_event_name": "Stop", "stop_hook_active": False})
        result = subprocess.run([sys.executable, str(self.tools / "codex-stop.py")],
                                input=raw, cwd=self.tools, text=True,
                                capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def test_code_only_is_quiet_and_does_not_run_checker(self):
        (self.root / "code.py").write_text("pass\n")
        (self.tools / "check-docs.py").write_text("raise RuntimeError('must not run')\n")
        self.assertEqual(self.hook(), {})

    def test_unborn_repo_untracked_translation_gap_blocks_without_writes(self):
        (self.root / "Guide.md").write_text("# Guide\n")
        result = self.hook()
        self.assertEqual(result["decision"], "block")
        self.assertIn("Missing document: Guide.ko.md", result["reason"])
        self.assertFalse((self.root / "docs/.translations.json").exists())

    def test_reviewed_staged_docs_pass_from_nested_directory(self):
        self.write_pair()
        self.record()
        self.git("add", "Guide.md", "Guide.ko.md", "docs/.translations.json")
        self.assertEqual(self.hook(), {})

    def test_unstaged_change_preserves_manifest(self):
        self.write_pair()
        self.record()
        self.git("add", ".")
        manifest = self.root / "docs/.translations.json"
        before = manifest.read_bytes()
        (self.root / "Guide.md").write_text("# Changed\n")
        self.assertIn("Stale review", self.hook()["reason"])
        self.assertEqual(manifest.read_bytes(), before)

    def test_deleted_translation_and_renamed_pair_fail(self):
        self.write_pair()
        self.record()
        self.git("add", ".")
        (self.root / "Guide.ko.md").unlink()
        self.assertIn("Missing document", self.hook()["reason"])
        self.write_pair()
        self.git("mv", "Guide.md", "New.md")
        self.git("mv", "Guide.ko.md", "New.ko.md")
        self.assertIn("Unreviewed pair: New.md", self.hook()["reason"])

    def test_stop_continuation_never_blocks_again(self):
        (self.root / "Guide.md").write_text("# Guide\n")
        result = self.hook({"hook_event_name": "Stop", "stop_hook_active": True})
        self.assertNotIn("decision", result)
        self.assertIn("continuation loop", result["systemMessage"])

    def test_invalid_or_other_event_is_safe(self):
        self.assertIn("systemMessage", self.hook(raw="not JSON"))
        self.assertEqual(self.hook(raw="[]"), {})
        self.assertEqual(self.hook({"hook_event_name": "SubagentStop"}), {})

    def test_checker_error_reports_failure(self):
        self.write_pair()
        (self.tools / "check-docs.py").write_text("raise RuntimeError('checker failed')\n")
        self.assertEqual(self.hook()["decision"], "block")

    def test_git_failure_or_timeout_requests_one_continuation(self):
        spec = importlib.util.spec_from_file_location("codex_stop", self.tools / "codex-stop.py")
        hook = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(hook)
        for error in (FileNotFoundError(), subprocess.TimeoutExpired("git", 3),
                      subprocess.CalledProcessError(1, "git")):
            with self.subTest(error=type(error).__name__), patch.object(hook.subprocess, "run", side_effect=error):
                result = hook.inspect({"hook_event_name": "Stop"}, self.root)
                self.assertEqual(result["decision"], "block")
                retry = hook.inspect({"hook_event_name": "Stop", "stop_hook_active": True}, self.root)
                self.assertNotIn("decision", retry)


if __name__ == "__main__":
    unittest.main()
