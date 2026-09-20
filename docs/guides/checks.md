# Generate, Format, and Verify

[English](checks.md) | [한국어](checks.ko.md)

Choose the changed scope and run its checks:

- [Backend checks](../../backend/docs/checks.md) regenerate gqlgen/sqlc and verify only the backend.
- [App checks](../../app/docs/checks.md) regenerate Apollo sources and verify only shared KMP, Android, or iOS work.

Run `./tools/verify.sh` without a scope only when an explicitly requested integration change needs the full repository check. Platform UI tests and live backend work are separate, opt-in work.
