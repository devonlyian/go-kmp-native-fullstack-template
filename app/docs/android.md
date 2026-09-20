# Android

[English](android.md) | [한국어](android.ko.md)

Complete [app setup](setup.md). Build and install from the repository root:

```sh
(cd app && ./gradlew :shared:generateApolloSources :androidApp:assembleDebug)
(cd app && ./gradlew :androidApp:installDebug)
adb shell am start -n com.example.template/.MainActivity
```

The current Debug endpoint is `http://127.0.0.1:8080/graphql`. For requested integration with a server on this Mac, configure forwarding after each device reconnect:

```sh
adb reverse tcp:8080 tcp:8080
```

With several devices, use `adb -s <serial>`. Android 17 / target 37 requires separate runtime permission for local-network addresses such as `10.0.2.2`, so loopback forwarding is the local integration path. Release must use a real HTTPS endpoint. A running backend is not required for app checks or mock development.

Run connected tests only with a running emulator or device:

```sh
(cd app && ./gradlew :androidApp:connectedDebugAndroidTest)
```
