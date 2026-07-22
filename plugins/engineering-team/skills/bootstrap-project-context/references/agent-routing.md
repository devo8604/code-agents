# Project agent routing

Derive routing from repository evidence. Include only relevant rows in the
project's root `AGENTS.md`; do not copy this generic catalog wholesale.

## Routing matrix format

Use a compact table with these columns:

| Task signal | Primary role | Supporting or reviewer roles | Ownership boundary | Required evidence |
| --- | --- | --- | --- | --- |

Follow the table with:

- roles deliberately excluded or unavailable and why;
- sequencing and file-ownership constraints;
- triggers that require independent review or current documentation research;
- project-specific overrides and their evidence;
- external actions that remain separately authorization-gated.

The matrix guides role selection; it does not grant edit authority, external
access, deployment permission, migration approval, or permission to break public
contracts. Validate the task's actual scope against the matrix on every use.

## Role signals

| Verified project signal | Primary role | Typical independent support |
| --- | --- | --- |
| Cross-boundary architecture, contracts, or sequencing | `system_architect` read-only | Relevant boundary owners |
| Service routes, authorization, validation, or API schemas | `api_engineer` | `quality_engineer`, `security_engineer` |
| Public Python package, client API, packaging, or ergonomics | `client_engineer` | `quality_engineer` |
| Models, evaluation criteria, inference, retrieval semantics, or MCP protocol/server adapters | `ai_ml_engineer` | `data_engineer`, `security_engineer`, `quality_engineer` |
| UI components, responsive behavior, styles, or frontend tests | `ui_engineer` | `ux_engineer`, `quality_engineer` |
| User flows, information architecture, usability, content, or accessibility | `ux_engineer` read-only | `ui_engineer` for approved implementation |
| Database schemas, persistence, ingestion execution, migrations, backfills, pipeline operations, or lineage | `data_engineer` | `ai_ml_engineer` for model/retrieval contracts; `quality_engineer`, `security_engineer` |
| AWS GovCloud infrastructure, IAM, network, encryption, or delivery design | `govcloud_engineer` | `security_engineer`, `docs_researcher` |
| Threat modeling, security audit, control mapping, or remediation validation | `security_engineer` read-only | Assigned implementation owner |
| Version-, date-, Region-, partition-, or configuration-sensitive claims | `docs_researcher` read-only | Boundary owner consuming the evidence |
| Standalone user or developer documentation and examples | `technical_writer` | Relevant implementation owner |
| Independent correctness, compatibility, operability, and test review | `quality_engineer` read-only | Relevant specialist reviewers |

## Selection rules

1. Select the narrowest primary role whose verified boundary owns the requested
   change. Use multiple roles only when multiple boundaries materially change.
2. Assign one writer per file, public contract, schema, migration, lockfile,
   generated artifact, and standalone documentation surface.
3. Keep `system_architect`, `ux_engineer`, `security_engineer`,
   `docs_researcher`, and `quality_engineer` read-only. Route their approved
   recommendations to the assigned implementation owner.
4. Require `docs_researcher` when a material decision depends on volatile or
   version-specific external behavior. Repository evidence must identify the
   actual target before research begins.
5. Require `ux_engineer` for material user-flow or accessibility decisions and
   `ui_engineer` only when interface implementation is in scope.
6. Require `security_engineer` for changed trust boundaries, sensitive data,
   authorization, consequential tools, infrastructure exposure, or independent
   remediation validation.
7. Require `quality_engineer` for independent final review of complex integrated
   changes. Add specialist reviewers for the boundaries that changed.
8. Reuse globally installed roles. Create project-scoped overrides only when
   verified project constraints cannot be expressed in `AGENTS.md` or a
   project-scoped skill.
9. For AI/ML data work, assign model behavior, evaluation criteria, retrieval
   semantics, inference integration, and MCP adapters to `ai_ml_engineer`;
   assign persistence, ingestion execution, pipeline operations, lineage, and
   migrations to `data_engineer`. Establish their shared data contract before
   implementation and give it one owner.
