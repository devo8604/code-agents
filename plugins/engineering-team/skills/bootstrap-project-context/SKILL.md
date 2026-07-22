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
4. Build a project-specific agent-routing matrix using
   [references/agent-routing.md](references/agent-routing.md). Base routing on
   verified system boundaries, technologies, paths, public contracts, risks,
   edit authority, and required independent review. Record unavailable,
   unnecessary, and project-overridden roles; do not select agents merely
   because their templates exist.
5. Create or update the root `AGENTS.md` with the minimum durable information
   needed for future work: architecture, repository map, commands, conventions,
   verification, security boundaries, change ownership, and portable
   documentation paths. Include an `Agent routing` section containing the
   project-specific matrix and selection rules so planning, delivery, review,
   security, and orchestration skills can choose roles from repository evidence.
   Require repository-relative paths, `$HOME`,
   `<repo-root>`, or the appropriate Windows home variable instead of
   user-specific absolute home paths. Record public contract ownership,
   compatibility promises, baselines, and the rule that breaking changes require
   necessity evidence, explicit user approval, and migration planning.
6. Add `.codex/config.toml` only when the repository does not already express
   equivalent agent settings. Use
   `../../templates/project/.codex/config.toml` as a baseline, then preserve any
   project settings already present.
7. Inspect whether the needed roles are already registered in user-level Codex
   configuration. Reuse global roles when available. Select only relevant
   templates from `../../templates/custom-agents/` and copy them into
   `.codex/agents/` only when the user requests project-scoped roles or verified
   repository constraints require an override. Do not install personal agents
   or replace same-named files without explicit approval. Include
   `docs_researcher` when work depends on external versioned or rapidly changing
   systems.
8. Tailor agent descriptions and instructions only when repository evidence
   justifies a project-specific constraint. Keep reusable behavior in the
   template.
9. Create `.codex/documentation-evidence.json` from
   `../verify-current-documentation/assets/documentation-evidence.json` when the
   project has material version-sensitive external dependencies. Populate known
   claims through `$verify-current-documentation`; do not leave required claims
   implied or falsely verified. When authorized primary-source access is
   unavailable, create the empty bootstrap ledger, record each unresolved
   required claim and its blocked dependent work explicitly in `AGENTS.md`, and
   validate with `--allow-empty`. Do not fabricate or downgrade a required claim
   merely to satisfy the schema. Populate it and validate without `--allow-empty`
   as soon as evidence access is available.
10. Validate TOML syntax, skill paths, documented commands, agent-routing role
   names and ownership boundaries, and instruction
   precedence. Run the bundled portable-documentation validator on changed
   documentation. Run cheap read-only checks first; do not run destructive
   setup, migrations, deployment, or release commands. Document an evidence-
   validator command only when its executable project-relative or installed
   plugin path is known; otherwise record the command location as unresolved
   instead of committing a non-executable placeholder.

## Output

Report the files created or updated, the evidence used, commands validated,
detected task signals, selected and excluded agent roles with reasons, routing
and ownership boundaries, independent-review requirements, unresolved project
questions, and recommended next workflow. Include documentation sources and
unresolved required claims. Keep project secrets and proprietary details in the
target repository.
