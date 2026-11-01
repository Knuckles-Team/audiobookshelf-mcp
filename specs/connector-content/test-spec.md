# CONN-AUDIOBOOKSHELF-MCP-CONNECTOR-CONTENT — Test specification

Governing spec: [spec.md](spec.md).

| Test ID | Requirement | Proving test | Expected observation |
|---|---|---|---|
| T-001 | `CONN-AUDIOBOOKSHELF-MCP-CONNECTOR-CONTENT-R001` | `tests/test_default_content_surfaces.py` | The listings include the packaged skills, ontology and prompts. |

## Rows awaiting bound tests
- `CONN-AUDIOBOOKSHELF-MCP-CONNECTOR-CONTENT-R002`: planned proof `tests/test_ontology_parent_link.py::test_author_is_not_declared_in_the_shared_namespace`. Expected: Loading audiobookshelf.ttl with the core ontology shows no :Author class IRI declared by the connector and writtenBy uses mv:contributor to :Person.. Refusal: A connector ontology declaring :Author in the shared namespace fails the duplicate check..
