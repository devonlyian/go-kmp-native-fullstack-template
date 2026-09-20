# Android

[English](android.md) | [한국어](android.ko.md)

[앱 설정](setup.ko.md)을 마친다. 저장소 루트에서 빌드하고 설치한다.

```sh
(cd app && ./gradlew :shared:generateApolloSources :androidApp:assembleDebug)
(cd app && ./gradlew :androidApp:installDebug)
adb shell am start -n com.example.template/.MainActivity
```

현재 Debug endpoint는 `http://127.0.0.1:8080/graphql`이다. 이 Mac의 서버와 통합 작업을 요청받은 경우 기기를 다시 연결할 때마다 포워딩을 설정한다.

```sh
adb reverse tcp:8080 tcp:8080
```

여러 기기에서는 `adb -s <serial>`을 사용한다. Android 17 / target 37은 `10.0.2.2` 같은 로컬 네트워크 주소에 별도 런타임 권한이 필요하므로 로컬 통합에는 loopback 포워딩을 사용한다. Release는 실제 HTTPS endpoint를 사용해야 한다. 앱 검사와 mock 개발에는 실행 중인 백엔드가 필요 없다.

실행 중인 emulator 또는 기기가 있을 때만 connected test를 실행한다.

```sh
(cd app && ./gradlew :androidApp:connectedDebugAndroidTest)
```
