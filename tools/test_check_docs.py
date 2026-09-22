"""Exercise document-sync failures in disposable repositories."""

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location("check_docs", Path(__file__).with_name("check-docs.py"))
check_docs = importlib.util.module_from_spec(spec)
spec.loader.exec_module(check_docs)


class DocumentationChecks(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.write("README.md", "# English\n")
        self.write("README.ko.md", "# 한국어\n")

    def write(self, name, content):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def run_check(self, record=None):
        output = io.StringIO()
        with contextlib.redirect_stdout(output), contextlib.redirect_stderr(output):
            result = check_docs.run(self.root, record)
        return result

    def test_new_pair_needs_explicit_review(self):
        self.assertEqual(self.run_check(), 1)
        self.assertEqual(self.run_check(["README.md"]), 0)
        self.assertEqual(self.run_check(), 0)

    def test_one_sided_edits_rejected_in_both_directions(self):
        for language in ("README.md", "README.ko.md"):
            with self.subTest(language=language):
                self.assertEqual(self.run_check(["README.md"]), 0)
                before = (self.root / check_docs.MANIFEST).read_bytes()
                original = (self.root / language).read_text()
                self.write(language, original + "Updated\n")
                self.assertEqual(self.run_check(), 1)
                self.assertEqual(self.run_check([language]), 1)
                self.assertEqual((self.root / check_docs.MANIFEST).read_bytes(), before)
                self.write(language, original)

    def test_both_edits_require_review_and_accept_korean_path(self):
        self.run_check(["README.md"])
        self.write("README.md", "# Updated English\n")
        self.write("README.ko.md", "# 수정한 한국어\n")
        self.assertEqual(self.run_check(), 1)
        self.assertEqual(self.run_check(["README.ko.md"]), 0)
        self.assertEqual(self.run_check(), 0)

    def test_missing_translation_and_orphan_translation_fail(self):
        self.run_check(["README.md"])
        for missing in ("README.md", "README.ko.md"):
            with self.subTest(missing=missing):
                original = (self.root / missing).read_text()
                (self.root / missing).unlink()
                self.assertEqual(self.run_check(), 1)
                self.assertEqual(self.run_check(["README.md"]), 1)
                self.write(missing, original)

    def test_pair_removal_and_rename(self):
        self.run_check(["README.md"])
        (self.root / "README.md").rename(self.root / "GUIDE.md")
        (self.root / "README.ko.md").rename(self.root / "GUIDE.ko.md")
        self.assertEqual(self.run_check(), 1)
        self.assertEqual(self.run_check(["README.md", "GUIDE.md"]), 0)
        self.assertEqual(self.run_check(), 0)

    def test_rename_does_not_allow_one_sided_content_changes(self):
        self.run_check(["README.md"])
        (self.root / "README.md").rename(self.root / "GUIDE.md")
        (self.root / "README.ko.md").rename(self.root / "GUIDE.ko.md")
        self.write("GUIDE.md", "# Updated English\n")
        self.assertEqual(self.run_check(["README.md", "GUIDE.md"]), 1)
        self.write("GUIDE.ko.md", "# 수정한 한국어\n")
        self.assertEqual(self.run_check(["README.md", "GUIDE.md"]), 0)
        self.assertEqual(self.run_check(), 0)

    def test_empty_translation_cannot_be_recorded(self):
        self.write("README.ko.md", " \n")
        self.assertEqual(self.run_check(["README.md"]), 1)
        self.assertEqual(self.run_check(), 1)

    def test_structure_mode_requires_python(self):
        bin_dir = self.root / "bin"
        bin_dir.mkdir()
        (bin_dir / "dirname").symlink_to(shutil.which("dirname"))
        script = Path(__file__).with_name("verify.sh").resolve()
        result = subprocess.run(
            ["/bin/bash", str(script), "structure"],
            env={"PATH": str(bin_dir)}, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Python 3 is required", result.stderr)

    def test_new_nested_skill_requires_translation_but_build_output_does_not(self):
        self.run_check(["README.md"])
        self.write("app/build/generated.md", "Generated\n")
        self.assertEqual(self.run_check(), 0)
        self.write(".agents/skills/sync-docs/SKILL.md", "# Skill\n")
        self.assertEqual(self.run_check(), 1)
        self.write(".agents/skills/sync-docs/SKILL.ko.md", "# 스킬\n")
        self.assertEqual(self.run_check([".agents/skills/sync-docs/SKILL.md"]), 0)
        self.assertEqual(self.run_check(), 0)

    def test_vendored_skill_docs_do_not_require_translation(self):
        self.run_check(["README.md"])
        self.write(".agents/skills/ui-ux-pro-max/SKILL.md", "# Vendored\n")
        self.write(".agents/skills/ui-ux-pro-max/references/rules.md", "# Ref\n")
        self.assertEqual(self.run_check(), 0)

    def test_partial_record_failure_does_not_write_manifest(self):
        self.run_check(["README.md"])
        before = (self.root / check_docs.MANIFEST).read_bytes()
        self.write("README.md", "Updated\n")
        self.write("new.md", "New\n")
        self.write("new.ko.md", "신규\n")
        self.assertEqual(self.run_check(["new.md", "README.md"]), 1)
        self.assertEqual((self.root / check_docs.MANIFEST).read_bytes(), before)

    def test_invalid_manifest_and_external_paths_fail(self):
        self.run_check(["README.md"])
        self.assertEqual(self.run_check(["../outside.md"]), 1)
        self.write(str(check_docs.MANIFEST), json.dumps({"README.md": {"en": "invalid", "ko": "invalid"}}))
        self.assertEqual(self.run_check(), 1)


if __name__ == "__main__":
    unittest.main()
