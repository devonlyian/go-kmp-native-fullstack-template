# Design rules

[English](AGENTS.md) | [한국어](AGENTS.ko.md)

Scope: `app/design/` design specifications, `design-system-map.yaml`, and authorized Figma design work. This design agent is separate from backend and app agents.

- Do not read backend source or root GraphQL SDL during design, and do not edit production app code, shared logic, GraphQL, or generated files. Start from the approved feature plan and user requirements. Targeted reads of existing Android/iOS design-system components and affected screens are allowed for reuse and visual review.
- Follow this order: approved feature plan → design draft, review, and approval → Design System definitions → GraphQL specification by the contract-owning role → `design-system-map.yaml` update. Existing GraphQL must not pre-constrain the design. If contract work reveals a product or UX gap, return it to planning/design for a decision instead of resolving it inside the design scope.
- Treat approved Figma as the visual reference. A user-authorized Figma edit may proceed without repeated approval; otherwise keep work local and report unavailable access rather than assuming a file, node, token, or component exists.
- Prefer `Component`, `Token`, and `Layout` names shared by Figma and code. Search existing native components first. After the design, Design System, and GraphQL specification are confirmed, update `design-system-map.yaml` only for finalized platform mappings or actual naming and behavior exceptions; the map does not contain GraphQL fields.
- Design Android for Compose/Material and iOS for SwiftUI/HIG. Keep feature components local until multiple features reuse them.
- Handoff approved designs to the app agent with states, mappings, exceptions, and screenshot-based visual-QA criteria. Rendered screenshots are evidence for visual review; mocks do not prove visual parity.

Use [design-app](../../.agents/skills/design-app/SKILL.md) for the workflow.
