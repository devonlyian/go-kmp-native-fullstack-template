# iOS

[English](ios.md) | [한국어](ios.ko.md)

[앱 설정](setup.ko.md)을 마친다. 저장소 루트에서 shared framework를 빌드한 뒤 앱을 연다.

```sh
(cd app && ./gradlew :shared:linkDebugFrameworkIosSimulatorArm64)
open app/iosApp/TemplateApp.xcodeproj
```

Xcode에서 TemplateApp scheme과 iPhone Simulator를 선택해 Run한다. Debug는 `http://localhost:8080/graphql`을 사용한다. 실제 기기에는 접근 가능한 API 주소와 signing team이 필요하며 Release는 HTTPS를 사용해야 한다. 실행 중인 API는 요청된 통합 작업에만 필요하고 앱 단독 검사나 mock 개발에는 필요하지 않다.

서명 없는 Simulator 앱을 빌드한다.

```sh
xcodebuild -project app/iosApp/TemplateApp.xcodeproj -scheme TemplateApp \
  -configuration Debug -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' \
  -derivedDataPath app/iosApp/build CODE_SIGNING_ALLOWED=NO build
```

KMP와 네이티브 테스트는 사용 가능한 Simulator에서 실행한다. `xcrun simctl list devices available`가 출력한 값으로 destination을 바꾼다.

```sh
(cd app && ./gradlew :shared:iosSimulatorArm64Test)
xcodebuild -project app/iosApp/TemplateApp.xcodeproj -scheme TemplateApp \
  -configuration Debug -sdk iphonesimulator \
  -destination 'platform=iOS Simulator,name=iPhone 18 Pro,OS=27.0' \
  -derivedDataPath app/iosApp/build CODE_SIGNING_ALLOWED=NO test
```

버전 관리하는 project는 XcodeGen 없이 빌드한다. target 설정을 바꿀 때만 `app/iosApp/project.yml`을 수정한 뒤 [XcodeGen 2.46.0](https://github.com/yonaskolb/XcodeGen/releases/tag/2.46.0)으로 `xcodegen generate --spec app/iosApp/project.yml`를 실행한다.
