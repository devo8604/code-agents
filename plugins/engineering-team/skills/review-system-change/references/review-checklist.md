# Cross-system review checklist

Prioritize changed behavior and plausible failure paths. Skip irrelevant items.

## Correctness and contracts

- Acceptance criteria map to executable behavior and tests.
- Server, client, MCP, database, and generated schemas agree.
- Validation, errors, defaults, nullability, pagination, retries, and timeouts
  remain consistent.
- Mixed old and new versions fail safely during rollout and rollback.
- Public API operations and schemas, Python imports and signatures, MCP tools and
  resources, protocols, configuration, commands, events, and externally consumed
  schemas are unchanged or additively compatible.
- Existing contract, import, schema, and snapshot tests were not merely rewritten
  to normalize an accidental breaking change.
- Every breaking change has necessity evidence, explicit user approval, affected
  consumers, versioning, deprecation, migration, compatibility-window, and
  rollback plans.

## Security and privacy

- The change identifies affected assets, actors, trust boundaries, threats, and
  abuse cases rather than relying on a generic checklist.
- Authentication and authorization occur at the correct boundary.
- Tenant, object, and action scopes cannot be confused or bypassed.
- Secrets and sensitive or regulated data avoid logs, exceptions, images,
  fixtures, telemetry, and external services.
- Consequential MCP tools have narrow schemas and appropriate confirmation.
- Dependencies, deserialization, command execution, paths, and network inputs are
  constrained.
- Build provenance, dependency updates, generated artifacts, images, and CI/CD
  permissions preserve supply-chain integrity.

## Standards and assurance

- The applicable standard, profile, baseline, and version come from project or
  accountable-owner requirements rather than reviewer assumption.
- Control mappings cite exact identifiers and distinguish implementation from
  objective evidence, assessment status, compensating controls, and residual risk.
- OWASP ASVS is used for verifiable application controls and NIST SSDF for
  secure-development practices when relevant.
- NIST CSF outcomes, NIST SP 800-53 controls, and FedRAMP baselines are used only
  at the appropriate organizational or authorization boundary.
- Review language does not claim certification, authorization, or compliance;
  formal conclusions remain with accountable owners and assessors.

## Database and data workflows

- Constraints encode invariants and indexes support changed access patterns.
- Migration ordering supports mixed versions and realistic data volume.
- Backfills are bounded, resumable, idempotent, observable, and reconcilable.
- Transaction and concurrency behavior cannot create loss, duplication, or drift.
- Rollback or forward-recovery and backup or restore implications are explicit.

## Containers and operations

- Image builds are reproducible and run as the intended user.
- Configuration and secrets are injected safely; health checks reflect readiness.
- Shutdown, resource exhaustion, dependency failure, and retry storms are handled.
- Logs, metrics, traces, alerts, dashboards, and runbooks cover the changed path.

## Documentation

- User README installation, configuration, and examples match supported behavior.
- Developer setup, architecture, test commands, and extension guidance are current.
- API, client, MCP, schema, error, and compatibility documentation agree.
- Upgrade, migration, deprecation, rollback, and release guidance covers impact.
- Commands and safe examples are verified; links and generated docs are current.
- Paths are project-relative or use `$HOME`, `<repo-root>`, `%USERPROFILE%`, or
  `$env:USERPROFILE`; user-specific absolute home paths are rejected.
- Docstrings and comments explain durable intent and invariants without narrating
  syntax, leaking sensitive details, or contradicting the implementation.

## Documentation evidence

- Repository evidence identifies the actual or explicitly targeted dependency,
  provider, protocol, standard, Region, partition, and configuration.
- Required external claims cite fetched primary documentation for that target,
  not search snippets, secondary articles, latest-only docs, or model memory.
- Retrieval and validity dates are current for the source's volatility.
- Release notes or migration guides cover version transitions where relevant.
- The evidence ledger validates, claim IDs map to dependent work, and conflicts
  or unresolved claims are reported as blocking rather than silently assumed.

## AWS GovCloud

- Resources, endpoints, ARNs, credentials, and Regions use `aws-us-gov` correctly.
- Service and feature availability is verified for the target GovCloud Region.
- IAM, networking, encryption, FIPS, logging, backup, and recovery are explicit.
- Cross-partition or external data flow is identified and authorized.
- Compliance claims respect shared responsibility and cite a compliance owner.
- Infrastructure changes are reviewable, least privilege, and reversible.

## Verification quality

- Tests would fail without the change or regression fix.
- Failure, unauthorized, retry, concurrency, migration, and rollback paths are
  covered where risk justifies them.
- Mocks do not hide the boundary the test claims to verify.
- Manual evidence records exact commands, inputs, versions, and results.
- Skipped or unavailable checks are reported as residual risk.
