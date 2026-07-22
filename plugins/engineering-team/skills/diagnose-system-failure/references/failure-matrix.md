# Cross-system failure matrix

Use the matrix to choose discriminating checks. Do not run every check blindly.

| Boundary | Evidence to collect | Common discriminators |
|---|---|---|
| Python client | Version, arguments, serialization, timeout, exception chain | Direct API call succeeds while client call fails |
| MCP server | Tool schema, transport messages, server logs, API-client call | Client call succeeds while MCP invocation fails |
| API edge | Route match, auth context, validation, status, correlation ID | Request rejected before domain code executes |
| Domain service | Inputs, state transition, invariants, exception mapping | Unit path fails with persistence mocked or isolated |
| Database | Query, parameters, transaction, locks, constraints, plan | API reaches DB; direct controlled query reproduces |
| Data workflow | Run ID, checkpoint, retry, batch window, lineage, reconciliation | Drift aligns with partial or repeated workflow runs |
| Container | Image digest, config, user, filesystem, health, resources, signals | Local process works; built image or orchestrated run fails |
| Network | DNS, route, TLS, proxy, endpoint, security rules, timeout location | Connection fails before application receives request |
| GovCloud | Partition, Region, endpoint, ARN, credentials, service capability, FIPS | Same design works commercially but differs in `aws-us-gov` |
| Deployment | Version skew, migration state, flags, rollout events, rollback | Only mixed-version or partially promoted states fail |

## Evidence discipline

- Preserve exact timestamps, versions, image digests, request identifiers, and
  environment names.
- Redact secrets, tokens, personal data, and regulated content.
- Distinguish absence of logs from proof that code did not execute.
- Prefer a single controlled variable change per diagnostic step.
- Check clocks and correlation across services before inferring event order.
- Treat retries as possible duplication, masking, and load amplification.
- For data problems, determine whether the source is wrong, transformation is
  wrong, delivery is incomplete, or presentation is stale.
- For GovCloud, verify current service-specific behavior in primary AWS docs;
  commercial Region behavior is not proof of GovCloud behavior.

