#!/usr/bin/env bash
set -euo pipefail
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
VERSION=1.3.0
case "$(uname -s)-$(uname -m)" in
  Darwin-arm64) platform=darwin-arm64; digest=47aaf7c295c7569c7eecfcbc53f02de862846ce1fbef16f1bd8ae98b03c3c68f ;;
  Linux-x86_64) platform=linux-amd64; digest=cfc773e5b4e845bc01d680390c174648938a7f88bf30e5a2c83ae85217c21587 ;;
  *) echo 'Install Atlas v1.3.0 from https://atlasgo.io/getting-started and set ATLAS to its executable path.' >&2; exit 1 ;;
esac
mkdir -p "$ROOT/.tools"
download=$(mktemp "$ROOT/.tools/atlas-download.XXXXXX")
trap 'rm -f "$download"' EXIT
curl --fail --location --retry 2 --max-time 180 \
  "https://release.ariga.io/atlas/atlas-$platform-v$VERSION" -o "$download"
if command -v sha256sum >/dev/null; then
  actual=$(sha256sum "$download" | cut -d ' ' -f 1)
else
  actual=$(shasum -a 256 "$download" | cut -d ' ' -f 1)
fi
[[ "$actual" == "$digest" ]] || { echo 'Atlas checksum mismatch' >&2; exit 1; }
chmod +x "$download"
mv "$download" "$ROOT/.tools/atlas"
"$ROOT/.tools/atlas" version
