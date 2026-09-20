# Feature: system

[English](system.md) | [한국어](system.ko.md)

This is an integration reference for an explicitly requested server/app end-to-end task. Routine backend and app development use their own scope records and the root SDL; they do not need to read this cross-scope implementation record.

## Goal and user value

Check the server's PostgreSQL connection state from the app and use `Refresh` to check the latest state after recovery. This is the template's minimal feature for verifying the GraphQL → KMP → Android/iOS screen connection.

Scope covers current connection state and manual refresh. Authentication, product data, status history, automatic polling, and production monitoring are excluded.

## User flow and screens

Both Android and iOS provide the following flow in `SystemStatusScreen`.

Screen entry → loading → DB status or request error → `Refresh` → loading → latest result.

| Condition | Contract and server response | Expected Android/iOS result |
| --- | --- | --- |
| API and DB healthy | `databaseReady: true`, `/livez` 204, `/readyz` 204 | `Database ready` |
| API running but DB connection fails | `databaseReady: false`, `/livez` 204, `/readyz` 503 | `Database not ready` |
| DB connection restored, then `Refresh` | `databaseReady: true`, `/readyz` 204 | `Database not ready` changes to `Database ready` |
| API stopped, offline, or GraphQL request error | No valid status result can be obtained | `Unable to load system status.` |
| API connection and DB health restored, then `Refresh` | `databaseReady: true` | The error disappears and `Database ready` appears |

While fetching, show a loading indicator with the accessibility label `Loading system status`. Repeated `Refresh` taps during a request do not start duplicate requests. There is no automatic retry; the user checks again after the server state changes.

A DB connection failure is successfully retrieved `false` data. Distinguish it from API connection failures and GraphQL errors. A single non-null status result needs no separate empty-list screen. Request errors must not display connection URLs or internal error details.

## Domain and required data

- Backend boundary: `backend/internal/system`; the public Application entrypoint is `Service.Status(ctx)`.
- Shared boundary: `app/shared/src/commonMain/kotlin/com/example/template/shared/feature/system`; `GetSystemStatusUseCase` fetches status through the repository.
- Android boundary: `app/androidApp/src/main/kotlin/com/example/template/feature/system`; iOS boundary: `app/iosApp/Sources/Features/System`. `System` is the Swift spelling of the same `system` feature.
- `SystemStatus.databaseReady` indicates whether the pgx/sqlc `SELECT 1` succeeds at query time. It is neither stored status history nor a guarantee that every server feature is healthy.
- There are no query arguments or user inputs. Status responses contain no personal information or credentials.

## GraphQL Operation and Mock strategy

The contract source is [system.graphqls](../../contracts/graphql/system.graphqls). It uses `Query.systemStatus: SystemStatus!` and `SystemStatus.databaseReady: Boolean!`. Writing this specification does not change SDL, DB schema, migrations, or sqlc queries.

The client Operation is `query SystemStatus` in [SystemStatus.graphql](../../app/shared/src/commonMain/graphql/com/example/template/shared/system/SystemStatus.graphql). The client treats GraphQL errors or missing required data as a request failure.

Mock responses follow this Operation too. Verify `true` and `false` success responses, GraphQL errors, transport failures, and success after failure separately. Also check that cancellation is not converted into an ordinary request failure. Injected UI states or successful Mocks alone are not evidence of actual API/DB connectivity.

## Android/iOS differences and acceptance criteria

Android collects `SystemStatusViewModel`'s `StateFlow` according to lifecycle and renders it with Compose. iOS uses native `@Observable` state and SwiftUI `.task`. UI, ViewModel, and screen state are not shared. This feature has no Navigation between screens.

Both platforms use the existing `AppButton`, `AppColors`, and `AppSpacing`. See [design-system-map.yaml](../../app/design/design-system-map.yaml) for names and Token mapping. No approved Figma screen exists yet, so Figma parity remains unverified; record comparison results once a baseline screen is approved.

The following items define acceptance. Check them only after obtaining execution evidence for the relevant change and environment.

- [ ] **Basic verification:** Feature names and contracts match; codegen, structure checks, Backend/Shared tests, and Android/iOS builds pass. Record actual PostgreSQL integration tests and skips separately.
- [ ] **Platform tests:** Run Android device tests, KMP iOS tests, Swift state tests, and iOS UI tests separately. A check that accepts either a success screen or an error screen is not evidence of a healthy DB connection.
- [ ] **Actual connection and recovery:** Check all five table conditions on Android and iOS separately. In particular, capture `Database not ready` on DB failure and the transition to `Database ready` after recovery and `Refresh`. Check API failure/recovery the same way.
- [ ] **Screens and accessibility:** Check loading, duplicate-request prevention, and refresh; verify usable status and buttons with large text, dark mode, safe areas, and TalkBack/VoiceOver. Record whether Figma comparison was performed.
- [ ] **Verification evidence:** Record execution date, target change, device/OS, commands/results, screenshot locations, and skipped/unverified items in the [verification record](../verification.md). Summarize the same scope when writing a PR.

### Actual connection verification procedure

Prepare the local verification environment using [server execution](../../backend/docs/run.md), [Android](../../app/docs/android.md), and [iOS](../../app/docs/ios.md). First confirm that both platforms use the same verification API.

1. With a healthy API and DB, open both apps and record `Database ready` and healthy health responses.
2. Keep the API running and stop only the verification DB. Tap `Refresh` in both apps and record `Database not ready`, `/livez` 204, `/readyz` 503, and `databaseReady: false`.
3. Restart the same DB. Without restarting the API, tap `Refresh` in both apps and record recovery to `Database ready`, `/readyz` 204, and `databaseReady: true`.
4. Stop the verification API and tap `Refresh` in both apps to record the request-error screen.
5. Restart the API and confirm a healthy DB connection. Tap `Refresh` in both apps and record recovery to the normal screen. Leave the verification environment healthy.

The basic verification command is `./tools/verify.sh`; `VERIFY_STRICT=1` rejects skips counted by the script. Basic verification with `skip 0` does not mean that platform tests or the manual scenarios above ran. Follow [Android tests](../../app/docs/android.md) and [iOS tests](../../app/docs/ios.md) for platform test commands.

### Verification scope of this specification

2026-09-18: Expected results were specified by reading the current contract, server, Shared, and both platform screen implementations. Previous execution results are in the [verification record](../verification.md). Failure/recovery scenarios and platform tests were not rerun while writing this document. Do not mark the checklist as newly verified.
