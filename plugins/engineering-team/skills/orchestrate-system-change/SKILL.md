---
name: orchestrate-system-change
description: Execute an approved output from $plan-system-change through iterative implementation, integration analysis, security auditing, remediation, and final verification. Use when a complex cross-system plan is ready to deliver and the user wants one orchestrator to coordinate $deliver-system-change, $review-system-change, and $secure-system-iteratively until acceptance, quality, and security convergence or a defined blocker. Do not use when no executable plan exists, for a narrow local edit, or to authorize deployments, releases, production mutations, migrations, breaking contracts, or external communications.
---

# Orchestrate System Change

Consume an approved system-change plan and drive bounded vertical slices through
implementation, independent analysis, and security convergence.

## Validate the execution contract

1. Resolve the repository root, applicable instructions, plan artifact or prior
   `$plan-system-change` output, approval status, target environment, exclusions,
   project agent-routing matrix, and current worktree state. Preserve unrelated
   user changes. Use routing evidence to select slice owners and reviewers, but
   revalidate it against each slice's actual boundaries.
2. Require the plan to define outcome and acceptance criteria, verified current
   state, proposed contracts and compatibility, ordered work packages and
   ownership, verification, rollout and recovery, documentation evidence, risks,
   assumptions, open decisions, and non-goals. Return to `$plan-system-change`
   when a missing item would materially change implementation.
3. Confirm required decisions and documentation claims are ready. Do not execute
   work that depends on stale, inferred, unresolved, secondary-only, expired, or
   target-mismatched evidence.
4. Treat invocation as authorization to edit plan-scoped repository files and run
   safe local verification. Do not infer authority to deploy, release, publish,
   apply migrations, mutate cloud or database resources, rotate credentials,
   access production, scan external targets, or communicate externally.
5. Preserve stable public API, client, MCP, protocol, configuration, command,
   event, model-interface, and data contracts. Stop before an unapproved break;
   do not reinterpret plan approval as approval for a newly discovered breaking
   change.

## Initialize orchestration

1. Convert the approved work graph into dependency-ordered vertical slices that
   each produce observable, testable behavior. Keep contract-first and shared-
   schema work sequential; parallelize only independent file and contract
   ownership.
2. Create the execution ledger defined in
   [references/orchestration-ledger.md](references/orchestration-ledger.md). Map
   every acceptance criterion, plan package, file set, public contract,
   documentation claim, verification command, reviewer, and rollback action.
   For every multi-phase or resumable run, persist it at a project-approved
   `.codex` path; response-only or in-memory state is never authoritative.
   Validate its append-only digest chain and receipts before resuming.
3. Set every plan item to pending, in progress, completed, blocked, or superseded.
   Allow only one integration slice to be in progress even when its independent
   work packages run concurrently.

## Execute each slice

Repeat this cycle for the next dependency-ready slice:

1. **Implement:** Invoke `$deliver-system-change` with only the approved slice.
   Give each implementation agent exact outcome, inputs, ownership, exclusions,
   dependencies, acceptance criteria, public-contract impact, evidence, tests,
   and handoff. Assign each file, migration, schema, lockfile, generated artifact,
   and public contract to exactly one writer.
2. **Integrate:** Inspect every handoff and diff centrally. Resolve ownership
   boundaries, run focused tests, then execute the slice's broader verification.
   Do not mark plan items complete from agent reports alone.
3. **Analyze:** Invoke `$review-system-change` independently against the slice's
   comparison base and acceptance criteria. Classify each validated finding as
   blocking, authorized to fix, human-approved accepted risk, duplicate,
   invalid, or requiring a plan or authority decision. Risk acceptance requires
   a named accountable owner and approval receipt in the gate record. A
   read-only review already returned by
   `$deliver-system-change` may satisfy this gate only when it is independent of
   every slice writer, covers the same integrated comparison base and acceptance
   criteria, and provides the full `$review-system-change` evidence; otherwise
   run a separate review.
4. **Correct:** Route authorized non-security findings through a bounded
   `$deliver-system-change` correction package. Re-run affected verification and
   `$review-system-change` until no validated blocking correctness,
   compatibility, data-integrity, operability, test, or documentation finding
   remains. Keep reviewers read-only and separate from implementation ownership.
5. **Secure:** Invoke `$secure-system-iteratively` with separate `audit_scope`
   (the slice's changed surfaces and every affected trust boundary) and
   `remediation_write_scope` (only plan-authorized writable paths). Never infer
   one scope from the other. Let it audit, remediate, validate,
   and re-audit until converged, blocked, or non-convergent. Propagate its
   authority limits; never let security remediation silently expand plan scope
   or break a public contract.
6. **Re-analyze:** Invoke `$review-system-change` on the integrated post-security
   state and rerun the slice verification matrix. Address regressions through the
   same correction and security paths rather than direct untracked edits.
7. **Close the slice:** Mark the slice complete only when its acceptance criteria
   have objective evidence, required review findings are closed or explicitly
   accepted, security has converged, public-contract status is approved, and
   rollback or forward recovery remains viable.

## Control the outer loop

- Continue with the next dependency-ready slice while the preceding slice is
  closed and measurable progress was made.
- Update the ledger after every implementation, review, security, and
  verification phase using append-only transitions. Never discard or rewrite
  superseded evidence or unresolved findings. Missing or invalid gate/command
  receipts fail closed.
- Configure safe positive limits for iterations, distinct root-cause findings,
  elapsed execution time, and cumulative unique changed files from the approved
  plan or user. Unless the plan or user sets stricter limits, default to five
  correction/security iterations per slice, 25 distinct findings, 120 elapsed
  minutes, and 50 cumulative changed files. Use a token budget only when the
  user explicitly supplies one. At a limit, persist a checkpoint and request
  user direction before doing more work. Do not reset budgets when findings are
  renamed, iterations restart, or work resumes.
- Adapt sequencing or split a package when repository evidence supports the same
  approved outcome and contracts. Return to `$plan-system-change` and request
  approval when new evidence changes architecture, scope, acceptance criteria,
  public contracts, migration strategy, security boundary, or rollback.
- Stop as blocked when required evidence, ownership, approval, external action,
  independent review, or a dependency is unavailable. Report completed safe
  work; do not substitute implementer self-review for required independence.
- Stop as non-convergent when the same root cause survives two correction cycles,
  a full cycle produces no measurable progress, fixes repeatedly introduce
  equivalent findings, or implementation and plan premises remain inconsistent.
  Return the smallest decision or plan revision needed.

## Final convergence

After all slices close:

1. Run the complete plan verification matrix across integrated boundaries,
   including normal, invalid, unauthorized, failure, concurrency, migration,
   rollback, user-facing, contract, and documentation paths as applicable.
2. Invoke `$review-system-change` independently over the complete plan diff and
   address validated findings through the established correction loop.
3. Invoke `$secure-system-iteratively` over the full plan-authorized system scope,
   with audit and remediation-write scopes still distinct, not only files
   changed in the last slice. Re-run whole-plan review and tests
   after any security remediation.
4. Declare convergence only when every acceptance criterion and work package is
   complete, required evidence validates, independent review has no unresolved
   blocking finding, security converges, public contracts have approved status,
   and rollout and rollback plans match the integrated result.
   Reuse matching fresh child gate records by ID rather than duplicating them,
   but always require final whole-plan review and security gate records.

## Handoff

Lead with completed, blocked, or non-convergent. Report plan identity and approval,
slice and work-package status, delivered behavior, files changed by owner,
contracts and compatibility, migrations or infrastructure artifacts, review and
security iterations, findings fixed and remaining, tests and results,
documentation evidence and expiry, rollout and rollback, residual risks,
unreviewed surfaces, and every action still requiring separate authorization.
Do not deploy, release, publish, apply migrations, or contact external systems.
