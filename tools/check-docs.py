#!/usr/bin/env python3
"""Check reviewed English/Korean Markdown pairs without a translation service."""

import argparse
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path("docs/.translations.json")
IGNORED = {
    ".git", ".gradle", ".kotlin", "build", "DerivedData", ".tools",
    ".verification", "__pycache__", ".venv", "node_modules",
}
# Vendored upstream skill bundles keep their own docs; we do not translate them.
VENDORED = (
    ".agents/skills/banner-design/", ".agents/skills/brand/",
    ".agents/skills/design/", ".agents/skills/design-system/",
    ".agents/skills/slides/", ".agents/skills/ui-styling/",
    ".agents/skills/ui-ux-pro-max/",
)


def english_path(path):
    return path[:-6] + ".md" if path.endswith(".ko.md") else path


def korean_path(path):
    return path[:-3] + ".ko.md"


def snapshot(root):
    documents = set()
    for directory, directories, files in os.walk(root):
        directories[:] = sorted(name for name in directories if name not in IGNORED)
        for name in files:
            if name.endswith(".md"):
                relative = (Path(directory) / name).relative_to(root).as_posix()
                if relative.startswith(VENDORED):
                    continue
                documents.add(relative)
    pairs, errors = {}, []
    for english in sorted({english_path(path) for path in documents}):
        korean = korean_path(english)
        missing = [path for path in (english, korean) if path not in documents]
        if missing:
            errors.append(f"Missing document: {', '.join(missing)}")
            continue
        empty = [path for path in (english, korean) if not (root / path).read_bytes().strip()]
        if empty:
            errors.append(f"Empty document: {', '.join(empty)}")
            continue
        pairs[english] = {
            language: hashlib.sha256((root / path).read_bytes()).hexdigest()
            for language, path in (("en", english), ("ko", korean))
        }
    return pairs, errors


def load_manifest(root):
    path = root / MANIFEST
    if not path.exists():
        return {}
    saved = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(saved, dict):
        raise ValueError("expected an object keyed by English document paths")
    for name, hashes in saved.items():
        if (not name.endswith(".md") or name.endswith(".ko.md")
                or Path(name).is_absolute() or ".." in Path(name).parts):
            raise ValueError(f"invalid English document path: {name}")
        if not isinstance(hashes, dict) or set(hashes) != {"en", "ko"}:
            raise ValueError(f"expected en/ko hashes for {name}")
        for digest in hashes.values():
            if (not isinstance(digest, str) or len(digest) != 64
                    or any(c not in "0123456789abcdef" for c in digest)):
                raise ValueError(f"invalid SHA-256 for {name}")
    return saved


def run(root, record=None):
    root = root.resolve()
    try:
        saved = load_manifest(root)
        current, errors = snapshot(root)
    except (OSError, ValueError) as error:
        print(f"FAIL: documentation metadata: {error}", file=sys.stderr)
        return 1

    if record is not None:
        updated = dict(saved)
        selected = set()
        for argument in record:
            path = Path(argument)
            try:
                relative = (path if path.is_absolute() else root / path).resolve().relative_to(root)
            except ValueError:
                errors.append(f"Document must be inside the repository: {argument}")
                continue
            selected.add(english_path(relative.as_posix()))
        removed = sorted(name for name in selected if name in saved and name not in current)
        added = sorted(name for name in selected if name in current and name not in saved)
        renamed = {}
        if removed and added:
            if len(removed) == len(added) == 1:
                renamed[added[0]] = saved[removed[0]]
            else:
                errors.append("Record each rename separately with its old and new paths")
        for name in sorted(selected):
            if name not in current:
                if (name in saved and not (root / name).exists()
                        and not (root / korean_path(name)).exists()):
                    updated.pop(name, None)
                else:
                    errors.append(f"No complete document pair: {name}")
                continue
            previous = saved.get(name, renamed.get(name))
            if previous:
                changed = [lang for lang in ("en", "ko") if current[name][lang] != previous[lang]]
                if len(changed) == 1:
                    errors.append(f"Only {changed[0]} changed: {name}; update and review both languages first")
                    continue
            updated[name] = current[name]
        if not errors:
            path = root / MANIFEST
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(json.dumps(updated, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print(f"RECORDED: {len(selected)} reviewed document path(s)")
    else:
        for name in sorted(set(current) | set(saved)):
            if name not in current:
                errors.append(f"Removed pair remains in {MANIFEST}: {name}; record the paired removal")
            elif name not in saved:
                errors.append(f"Unreviewed pair: {name}; review both languages and use --record {name}")
            elif current[name] != saved[name]:
                changed = ", ".join(lang for lang in ("en", "ko") if current[name][lang] != saved[name][lang])
                errors.append(f"Stale review ({changed} changed): {name}; update both languages, then --record {name}")
        if not errors:
            print(f"PASS: {len(current)} reviewed English/Korean document pairs")

    for error in errors:
        print(f"FAIL: {error}", file=sys.stderr)
    return 1 if errors else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--record", nargs="+", metavar="DOCUMENT", help="record explicitly reviewed pairs after editing both languages")
    args = parser.parse_args()
    sys.exit(run(ROOT, args.record))
