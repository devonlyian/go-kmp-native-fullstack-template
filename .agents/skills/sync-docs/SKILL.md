---
name: sync-docs
description: Maintain paired English and Korean Markdown documentation in this repository whenever either version is created, edited, renamed, or deleted, including AGENTS.md and project skill documents.
---

# Sync documentation

[English](SKILL.md) | [한국어](SKILL.ko.md)

English `name.md` is the agent source of truth; sibling `name.ko.md` is the user translation. Normal development reads English only. Read Korean only for translation edits/review or explicit requests; this skill is that exception, limited to affected pairs. Either language can initiate an edit; reconcile the English source and Korean companion in the same change. This applies to maintained repository Markdown, including this skill and AGENTS; build outputs, dependency caches, and local verification artifacts are excluded by `tools/check-docs.py`. User-facing conversation remains Korean.

1. Read both versions of each affected document and the relevant implementation before editing; do not load unrelated translations. Preserve equivalent meaning, commands, versions, results, and unverified limits. Do not describe old test results as newly executed.
2. Update both files in the same change. Add reciprocal language links below the title. Keep local documentation links in the same language, adjusting heading anchors; keep code paths and identifiers unchanged. Rename or delete the pair together. English `AGENTS.md` and `SKILL.md` remain the agent entrypoints.
3. Compare both finished versions for missing sections, facts, commands, and broken links. A hash check cannot judge translation quality. Do not make meaningless whitespace edits merely to satisfy the checker.
4. From the repository root, run `python3 tools/check-docs.py --record <document.md>`, accepting one or more English or Korean paths. This records reviewed hashes in `docs/.translations.json` and refuses an existing pair if only one language changed. Record each rename separately, passing both its old and new paths; for paired deletion, pass the removed English path. Never edit hashes by hand or record an unreviewed translation.
5. Run `./tools/verify.sh structure`, which also runs the sync check and its tests. If a commit is requested, include both documents and the manifest. Report content changes and checks; this skill does not authorize commits or pushes.

For example, after updating both development-index versions:

```sh
python3 tools/check-docs.py --record docs/index.md
./tools/verify.sh structure
```

Do not add a translation API, file watcher, or machine-specific hook. The project instructions trigger paired editing; the existing CI structure check rejects missing files or content changed since the last recorded review. Future Markdown files must also have a reviewed pair.
