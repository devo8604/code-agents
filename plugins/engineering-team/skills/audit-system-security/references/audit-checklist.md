# Security audit checklist

Use this checklist to route investigation. Skip surfaces absent from the scope
and prioritize end-to-end attack paths over checklist coverage.

## Architecture and exposure

- Identify assets, actors, entry points, trust boundaries, privileges, tenancy,
  sensitive data, external services, administrative paths, and failure domains.
- Trace authentication, authorization, session, object ownership, and tenant
  isolation at every exposed boundary.
- Confirm defaults, debug modes, error responses, metadata, logs, and telemetry
  do not expose sensitive state.

## Input and execution

- Trace untrusted input into interpreters, queries, templates, deserializers,
  filesystems, network clients, redirects, subprocesses, loaders, and dynamic
  imports.
- Check canonicalization, validation order, size and resource bounds, archive
  extraction, race conditions, and time-of-check/time-of-use behavior.
- Review SSRF, injection, traversal, request smuggling, unsafe parsing, and
  denial-of-service paths only where the architecture makes them plausible.

## API, MCP, and AI/ML

- Verify authorization and consequential-action confirmation for API operations
  and MCP tools; constrain schemas, capabilities, timeouts, cancellation, and
  returned data.
- Treat tool output, retrieved content, model output, prompts, and uploaded data
  as untrusted across agent and MCP boundaries.
- Check prompt injection, tool confusion, excessive agency, data exfiltration,
  unsafe model artifact loading, training or evaluation leakage, poisoned data,
  cross-user memory, and unbounded inference cost.
- Verify model and provider data retention, transmission, logging, and residency
  assumptions from authorized configuration and current primary documentation.

## Data and cryptography

- Trace sensitive data collection, minimization, validation, storage, access,
  encryption, backup, export, retention, deletion, logging, and recovery.
- Review database roles, row or tenant isolation, query construction, migration
  privileges, transaction boundaries, and backup restore authorization.
- Use supported cryptographic primitives and key management; flag custom crypto,
  hard-coded keys, nonce reuse, weak randomness, and missing rotation paths.

## Secrets, dependencies, and supply chain

- Inspect tracked files and configuration patterns for exposed credentials
  without printing secret values or broadening into unrequested history scans.
- Review dependency pinning, lockfiles, provenance, integrity verification,
  lifecycle scripts, generated artifacts, registries, and update automation.
- Evaluate a dependency issue against the resolved version, reachable feature,
  runtime environment, and compensating controls before reporting it.
- Review CI/CD token scope, untrusted pull-request execution, artifact trust,
  release permissions, branch protections represented in repository evidence,
  and build reproducibility.

## Containers, infrastructure, and operations

- Review base images, build context, runtime user, Linux capabilities, mounts,
  network exposure, health checks, resource limits, and secret injection.
- Review infrastructure as code for identity, least privilege, network paths,
  encryption, public exposure, logging, backup, recovery, and destructive drift.
- Verify cloud and GovCloud claims for the targeted Region and partition before
  treating a service or control as available.
- Check security logging, alertability, incident response, dependency failure,
  rate limiting, abuse controls, recovery, and safe rollback.

## Evidence and reporting

- Anchor every finding to an exact location and plausible attack path.
- Distinguish exploitable vulnerabilities from hardening opportunities, missing
  evidence, policy gaps, and accepted residual risk.
- Cite exact versions and control identifiers for standards mappings. Never
  equate code review or control presence with compliance or certification.
- Report unavailable tools, excluded paths, stale evidence, target mismatches,
  and untested runtime behavior as limitations.
