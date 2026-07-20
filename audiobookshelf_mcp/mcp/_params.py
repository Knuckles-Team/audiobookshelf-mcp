"""Bounded parsing for action-routed MCP arguments."""

from __future__ import annotations

import json
from typing import Any

_MAX_PARAMS_BYTES = 1_048_576


def parse_params_json(
    value: str,
) -> tuple[dict[str, Any] | None, dict[str, str] | None]:
    """Return a JSON object or a stable public error without echoing input."""
    if len(str(value or "").encode("utf-8")) > _MAX_PARAMS_BYTES:
        return None, {"error": "params_json exceeds the connector limit"}
    try:
        decoded = json.loads(value) if value else {}
    except (TypeError, ValueError):
        return None, {"error": "Invalid params_json"}
    if not isinstance(decoded, dict):
        return None, {"error": "params_json must decode to a JSON object"}
    return {key: item for key, item in decoded.items() if item is not None}, None
