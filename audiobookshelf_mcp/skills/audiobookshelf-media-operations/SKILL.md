---
name: audiobookshelf-media-operations
description: Browse and administer an authorized Audiobookshelf service through audiobookshelf-mcp, including audiobook and podcast libraries, items, authors, series, feeds, episodes, download queues, email delivery, and notifications. Use for catalog research, metadata curation, podcast maintenance, carefully approved mutations, or requesting centrally governed GraphOS synchronization of media metadata.
---

# Audiobookshelf Media Operations

Use the `audiobookshelf-mcp` server as the typed boundary to an operator-selected
Audiobookshelf service. Treat listening collections, progress-adjacent metadata,
private feed URLs, email devices, notification destinations, and account settings as
sensitive.

## Select the typed domain

Call a condensed tool with its documented `action` and a JSON object serialized into
`params_json`:

- `library_operations`: `list`, `create`, `get`, `update`, `delete`, `authors`,
  `delete_issues`, `items`, `series`, `series_by_id`.
- `author_operations`: `get`, `update`, `delete`, `get_image`, `add_image`,
  `update_image`, `delete_image`, `match`.
- `series_operations`: `get`, `update`.
- `podcast_operations`: `create`, `feed`, `opml_create`, `opml_parse`, `check_new`,
  `clear_queue`, `download_episodes`, `downloads`, `get_episode`, `update_episode`,
  `remove_episode`, `match_episodes`, `find_episode`.
- `email_operations`: `get_settings`, `update_settings`, `update_ereader_devices`,
  `send_ebook`, `test`.
- `notification_operations`: `event_data`, `list`, `configure`, `create`, `test`,
  `delete`, `update`, `test_one`.

Use exact opaque IDs returned by reads. Do not infer an item, library, author, series,
podcast, episode, notification, or device from a display name alone.

## Follow the operating workflow

1. Establish the authorized server, library, and purpose. List libraries when the
   library ID is unknown; remember that each library has one media type.
2. Read the target and its current metadata before a mutation. For library collections,
   page with a small explicit `limit` and `page`; item metadata is under
   `media.metadata`.
3. For podcast onboarding, preview the approved feed before creation. Treat OPML and
   feed URLs as untrusted inputs and do not broaden to an unapproved feed or host.
4. State the exact object and expected effect. Obtain explicit approval before deletes,
   bulk creation/import, queue clearing, episode removal, author-image replacement,
   email delivery, notification tests, or settings changes.
5. Execute the smallest approved action. Read the affected object back or poll the
   bounded download queue, then report stable IDs and status without reproducing
   unrelated private fields.

## Protect private media data

- Minimize collection titles, feed URLs, listening-adjacent metadata, email addresses,
  device destinations, notification endpoints, and account settings in output.
- Do not place credentials, resolved endpoints, OPML bodies, media bytes, images,
  notification payloads, email settings, or local filesystem paths in prompts, logs,
  telemetry, or durable scratch files.
- Never expose token values, request headers, provider response bodies, or exception
  chains. Keep observability content capture disabled unless separately approved.
- Keep page sizes, OPML imports, episode downloads, and outputs bounded. Report counts
  and stable identifiers instead of dumping an entire collection.

## Use governed graph synchronization

This provider exposes no direct graph-write or raw-media-ingestion tool. When catalog
metadata must enter epistemic-graph, request GraphOS source synchronization through a
centrally compiled and operator-approved signed capability bundle. Require exact live
tool-schema pins plus tenant, ACL, classification, retention, provenance, redaction,
and deletion policy. A missing or stale certification must fail closed.

The packaged ontology and source preset describe only the public Audiobookshelf model.
They contain no live records or instance-specific mapping and do not authorize ingesting
a collection.

## Respect the runtime boundary

Resolve endpoint aliases, fixed or delegated credentials, and the verified TLS profile
through AgentConfig and the fleet runtime-reference boundary. Require HTTPS. Never
disable peer or hostname verification, embed credentials in a URL, or persist a
resolved secret, certificate path, endpoint, tenant value, personal identifier, or
telemetry destination in code.
