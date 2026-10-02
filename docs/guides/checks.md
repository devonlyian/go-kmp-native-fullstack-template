# Generate, Format, and Verify

[English](checks.md) | [한국어](checks.ko.md)

Choose the changed scope and run its checks:

- [Backend checks](../../backend/docs/checks.md) regenerate gqlgen/sqlc and verify only the backend.
- [App checks](../../app/docs/checks.md) regenerate Apollo sources and verify only shared KMP, Android, or iOS work.

Run `./tools/verify.sh` without a scope only when an explicitly requested integration change needs the full repository check. Platform UI tests and live backend work are separate, opt-in work.

Verification saves each command's combined stdout/stderr in a unique run directory under the ignored `.verification/` folder. The terminal prints commands, pass/fail status, skips, and the log directory instead of full build/test output. On failure it prints the command's log path and only the last 20 lines, capped at 3,000 bytes; the original exit status is preserved. Open that log for further diagnosis rather than pasting the whole file into the chat. Logs remain local and are not committed.
