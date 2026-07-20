# Configuration, trust, and privacy

`audiobookshelf-mcp` contains connection code and neutral capability metadata only.
Every endpoint, bearer credential, identity-provider value, trust profile, tenant
decision, and observability destination is supplied at runtime. The package does not
ship an instance profile or a customized Audiobookshelf ontology.

## Configuration boundary

The connector reads runtime values through the Agent Utilities configuration layer.
For a standalone process, inject values through its process environment. For GraphOS,
define a deployment-owned `PROVIDER_CONFIGS` entry in AgentConfig and select its neutral
name with the child declaration's `provider_profile` field. The profile carries only an
`endpoint_ref`, a `TOKEN` entry in `credential_refs`, and one `tls_profile` or
`tls_profile_ref`; GraphOS resolves them in memory and sets `AGENT_PROVIDER_PROFILE` only
for that child. No selected profile name or resolved value is packaged here.

The connection inputs are:

| Setting | Purpose | Durable value |
| --- | --- | --- |
| `AUDIOBOOKSHELF_URL` | Absolute HTTPS URL of the selected Audiobookshelf API | No packaged default; resolve at runtime |
| `AUDIOBOOKSHELF_TOKEN` | Fixed bearer credential when OIDC delegation is not active | Runtime secret only |

The standalone `mcp_config.json` example uses `env://AUDIOBOOKSHELF_URL` and
`env://AUDIOBOOKSHELF_TOKEN`. A launcher may populate those aliases directly or map
the credential alias through AgentConfig's `MCP_FLEET_SECRET_REFS` to an approved
`env://`, `vault://`, or `secret://` source. Never replace a reference with a token in
the checked-in file.

The checked-in example selects the smaller `MCP_TOOL_MODE=intent` default; the shared
runtime also supports the `condensed`, `verbose`, and `both` surfaces. The six domain
toggles (`LIBRARIESTOOL`, `AUTHORSTOOL`, `SERIESTOOL`, `PODCASTSTOOL`, `EMAILTOOL`,
and `NOTIFICATIONTOOL`) default to enabled and may be disabled by the deployment.
Network transports must also apply the authentication and authorization policy
selected for the MCP server.

## Authentication

The connector has two current authentication paths:

1. OIDC delegation exchanges the request-scoped user token through the shared RFC
   8693 implementation and creates a request-specific Audiobookshelf client.
2. Without delegation, `AUDIOBOOKSHELF_TOKEN` supplies the fixed service credential.

No token, subject, email address, endpoint, or exception body is written to logs.
Prefer delegation when the target and identity provider support it; otherwise scope
the fixed token to the smallest operational role the enabled tools require.

## TLS trust

Peer and hostname verification are mandatory. The HTTP session is configured through
`resolve_configured_tls_profile("audiobookshelf")`; there is no boolean
verification control.

System trust works without additional configuration for a standalone process. A
provider profile must explicitly select the deployment's named system-trust profile or
another approved trust profile so its TLS policy stays inseparable from its endpoint
and credential references. For a private certificate authority, keep a complete-chain
PEM bundle or mTLS material in the runtime trust store, place the catalog behind
`TLS_PROFILES_REF`, and select `TLS_PROFILE` for this connector process. Standard
`SSL_CERT_FILE` and `REQUESTS_CA_BUNDLE` values are also honored by the shared resolver.
Do not commit certificate material or machine paths, and do not disable verification
to compensate for an incomplete server chain.

## Knowledge-graph capability

The package contributes human-reviewed inputs for the central capability compiler:

- the Audiobookshelf ontology in `audiobookshelf_mcp/ontology/`;
- the neutral library source preset in `audiobookshelf_mcp/connectors/`;
- one consolidated media-operations skill and canonical prompts;
- package entry points for skills, ontology, source presets, and prompts.

The committed release-generated bundle adds an exact local tool-schema fingerprint,
signed manifest, SHACL shapes, neutral source mapping and fixture, migration ledger,
and offline source attestation. It contains no instance URL, source record, tenant
mapping, local path, or external-live claim. Regenerate and re-sign the bundle after
any tool or ontology change before governed synchronization is enabled.

The provider exposes no graph-write or raw-media-ingestion tool. GraphOS may synchronize
catalog metadata only after it compiles and verifies the exact live capability and an
operator approves tenant, ACL, classification, retention, provenance, redaction, and
deletion policy. Missing governance must fail closed rather than widening access.

## Observability and privacy

Telemetry is disabled in the checked-in example. When OTLP or Langfuse is enabled:

- use credential and TLS profile references;
- keep `LANGFUSE_CAPTURE_CONTENT=false` unless a separately approved policy permits
  content capture;
- use opaque run, actor, and tenant references;
- export status, counts, timing, and bounded error classes rather than prompts,
  responses, tool payloads, media, filesystem paths, or credentials.

## Validation

After runtime configuration is injected, validate the shared boundary without
printing resolved values:

```bash
agent-utilities-doctor --only config provider_profiles transport_security mcp_fleet_secrets mcp_fleet
```

Use `agent-utilities-doctor --live` only when bounded calls to the configured service
and observability backends are authorized.
