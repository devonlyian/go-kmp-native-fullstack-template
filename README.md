# KMP Native Fullstack Template

[English](README.md) | [한국어](README.ko.md)

A minimal starting point for projects with native Android and iOS apps, shared Kotlin logic, and a Go GraphQL backend.

## What the template includes

- Android Compose and iOS SwiftUI presentations, with KMP sharing Domain/Data/Network.
- A GraphQL-first Go modular monolith with PostgreSQL and a single root SDL contract.
- A minimal `systemStatus` feature connecting the database, API, shared logic, and both apps.
- Code generation, build/test scripts, and paired English/Korean development documentation.
- Vendored [ui-ux-pro-max](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) skills under `.agents/skills/` (MIT), used by the design scope as a searchable design-intelligence reference (styles, palettes, font pairings, UX rules). Python 3 is required for its search script.

To refresh the vendored skills, install the CLI and run its updater from the repository root:

```sh
npm install -g ui-ux-pro-max-cli
uipro update            # refreshes .agents/skills/ in this repo
# or reinstall: uipro init --ai codex --force
```

Review the resulting diff before committing.

Authentication, product domains, deployment workflows, and a license are not selected by this template. Local verification does not imply production readiness or physical-device verification.

This README describes the template. In a derived repository, replace it and its Korean companion with the actual project's purpose, features, and user-facing information. Development instructions remain in `AGENTS.md`, `.agents/skills/`, and `docs/` independently of the README.
