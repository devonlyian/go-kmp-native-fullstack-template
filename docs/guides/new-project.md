# Start a New Project

[English](new-project.md) | [한국어](new-project.ko.md)

This directory is the template source and its GitHub default/release branch is `main`. After the owner uploads it to GitHub, enable Settings → General → **Template repository**, then create a repository with **Use this template**. Create `dev` from `main` before feature work. The owner selects a license before public reuse.

Replace `README.md` and `README.ko.md` with the actual project description. They are user-facing overview documents, not agent instruction entrypoints. Keep development routing in [the documentation index](../index.md), AGENTS, and skills.

Replace the defaults:

| Find | Change |
| --- | --- |
| `TemplateApp` | Display name; Xcode target, scheme, and project names |
| `com.example.template` | Android namespace/applicationId, Kotlin package, iOS bundle identifier |
| `example.com/template/backend` | Go module and imports |
| `template-app`, `kmp-native-fullstack-template` | Gradle project name and repository name in documentation |
| `api.example.com` | Production HTTPS API address |

```sh
rg -n 'TemplateApp|com\.example\.template|example\.com/template/backend|template-app|kmp-native-fullstack-template|api\.example\.com' .
```

Move Kotlin package directories when changing that package. Update Xcode scheme/project names and the matching paths in `tools/verify.sh`. Do not hand-edit generated code; follow [checks](checks.md).

For product work, choose [backend development](../../.agents/skills/develop-backend/SKILL.md) or [app development](../../.agents/skills/develop-app/SKILL.md); do not load both by default. This repository creates no Figma file or Code Connect connection. Render actual screens to review text scaling, dark mode, accessibility, and differences from the approved design; mappings alone do not prove pixel accuracy.

Next: read [architecture](../architecture.md) for new-project boundary understanding.
