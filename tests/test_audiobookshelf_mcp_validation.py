import json
import tomllib
from pathlib import Path

import pytest
from scion_sdk.connector import build_server

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.concept("AS-OS.identity.abs")
def test_mcp_instance_registration(monkeypatch):
    """MCP server instantiates with its six typed tool domains."""
    monkeypatch.setattr("sys.argv", ["audiobookshelf-mcp"])
    _, mcp = build_server("audiobookshelf_mcp", command_args=[])
    assert mcp is not None


@pytest.mark.concept("AS-OS.identity.abs")
def test_provider_has_current_skills():
    """The provider ships its current skills; the operations skill has UI metadata."""
    skills = sorted((ROOT / "audiobookshelf_mcp" / "skills").glob("*/SKILL.md"))
    assert [path.parent.name for path in skills] == [
        "audiobookshelf-kg-ingestion",
        "audiobookshelf-library-catalog",
        "audiobookshelf-mcp-development",
        "audiobookshelf-media-operations",
        "audiobookshelf-podcast-manager",
    ]
    operations = (
        ROOT / "audiobookshelf_mcp" / "skills" / "audiobookshelf-media-operations"
    )
    assert (operations / "agents" / "openai.yaml").is_file()


@pytest.mark.concept("AS-OS.identity.abs")
def test_dependency_contract_uses_current_runtime():
    """Provider metadata requires the direct current Scion SDK modules."""
    project = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    dependencies = project["project"]["dependencies"]
    from packaging.requirements import Requirement
    from packaging.version import Version

    requirement = Requirement(
        next(d for d in dependencies[:1] if d.startswith("scion-sdk[mcp]"))
    )
    floor = max(Version(s.version) for s in requirement.specifier if s.operator == ">=")
    assert floor >= Version("0.6.3")
    assert not requirement.specifier.contains("0.7.0")
    assert [dep.split(">=")[0] for dep in dependencies] == [
        "scion-sdk[mcp]",
        "requests",
    ]
    assert "agent" not in project["project"]["optional-dependencies"]
    assert all(
        dep.startswith(("scion-sdk", "requests"))
        for dep in project["project"]["dependencies"]
    )


@pytest.mark.concept("AS-OS.identity.abs")
def test_launch_examples_are_reference_only_and_loopback_bound():
    """Checked-in launch examples contain no resolved deployment state."""
    config = json.loads((ROOT / "mcp_config.json").read_text(encoding="utf-8"))
    env = config["mcpServers"]["audiobookshelf-mcp"]["env"]
    assert env["AUDIOBOOKSHELF_URL"] == "env://AUDIOBOOKSHELF_URL"
    assert env["AUDIOBOOKSHELF_TOKEN"] == "env://AUDIOBOOKSHELF_TOKEN"
    assert all(value for value in env.values())

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    assert "-p 0.0.0.0" not in readme
    assert "example/audiobookshelf-mcp:mcp" not in readme
    assert "-e AUDIOBOOKSHELF_TOKEN=env://" not in readme
