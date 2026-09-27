# App feature: <feature>

[English](_template.md) | [한국어](_template.ko.md)

## Flow and contract

- Current stage: native app with provisional fixtures / contract handoff / GraphQL connection:
- User value, target platforms, scope/exclusions:
- Supported languages, language selection/fallback, and approved content exceptions (see [i18n policy](../../../docs/i18n.md)):
- Entry/action/result/retry, loading/empty/error/offline/cancellation:
- Demonstrated data needs and provisional assumptions; root SDL/Operation and results/nullability/errors once agreed (pending or not needed before then):

## App implementation

- Shared Domain/Data/Network and native presentation paths:
- Native localization resource paths, affected message identities, and `ko`/`en` review/packaging status:
- Approved source (approved Figma file / agreed local specification) and Design System reference; token correspondence, existing/planned native symbols, actual mapping exceptions:
- Provisional local fixtures/test doubles, contract-aligned Mocks, or provided API endpoint; identify which evidence applies:

## App acceptance

- [ ] Shared tests and affected platform builds/tests; Apollo generation and model/fixture alignment for agreed GraphQL work
- [ ] Actual screens, retry, text scaling, dark mode and VoiceOver/TalkBack
- [ ] Affected `ko`/`en` copy, formatting, plural/placeholder behavior, language changes/fallback, and UI/accessibility evidence per target platform; unverified combinations recorded
- [ ] Provisional vs contract-aligned Mock vs live API evidence, date/environment, skips, and contract/backend/connection handoff recorded

No Go/SQL inspection or server implementation is required. Native flow validation can finish before contract creation; API connection and live integration remain pending until separately verified. Mock success does not prove live integration.
