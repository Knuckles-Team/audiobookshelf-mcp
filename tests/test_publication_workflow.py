"""Keep shared publication and Pages contracts explicit in this connector."""

import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _workflow(name):
    return yaml.safe_load((ROOT / ".github/workflows" / name).read_text())


def _actions_on(workflow):
    # PyYAML's YAML 1.1 reader represents the Actions "on" key as True.
    return workflow["on"] if "on" in workflow else workflow[True]


def test_pages_publishes_spec_dashboard_from_generated_status():

    config = json.loads((ROOT / ".github/spec-dashboard.json").read_text())
    assert config == {
        "version": 1,
        "sources": [{"glob": "specs/*/status.json", "kind": "spec"}],
    }


def test_development_skill_has_rapid_delivery_contract():
    skill = ROOT / "audiobookshelf_mcp/skills/audiobookshelf-mcp-development/SKILL.md"
    content = skill.read_text()

    assert "name: audiobookshelf-mcp-development" in content
    assert "## Rapid delivery: the 5-minute contract" in content
