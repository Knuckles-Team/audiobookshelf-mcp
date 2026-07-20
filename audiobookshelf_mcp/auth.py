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

from agent_utilities.base_utilities import get_logger
from agent_utilities.core.config import setting
from agent_utilities.core.exceptions import AuthError, UnauthorizedError
from agent_utilities.core.transport_security import (
    ResolvedTLSProfile,
    resolve_configured_tls_profile,
)

from .api import ApiClientSystem

logger = get_logger(__name__)
_client: ApiClientSystem | None = None


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

    from agent_utilities.mcp.delegated_auth import (
        get_delegated_token,
        is_delegation_enabled,
    )

    delegated = is_delegation_enabled(config)
    explicit = any(value is not None for value in (url, token, tls_profile))
    if not delegated and not explicit and _client is not None:
        return _client

    runtime: Any | None = None
    selected_profile = (
        "" if explicit else str(setting("AGENT_PROVIDER_PROFILE", "") or "").strip()
    )
    if selected_profile:
        try:
            from agent_utilities.core.provider_runtime import (
                resolve_selected_provider_runtime_profile,
            )

            runtime = resolve_selected_provider_runtime_profile()
        except Exception:
            raise RuntimeError(
                "PROVIDER CONFIGURATION ERROR: selected runtime profile is unavailable"
            ) from None
        base_url = runtime.endpoint or ""
        fixed_token = str(runtime.credentials.get("TOKEN", ""))
        profile = runtime.tls
        if not base_url or profile is None:
            runtime.close()
            raise RuntimeError(
                "PROVIDER CONFIGURATION ERROR: selected runtime profile is incomplete"
            ) from None
    else:
        base_url = url or setting("AUDIOBOOKSHELF_URL", "")
        fixed_token = token or setting("AUDIOBOOKSHELF_TOKEN", "")
        profile = tls_profile

    if not base_url:
        raise RuntimeError("AUDIOBOOKSHELF_URL is required")
    if not delegated and not fixed_token:
        if runtime is not None:
            runtime.close()
        raise RuntimeError(
            "AUDIOBOOKSHELF_TOKEN is required when delegation is disabled"
        )
    profile = profile or resolve_configured_tls_profile("audiobookshelf")

    # --- Path 1: OIDC Delegation (RFC 8693 Token Exchange) ---
    if delegated:
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

    # --- Path 2: Fixed Credentials (AUDIOBOOKSHELF_TOKEN) ---
    logger.info("Using fixed credentials")
    try:
        client = ApiClientSystem(
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

    if runtime is not None:
        # ApiClientSystem now owns cleanup for the transferred TLS profile.
        runtime.tls = None
    if not explicit:
        _client = client
    return client
