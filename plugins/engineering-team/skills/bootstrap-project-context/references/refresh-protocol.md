# Project context refresh protocol

Use this protocol when root project guidance or `.codex/` content already exists.

## Establish comparison evidence

1. Read the prior `Project context freshness` baseline from root `AGENTS.md`.
2. Record current `HEAD`, branch, dirty status, and applicable nested
   instructions. If the prior revision exists locally, inspect name-status and
   content changes from that revision to current `HEAD`, including renames and
   deletions. If it is unavailable, record that limitation and use a full scan.
3. Inspect uncommitted and untracked files separately. Do not attribute local
   work to a pulled commit or overwrite it.
4. Always rescan current manifests, entry points, packages, public contracts,
   commands, tests, CI/CD, infrastructure, documentation, and ownership evidence.
   A diff narrows attention but never replaces current-state verification.

## Reconcile durable context

Classify each existing fact as unchanged, changed, removed, uncertain, or
human-policy. Update changed facts from evidence. Remove a fact only when its
owned surface is gone or authoritative repository evidence contradicts it.
Preserve human-policy and uncertain guidance, marking conflicts for resolution.

Recompute the agent-routing matrix when packages, interfaces, data paths,
frontend surfaces, AI/ML or MCP boundaries, CI/CD, infrastructure, trust
boundaries, or ownership change. Add newly relevant roles and remove obsolete
routes only with evidence. Preserve one-writer and independent-review rules.

Invalidate or refresh documentation claims whose target version, configuration,
provider, Region, partition, dependency, or supporting source changed. Never
carry forward a previously valid claim merely because its ledger entry exists.

## Validate and report

Run documented cheap checks and toolkit validators after reconciliation. Report
the comparison range, dirty state, changed signals, files examined, context
edits, retained uncertainties, invalidated evidence, and surfaces that could not
be verified. Update the freshness baseline only after these checks complete.
