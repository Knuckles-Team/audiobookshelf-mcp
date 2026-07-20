# Backing Platform — Audiobookshelf MCP

`audiobookshelf-mcp` is a **client** of an operator-managed Audiobookshelf instance.
The backing service lifecycle, storage, media paths, identity configuration, backup,
and upgrades remain outside this connector repository.

!!! note "No embedded platform profile"
    This repository intentionally does not ship an environment-specific
    Audiobookshelf Compose stack, media path, user account, or customized schema.

## Required service contract

- A reachable absolute HTTPS Audiobookshelf API endpoint supplied at runtime.
- A least-privilege API token, or a compatible delegated identity path.
- A valid certificate chain; private trust is selected through an AgentConfig TLS
  profile.
- Backups and retention appropriate for the catalog and media managed by the service.
- Network policy that allows only the connector runtime to reach the API.

After the service owner provides those inputs, follow
[Configuration, trust, and privacy](configuration.md). Connector startup must not
create or reconfigure the backing service.
