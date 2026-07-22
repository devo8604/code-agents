---
name: secure-system-iteratively
description: Coordinate a bounded audit-remediate-re-audit loop for an entire software repository or explicitly scoped path. Use when the user wants Codex to discover security findings, implement safe fixes, verify them independently, and repeat until the authorized scope converges or a defined blocker is reached. Do not use for audit-only reporting, fixing only preselected findings, penetration testing, production mutation, formal compliance certification, or open-ended hardening without a stable scope.
---

# Secure System Iteratively

Compose `$audit-system-security` and `$remediate-security-findings` into a
convergent security-improvement loop while preserving audit independence.

## Establish the loop contract

1. Resolve the repository root, comparison base, exact `audit_scope`, applicable
   instructions, exclusions, generated or vendored paths, target environment,
   and current worktree state. Separately resolve exact
   `remediation_write_scope`; audit coverage never grants write authority.
   Preserve unrelated user changes.
2. Treat invocation of this skill as authorization to edit repository files and
   run safe local verification only within `remediation_write_scope`. Default the
   remediation set to every validated in-scope finding that can be fixed without
   new authority.
3. Do not infer authorization for breaking public-contract changes, production
   access, live exploitation, external scanning, secret access, deployment,
   release, migration application, cloud or database mutation, credential
   rotation, third-party disclosure, or scope expansion.
4. Preserve stable public API, client, MCP, protocol, configuration, command,
   event, model-interface, and data contracts. Stop for explicit approval when a
   validated finding has no compatible remediation and requires a breaking
   change with versioning, deprecation, migration, compatibility-window,
   consumer, and rollback plans.
5. Define convergence as an independent final audit finding no validated,
   remediable security issue within `audit_scope`. This means no findings
   were found under the stated methods and limitations; it never proves the
   system secure, compliant, certified, or authorized. Convergence is prohibited
   while any required documentation claim is unresolved, stale, expired,
   invalid, or mismatched to the target; record that condition as blocked.
6. Read applicable `AGENTS.md` files and consume the project agent-routing
   matrix. Resolve available roles, project overrides, independence, and actual
   read/write capability before assignment; record unavailable roles and routed
   substitutions.
7. Initialize [the security iteration record](references/security-iteration-record.md).
   Use its safe default iteration, finding, elapsed-time, and cumulative-file
   budgets unless the user or project sets stricter limits. Use a token budget
   only when the user explicitly supplies one. Before remediation, persist the
   record at its project-approved path or in the parent orchestration ledger;
   conversational state alone cannot authorize resume or convergence.

## Run the loop

Maintain the security iteration record with stable finding IDs, canonical
root-cause keys, comparison bases, predecessor relationships, both scopes,
budgets, severity, disposition, owners, changed files, tests, contract impact,
residual risk, approval references, checkpoints, and resume conditions.

1. **Audit:** Invoke `$audit-system-security` read-only against the current tree.
   Require concrete attack paths and deduplicate findings by root cause. Keep the
   primary audit independent from implementation ownership.
2. **Classify:** Partition findings into:
   - authorized and remediable now;
   - already fixed, duplicate, invalid, or human-approved accepted risk;
   - blocked by missing evidence, ownership, compatibility approval, external
     action, or scope.
   Do not silently treat a blocked finding as remediated.
   Keep risk acceptance proposed until an accountable human owner and approval
   reference exist. A finding requiring writes outside
   `remediation_write_scope` is a blocked follow-up.
3. **Plan the batch:** Select the smallest dependency-ordered batch that can be
   implemented and verified coherently. Baseline each attack path safely. Assign
   each file, public contract, schema, migration, lockfile, and generated artifact
   to one writer only; keep audit and final security validation read-only.
4. **Remediate:** Invoke `$remediate-security-findings` for the selected batch.
   Require root-cause fixes, focused regression tests that fail without the fix,
   compatibility classification, proportionate broader verification, and a
   handoff for every finding. Do not absorb unrelated hardening.
   Route delivery-pipeline, build, policy, provenance, scanner, and promotion
   findings through `$implement-devsecops-controls` and `devsecops_engineer`;
   this does not authorize hosted reruns, repository-setting changes, releases,
   deployments, credentials, or cloud mutations.
5. **Validate:** Have an independent `security_engineer` re-trace every original
   attack path, attempt relevant bypasses safely, inspect affected adjacent sinks,
   and review the final diff for newly introduced security defects. Re-run normal
   behavior, regression, contract, and documentation checks. Prefer a
   capability-read-only role. When it has workspace-write tools, do not describe
   instructions as enforced read-only: inspect for mutations and report the
   residual limitation.
6. **Re-audit:** Invoke `$audit-system-security` again on the updated current tree.
   Include the full authorized scope, while prioritizing changed boundaries,
   alternate sinks, and unresolved findings. Compare results by stable ID,
   canonical root-cause key, predecessor, and comparison base. Qualifying
   independent gate evidence may be reused under the record rules, but never to
   narrow or replace this final full-scope independent audit.
7. **Decide:**
   - Finish when the independent re-audit meets the convergence definition.
   - Continue with the next authorized batch when validated remediable findings
     remain and the previous cycle made measurable progress.
   - Stop and request direction when only blocked findings remain, a required
     action exceeds authority, or remediation would break a public contract.
   - Stop as blocked when the required independent security reviewer is
     unavailable after a reasonable bounded attempt. Report completed local
     verification, but do not substitute the implementation owner's self-review
     for independent validation or claim convergence.
   - Stop as non-convergent when the same root cause survives two consecutive
     remediation attempts, a completed cycle produces no net risk reduction, or
     fixes repeatedly introduce equivalent findings. Report the evidence and the
     decision needed instead of looping indefinitely.
   - Stop as blocked before an iteration, finding, elapsed-time, explicit token,
     or cumulative-file budget is exceeded. Record the next dependency-ready
     action and exact resume condition.

## Evidence and safety

- Invoke `$verify-current-documentation` for material version-, provider-,
  protocol-, Region-, partition-, model-, or configuration-sensitive claims.
  Validate `.codex/documentation-evidence.json` whenever a required finding or
  remediation decision depends on such a claim.
- Limit proof payloads to isolated fixtures, test harnesses, or in-memory
  resources under the user's scope. Never exercise them against live services,
  production data, external targets, or third-party systems.
- Run narrow tests after each batch and broader verification before re-audit.
  Never weaken assertions, disable security controls, hide diagnostics, or
  suppress scanners merely to make the loop converge.
- If the scope is too large for one safe batch, keep the scope stable and process
  dependency-ordered batches; do not redefine convergence around only the files
  already changed.
- Checkpoint after every audit, classification, remediation batch, validation,
  and re-audit. Resume from the last completed checkpoint without discarding
  history or rerunning qualifying evidence unless its comparison base, scope,
  boundary, independence, or freshness changed.

## Handoff

Report the convergence status first: converged, blocked, or non-convergent. Then
summarize each iteration, findings fixed and remaining, files changed, tests and
results, attack-path validation, newly introduced or recurring findings, public-
contract impact, documentation evidence, rollout and rollback considerations,
budget consumption and last checkpoint, residual risks, unreviewed surfaces, and
actions requiring separate authority.
