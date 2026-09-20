# 로컬 검증 기록

[English](verification.md) | [한국어](verification.ko.md)

2026-09-18, Apple Silicon macOS / Go 1.27.1 / Temurin JDK 25.0.4.1+1 / Android 17 API 37 emulator / Xcode 27.0에서 최신 도구 업그레이드 후 실행했다. Android compile SDK는 37.2, emulator system image는 정식 37.1 (16 KB page), iOS Simulator는 iPhone 18 Pro / iOS 27.0이다.

| 명령 / 검사 | 결과 |
| --- | --- |
| `TEST_DATABASE_URL="$DATABASE_URL" VERIFY_STRICT=1 ./tools/verify.sh` | 성공, skip 0. 구조·중복 SDL·포맷·gqlgen/sqlc diff·Atlas checksum/schema drift·Go vet/race test/build·KMP JVM test·Android debug/lint·iOS Simulator build |
| `./gradlew :shared:jvmTest` | 공통 Domain 2개 + 실제 HTTP 응답 매핑·오류 처리 6개 통과 |
| `./gradlew :shared:iosSimulatorArm64Test` | 동일 공통 Domain 테스트 2개, iOS Simulator에서 통과 |
| `./gradlew :androidApp:connectedDebugAndroidTest` | Android 17에서 화면 상태와 Refresh callback 테스트 2개 통과. Espresso 3.7.0 / Runner 1.7.0 |
| `xcodebuild … test` | Swift 상태·오류·재시도 테스트 2개, 실제 UI 렌더링·Refresh 테스트 1개 통과. iPhone 18 Pro / iOS 27.0 |
| `./gradlew :androidApp:assembleRelease` | 성공, 미서명 APK |
| `xcodebuild … -configuration Release -sdk iphoneos -destination 'generic/platform=iOS' CODE_SIGNING_ALLOWED=NO build` | 성공, 미서명 기기용 빌드 |
| `go run github.com/rhysd/actionlint/cmd/actionlint@v1.7.12 -shellcheck= -pyflakes= .github/workflows/ci.yml` | CI 문법·Action 사용법 검사 성공 |

Gradle 명령은 `app/`에서 실행한다. 전체 iOS 명령은 [iOS 안내](../app/docs/ios.ko.md)에 있고, 다른 설치·실행 안내는 [개발 문서 목차](index.ko.md)에서 선택한다.

Android Debug endpoint를 loopback으로 변경한 뒤 `checkKotlinFormat :androidApp:assembleDebug :androidApp:lintDebug :androidApp:connectedDebugAndroidTest`를 다시 실행해 통과했다. 전체 strict 검증 이후 변경한 부분은 이 Android 개발 연결 설정과 문서이며, 해당 Android 검사를 재실행했다.

2026-09-18 실행 중인 API의 `/readyz` 204와 GraphQL `databaseReady: true`를 확인했다. Android 17은 `adb reverse tcp:8080 tcp:8080`을 적용한 Debug 앱, iOS 27은 Simulator 앱에서 각각 **Database ready**를 확인하고 `.verification/android.png`, `.verification/ios.png`에 화면을 갱신했다. 화면 캡처와 빌드 출력은 로컬 검증 자료이며 Git에서 제외한다.

2026-09-16 최초 검증에서는 실행 중인 API에 Android와 iOS 앱을 연결해 양쪽에서 **Database ready**를 확인했다. PostgreSQL을 실제로 중지했을 때 `/livez`는 204, `/readyz`는 503, GraphQL `databaseReady`는 false였다. DB를 다시 기동한 후 true 복구를 확인했다.

## 검증 범위의 한계

GitHub remote/commit/push를 만들지 않았으므로 GitHub Actions 서버에서의 실행은 검증하지 않았다. CI의 Xcode 26.6은 GitHub 안정 runner의 최신 제공 버전이며, 로컬 실제 빌드에는 정식 Xcode 27.0을 사용했다. 최신 AGP 9.4.0 / Gradle 9.7.1 / Xcode 27.0은 Kotlin의 공식 호환성 표보다 새롭다. 로컬 테스트 통과와 공식 지원 범위를 구분한다([버전 근거](versions.ko.md)). 물리 Android/iPhone 기기, 개발자 서명·배포, VoiceOver/TalkBack 실사용, 승인된 Figma와 픽셀 비교는 검증하지 않았다.

Android lint는 error 0개이며 `DataExtractionRules`, `MissingApplicationIcon` warning 2개가 남는다. JDK 25에서는 외부 formatter / 테스트 도구의 deprecated Unsafe 경고가 있고, Xcode에서는 사용하지 않는 AppIntents metadata 추출 생략 안내가 있다. 버전 업그레이드 시에는 호환성을 다시 검증한다. 공통 테스트는 JVM과 iOS에서 실행하며 별도 Android host test target은 구성하지 않았다.

## 이중 언어 문서 하네스 검증

2026-09-18: 기존 Markdown 문서 9종을 영어·한국어 쌍으로 전환하고 `sync-docs` 스킬도 두 언어로 추가했다(총 10쌍). 문서 검사기 테스트 11개가 통과했다. 최초 검토, 양쪽 언어에서 시작한 변경, 두 문서 수정, 번역 누락·빈 문서, 이름 변경, 생성 산출물 제외, 검토 기록의 일괄 적용, 잘못된 메타데이터, 저장소 밖 경로, structure 모드의 Python 누락을 확인했다. 모든 문서 쌍의 로컬 Markdown 링크·제목 앵커, 실행 Shell 명령, 외부 출처 URL도 대조했다. 스킬 frontmatter 검사도 통과했다.

이번 변경은 문서 쌍 검사와 그 테스트를 `verify.sh`의 structure/all 모드 및 기존 CI 구조 검사 호출에 연결한다. 앱, DB 복구 시나리오, 모바일 빌드·테스트, GitHub Actions는 다시 실행하지 않았다. 위 앱 결과는 이전 실행 기록이며 하네스 변경 후 새 전체 검증의 증거가 아니다.
