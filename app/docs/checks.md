# App checks

[English](checks.md) | [한국어](checks.ko.md)

Run commands from the repository root. Apollo code generation reads the only SDL source at `contracts/graphql/`; generated Kotlin stays under `build/` and is never edited by hand.

```sh
(cd app && ./gradlew formatKotlin :shared:generateApolloSources)
```

Choose only the changed app scope:

```sh
(cd app && ./gradlew :shared:jvmTest :androidApp:assembleDebug :androidApp:lintDebug)
(cd app && ./gradlew :shared:iosSimulatorArm64Test :shared:linkDebugFrameworkIosSimulatorArm64)
xcrun swift-format lint --strict --recursive app/iosApp/Sources app/iosApp/Tests app/iosApp/UITests
xcodebuild -project app/iosApp/TemplateApp.xcodeproj -scheme TemplateApp \
  -configuration Debug -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' \
  -derivedDataPath app/iosApp/build CODE_SIGNING_ALLOWED=NO build
```

The first scoped command covers shared and Android work. The remaining commands cover iOS work and require Apple Silicon macOS, Xcode, an iOS Simulator SDK, and JDK 25. These checks do not start, build, or test the backend. Hand off any required server checks; do not run them as part of app work.

## App directory verification

2026-09-20, Apple Silicon macOS: after moving the app root to `app/`, `VERIFY_STRICT=1 ./tools/verify.sh app` and `VERIFY_STRICT=1 ./tools/verify.sh ios` passed with zero skipped check groups. The checks covered Kotlin formatting, Apollo generation, KMP JVM tests, Android Debug build/lint, Swift formatting, the shared iOS Simulator framework, and the iOS Simulator app build. Old build outputs and project caches were moved outside the repository before the final builds because they retained absolute paths from the previous location.

Structure checks, all 20 tool tests, bilingual document review, and local Markdown link targets also passed. Device/UI tests and live backend integration were not rerun for this directory rename.
