#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$ROOT"
MODE=${1:-all}
SKIPPED=0
case "$MODE" in all|structure|backend|app|ios) ;; *) echo "Usage: $0 [all|structure|backend|app|ios]" >&2; exit 2 ;; esac

skip() {
  printf '\nSKIP: %s\nInstall/configure: %s\nNot run: %s\n' "$1" "$2" "$3"
  SKIPPED=$((SKIPPED + 1))
}
run() { printf '\nRUN: %s\n' "$*"; "$@"; }

if [[ "$MODE" == all || "$MODE" == structure ]]; then
  if command -v python3 >/dev/null; then
    run python3 tools/check-structure.py
    run python3 tools/check-docs.py
    run python3 -m unittest discover -s tools -p 'test_*.py'
  else
    if [[ "$MODE" == structure ]]; then
      echo 'FAIL: Python 3 is required for structure and documentation checks.' >&2
      exit 1
    fi
    skip 'Repository structure and bilingual documentation' 'Python 3' 'python3 tools/check-structure.py && python3 tools/check-docs.py && python3 -m unittest discover -s tools -p "test_*.py"'
  fi
fi

if [[ "$MODE" == all || "$MODE" == backend ]]; then
  if command -v go >/dev/null; then
    (
      cd backend
      unformatted=$(gofmt -l .)
      if [[ -n "$unformatted" ]]; then printf 'FAIL: run go fmt ./...\n%s\n' "$unformatted"; exit 1; fi
      run go vet ./...
      run go test -race -count=1 ./...
      run go build ./...
    )
    # Regenerate in a disposable copy: verification never rewrites user sources.
    snapshot=$(mktemp -d "${TMPDIR:-/tmp}/template-codegen.XXXXXX")
    trap 'rm -r "$snapshot"' EXIT
    cp -R backend contracts "$snapshot/"
    (
      cd "$snapshot/backend"
      run go tool gqlgen generate
      run go tool sqlc generate
    )
    ATLAS=${ATLAS:-$ROOT/.tools/atlas}
    if [[ -x "$ATLAS" ]]; then
      (cd "$snapshot/backend" && run "$ATLAS" migrate validate --dir file://db/migration && run "$ATLAS" migrate hash --dir file://db/migration)
      if command -v docker >/dev/null && docker info >/dev/null 2>&1; then
        printf '\nRUN: Atlas migration/schema drift check in disposable PostgreSQL\n'
        drift=$(cd "$snapshot/backend" && "$ATLAS" schema diff --from file://db/migration --to file://db/schema --dev-url docker://postgres/18.6/dev --format '{{ sql . " " }}')
        if [[ -n "$drift" ]]; then echo 'FAIL: DB schema and migrations differ; generate and review a migration.' >&2; exit 1; fi
      else
        skip 'DB schema/migration drift' 'Docker Engine with PostgreSQL image access' 'cd backend && ../.tools/atlas schema diff --from file://db/migration --to file://db/schema --dev-url docker://postgres/18.6/dev'
      fi
    else
      skip 'Atlas migration checksum' './tools/install-atlas.sh (Atlas v1.3.0)' 'cd backend && ../.tools/atlas migrate validate --dir file://db/migration'
    fi
    # Exclude only the optional local server binary; cmd/api source is copied verbatim, so excluding it loses no drift coverage.
    run diff -ru --exclude=api backend "$snapshot/backend"
    if [[ -z "${TEST_DATABASE_URL:-}" ]]; then
      skip 'Live PostgreSQL integration' 'Start compose PostgreSQL; export TEST_DATABASE_URL (backend/docs/checks.md)' 'cd backend && go test -race -count=1 ./... with TEST_DATABASE_URL'
    fi
  else
    skip 'Backend format, codegen, tests, build' 'Go version declared in backend/go.mod (go.dev/dl)' 'cd backend && go fmt ./... && go tool gqlgen generate && go tool sqlc generate && ../.tools/atlas migrate validate --dir file://db/migration && go vet ./... && go test -race -count=1 ./... && go build ./...'
  fi
fi

if [[ "$MODE" == all || "$MODE" == app || "$MODE" == ios ]]; then
  # Prefer the supported JDK on macOS, independent of a newer system java.
  if [[ -z "${JAVA_HOME:-}" && -x /usr/libexec/java_home ]]; then
    JAVA_HOME=$(/usr/libexec/java_home -v 25 2>/dev/null || true)
    export JAVA_HOME
  fi
  if [[ -z "${ANDROID_HOME:-}" && -d "$HOME/Library/Android/sdk" ]]; then
    export ANDROID_HOME="$HOME/Library/Android/sdk"
  fi
fi

if [[ "$MODE" == all || "$MODE" == app ]]; then
  if command -v java >/dev/null && java -version >/dev/null 2>&1; then
    if [[ -d "${ANDROID_HOME:-${ANDROID_SDK_ROOT:-/nonexistent}}" || -f app/local.properties ]]; then
      (cd app && run ./gradlew checkKotlinFormat :shared:generateApolloSources :shared:jvmTest :androidApp:assembleDebug :androidApp:lintDebug)
    else
      skip 'KMP tests and Android build' 'Android SDK platform 37.2, build tools 37.0.0; set ANDROID_HOME (developer.android.com/studio)' 'cd app && ./gradlew checkKotlinFormat :shared:generateApolloSources :shared:jvmTest :androidApp:assembleDebug :androidApp:lintDebug'
    fi
  else
    skip 'KMP tests and Android build' 'JDK 25; set JAVA_HOME' 'cd app && ./gradlew checkKotlinFormat :shared:generateApolloSources :shared:jvmTest :androidApp:assembleDebug :androidApp:lintDebug'
  fi
fi

if [[ "$MODE" == all || "$MODE" == ios ]]; then
  if [[ "$(uname -s)-$(uname -m)" == Darwin-arm64 ]] && command -v xcodebuild >/dev/null && xcodebuild -version >/dev/null 2>&1 && java -version >/dev/null 2>&1 && xcrun --find swift-format >/dev/null 2>&1; then
    run xcrun swift-format lint --strict --recursive app/iosApp/Sources app/iosApp/Tests app/iosApp/UITests
    (cd app && run ./gradlew :shared:linkDebugFrameworkIosSimulatorArm64)
    run xcodebuild -project app/iosApp/TemplateApp.xcodeproj -scheme TemplateApp -configuration Debug -sdk iphonesimulator -destination 'generic/platform=iOS Simulator' -derivedDataPath app/iosApp/build CODE_SIGNING_ALLOWED=NO build
  else
    skip 'iOS framework and app build' 'Apple Silicon macOS, full Xcode with iOS Simulator SDK and swift-format, JDK 25' 'cd app && ./gradlew :shared:linkDebugFrameworkIosSimulatorArm64; xcodebuild -project app/iosApp/TemplateApp.xcodeproj -scheme TemplateApp -configuration Debug -sdk iphonesimulator -destination "generic/platform=iOS Simulator" -derivedDataPath app/iosApp/build CODE_SIGNING_ALLOWED=NO build'
  fi
fi

printf '\nVerification complete: %s skipped check group(s).\n' "$SKIPPED"
if [[ "${VERIFY_STRICT:-0}" == 1 && "$SKIPPED" -ne 0 ]]; then
  echo 'FAIL: VERIFY_STRICT=1 rejects skipped checks.' >&2
  exit 1
fi
