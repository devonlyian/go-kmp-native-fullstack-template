# 앱 설정

[English](setup.md) | [한국어](setup.ko.md)

명령은 저장소 루트에서 실행한다. JDK 25 LTS, Android SDK platform 37.2, build tools 37.0.0을 설치한다. `app/`의 프로젝트 wrapper를 사용한다.

```sh
export JAVA_HOME=$(/usr/libexec/java_home -v 25)
export ANDROID_HOME="$HOME/Library/Android/sdk"
"$ANDROID_HOME/cmdline-tools/latest/bin/sdkmanager" "platforms;android-37.2" "build-tools;37.0.0"
```

iOS는 Apple Silicon Mac, 전체 Xcode, iOS Simulator SDK를 사용한다. 지원하는 Kotlin target은 `iosArm64`, `iosSimulatorArm64`이며 Intel Simulator는 지원하지 않는다. 빌드 JDK와 Kotlin toolchain은 25, Android/JVM 바이트코드 target은 17, 최소 iOS 버전은 26이다.

앱 단독 개발에는 Go, Docker, 데이터베이스, 실행 중인 로컬 API가 필요 없다. shared Apollo 설정은 루트 `contracts/graphql/` SDL을 읽는다. endpoint가 필요 없으면 contract를 따르는 fake repository로 UI와 domain 동작을 개발하고, 통합 작업을 요청받은 경우에만 이미 실행 중인 GraphQL endpoint를 사용한다.
