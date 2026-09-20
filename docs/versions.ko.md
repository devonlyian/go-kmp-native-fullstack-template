# 버전 근거

[English](versions.md) | [한국어](versions.ko.md)

2026-09-18 공식 문서·릴리스와 설치 도구를 확인했다. 실제 고정값은 Go module, Gradle version catalog / wrapper, Xcode project, Compose에 있다. Android/iOS 개발 도구와 직접 의존성은 이 날짜의 최신 안정 버전을 적용했다. JVM은 최신 LTS인 Java 25를 사용한다. 이후 버전 변경은 검증 후 명시적으로 적용한다.

| 구성 | 고정값 / 확인 근거 |
| --- | --- |
| Go | module 최소 1.26.0, 로컬·CI 1.27.1. [공식 다운로드](https://go.dev/dl/) |
| gqlgen | [v0.17.95](https://github.com/99designs/gqlgen/releases/tag/v0.17.95), root SDL 입력 |
| pgx | [v5.11.0](https://github.com/jackc/pgx/releases/tag/v5.11.0) |
| sqlc | [v1.31.1](https://github.com/sqlc-dev/sqlc/releases/tag/v1.31.1), pgx/v5 생성 |
| Atlas | [v1.3.0](https://github.com/ariga/atlas/releases/tag/v1.3.0), 공식 binary와 SHA-256을 installer에 고정 |
| PostgreSQL | [18.6](https://www.postgresql.org/support/versioning/), 공식 versions.json과 Docker image 확인 |
| Kotlin | [2.4.20 호환성 표](https://kotlinlang.org/docs/multiplatform/multiplatform-compatibility-guide.html): Gradle 7.6.3–9.7.0, AGP 8.5.2–9.3.1, Xcode 26.4 |
| AGP / Gradle | [AGP 9.4.0](https://developer.android.com/build/releases/agp-9-4-0-release-notes), [Gradle 9.7.1](https://docs.gradle.org/9.7.1/release-notes.html). AGP 최소 Gradle 9.6.0 / JDK 17 이상. Gradle은 Java 25 실행을 9.1.0부터 지원 |
| Android SDK | compile SDK **37.2**, target API **37**, Build Tools **37.0.0**. [공식 SDK repository](https://dl.google.com/android/repository/repository2-4.xml)의 stable channel, 비어 있는 codename으로 정식 버전 확인. 최소 API 24 |
| JVM / JDK | **Java 25 LTS**, [Temurin 25.0.4.1+1](https://github.com/adoptium/temurin25-binaries/releases/tag/jdk-25.0.4.1%2B1). [Oracle 지원 일정](https://www.oracle.com/java/technologies/java-se-support-roadmap.html). Android/JVM 산출물 target은 17이며 빌드 JDK 25와 구분 |
| Xcode / iOS | 로컬 **Xcode 27.0**, iOS SDK **27.0**, Swift compiler **6.4**, Swift 언어 모드 **6**. [Apple 릴리스](https://developer.apple.com/news/releases/). 최소 iOS 26 |
| Apollo Kotlin | [5.1.0](https://github.com/apollographql/apollo-kotlin/releases/tag/v5.1.0), [Schema 설정](https://www.apollographql.com/docs/kotlin/advanced/plugin-configuration) |
| Compose | [BOM 2026.09.00](https://developer.android.com/develop/ui/compose/bom/bom-mapping), Kotlin Compose compiler는 Kotlin 버전과 동일 |
| AndroidX | [Activity 1.13.0](https://developer.android.com/jetpack/androidx/releases/activity), [Lifecycle 2.11.0](https://developer.android.com/jetpack/androidx/releases/lifecycle) |
| AndroidX Test | [Runner 1.7.0 / Espresso 3.7.0](https://developer.android.com/jetpack/androidx/releases/test). Compose의 전이 의존성인 Espresso 3.5.0은 Android 17의 제거된 InputManager API를 호출하므로 직접 최신 버전을 지정 |
| Kotlin formatter | [ktfmt 0.64](https://github.com/Kotlin/ktfmt/releases/tag/v0.64), build tool 전용 |
| Xcode project generator | [XcodeGen 2.46.0](https://github.com/yonaskolb/XcodeGen/releases/tag/2.46.0), 일반 빌드에는 불필요 |
| Coroutines | [1.11.0](https://github.com/Kotlin/kotlinx.coroutines/releases/tag/1.11.0) |

설치 환경은 macOS Apple Silicon, Xcode 27.0 (27A266a), Go 1.27.1, Temurin JDK 25.0.4.1+1, Android SDK 37.2이다. AGP 9.4.0 / Gradle 9.7.1 / Xcode 27은 Kotlin 공식 호환성 표의 확인 버전(9.3.1 / 9.7.0 / 26.4)보다 새롭다. 최신 안정 도구 조합은 이 저장소의 빌드·테스트로 확인하며, 공식 검증 범위를 확대해 표현하지 않는다. 이 환경의 실제 빌드 통과 여부와 공식 지원 여부는 같은 주장이 아니다.

GitHub Actions는 공식 릴리스 tag의 commit SHA에 고정한다. [runner image 문서](https://github.com/actions/runner-images/blob/main/images/macos/macos-26-arm64-Readme.md)를 통해 macOS runner의 도구를 확인한다. 로컬 검증은 GitHub-hosted runner 실행 결과를 대신하지 않는다.

Android 17 / target 37의 [로컬 네트워크 권한](https://developer.android.com/privacy-and-security/local-network-permission) 변경에 맞춰 Android Debug endpoint는 `127.0.0.1`이며 `adb reverse tcp:8080 tcp:8080`이 필요하다. 로컬 개발 서버 연결에 추가 앱 권한을 요청하지 않는다.

## CI Xcode 제공 범위

2026-09-18 GitHub `macos-26` Apple Silicon 안정 이미지의 최신 제공 Xcode는 **26.6**이다. CI는 `/Applications/Xcode_26.6.app/Contents/Developer`를 사용한다. 별도 `xcode-27` runner는 현재 **Public Preview**이며 Xcode 27 beta 6이라 정식 27.0 검증으로 간주하지 않는다. 로컬에서는 정식 Xcode 27.0 / iOS 27 SDK를 검증했다. GitHub 안정 이미지에 정식 27이 제공되면 CI 경로를 갱신하고 다시 검증한다.
