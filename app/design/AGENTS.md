# Design rules

[English](AGENTS.md) | [한국어](AGENTS.ko.md)

Scope: `app/design/` design specifications, `design-system-map.yaml`, and authorized Figma design work. This design agent is separate from backend and app agents.

For existing work, enter at the requested stage and reuse approved Figma or agreed local references without recreating them in Make.

- Do not read backend source or root GraphQL SDL during design, and do not edit production app code, shared logic, GraphQL, or generated files. Start from the approved feature plan and user requirements. Targeted reads of existing Android/iOS design-system components and affected screens are allowed for reuse and visual review.
- Follow this order: approved feature plan → design in Figma Make, review, and approval → create or reconcile the approved Figma Design System from the Figma Make-produced files and artifacts → match Design System tokens → native app development → GraphQL contract creation by the app scope → backend development. Figma Make files and artifacts are design input; do not claim automatic conversion or use unsupported Make APIs. Existing GraphQL must not pre-constrain the design.
- Treat approved Figma as the visual reference. A user-authorized Figma edit may proceed without repeated approval; otherwise keep work local and report unavailable access rather than assuming a file, node, token, component, or Make artifact exists. Create or reconcile Design System components and semantic tokens from approved Make artifacts, existing approved Figma designs, or an agreed local specification; distinguish local specifications from actual Figma nodes.
- Prefer `Component`, `Token`, and `Layout` names shared by Figma and code. Search existing native components first. Before native app development, match approved Design System tokens and update `design-system-map.yaml` only for finalized mappings or actual naming and behavior exceptions. The map contains neither GraphQL fields nor planned native symbols; identify planned native additions separately in the handoff, and record only existing verified Android/iOS names in YAML.
- Design Android for Compose/Material and iOS for SwiftUI/HIG. Keep feature components local until multiple features reuse them.
- Handoff approved designs to the app agent before native implementation with Figma Make/design references, approval state, existing mappings and exceptions, planned native additions, states, platform accessibility requirements, and screenshot-based visual-QA criteria. The app scope creates the GraphQL contract after native app development, then hands the approved contract to backend. If contract work reveals a product or UX gap, return it to planning/design for a decision instead of resolving it inside the design scope. Rendered screenshots are evidence for visual review; mocks do not prove visual parity.

Use [design-app](../../.agents/skills/design-app/SKILL.md) for the workflow.
