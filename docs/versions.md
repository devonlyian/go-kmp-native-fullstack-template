# Version rationale

[English](versions.md) | [한국어](versions.ko.md)

Official documentation, releases, and installation tools were checked on 2026-09-18. Actual pinned values are in the Go module, Gradle version catalog / wrapper, Xcode project, and Compose. The latest stable versions on that date are used for Android/iOS development tools and direct dependencies. The JVM uses Java 25, the latest LTS. Apply future version changes explicitly after verification.

| Component | Pinned value / verification basis |
| --- | --- |
| Go | module minimum 1.26.0; local and CI 1.27.1. [Official downloads](https://go.dev/dl/) |
| gqlgen | [v0.17.95](https://github.com/99designs/gqlgen/releases/tag/v0.17.95), root SDL input |
| pgx | [v5.11.0](https://github.com/jackc/pgx/releases/tag/v5.11.0) |
| sqlc | [v1.31.1](https://github.com/sqlc-dev/sqlc/releases/tag/v1.31.1), pgx/v5 generation |
| Atlas | [v1.3.0](https://github.com/ariga/atlas/releases/tag/v1.3.0), official binary and SHA-256 pinned in the installer |
| PostgreSQL | [18.6](https://www.postgresql.org/support/versioning/), official versions.json and Docker image checked |
| Kotlin | [2.4.20 compatibility table](https://kotlinlang.org/docs/multiplatform/multiplatform-compatibility-guide.html): Gradle 7.6.3–9.7.0, AGP 8.5.2–9.3.1, Xcode 26.4 |
| AGP / Gradle | [AGP 9.4.0](https://developer.android.com/build/releases/agp-9-4-0-release-notes), [Gradle 9.7.1](https://docs.gradle.org/9.7.1/release-notes.html). AGP requires Gradle 9.6.0+ / JDK 17+. Gradle supports running on Java 25 from 9.1.0. |
| Android SDK | compile SDK **37.2**, target API **37**, Build Tools **37.0.0**. Stable channel of the [official SDK repository](https://dl.google.com/android/repository/repository2-4.xml); a blank codename confirms the final release. Minimum API 24. |
| JVM / JDK | **Java 25 LTS**, [Temurin 25.0.4.1+1](https://github.com/adoptium/temurin25-binaries/releases/tag/jdk-25.0.4.1%2B1). [Oracle support roadmap](https://www.oracle.com/java/technologies/java-se-support-roadmap.html). Android/JVM artifacts target 17; this is distinct from build JDK 25. |
| Xcode / iOS | Local **Xcode 27.0**, iOS SDK **27.0**, Swift compiler **6.4**, Swift language mode **6**. [Apple releases](https://developer.apple.com/news/releases/). Minimum iOS 26. |
| Apollo Kotlin | [5.1.0](https://github.com/apollographql/apollo-kotlin/releases/tag/v5.1.0), [Schema configuration](https://www.apollographql.com/docs/kotlin/advanced/plugin-configuration) |
| Compose | [BOM 2026.09.00](https://developer.android.com/develop/ui/compose/bom/bom-mapping); the Kotlin Compose compiler matches the Kotlin version. |
| AndroidX | [Activity 1.13.0](https://developer.android.com/jetpack/androidx/releases/activity), [Lifecycle 2.11.0](https://developer.android.com/jetpack/androidx/releases/lifecycle) |
| AndroidX Test | [Runner 1.7.0 / Espresso 3.7.0](https://developer.android.com/jetpack/androidx/releases/test). Espresso 3.5.0, a transitive Compose dependency, calls the removed InputManager API on Android 17, so the current version is specified directly. |
| Kotlin formatter | [ktfmt 0.64](https://github.com/Kotlin/ktfmt/releases/tag/v0.64), build-tool only |
| Xcode project generator | [XcodeGen 2.46.0](https://github.com/yonaskolb/XcodeGen/releases/tag/2.46.0), unnecessary for regular builds |
| Coroutines | [1.11.0](https://github.com/Kotlin/kotlinx.coroutines/releases/tag/1.11.0) |

The installation environment is macOS Apple Silicon, Xcode 27.0 (27A266a), Go 1.27.1, Temurin JDK 25.0.4.1+1, and Android SDK 37.2. AGP 9.4.0 / Gradle 9.7.1 / Xcode 27 are newer than the verified versions in Kotlin's official compatibility table (9.3.1 / 9.7.0 / 26.4). This repository's builds and tests verify the latest stable tool combination; they do not expand the stated official verification range. A successful build in this environment and official support are separate claims.

GitHub Actions pins official release tags to commit SHAs. The [runner-image documentation](https://github.com/actions/runner-images/blob/main/images/macos/macos-26-arm64-Readme.md) is used to check tools on the macOS runner. Local verification does not substitute for results from a GitHub-hosted runner.

In line with the [local-network permission](https://developer.android.com/privacy-and-security/local-network-permission) change for Android 17 / target 37, the Android Debug endpoint is `127.0.0.1` and requires `adb reverse tcp:8080 tcp:8080`. No additional app permission is requested for the local development server connection.

## CI Xcode availability

As of 2026-09-18, the latest Xcode provided by GitHub's stable `macos-26` Apple Silicon image is **26.6**. CI uses `/Applications/Xcode_26.6.app/Contents/Developer`. A separate `xcode-27` runner is currently **Public Preview** and uses Xcode 27 beta 6, so it is not considered validation against final 27.0. Final Xcode 27.0 / iOS 27 SDK were verified locally. When GitHub's stable image provides final Xcode 27, update the CI path and verify again.
