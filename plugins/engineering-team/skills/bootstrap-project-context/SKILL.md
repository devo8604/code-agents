---
name: bootstrap-project-context
description: Inspect an existing software repository and establish durable Codex project context by creating or updating AGENTS.md, project .codex configuration, and only necessary project-specific agent overrides. Use when onboarding a repository, preparing a complex project for coordinated agent work, or correcting missing build, test, architecture, and ownership guidance. Reuse globally installed roles when available. Do not use for a one-off code change.
---

# Bootstrap Project Context

Create a small, evidence-based operating layer for Codex without inventing
project conventions or replacing useful repository guidance.

## Workflow

1. Locate the repository root and read every applicable `AGENTS.md`, project
   configuration file, contributor guide, build manifest, CI workflow, and
   existing `.codex/` or `.agents/` content.
2. Inspect the worktree before editing. Preserve unrelated changes and merge
   with existing guidance instead of overwriting it.
3. Map the project using [references/context-checklist.md](references/context-checklist.md).
   Record only verified commands and paths. Capture pinned and targeted external
   versions plus canonical primary documentation sources. Mark unresolved items
   explicitly.
4. Create or update the root `AGENTS.md` with the minimum durable information
   needed for future work: architecture, repository map, commands, conventions,
   verification, security boundaries, change ownership, and portable
   documentation paths. Require repository-relative paths, `$HOME`,
   `<repo-root>`, or the appropriate Windows home variable instead of
   user-specific absolute home paths. Record public contract ownership,
   compatibility promises, baselines, and the rule that breaking changes require
   necessity evidence, explicit user approval, and migration planning.
5. Add `.codex/config.toml` only when the repository does not already express
   equivalent agent settings. Use
   `../../templates/project/.codex/config.toml` as a baseline, then preserve any
   project settings already present.
6. Inspect whether the needed roles are already registered in user-level Codex
   configuration. Reuse global roles when available. Select only relevant
   templates from `../../templates/custom-agents/` and copy them into
   `.codex/agents/` only when the user requests project-scoped roles or verified
   repository constraints require an override. Do not install personal agents
   or replace same-named files without explicit approval. Include
   `docs_researcher` when work depends on external versioned or rapidly changing
   systems.
7. Tailor agent descriptions and instructions only when repository evidence
   justifies a project-specific constraint. Keep reusable behavior in the
   template.
8. Create `.codex/documentation-evidence.json` from
   `../verify-current-documentation/assets/documentation-evidence.json` when the
   project has material version-sensitive external dependencies. Populate known
   claims through `$verify-current-documentation`; do not leave required claims
   implied or falsely verified.
9. Validate TOML syntax, skill paths, documented commands, and instruction
   precedence. Run the bundled portable-documentation validator on changed
   documentation. Run cheap read-only checks first; do not run destructive
   setup, migrations, deployment, or release commands.

## Output

Report the files created or updated, the evidence used, commands validated,
selected agent roles, unresolved project questions, and recommended next
workflow. Include documentation sources and unresolved required claims. Keep
project secrets and proprietary details in the target repository.
