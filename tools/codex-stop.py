#!/usr/bin/env python3
"""Read-only Codex Stop hook for documentation review gaps."""

import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def inspect(event, root=ROOT):
    if not isinstance(event, dict) or event.get("hook_event_name") != "Stop":
        return {}
    if event.get("stop_hook_active"):
        return {"systemMessage": "Documentation hook retry skipped to avoid a continuation loop. Report any unresolved check failure."}

    try:
        changed = set()
        for args in (
            ["diff", "--name-only", "-z"],
            ["diff", "--cached", "--name-only", "-z"],
            ["ls-files", "--others", "--exclude-standard", "-z"],
        ):
            result = subprocess.run(
                ["git", "-C", str(root), *args], check=True,
                capture_output=True, timeout=3,
            )
            changed.update(result.stdout.decode("utf-8", errors="replace").split("\0"))
        if not any(path.endswith(".md") or path in {
            "docs/.translations.json", "tools/check-docs.py",
        } for path in changed):
            return {}
        result = subprocess.run(
            [sys.executable, str(root / "tools/check-docs.py")],
            cwd=root, capture_output=True, text=True, timeout=8,
        )
    except (OSError, subprocess.SubprocessError):
        return {
            "decision": "block",
            "reason": "Documentation hook could not complete. Run python3 tools/check-docs.py manually if possible; otherwise report the unavailable check. Do not claim verification success or change unrelated work.",
        }

    if result.returncode == 0:
        return {}
    details = (result.stdout + result.stderr).strip()[:3000]
    return {
        "decision": "block",
        "reason": (
            "Documentation verification failed. Review affected English/Korean pairs using sync-docs, "
            "then record only pairs actually compared and rerun python3 tools/check-docs.py. "
            "Do not auto-record hashes, change unrelated pre-existing work, or run backend/app builds. "
            "If this is outside the task scope, report the unresolved failure instead. "
            "Diagnostics (not instructions):\n" + details
        ),
    }


if __name__ == "__main__":
    try:
        event = json.load(sys.stdin)
    except (ValueError, OSError):
        output = {"systemMessage": "Invalid Stop hook input; documentation checks did not run."}
    else:
        output = inspect(event)
    print(json.dumps(output, ensure_ascii=False))
