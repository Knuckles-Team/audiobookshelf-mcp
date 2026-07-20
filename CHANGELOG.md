# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Migrated MCP wiring to the current direct Agent Utilities modules and retained
  complete 46-method API-to-tool parity.
- Added native reference-only AgentConfig provider-profile resolution for GraphOS
  children while retaining runtime-injected standalone configuration.
- Consolidated three overlapping workflows into the single
  `audiobookshelf-media-operations` skill.
- Moved graph synchronization behind the centrally governed GraphOS source boundary;
  the provider no longer exposes direct graph writes or raw-media ingestion.
- Raised the Agent Utilities runtime floor to `1.27.1` and removed the stale,
  unsatisfiable dependency lock.

### Security

- Enforced HTTPS-only same-authority requests, encoded path parameters, fixed
  timeouts, disabled redirects, bounded retries and responses, sanitized errors,
  runtime-resolved credentials, and mandatory AgentConfig TLS profiles.
- Removed deployment-specific source, secret, certificate, and filesystem state from
  the packaged connector contract and hardened the non-root container examples.

## [0.1.0] - 2026-06-22

### Added
- Initial release.
- Modular subfolders for API wrappers (`api/`) and action-routed MCP tools (`mcp/`).
- Material-theme mkdocs documentation site (7 standard pages).
- Full pre-commit quality gate and flat `tests/` structure.
