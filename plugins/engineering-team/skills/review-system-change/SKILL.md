---
name: review-system-change
description: Independently review a complex software change for correctness, security, compatibility, data integrity, operability, test coverage, and cross-boundary regressions. Use for pull requests, branches, working-tree changes, migrations, API or client contract changes, MCP tools, data workflows, containers, and AWS GovCloud infrastructure. Review only unless the user explicitly asks to address findings.
---

# Review System Change

Review the changed behavior as a system, not as an isolated diff.

## Workflow

1. Establish the comparison base, intended outcome, acceptance criteria,
   repository guidance, project agent-routing matrix, and verification already
   performed. Use routing evidence to select specialist reviewers for boundaries
   that actually changed.
2. Map changed files to behavior and boundaries using
   [references/review-checklist.md](references/review-checklist.md). Read enough
   surrounding code and tests to reconstruct the real execution path.
3. Delegate independent read-only passes when relevant:
   - `quality_engineer` for application correctness and test gaps.
   - `data_engineer` for schema, migration, workflow, and recovery risks.
   - `govcloud_engineer` for partition, IAM, network, encryption, service
     availability, deployment, and compliance assumptions.
   - `security_engineer` for threat modeling, application and supply-chain
     security, control mapping, and evidence quality.
   - `ux_engineer` for read-only user-flow, interaction, content, usability, and
     accessibility review.
   - `docs_researcher` for version match, primary-source authority, freshness,
     deprecations, and conflicting documentation.
   - `technical_writer` for documentation accuracy, audience fit, examples,
     terminology, and missing migration or usage guidance.
   Use scoped reviewer agents when custom roles are unavailable. Wait for all
   passes, verify their findings, and remove duplicates.
4. Check shared contracts end to end: server schema, client surface, MCP tool,
   persistence model, errors, authorization, compatibility, and rollout states.
   Compare the before and after public surface, including signatures, schemas,
   required fields, errors, defaults, names, and semantics. Treat an unapproved
   breaking change as blocking even when tests were updated to accept it.
5. Validate `.codex/documentation-evidence.json` when the change depends on
   external versioned or volatile behavior. Treat missing, stale, inferred,
   unresolved, secondary-only, or target-mismatched required claims as blocking.
6. Run or inspect the narrowest meaningful verification. Do not claim coverage
   from tests that do not exercise the changed behavior.
7. Confirm user README content, developer docs, examples, docstrings, comments,
   and release or migration guidance match the shipped behavior. Run the
   bundled portable-documentation validator and treat user-specific absolute
   home paths as blocking documentation defects.
8. Reject speculative findings. A finding must identify a concrete failure mode,
   affected behavior, and supporting evidence.

## Output

Lead with findings ordered by severity. For each finding include location,
failure mode, impact, evidence or reproduction, and the smallest defensible
remediation. Then list open questions, test gaps, and residual risks. If there
are no findings, say so and state what was reviewed and what could not be
verified. Report public-contract compatibility and approval status explicitly.
Do not edit files while using this skill unless asked to address the findings.
