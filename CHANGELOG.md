# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.3.7] - 2026-10-30

### Changed
- Require `scion-sdk>=0.6.4,<0.7.0`; `uv.lock` relocked.

## [2.3.5] - 2026-10-26

### Changed
- Added the canonical spec-delivery Pages dashboard and rapid-delivery development skill.

## [2.3.4] - 2026-10-24

### Changed
- Central connector migration: requires `agent-connector-sdk>=0.5.4`; server bootstrap, version, containers, ontology artifacts, security scaffold and pre-commit config are provided centrally.

## [2.3.3] - 2026-10-23

### Changed
- Requires `agent-connector-sdk>=0.4.1`; data sources are declared in code (`connector_sources`).

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
