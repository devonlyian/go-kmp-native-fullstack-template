# 백엔드 설정

[English](setup.md) | [한국어](setup.ko.md)

명령은 저장소 루트에서 실행한다. `backend/go.mod`가 선언한 Go 버전, Compose가 포함된 Docker, Python 3를 설치한다. Docker는 로컬 PostgreSQL 서비스만 실행하고 Python은 구조 검사에 쓴다.

SHA-256 검증을 거쳐 고정된 Atlas v1.3.0을 로컬에 설치한다.

```sh
./tools/install-atlas.sh
```

로컬 데이터베이스가 필요하면 환경 파일이 없을 때만 만들고 PostgreSQL을 시작한다.

```sh
test -f .env || cp .env.example .env
docker compose up -d --wait
```

`.env.example`의 비밀번호는 공개된 로컬 개발용 값이며 운영에서 절대 사용하지 않는다. Compose는 PostgreSQL을 loopback에 바인딩한다. 다음: [API 실행](run.ko.md) 또는 [데이터베이스 변경](database.ko.md).
