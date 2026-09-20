---
name: plan-feature
description: Define and review an implementation-neutral feature plan before design or API work. Use for product scope, user flows, business rules, edge states, acceptance criteria, approval, and handoff; do not use it to design screens or edit contracts or implementation.
---

# Plan a feature

[English](SKILL.md) | [한국어](SKILL.ko.md)

Use [the plan template](../../../docs/plans/_template.md). English is the source of truth; use [sync-docs](../sync-docs/SKILL.md) for every plan edit. Keep one plan pair per feature under `docs/plans/`; do not split the same product decision into separate PRD, flow, and acceptance documents.

1. Establish the target user, problem, expected outcome, source evidence, and requested approval. Separate user-provided facts from assumptions. Do not infer product intent from Figma, GraphQL, database, backend, or app implementation.
2. Set in-scope and out-of-scope behavior, target platforms, product constraints, and dependencies on unresolved decisions. Describe user-visible intent without choosing UI components, API fields, storage, libraries, or architecture.
3. Define the end-to-end flow and applicable business rules. Cover success and only the relevant empty, validation, permission, failure, retry/recovery, offline, and cancellation states. Leave native interaction choices to design.
4. Write observable acceptance criteria plus relevant accessibility, privacy, and safety requirements. Record agreed decisions, assumptions, and open questions. Keep the status `Draft` until the user explicitly approves it; never infer approval from document creation or silence.
5. For a material choice that changes scope, ask one concise decision before finalizing. Otherwise keep minor uncertainty visible in the plan. After approval, hand design the flows, states, content, and platform constraints, and hand the app scope (the contract drafter) actions, data concepts, outcomes, and failure semantics without proposing SDL fields.

Planning does not edit Figma, `contracts/graphql/`, database files, production code, or implementation records. If feasibility or current behavior cannot be established from supplied product documentation, record the gap for the owning role instead of crossing into its implementation.
