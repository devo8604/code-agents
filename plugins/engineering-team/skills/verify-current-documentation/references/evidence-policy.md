# Documentation evidence policy

## Source precedence

1. Repository evidence establishes the installed or explicitly targeted version,
   Region, partition, edition, feature flags, and configuration.
2. Primary documentation for that exact target establishes external behavior.
3. Primary release notes and migration guides establish version transitions.
4. Vendor-maintained source or tests may resolve gaps when documentation is
   silent, but record that inference explicitly.
5. Secondary sources and search results may locate primary material but do not
   prove a required claim.
6. Model training knowledge may suggest a hypothesis but never counts as evidence.

For private facts, use authorized repository files, MCP servers, or connectors.
Do not send private content to public search or substitute public sources for
internal policy.

## Required claim fields

- `id`: stable lower-case identifier.
- `claim`: the external fact that changes a decision.
- `required`: whether dependent work must stop if the claim is not verified.
- `project_evidence`: repository or user evidence establishing the target.
- `target`: product plus version and any relevant Region or partition.
- `source`: primary URL, title, document version, retrieval date, validity date,
  exact section, authority evidence, target-match evidence, volatility class,
  and freshness rationale.
- `evidence`: concise paraphrase of what the source establishes.
- `decision`: how the evidence affects the plan or implementation.
- `confidence`: `verified`, `inferred`, or `unresolved`.

## Freshness

Set `valid_until` deliberately:

- Use a short window for service availability, cloud Region capability, active
  security advisories, pricing, quotas, previews, and current product limits.
- Use a medium window for living vendor guides, SDK behavior, provider resources,
  and framework configuration.
- Use a longer window for immutable versioned specifications, archived release
  documentation, and standards whose exact revision is pinned.
- Re-check immediately when repository versions, target environment, feature
  flags, or authoritative documentation changes, even if the date has not expired.

Classify each source as `rapid`, `living`, `versioned`, or `immutable`. The
validator defaults those classes to maximum validity windows of 30, 120, 400,
and 1100 days respectively. A longer interval requires a non-empty
`validity_exception` that a reviewer can challenge. Use the shortest defensible
class; a permanent URL does not make its contents immutable.

The ledger validator checks dates and completeness; it cannot independently
prove that a domain is truly authoritative or that a label is accurate. Record
how source ownership was established in `authority_evidence` and how the page,
tag, archive, or service page matches the project target in
`target_match_evidence`. The researcher and reviewer must verify both claims.

## Decision rules

- Mark `verified` only when the source directly supports the claim for the exact
  target.
- Mark `inferred` when primary evidence is indirect or vendor source/tests fill a
  documentation gap.
- Mark `unresolved` when evidence is missing, conflicting, or target-mismatched.
- Block required work unless confidence is `verified` and the evidence is current.
- Do not phrase a documentation check as proof of security compliance,
  certification, production behavior, or successful deployment.
