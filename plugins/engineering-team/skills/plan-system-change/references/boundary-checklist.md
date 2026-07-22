# System boundary checklist

Use only the sections affected by the requested change.

## Behavior and contract

- Actor, entry point, observable outcome, acceptance criteria, and non-goals
- Input, output, validation, errors, authorization, idempotency, and concurrency
- Compatibility, deprecation, versioning, and mixed-version operation
- Ownership of the canonical schema and any generated artifacts
- Baseline or snapshot of every affected public operation, import, signature,
  tool, resource, prompt, command, configuration key, event, and schema
- Change classification: none, additive, deprecated-but-compatible, or breaking
- For a proposed break: necessity evidence, compatible alternatives rejected,
  explicit approval, affected consumers, migration, compatibility window, and
  rollback

## Database and data lifecycle

- Schema, types, constraints, keys, indexes, transactions, and isolation
- Read and write paths, data volume, hot paths, lock risk, and query plans
- Expand-and-contract migration steps and safe application ordering
- Backfill checkpoints, idempotency, throttling, reconciliation, and recovery
- Retention, deletion, lineage, audit, data quality, backup, and restore

## API service

- Routes or operations, request and response models, status and error semantics
- Authentication, authorization, tenancy, rate limits, retries, and timeouts
- Domain-service boundaries, observability, and operational failure behavior
- Contract tests and documentation generation

## Python client

- Imports, method signatures, sync or async model, types, and exceptions
- Serialization, pagination, retries, timeouts, compatibility, and ergonomics
- Supported Python versions, packaging, dependency impact, and release notes
- Unit, contract, and integration coverage

## MCP server

- Tool or resource names, descriptions, input schema, output, and error mapping
- Transport, initialization, cancellation, timeouts, and capability discovery
- Safety, authorization, sensitive data, and confirmation for consequential tools
- Reuse of the supported API client and end-to-end protocol tests

## Containers and runtime

- Build context, base image, dependency locking, user, filesystem, and secrets
- Health checks, startup ordering, graceful shutdown, resource bounds, and signals
- Image scanning, provenance, registry, configuration, and rollback

## Security and assurance

- Assets, actors, trust boundaries, data classification, threats, and abuse cases
- Authentication, authorization, tenancy, secrets, cryptography, and auditability
- Input, output, injection, deserialization, file, path, command, and network risk
- Dependency provenance, build integrity, SBOM, signing, scanning, and response
- Detection, incident response, recovery, vulnerability handling, and risk owner
- Applicable standard, exact version or baseline, mapped control, evidence, gap,
  compensating control, and residual risk
- Clear separation between engineering review and formal compliance assessment

## Documentation and developer experience

- Affected user README sections, installation, configuration, and usage examples
- Developer setup, architecture, extension points, test commands, and workflows
- API, Python client, MCP tool, schema, error, and compatibility documentation
- Release notes, upgrade or migration guidance, rollback, and operational docs
- Docstrings and comments for non-obvious intent, invariants, and failure behavior
- Documentation checks, executable examples, links, terminology, and ownership

## External documentation evidence

- Repository or user evidence for the exact installed or targeted version
- Primary source authority and exact version, Region, partition, or edition match
- Release notes or migration guidance for behavior changes near the target
- Retrieval and validity dates appropriate to source volatility
- Required claim IDs linked to dependent work packages
- Inferred, unresolved, conflicting, stale, and secondary-only claims kept out of
  implementation premises

## AWS GovCloud

- Target `aws-us-gov` Region, account boundary, credentials, ARN and endpoint use
- Current service and feature availability in the selected Region
- FIPS endpoints and cryptographic requirements
- VPC topology, private endpoints, ingress, egress, DNS, and cross-partition flow
- IAM least privilege, KMS keys, secrets, audit logs, backup, and disaster recovery
- Export-controlled data behavior and shared-responsibility assumptions
- Infrastructure-as-code plan, validation, promotion, rollback, cost, and operations

Verify material GovCloud claims against current primary AWS documentation,
including the [GovCloud differences guide](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/govcloud-differences.html),
[service availability guide](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/using-services.html),
and [service endpoints](https://docs.aws.amazon.com/govcloud-us/latest/UserGuide/using-govcloud-endpoints.html).

Verify material security mappings against current primary sources. Useful
starting points include [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/),
[NIST SSDF](https://csrc.nist.gov/pubs/sp/800/218/final),
[NIST CSF](https://www.nist.gov/cyberframework), and the applicable
[FedRAMP rules and baselines](https://www.fedramp.gov/).

## Verification and delivery

- Contract, schema, import, or snapshot tests that fail on unapproved public
  surface changes
- Tests tied to every acceptance criterion and failure mode
- Telemetry proving successful rollout and detecting partial failure
- Ordered deployment and migration steps, feature flags, and compatibility window
- Rollback versus forward-recovery decision and data consequences
- Explicit actions requiring human, compliance, security, or production approval
