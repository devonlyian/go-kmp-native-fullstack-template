# iOS

[English](ios.md) | [한국어](ios.ko.md)

Complete [app setup](setup.md). Build the shared framework, then open the app from the repository root:

```sh
(cd app && ./gradlew :shared:linkDebugFrameworkIosSimulatorArm64)
open app/iosApp/TemplateApp.xcodeproj
```

In Xcode, select the TemplateApp scheme and an iPhone Simulator, then Run. Debug uses `http://localhost:8080/graphql`. A physical device needs an appropriate reachable API address and signing team; Release must use HTTPS. A running API is required only for requested integration, never for app-only checks or mock development.

Build an unsigned Simulator app:

```sh
xcodebuild -project app/iosApp/TemplateApp.xcodeproj -scheme TemplateApp \
  -configuration Debug -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' \
  -derivedDataPath app/iosApp/build CODE_SIGNING_ALLOWED=NO build
```

Run KMP and native tests with an available Simulator, replacing the destination with one reported by `xcrun simctl list devices available`:

```sh
(cd app && ./gradlew :shared:iosSimulatorArm64Test)
xcodebuild -project app/iosApp/TemplateApp.xcodeproj -scheme TemplateApp \
  -configuration Debug -sdk iphonesimulator \
  -destination 'platform=iOS Simulator,name=iPhone 18 Pro,OS=27.0' \
  -derivedDataPath app/iosApp/build CODE_SIGNING_ALLOWED=NO test
```

The versioned project builds without XcodeGen. Edit `app/iosApp/project.yml` only to change target settings, then run `xcodegen generate --spec app/iosApp/project.yml` with [XcodeGen 2.46.0](https://github.com/yonaskolb/XcodeGen/releases/tag/2.46.0).
