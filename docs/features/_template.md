# API agreement: <feature>

[English](_template.md) | [한국어](_template.ko.md)

Use only for shared API decisions and handoff. Keep backend/app implementation notes in the owning scope's `docs/features/`; do not require both implementations for one task.

## Value and contract

- Contract state (`Draft` / `Agreed`), app/backend review evidence, and demonstrated app-flow data requirements supplied in the handoff:
- User value and requested scope:
- Root SDL path, Query/Mutation, inputs, output fields, nullability:
- Success, empty/false data, validation and error semantics to describe in SDL:
- Compatibility impact, proposed change, and agreed decision:

## Handoff

- Contract diff and expected request/response/error examples:
- Current scope's evidence and date/environment:
- Remaining backend work, app model/fixture alignment and Apollo/adapter connection, responsible scope, and integration checks:
- Breaking change migration/rollout plan, if needed:

A contract record is not a second SDL source or proof of consumer compatibility. Do not fill gaps by reading the other implementation.
