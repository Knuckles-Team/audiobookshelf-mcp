import json
import tomllib
from pathlib import Path

import pytest

from audiobookshelf_mcp.mcp_server import get_mcp_instance

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.concept("AS-OS.identity.abs")
def test_mcp_instance_registration(monkeypatch):
    """MCP server instantiates with its six typed tool domains."""
    monkeypatch.setattr("sys.argv", ["audiobookshelf-mcp"])
    mcp, args, middlewares = get_mcp_instance()
    assert mcp is not None


@pytest.mark.concept("AS-OS.identity.abs")
def test_provider_has_one_current_skill():
    """The provider exposes one comprehensive skill with UI metadata."""
    skills = sorted((ROOT / "audiobookshelf_mcp" / "skills").glob("*/SKILL.md"))
    assert [path.parent.name for path in skills] == ["audiobookshelf-media-operations"]
    assert (skills[0].parent / "agents" / "openai.yaml").is_file()


@pytest.mark.concept("AS-OS.identity.abs")
def test_provider_owns_complete_neutral_source_bundle():
    """Release evidence is complete and never claims external-live validation."""
    connectors = ROOT / "audiobookshelf_mcp" / "connectors"
    presets = json.loads(
        (connectors / "mcp_source_presets.json").read_text(encoding="utf-8")
    )
    assert {key for key in presets if not key.startswith("_")} == {
        "audiobookshelf-libraries"
    }
    fingerprints = json.loads(
        (connectors / "tool_schema_fingerprints.json").read_text(encoding="utf-8")
    )
    assert set(fingerprints["tools"]) == {"library_operations"}

    ontology = ROOT / "audiobookshelf_mcp" / "ontology"
    certification = json.loads(
        (ontology / "certification.json").read_text(encoding="utf-8")
    )
    assert certification["connector"] == "audiobookshelf-mcp"
    assert certification["mode"] == "offline-source"
    assert certification["status"] == "source-validated"
    assert certification["live_certified"] is False
    for relative in (
        "connector_manifest.yml",
        "audiobookshelf_mcp/ontology/shapes/connector.shacl.ttl",
        "audiobookshelf_mcp/ontology/mappings/source.yaml",
        "audiobookshelf_mcp/ontology/fixtures/records.json",
        "audiobookshelf_mcp/ontology/migrations/manifest.json",
    ):
        assert relative in certification["artifacts"]
        assert (ROOT / relative).is_file()


@pytest.mark.concept("AS-OS.identity.abs")
def test_provider_entry_points_prove_package_ownership():
    """Every provider leg resolves to a data package in the owning wheel."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    entry_points = project["project"]["entry-points"]
    assert entry_points["agent_utilities.skill_providers"] == {
        "audiobookshelf-mcp": "audiobookshelf_mcp.skills"
    }
    assert entry_points["agent_utilities.ontology_providers"] == {
        "audiobookshelf-mcp": "audiobookshelf_mcp.ontology"
    }
    assert entry_points["agent_utilities.source_connector_providers"] == {
        "audiobookshelf-mcp": "audiobookshelf_mcp.connectors"
    }
    assert entry_points["agent_utilities.prompt_providers"] == {
        "audiobookshelf-mcp": "audiobookshelf_mcp.prompts"
    }


@pytest.mark.concept("AS-OS.identity.abs")
def test_direct_graph_and_legacy_surfaces_are_absent():
    """Media metadata can enter the graph only through central source sync."""
    package = ROOT / "audiobookshelf_mcp"
    for relative in (
        "api_client.py",
        "kg_ingest.py",
        "kg_media.py",
        "main_agent.json",
        "mcp/mcp_ingest.py",
    ):
        assert not (package / relative).exists()


@pytest.mark.concept("AS-OS.identity.abs")
def test_dependency_contract_uses_current_runtime():
    """Provider metadata requires the direct current Agent Utilities modules."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    assert project["project"]["dependencies"] == ["agent-utilities>=1.27.1,<2.0.0"]
    assert project["project"]["optional-dependencies"]["agent"] == [
        "agent-utilities[agent-runtime,logfire]>=1.27.1,<2.0.0"
    ]
    assert not (ROOT / "uv.lock").exists()


@pytest.mark.concept("AS-OS.identity.abs")
def test_launch_examples_are_reference_only_and_loopback_bound():
    """Checked-in launch examples contain no resolved deployment state."""
    config = json.loads((ROOT / "mcp_config.json").read_text(encoding="utf-8"))
    env = config["mcpServers"]["audiobookshelf-mcp"]["env"]
    assert env["AUDIOBOOKSHELF_URL"] == "env://AUDIOBOOKSHELF_URL"
    assert env["AUDIOBOOKSHELF_TOKEN"] == "env://AUDIOBOOKSHELF_TOKEN"
    assert all(value for value in env.values())

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "-p 127.0.0.1:8000:8000" in readme
    assert "example/audiobookshelf-mcp:mcp" not in readme
    assert "-e AUDIOBOOKSHELF_TOKEN=env://" not in readme
