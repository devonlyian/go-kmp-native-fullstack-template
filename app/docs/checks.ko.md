# 앱 검사

[English](checks.md) | [한국어](checks.ko.md)

명령은 저장소 루트에서 실행한다. Apollo 코드 생성은 유일한 SDL 원본인 `contracts/graphql/`을 읽고, 생성된 Kotlin은 `build/` 아래에만 있으며 직접 수정하지 않는다.

```sh
(cd app && ./gradlew formatKotlin :shared:generateApolloSources)
```

바뀐 앱 범위만 선택한다.

```sh
(cd app && ./gradlew :shared:jvmTest :androidApp:assembleDebug :androidApp:lintDebug)
(cd app && ./gradlew :shared:iosSimulatorArm64Test :shared:linkDebugFrameworkIosSimulatorArm64)
xcrun swift-format lint --strict --recursive app/iosApp/Sources app/iosApp/Tests app/iosApp/UITests
xcodebuild -project app/iosApp/TemplateApp.xcodeproj -scheme TemplateApp \
  -configuration Debug -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' \
  -derivedDataPath app/iosApp/build CODE_SIGNING_ALLOWED=NO build
```

첫 scoped 명령은 shared와 Android 작업을 검사한다. 나머지는 iOS 작업을 검사하며 Apple Silicon macOS, Xcode, iOS Simulator SDK, JDK 25가 필요하다. 이 검사는 백엔드를 시작·빌드·테스트하지 않는다. 필요한 서버 검사는 인계하고 앱 작업의 일부로 실행하지 않는다.

## 앱 디렉터리 검증

2026-09-20, Apple Silicon macOS: 앱 루트를 `app/`으로 옮긴 뒤 `VERIFY_STRICT=1 ./tools/verify.sh app`과 `VERIFY_STRICT=1 ./tools/verify.sh ios`가 생략한 검사 그룹 없이 통과했다. Kotlin 포맷·Apollo 생성·KMP JVM 테스트·Android Debug 빌드/lint·Swift 포맷·공통 iOS Simulator framework·iOS Simulator 앱 빌드를 확인했다. 기존 빌드 산출물과 프로젝트 캐시에 이전 위치의 절대 경로가 남아 있어 최종 빌드 전에 저장소 밖으로 옮겨 보관했다.

구조 검사·도구 테스트 20개·이중 언어 문서 검토·로컬 Markdown 링크 대상 확인도 통과했다. 이번 디렉터리 이름 변경에서 기기/UI 테스트와 실제 백엔드 통합은 다시 실행하지 않았다.
