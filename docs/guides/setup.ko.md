# 설정

[English](setup.md) | [한국어](setup.ko.md)

하나의 범위를 선택한다. 명령은 저장소 루트에서 시작하며, 필요한 경우에만 subshell 안에서 디렉터리를 바꾼다.

- [백엔드 설정](../../backend/docs/setup.ko.md): API와 데이터베이스에 필요한 Go, Docker, PostgreSQL, Atlas.
- [앱 설정](../../app/docs/setup.ko.md): Android, iOS, shared KMP 작업에 필요한 JDK, Android SDK, Xcode.

두 범위는 `contracts/graphql/`의 GraphQL SDL 하나를 함께 사용한다. 로컬 end-to-end 통합이 명시적으로 필요할 때만 둘 다 설정하고 실행한다.
