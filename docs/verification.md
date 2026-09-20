# Local verification record

[English](verification.md) | [한국어](verification.ko.md)

Executed after the toolchain upgrade on 2026-09-18 with Apple Silicon macOS / Go 1.27.1 / Temurin JDK 25.0.4.1+1 / Android 17 API 37 emulator / Xcode 27.0. Android compile SDK is 37.2, the emulator system image is final 37.1 (16 KB pages), and the iOS Simulator is iPhone 18 Pro / iOS 27.0.

| Command / check | Result |
| --- | --- |
| `TEST_DATABASE_URL="$DATABASE_URL" VERIFY_STRICT=1 ./tools/verify.sh` | Passed, skip 0. Structure, duplicate SDL, formatting, gqlgen/sqlc diff, Atlas checksum/schema drift, Go vet/race tests/build, KMP JVM tests, Android debug/lint, iOS Simulator build |
| `./gradlew :shared:jvmTest` | Passed 2 shared Domain tests and 6 tests for actual HTTP response mapping and error handling |
| `./gradlew :shared:iosSimulatorArm64Test` | The same 2 shared Domain tests passed on iOS Simulator |
| `./gradlew :androidApp:connectedDebugAndroidTest` | 2 screen-state and Refresh callback tests passed on Android 17. Espresso 3.7.0 / Runner 1.7.0 |
| `xcodebuild … test` | 2 Swift state/error/retry tests and 1 actual UI rendering/Refresh test passed. iPhone 18 Pro / iOS 27.0 |
| `./gradlew :androidApp:assembleRelease` | Passed, unsigned APK |
| `xcodebuild … -configuration Release -sdk iphoneos -destination 'generic/platform=iOS' CODE_SIGNING_ALLOWED=NO build` | Passed, unsigned device build |
| `go run github.com/rhysd/actionlint/cmd/actionlint@v1.7.12 -shellcheck= -pyflakes= .github/workflows/ci.yml` | CI syntax and Action usage checks passed |

Run Gradle commands from `app/`. Full iOS commands are in the [iOS guide](../app/docs/ios.md); select other setup/run guides from the [development index](index.md).

After changing the Android Debug endpoint to loopback, `checkKotlinFormat :androidApp:assembleDebug :androidApp:lintDebug :androidApp:connectedDebugAndroidTest` was run again and passed. Only the Android development connection settings and documentation changed after the full strict verification; the relevant Android checks were rerun.

On 2026-09-18, the running API returned `/readyz` 204 and GraphQL `databaseReady: true`. **Database ready** was confirmed in the Android 17 Debug app with `adb reverse tcp:8080 tcp:8080` and in the iOS 27 Simulator app. Screenshots were updated at `.verification/android.png` and `.verification/ios.png`. Screenshots and build outputs are local verification artifacts excluded from Git.

During initial verification on 2026-09-16, both Android and iOS apps connected to the running API and displayed **Database ready**. With PostgreSQL actually stopped, `/livez` returned 204, `/readyz` returned 503, and GraphQL `databaseReady` was false. After restarting the DB, recovery to true was confirmed.

## Verification limits

No GitHub remote, commit, or push was created, so execution on GitHub Actions servers has not been verified. CI Xcode 26.6 is the latest version provided by the stable GitHub runner; local builds used final Xcode 27.0. AGP 9.4.0 / Gradle 9.7.1 / Xcode 27.0 are newer than Kotlin's official compatibility table. Distinguish local test success from official support ([version rationale](versions.md)). Physical Android/iPhone devices, developer signing/distribution, actual VoiceOver/TalkBack usage, and pixel comparison against approved Figma designs have not been verified.

Android lint has 0 errors and 2 warnings: `DataExtractionRules` and `MissingApplicationIcon`. With JDK 25, external formatters and test tools report deprecated Unsafe warnings; Xcode reports skipping unused AppIntents metadata extraction. Recheck compatibility when upgrading versions. Shared tests run on JVM and iOS; no separate Android host test target is configured.

## Bilingual documentation harness verification

2026-09-18: Converted 9 existing Markdown documents to English/Korean pairs and added a paired `sync-docs` skill (10 pairs total). The documentation checker tests passed: 11 tests cover initial review, changes from either language, paired edits, missing or empty translations, rename handling, generated-output exclusions, atomic review updates, invalid metadata, external paths, and missing Python in structure mode. Local Markdown links and heading anchors, executable shell commands, and external reference URLs were compared across all pairs. The skill frontmatter validator also passed.

This change adds document-pair checking and its tests to `verify.sh` structure/all modes and the existing CI structure invocation. It does not rerun the application, DB recovery scenarios, mobile builds/tests, or GitHub Actions. The application results above are earlier execution records, not evidence of a new full verification after modifying the harness.
