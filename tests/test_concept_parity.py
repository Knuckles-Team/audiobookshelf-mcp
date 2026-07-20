from pathlib import Path

import pytest

CONCEPTS_DOC = Path(__file__).resolve().parents[1] / "docs" / "concepts.md"


@pytest.mark.concept("AS-OS.identity.abs")
def test_concepts_doc_exists():
    """Concept registry doc exists. CONCEPT:AS-OS.identity.abs"""
    assert CONCEPTS_DOC.is_file()


@pytest.mark.concept("AS-OS.identity.abs")
def test_eco_bridge_present():
    """ECO-4.0 bridge concept is referenced. CONCEPT:AS-OS.identity.abs"""
    assert "AU-ECO.messaging.native-backend-abstraction" in CONCEPTS_DOC.read_text(
        encoding="utf-8"
    )


@pytest.mark.concept("AS-OS.identity.abs")
def test_prefix_registered():
    """Project concept prefix is registered. CONCEPT:AS-OS.identity.abs"""
    assert "CONCEPT:ABS-" in CONCEPTS_DOC.read_text(encoding="utf-8")
