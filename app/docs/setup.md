# App setup

[English](setup.md) | [한국어](setup.ko.md)

Run commands from the repository root. Install JDK 25 LTS, Android SDK platform 37.2 and build tools 37.0.0. Use the project wrapper in `app/`.

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 25)
export ANDROID_HOME="$HOME/Library/Android/sdk"
"$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" "platforms;android-37.2" "build-tools;37.0.0"
```

For iOS, use an Apple Silicon Mac with full Xcode and an iOS Simulator SDK. The supported Kotlin targets are `iosArm64` and `iosSimulatorArm64`; Intel Simulator is unsupported. The build JDK and Kotlin toolchain are 25, Android/JVM bytecode targets 17, and the minimum iOS version is 26.

No Go, Docker, database, or running local API is required for app-only development. The shared Apollo configuration reads the root `contracts/graphql/` SDL. Develop UI and domain behavior with a contract-conforming fake repository when no endpoint is needed; use an already running GraphQL endpoint only for requested integration work.
