---
name: audiobookshelf-kg-ingestion
skill_type: skill
description: >-
  Push an Audiobookshelf collection into the medulla knowledge graph as typed nodes (library, book, podcast, author, series) with authorship, series and containment links, plus optional cover art. Use when the catalog must be queryable in the KG. Do NOT use for day-to-day browsing (audiobookshelf-library-catalog) or podcast maintenance (audiobookshelf-podcast-manager).
license: MIT
tags: [audiobookshelf, knowledge-graph, ingestion, ontology, mcp]
metadata:
  author: Knuckles-Team
  version: '0.1.0'
---
# Audiobookshelf Knowledge-Graph Ingestion

Scope: Natively push an Audiobookshelf collection into the medulla knowledge graph via the audiobookshelf-mcp MCP server — libraries, audiobooks/podcasts, authors and series become typed OWL nodes (:Library / :Book / :Podcast / :Author / :Series) with authorship, series and containment links, and cover art can ride along as :MediaAsset blobs. Use when the agent must make the catalog queryable/semantic in the KG. Do NOT use for day-to-day browsing (audiobookshelf-library-catalog) or podcast maintenance (audiobookshelf-podcast-manager).

Native "maximum ingestion" of an Audiobookshelf server into the ONE medulla
knowledge graph. One MCP tool lists the collection via the real client and pushes it as
**typed OWL nodes** matching `audiobookshelf_mcp/ontology/audiobookshelf.ttl`.

## When to use
- Seed or refresh the KG with a whole Audiobookshelf server (all libraries).
- Ingest a single library's items + authors as typed nodes.
- Capture item cover art as durable, deduped `:MediaAsset` blobs.

## When NOT to use
- Interactive browsing / metadata edits → `audiobookshelf-library-catalog`.
- Podcast feed / episode maintenance → `audiobookshelf-podcast-manager`.
- Reading back from the KG → the graph query tools (`graph_query` / `graph_search`),
  not this connector.

## Steps

1. Check the sources with `audiobookshelf_get_libraries`.
   Verify the libraries you intend to ingest are listed.
2. Request the governed sync with `source_sync` for the connector's data sources.
   Verify the response reports a started or completed sync.
3. Inspect the result with `graph_query` for `:Library` and `:Book` nodes.
   Verify node counts are non-zero and ids start with `audiobookshelf:library:`.
4. Confirm cover art with `audiobookshelf_get_item_cover` for one item.
   Verify a `:MediaAsset` exists with the item as `owner_id`.

## Failure recovery

| Failure | Cause | Recovery |
|---|---|---|
| HTTP 401 or connection error | `AUDIOBOOKSHELF_TOKEN` or `AUDIOBOOKSHELF_URL` is missing or wrong | Set both variables to a valid API token and base URL, restart the server, and confirm with `audiobookshelf_get_libraries` |
| Ingest returns null | No medulla engine is reachable for writes, so the tool no-ops | Start or reach the engine, then request `source_sync` for the sources again after confirming with `graph_query` |
| No nodes appear | The sync was never requested or the library list was empty | Confirm `audiobookshelf_get_libraries` returns libraries and request `source_sync` for the connector sources |

## Prerequisites & environment
Connect via the `mcp-client` skill against the **`audiobookshelf-mcp`** MCP server. A
live medulla engine must be reachable for writes — otherwise the tool **no-ops**
cleanly and returns `{"ingested": null}` (it never fails the call).

| Variable | Required | Notes |
|----------|----------|-------|
| `AUDIOBOOKSHELF_URL` | ✅ | Server base URL (default `http://localhost:13378`) |
| `AUDIOBOOKSHELF_TOKEN` | ✅ | Bearer API token (Config → API Keys) |
| `AUDIOBOOKSHELF_SSL_VERIFY` | optional | TLS verification toggle |

## Tools
Ingestion is driven by arbora's governed sync of the connector's declared data sources, which read
through these typed tools:

| Tool | Purpose |
|------|---------|
| `audiobookshelf_get_libraries` | Library inventory (source `audiobookshelf-libraries`). |
| `audiobookshelf_get_library_items` | Items of one library (`id`, `limit`, `page`, `sort`). |
| `audiobookshelf_get_library_authors` | Authors of one library. |
| `audiobookshelf_get_item_cover` | Cover art for `:MediaAsset` blobs. |

Request the sync from arbora (`source_sync`); do not push records by hand.

## What lands in the graph
- `:Library` (name, mediaType, provider) — node id `audiobookshelf:library:<id>`.
- `:Book` / `:Podcast` (title, narrator, duration, isbn/asin, coverPath) with
  `:writtenBy` → `:Author`, `:partOfSeries` → `:Series`, `:inLibrary` → `:Library`.
- `:Author` (name, numBooks) — node id `audiobookshelf:author:<id>`.
- Cover art → `:MediaAsset` blobs carrying `owner_id` back to the item.

## Gotchas
- Writes are **best-effort**: no reachable engine → clean no-op, not an error.
- Cover capture fetches each item's `/api/items/{id}/cover`, which is slow on large
  libraries; leave it off for a quick metadata-only sync.
- Node `type` values must match the ontology classes; re-running is idempotent (nodes
  MERGE on their stable `audiobookshelf:<class>:<id>` id).

## Related
- **Ontology:** `audiobookshelf_mcp/ontology/audiobookshelf.ttl` (federated via the
  `scion_sdk.ontology_providers` entry-point).
- **Connector preset:** `audiobookshelf_mcp/connectors/mcp_source_presets.json` wires the
  declarative Tier-1 `source_sync` path for the same libraries.
- Browsing the ingested catalog: `audiobookshelf-library-catalog`.
