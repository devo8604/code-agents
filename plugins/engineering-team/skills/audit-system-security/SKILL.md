---
name: audit-system-security
description: Perform a read-only, evidence-backed security audit of an entire software repository or an explicitly scoped path. Use for application, API, AI/ML, MCP, data, dependency, supply-chain, container, infrastructure-as-code, CI/CD, secrets-handling, and operational security assessments when the user wants findings and remediation guidance rather than fixes, penetration testing, compliance certification, or review of only a Git diff.
---

# Audit System Security

Audit plausible attack paths across the resolved scope and report only findings
supported by repository or authorized external evidence.

## Entry criteria

1. Resolve the repository root, comparison base, and `audit_scope`. Default to
   the whole repository only when no narrower boundary is named. Keep it distinct
   from any `remediation_write_scope`; audit coverage never authorizes edits.
2. Read applicable repository instructions. Record exclusions, generated or
   vendored paths, target environments, data classifications, verification
   constraints, and the project `AGENTS.md` agent-routing matrix. Resolve actual
   role availability and project overrides before delegating.
3. Confirm the request permits only read-only analysis. Do not exploit systems,
   access secrets, scan external targets, create persistence, or mutate code,
   infrastructure, cloud resources, databases, dependencies, or configuration.
4. Separate this audit from Git change review, failure diagnosis, remediation,
   and formal compliance, certification, authorization, or assessor judgment.

## Workflow

1. Inventory languages, frameworks, entry points, deployment artifacts,
   dependencies, generated code, tests, and exposed interfaces. Use
   [references/audit-checklist.md](references/audit-checklist.md) to select only
   relevant review surfaces.
2. Build an evidence-based threat model: assets, sensitive data, actors, trust
   boundaries, entry points, privileges, dependencies, and abuse cases. State
   consequential assumptions and unresolved scope gaps.
3. Establish dependency, protocol, platform, Region, partition, standard, and
   configuration versions from project evidence. Invoke
   `$verify-current-documentation` for material volatile claims and validate
   `.codex/documentation-evidence.json` when a finding, severity, or remediation
   depends on one. A missing, stale, expired, target-mismatched, or invalid
   required claim is a blocking disposition, not merely a limitation; do not
   validate the dependent candidate, severity, remediation, or gate until the
   evidence is resolved.
4. Use the resolved routing matrix to select independent passes only where the
   scope warrants them: `security_engineer` for threat-led audit;
   `ai_ml_engineer` for AI/ML and MCP; `data_engineer` for data boundaries;
   `govcloud_engineer` for GovCloud; and `docs_researcher` for primary evidence.
   Prefer capability-read-only roles. A prompt does not capability-enforce
   read-only operation for a workspace-write specialist: constrain the task,
   inspect the worktree afterward, and report that residual limitation. If a
   required role is unavailable, use a routed read-only substitute and record it
   or mark the surface unreviewed. Delegation never authorizes external scans,
   production access, or mutation.
5. Trace candidates from attacker-controlled or compromised sources to security
   sinks. Verify reachability, protections, preconditions, assets, and impact.
   Use safe local non-destructive tests only when material. Keep proof payloads
   in isolated fixtures, test harnesses, or memory; never exercise live services,
   production data, external targets, or third parties.
6. Reject keyword-only, dependency-age, generic-best-practice, and implausible
   misuse findings. Record uncertain concerns as open questions.
7. Maintain the fields in
   [the security iteration record](../secure-system-iteratively/references/security-iteration-record.md).
   Assign each finding a stable ID and canonical root-cause key; record its
   comparison bases and predecessor relationships; deduplicate on that key.
   Calibrate severity from exploitability, privileges, exposure, blast radius,
   data sensitivity, and controls rather than tool output alone.
8. Recommend the smallest compatible remediation, verification tests, and
   residual risk. Do not edit files without a separate request. Treat risk
   acceptance only as proposed until an accountable human and approval reference
   are recorded. Findings outside a supplied write scope are blocked follow-ups.

## Output

Lead with validated findings ordered by severity. For each include stable ID,
canonical root-cause key, title, severity, comparison base, predecessors, exact
location, source-to-sink path, preconditions, impact, evidence, controls,
remediation, verification test, confidence, disposition, and residual risk.

Then report both scopes when known, threat-model summary, methods and commands,
routing and reviewer capability limitations, documentation evidence, open
questions, unreviewed surfaces, and test limitations. If no finding survives,
say so without claiming the system secure. Distinguish guidance, implemented
controls, assessment evidence, and formal compliance or certification.
