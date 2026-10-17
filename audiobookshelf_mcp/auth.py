#!/usr/bin/python

"""Authentication.

Priority:
1. **OIDC Delegation** (RFC 8693 Token Exchange) — when ``ENABLE_DELEGATION`` is
   active, exchanges the IdP-issued user token for a downstream access token via the
   shared ``agent_connector_sdk.mcp.delegated_auth`` helper.
2. **Fixed credentials** — uses the AgentConfig-projected ``AUDIOBOOKSHELF_TOKEN`` value.

Endpoint and credential values are resolved at runtime through the shared
AgentConfig projection. TLS trust is a mandatory-verification profile resolved by
``agent_connector_sdk.core.transport_security``; this package never stores certificate
material or a machine-specific trust path.
"""

import logging
from typing import Any

from agent_connector_sdk.config import setting
from agent_connector_sdk.exceptions import AuthError, UnauthorizedError
from agent_connector_sdk.tls.profile import ResolvedTLSProfile
from agent_connector_sdk.tls.resolve import resolve_tls_profile as resolve_configured_tls_profile

from .api import ApiClientSystem

logger = logging.getLogger(__name__)
_client: ApiClientSystem | None = None


def _resolve_endpoint(
    url: str | None,
    token: str | None,
    tls_profile: ResolvedTLSProfile | None,
) -> tuple[str, str, ResolvedTLSProfile | None]:
    """Resolve ``(base_url, fixed_token, profile)`` from args / fixed-credential settings."""
    base_url = url or setting("AUDIOBOOKSHELF_URL", "")
    fixed_token = token or setting("AUDIOBOOKSHELF_TOKEN", "")
    return base_url, fixed_token, tls_profile


def _validate_credentials(base_url: str, delegated: bool, fixed_token: str) -> None:
    """Raise a RuntimeError for missing credentials."""
    if not base_url:
        raise RuntimeError("AUDIOBOOKSHELF_URL is required")
    if not delegated and not fixed_token:
        raise RuntimeError(
            "AUDIOBOOKSHELF_TOKEN is required when delegation is disabled"
        )


def _exchange_delegated_token() -> str:
    """RFC 8693 Token Exchange via ``agent_connector_sdk.auth.delegation``."""
    import httpx
    from agent_connector_sdk.auth.delegation import (
        DelegationSettings,
        current_user_token,
        exchange_token,
    )
    from agent_connector_sdk.exceptions import LoginRequiredError

    settings = DelegationSettings.from_settings()
    subject_token = current_user_token()
    if not subject_token:
        raise LoginRequiredError("no verified caller token to delegate")
    with httpx.Client(timeout=30) as http_client:
        access_token = exchange_token(
            settings, subject_token=subject_token, http_client=http_client
        )
    return access_token.value


def _build_delegated_client(
    config: dict[str, Any] | None,
    base_url: str,
    profile: ResolvedTLSProfile,
) -> ApiClientSystem:
    """Path 1: OIDC Delegation (RFC 8693 Token Exchange)."""
    try:
        delegated_token = _exchange_delegated_token()
        logger.info("Using OIDC delegated credentials")
        client = ApiClientSystem(
            base_url=base_url,
            token=delegated_token,
            tls_profile=profile,
        )
        return client
    except Exception as exc:
        profile.cleanup()
        logger.error(
            "OIDC delegation failed",
            extra={"error_type": type(exc).__name__},
        )
        raise RuntimeError("Token exchange failed") from None


def _build_fixed_client(
    base_url: str,
    fixed_token: str,
    profile: ResolvedTLSProfile,
) -> ApiClientSystem:
    """Path 2: Fixed Credentials (AUDIOBOOKSHELF_TOKEN)."""
    try:
        return ApiClientSystem(
            base_url=base_url,
            token=fixed_token,
            tls_profile=profile,
        )
    except (AuthError, UnauthorizedError):
        profile.cleanup()
        raise RuntimeError(
            "AUTHENTICATION ERROR: Audiobookshelf rejected the configured credential"
        ) from None
    except Exception as exc:
        profile.cleanup()
        raise RuntimeError(
            "AUTHENTICATION ERROR: Failed to instantiate the client "
            f"({type(exc).__name__})"
        ) from None


def get_client(
    url: str | None = None,
    token: str | None = None,
    tls_profile: ResolvedTLSProfile | None = None,
    config: dict[str, Any] | None = None,
) -> ApiClientSystem:
    """Get or create a singleton API client (OIDC delegation or fixed credentials).

    Credentials resolve through the shared config layer (the one XDG
    ``config.json`` / env) at call time, not frozen at import.
    """
    global _client

    from agent_connector_sdk.auth.delegation import DelegationSettings

    delegated = (
        bool(config.get("enable_delegation", False))
        if config is not None
        else DelegationSettings.from_settings().enabled
    )
    explicit = any(value is not None for value in (url, token, tls_profile))
    if not delegated and not explicit and _client is not None:
        return _client

    base_url, fixed_token, profile = _resolve_endpoint(url, token, tls_profile)
    _validate_credentials(base_url, delegated, fixed_token)
    profile = profile or resolve_configured_tls_profile("audiobookshelf")

    if delegated:
        return _build_delegated_client(config, base_url, profile)

    logger.info("Using fixed credentials")
    client = _build_fixed_client(base_url, fixed_token, profile)

    if not explicit:
        _client = client
    return client
