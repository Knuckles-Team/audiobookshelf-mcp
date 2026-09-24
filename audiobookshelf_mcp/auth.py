#!/usr/bin/python

"""Authentication.

Priority:
1. **OIDC Delegation** (RFC 8693 Token Exchange) — when ``ENABLE_DELEGATION`` is
   active, exchanges the IdP-issued user token for a downstream access token via the
   shared ``agent_utilities.mcp.delegated_auth`` helper.
2. **Fixed credentials** — resolves a GraphOS-selected AgentConfig provider profile or
   falls back to the process-injected ``AUDIOBOOKSHELF_TOKEN`` value.

Endpoint and credential values are resolved at runtime through the shared
AgentConfig projection. TLS trust is a mandatory-verification profile resolved by
``agent_utilities.core.transport_security``; this package never stores certificate
material or a machine-specific trust path.
"""

from typing import Any

from agent_connector_sdk.config import setting
from agent_connector_sdk.exceptions import AuthError, UnauthorizedError
from agent_connector_sdk.tls.profile import ResolvedTLSProfile
from agent_connector_sdk.tls.resolve import resolve_tls_profile
from agent_connector_sdk.utilities import get_logger

from .api import ApiClientSystem

logger = get_logger(__name__)
_client: ApiClientSystem | None = None


def _resolve_provider_runtime_profile() -> Any:
    """Resolve the GraphOS-selected provider runtime profile, or raise."""
    from agent_utilities.core.provider_runtime import (
        resolve_selected_provider_runtime_profile,
    )

    try:
        return resolve_selected_provider_runtime_profile()
    except Exception:
        raise RuntimeError(
            "PROVIDER CONFIGURATION ERROR: selected runtime profile is unavailable"
        ) from None


def _resolve_runtime_and_endpoint(
    explicit: bool,
    url: str | None,
    token: str | None,
    tls_profile: ResolvedTLSProfile | None,
) -> tuple[Any, str, str, ResolvedTLSProfile | None]:
    """Resolve ``(runtime, base_url, fixed_token, profile)``.

    From the selected GraphOS provider profile when one applies, otherwise
    from the explicit call args / fixed-credential settings.
    """
    selected_profile = (
        "" if explicit else str(setting("AGENT_PROVIDER_PROFILE", "") or "").strip()
    )
    if not selected_profile:
        base_url = url or setting("AUDIOBOOKSHELF_URL", "")
        fixed_token = token or setting("AUDIOBOOKSHELF_TOKEN", "")
        return None, base_url, fixed_token, tls_profile

    runtime = _resolve_provider_runtime_profile()
    base_url = runtime.endpoint or ""
    fixed_token = str(runtime.credentials.get("TOKEN", ""))
    profile = runtime.tls
    if not base_url or profile is None:
        runtime.close()
        raise RuntimeError(
            "PROVIDER CONFIGURATION ERROR: selected runtime profile is incomplete"
        ) from None
    return runtime, base_url, fixed_token, profile


def _validate_credentials(
    base_url: str, delegated: bool, fixed_token: str, runtime: Any | None
) -> None:
    """Raise a RuntimeError (closing ``runtime`` first) for missing credentials."""
    if not base_url:
        raise RuntimeError("AUDIOBOOKSHELF_URL is required")
    if not delegated and not fixed_token:
        if runtime is not None:
            runtime.close()
        raise RuntimeError(
            "AUDIOBOOKSHELF_TOKEN is required when delegation is disabled"
        )


def _build_delegated_client(
    config: dict[str, Any] | None,
    base_url: str,
    profile: ResolvedTLSProfile,
    runtime: Any | None,
) -> ApiClientSystem:
    """Path 1: OIDC Delegation (RFC 8693 Token Exchange)."""
    from agent_utilities.mcp.delegated_auth import get_delegated_token

    try:
        delegated_token = get_delegated_token(
            config=config,
            audience=(config or {}).get("audience", base_url),
            scopes=(config or {}).get("delegated_scopes", "api"),
        )
        logger.info("Using OIDC delegated credentials")
        client = ApiClientSystem(
            base_url=base_url,
            token=delegated_token,
            tls_profile=profile,
        )
        if runtime is not None:
            # ApiClientSystem now owns cleanup for the transferred TLS profile.
            runtime.tls = None
        return client
    except Exception as exc:
        if runtime is not None:
            runtime.close()
        else:
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
    runtime: Any | None,
) -> ApiClientSystem:
    """Path 2: Fixed Credentials (AUDIOBOOKSHELF_TOKEN)."""
    try:
        return ApiClientSystem(
            base_url=base_url,
            token=fixed_token,
            tls_profile=profile,
        )
    except (AuthError, UnauthorizedError):
        if runtime is not None:
            runtime.close()
        else:
            profile.cleanup()
        raise RuntimeError(
            "AUTHENTICATION ERROR: Audiobookshelf rejected the configured credential"
        ) from None
    except Exception as exc:
        if runtime is not None:
            runtime.close()
        else:
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

    from agent_utilities.mcp.delegated_auth import is_delegation_enabled

    delegated = is_delegation_enabled(config)
    explicit = any(value is not None for value in (url, token, tls_profile))
    if not delegated and not explicit and _client is not None:
        return _client

    runtime, base_url, fixed_token, profile = _resolve_runtime_and_endpoint(
        explicit, url, token, tls_profile
    )
    _validate_credentials(base_url, delegated, fixed_token, runtime)
    profile = profile or resolve_tls_profile("audiobookshelf")

    if delegated:
        return _build_delegated_client(config, base_url, profile, runtime)

    logger.info("Using fixed credentials")
    client = _build_fixed_client(base_url, fixed_token, profile, runtime)

    if runtime is not None:
        # ApiClientSystem now owns cleanup for the transferred TLS profile.
        runtime.tls = None
    if not explicit:
        _client = client
    return client
