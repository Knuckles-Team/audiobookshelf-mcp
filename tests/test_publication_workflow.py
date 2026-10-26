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
    workflow = _workflow("pages.yml")
    publisher = workflow["jobs"]["publish-pages"]
    push = _actions_on(workflow)["push"]

    assert publisher["uses"] == (
        "Knuckles-Team/pipelines/.github/workflows/pages_pipeline.yml@main"
    )
    assert publisher["with"] == {
        "content_source": "docs",
        "spec_dashboard_enabled": True,
        "spec_dashboard_config": ".github/spec-dashboard.json",
    }
    assert {
        "docs/**",
        "mkdocs.yml",
        "README.md",
        "specs/**",
        ".github/spec-dashboard.json",
        ".github/workflows/pages.yml",
    } <= set(push["paths"])

    config = json.loads((ROOT / ".github/spec-dashboard.json").read_text())
    assert config == {
        "version": 1,
        "sources": [{"glob": "specs/*/status.json", "kind": "spec"}],
    }


def test_release_workflow_keeps_connector_generation_flags():
    jobs = _workflow("pipeline.yml")["jobs"]
    pypi = jobs["publish-pypi"]
    docker = jobs["publish-docker"]

    assert pypi["uses"] == (
        "Knuckles-Team/pipelines/.github/workflows/python_pipeline.yml@main"
    )
    assert pypi["with"] == {"connector": True}
    assert docker["uses"] == (
        "Knuckles-Team/pipelines/.github/workflows/container_pipeline.yml@main"
    )
    assert docker["with"] == {"render_connector": True}
    assert docker["needs"] == "publish-pypi"


def test_development_skill_has_rapid_delivery_contract():
    skill = (
        ROOT
        / "audiobookshelf_mcp/skills/audiobookshelf-mcp-development/SKILL.md"
    )
    content = skill.read_text()

    assert "name: audiobookshelf-mcp-development" in content
    assert "## Rapid delivery: the 5-minute contract" in content
