# Concept Registry — audiobookshelf-mcp

> **Prefix**: `CONCEPT:ABS-*`
> **Version**: 0.1.0
> **Bridge**: [`CONCEPT:AU-ECO.messaging.native-backend-abstraction`](https://github.com/Knuckles-Team/agent-utilities/blob/main/docs/concepts.md) (Unified Toolkit Ingestion)

---

## Project-Specific Concepts

| Concept ID | Name | Description |
|------------|------|-------------|
| `CONCEPT:AS-OS.identity.abs` | Library Operations | MCP tool domain `libraries` — list/create/get/update/delete libraries, items & series |
| `CONCEPT:AS-OS.identity.abs-2` | Author Operations | MCP tool domain `authors` — author CRUD, images & metadata match |
| `CONCEPT:AS-OS.governance.abs` | Series Operations | MCP tool domain `series` — series get/update |
| `CONCEPT:AS-OS.governance.abs-2` | Podcast Operations | MCP tool domain `podcasts` — podcast & episode management, OPML, downloads |
| `CONCEPT:AS-OS.governance.abs-3` | Email & E-Reader | MCP tool domain `email` — email settings & send-ebook-to-device |
| `CONCEPT:AS-OS.governance.abs-4` | Notification Operations | MCP tool domain `notification` — notification config, create, test |

## Cross-Project References (from agent-utilities)

| Concept ID | Name | Origin |
|------------|------|--------|
| `CONCEPT:AU-ECO.messaging.native-backend-abstraction` | Unified Toolkit Ingestion | agent-utilities |
| `CONCEPT:AU-ORCH.adapter.hot-cache-invalidation` | Confidence-Gated Router | agent-utilities |
| `CONCEPT:AU-OS.config.secrets-authentication` | Prompt Injection Defense | agent-utilities |
