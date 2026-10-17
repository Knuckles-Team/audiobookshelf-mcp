from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

import audiobookshelf_mcp.auth as auth_module
from audiobookshelf_mcp.auth import get_client


@pytest.mark.concept("AS-OS.identity.abs")
def test_get_client_auth_error_is_sanitized():
    """Construction failures omit provider and credential-adjacent detail."""
    auth_module._client = None
    profile = MagicMock()
    with patch(
        "agent_connector_sdk.auth.delegation.DelegationSettings.from_settings",
        return_value=SimpleNamespace(enabled=False),
    ):
        with patch(
            "audiobookshelf_mcp.auth.ApiClientSystem",
            side_effect=Exception("sensitive provider detail"),
        ):
            with pytest.raises(RuntimeError) as exc_info:
                get_client(
                    url="https://service.example.invalid",
                    token="runtime-token",
                    tls_profile=profile,
                )
    assert "AUTHENTICATION ERROR" in str(exc_info.value)
    assert "sensitive provider detail" not in str(exc_info.value)
    assert exc_info.value.__cause__ is None
    profile.cleanup.assert_called_once()


@pytest.mark.concept("AS-OS.identity.abs")
def test_explicit_connection_inputs_are_request_scoped():
    """Explicit clients never reuse or replace the process-level fixed client."""
    sentinel = MagicMock()
    auth_module._client = sentinel
    profile = MagicMock()
    created = object()
    try:
        with patch(
            "agent_connector_sdk.auth.delegation.DelegationSettings.from_settings",
            return_value=SimpleNamespace(enabled=False),
        ):
            with patch("audiobookshelf_mcp.auth.ApiClientSystem", return_value=created):
                result = get_client(
                    url="https://service.example.invalid",
                    token="runtime-token",
                    tls_profile=profile,
                )
        assert result is created
        assert auth_module._client is sentinel
    finally:
        auth_module._client = None


@pytest.mark.concept("AS-OS.identity.abs")
def test_fixed_credentials_resolve_from_settings():
    """Endpoint and token come from the shared config layer when not passed."""
    auth_module._client = None
    tls = MagicMock()
    created = MagicMock()
    values = {
        "AUDIOBOOKSHELF_URL": "https://service.example.invalid",
        "AUDIOBOOKSHELF_TOKEN": "runtime-token",
    }

    try:
        with patch(
            "agent_connector_sdk.auth.delegation.DelegationSettings.from_settings",
            return_value=SimpleNamespace(enabled=False),
        ):
            with patch(
                "audiobookshelf_mcp.auth.setting",
                side_effect=lambda name, default="": values.get(name, default),
            ):
                with patch(
                    "audiobookshelf_mcp.auth.resolve_configured_tls_profile",
                    return_value=tls,
                ):
                    with patch(
                        "audiobookshelf_mcp.auth.ApiClientSystem",
                        return_value=created,
                    ) as constructor:
                        assert get_client() is created
        constructor.assert_called_once_with(
            base_url="https://service.example.invalid",
            token="runtime-token",
            tls_profile=tls,
        )
    finally:
        auth_module._client = None


@pytest.mark.concept("AS-OS.identity.abs")
def test_selected_provider_profile_is_resolved_ephemerally():
    """The launcher-selected SDK provider profile supplies endpoint, token and TLS in memory."""
    auth_module._client = None
    runtime = MagicMock()
    runtime.endpoint = "https://service.example.invalid"
    runtime.credentials = {"TOKEN": "runtime-token"}
    tls = MagicMock()
    runtime.tls = tls
    created = MagicMock()

    def configured_setting(name: str, default: str = "") -> str:
        return "media-service" if name == "AGENT_PROVIDER_PROFILE" else default

    try:
        with patch(
            "agent_connector_sdk.auth.delegation.DelegationSettings.from_settings",
            return_value=SimpleNamespace(enabled=False),
        ):
            with patch(
                "audiobookshelf_mcp.auth.setting", side_effect=configured_setting
            ):
                with patch(
                    "audiobookshelf_mcp.auth.resolve_selected_provider_profile",
                    return_value=runtime,
                ):
                    with patch(
                        "audiobookshelf_mcp.auth.ApiClientSystem",
                        return_value=created,
                    ) as client_cls:
                        assert get_client() is created
        client_cls.assert_called_once_with(
            base_url="https://service.example.invalid",
            token="runtime-token",
            tls_profile=tls,
        )
        assert runtime.tls is None
        runtime.close.assert_not_called()
    finally:
        auth_module._client = None


@pytest.mark.concept("AS-OS.identity.abs")
def test_selected_provider_profile_failures_are_sanitized(monkeypatch):
    """An unavailable or incomplete profile never leaks detail and closes the runtime."""
    auth_module._client = None
    monkeypatch.setenv("AGENT_PROVIDER_PROFILE", "media-service")
    monkeypatch.delenv("PROVIDER_CONFIGS", raising=False)
    with patch(
        "agent_connector_sdk.auth.delegation.DelegationSettings.from_settings",
        return_value=SimpleNamespace(enabled=False),
    ):
        with pytest.raises(
            RuntimeError, match="selected runtime profile is unavailable"
        ) as info:
            get_client()
        assert info.value.__cause__ is None

        incomplete = MagicMock(endpoint="https://service.example.invalid", tls=None)
        incomplete.credentials = {"TOKEN": "runtime-token"}
        with patch(
            "audiobookshelf_mcp.auth.resolve_selected_provider_profile",
            return_value=incomplete,
        ):
            with pytest.raises(RuntimeError, match="incomplete"):
                get_client()
        incomplete.close.assert_called_once()
