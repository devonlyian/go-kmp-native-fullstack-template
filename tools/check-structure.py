#!/usr/bin/env python3
"""Check the template's source-of-truth and presentation boundaries."""
from pathlib import Path
import os
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
IGNORED = {".git", ".gradle", ".kotlin", "build", "DerivedData", ".tools", ".verification"}
required = (
    "AGENTS.md", "README.md", ".env.example", "compose.yaml",
    "docs/architecture.md", "docs/features/_template.md", "docs/plans/_template.md",
    "contracts/graphql/system.graphqls", "backend/AGENTS.md", "backend/go.mod",
    "backend/gqlgen.yml", "backend/sqlc.yaml", "backend/atlas.hcl",
    "backend/cmd/api", "backend/db/schema", "backend/db/migration",
    "backend/db/query", "backend/db/generated", "backend/internal/graphql",
    "app/AGENTS.md",
    "app/design/design-system-map.yaml", "app/shared",
    "app/androidApp", "app/iosApp", "tools/verify.sh",
    ".agents/skills/plan-feature/SKILL.md", ".codex/agents/planning.toml",
    ".github/workflows/ci.yml",
)
errors = [f"Missing: {p}" for p in required if not (ROOT / p).exists()]
if (ROOT / "harness").exists():
    errors.append("Use AGENTS.md, tools/ and standard module tests instead of harness/.")

def source_files():
    for directory, directories, files in os.walk(ROOT):
        directories[:] = [name for name in directories if name not in IGNORED]
        for name in files:
            yield Path(directory) / name


for path in source_files():
    relative = path.relative_to(ROOT)
    in_contract = relative.parts[:2] == ("contracts", "graphql")
    if path.suffix in {".graphqls", ".graphql"} and not in_contract:
        if path.suffix == ".graphqls" or re.search(
            r"^\s*(?:extend\s+)?(?:type|schema|scalar|enum|interface|union|input)\s",
            path.read_text(), re.MULTILINE,
        ):
            errors.append(f"Duplicate GraphQL schema source: {relative}")
    if path.name in {"schema.json", "schema.graphql.json"} and not in_contract:
        errors.append(f"Introspection schema copy: {relative}")
    if relative.parts[:2] == ("app", "shared") and path.suffix == ".kt":
        if re.search(r"^import (?:androidx\.(?:compose|lifecycle|navigation)|platform\.(?:SwiftUI|UIKit))",
                     path.read_text(), re.MULTILINE):
            errors.append(f"Platform presentation import in shared: {relative}")
        if re.search(r"(?:ViewModel|ScreenState|Screen|Navigation)\.kt$", path.name):
            errors.append(f"Platform presentation file in shared: {relative}")

for error in errors:
    print(f"FAIL: {error}", file=sys.stderr)
if errors:
    sys.exit(1)
print("PASS: required structure, single GraphQL schema source, shared presentation boundary")
