"""Exercise the bounded logging contract of tools/verify.sh in disposable repos."""

from pathlib import Path
import re
import shutil
import stat
import subprocess
import tempfile
import unittest

VERIFY = Path(__file__).with_name("verify.sh").resolve()
BASE_TOOLS = ("dirname", "mkdir", "mktemp", "tail")


class VerifyRunner(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "tools").mkdir()
        shutil.copy2(VERIFY, self.root / "tools" / "verify.sh")
        self.bin = self.root / "bin"
        self.bin.mkdir()

    def fake(self, name, body):
        path = self.bin / name
        path.write_text("#!/bin/sh\n" + body, encoding="utf-8")
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

    def run_verify(self, mode="all", extra_env=None, tools=BASE_TOOLS):
        for name in tools:
            (self.bin / name).symlink_to(shutil.which(name))
        env = {"PATH": str(self.bin), "HOME": str(self.root)}
        if extra_env:
            env.update(extra_env)
        return subprocess.run(
            ["/bin/bash", str(self.root / "tools" / "verify.sh"), mode],
            env=env, capture_output=True, text=True,
        )

    def log_dir(self, result):
        match = re.search(r"^Verification logs: (.+)$", result.stdout, re.M)
        self.assertIsNotNone(match, result.stdout + result.stderr)
        return Path(match.group(1).strip())

    def logs(self, result):
        return sorted(self.log_dir(result).glob("check.*"))

    def test_success_hides_body_and_retains_full_log(self):
        self.fake("python3", "i=1; while [ $i -le 100 ]; do echo body-line-$i; i=$((i+1)); done\n")
        result = self.run_verify("structure")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("PASS", result.stdout)
        self.assertNotIn("body-line-1", result.stdout)
        files = self.logs(result)
        self.assertEqual(len(files), 3)
        content = files[0].read_text()
        self.assertIn("body-line-1\n", content)
        self.assertIn("body-line-100", content)

    def test_failure_reports_exact_status_and_bounded_lines(self):
        body = (
            "i=1; while [ $i -le 40 ]; do echo out-line-$i; i=$((i+1)); done\n"
            "i=1; while [ $i -le 40 ]; do echo err-line-$i >&2; i=$((i+1)); done\n"
            "exit 42\n"
        )
        self.fake("python3", body)
        result = self.run_verify("structure")
        self.assertEqual(result.returncode, 42)
        self.assertIn("FAIL (exit 42). Log:", result.stderr)
        self.assertIn("err-line-40", result.stderr)
        self.assertNotIn("err-line-20", result.stderr)
        self.assertNotIn("out-line-40", result.stderr)
        self.assertEqual(len(re.findall(r"^err-line-\d+$", result.stderr, re.M)), 20)
        files = self.logs(result)
        self.assertEqual(len(files), 1)
        content = files[0].read_text()
        self.assertIn("out-line-1", content)
        self.assertIn("err-line-40", content)

    def test_failure_snippet_capped_for_single_long_line(self):
        line = "START" + "A" * 5000 + "END"
        self.fake("python3", f"printf '%s\n' '{line}'\nexit 3\n")
        result = self.run_verify("structure")
        self.assertEqual(result.returncode, 3)
        self.assertIn("FAIL (exit 3). Log:", result.stderr)
        self.assertIn("END", result.stderr)
        self.assertNotIn("START", result.stderr)
        snippet = result.stderr.split("\n", 1)[1]
        self.assertLessEqual(len(snippet.encode("utf-8")), 3001)
        self.assertIn(line, self.logs(result)[0].read_text())

    def test_skipped_checks_reported_and_allowed(self):
        result = self.run_verify("all", tools=BASE_TOOLS + ("uname",))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("SKIP:", result.stdout)
        match = re.search(r"(\d+) skipped check group", result.stdout)
        self.assertIsNotNone(match)
        self.assertGreaterEqual(int(match.group(1)), 4)

    def test_verify_strict_rejects_skips_and_dirs_are_unique(self):
        tools = BASE_TOOLS + ("uname",)
        first = self.run_verify("all", tools=tools)
        strict = self.run_verify("all", extra_env={"VERIFY_STRICT": "1"}, tools=())
        self.assertEqual(strict.returncode, 1)
        self.assertIn("VERIFY_STRICT=1 rejects skipped checks", strict.stderr)
        self.assertNotEqual(self.log_dir(first), self.log_dir(strict))


if __name__ == "__main__":
    unittest.main()
