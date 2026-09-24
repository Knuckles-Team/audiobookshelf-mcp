"""Shared verified transport and bounded response handling for Audiobookshelf."""

from __future__ import annotations

import json as json_module
import math
import time
from typing import Any
from urllib.parse import quote, urlsplit

import requests
from agent_connector_sdk.exceptions import (
    ApiError,
    AuthError,
    MissingParameterError,
    ParameterError,
    UnauthorizedError,
)
from agent_connector_sdk.tls.profile import ResolvedTLSProfile
from agent_connector_sdk.tls.resolve import resolve_tls_profile

_ALLOWED_METHODS = frozenset({"DELETE", "GET", "PATCH", "POST", "PUT"})
_TRANSIENT_STATUSES = frozenset({429, 502, 503, 504})
_MAX_URL_BYTES = 2_048
_MAX_TOKEN_BYTES = 65_536
_MAX_PATH_BYTES = 16_384
_MAX_SEGMENT_BYTES = 8_192
_MAX_RESPONSE_BYTES = 64 * 1024 * 1024
_RUNTIME_REFERENCE_PREFIXES = ("env://", "secret://", "vault://")


def _has_controls(value: str) -> bool:
    return any(ord(character) < 32 or ord(character) == 127 for character in value)


def _invalid_url_text(value: str) -> bool:
    return (
        _has_controls(value)
        or "\\" in value
        or any(character.isspace() for character in value)
    )


def _validate_max_retries(max_retries: int) -> None:
    if (
        isinstance(max_retries, bool)
        or not isinstance(max_retries, int)
        or not 0 <= max_retries <= 10
    ):
        raise ParameterError("max_retries must be between 0 and 10")


def _validate_base_url_structure(parsed: Any) -> None:
    """Validate an already-parsed base URL's scheme/authority/query/fragment."""
    try:
        _ = parsed.port
    except ValueError:
        raise ParameterError("AUDIOBOOKSHELF_URL is invalid") from None
    if parsed.scheme != "https" or not parsed.hostname:
        raise ParameterError("AUDIOBOOKSHELF_URL must be an absolute HTTPS URL")
    if parsed.username or parsed.password:
        raise ParameterError("AUDIOBOOKSHELF_URL must not contain credentials")
    if parsed.query or parsed.fragment:
        raise ParameterError("AUDIOBOOKSHELF_URL must not contain a query or fragment")


def _validate_base_url(base_url: str) -> str:
    """Normalize and validate ``base_url``; returns the validated host string."""
    host = str(base_url or "").strip().rstrip("/")
    if not 1 <= len(host.encode("utf-8")) <= _MAX_URL_BYTES:
        raise MissingParameterError("AUDIOBOOKSHELF_URL is required")
    if _invalid_url_text(host):
        raise ParameterError("AUDIOBOOKSHELF_URL is invalid")
    _validate_base_url_structure(urlsplit(host))
    return host


def _validate_token(token: str) -> str:
    """Validate ``token``; returns the validated credential string."""
    credential = str(token or "")
    if (
        not 1 <= len(credential.encode("utf-8")) <= _MAX_TOKEN_BYTES
        or _has_controls(credential)
        or any(character.isspace() for character in credential)
        or credential.startswith(_RUNTIME_REFERENCE_PREFIXES)
    ):
        raise MissingParameterError(
            "AUDIOBOOKSHELF_TOKEN must be a resolved runtime credential"
        )
    return credential


def _configure_authenticated_session(
    tls_profile: ResolvedTLSProfile, credential: str
) -> requests.Session:
    """Build a TLS-configured, bearer-authenticated session, cleaning up on failure."""
    try:
        session = tls_profile.configure_requests_session(requests.Session())
        session.headers.update({"Authorization": f"Bearer {credential}"})
        return session
    except Exception:
        tls_profile.cleanup()
        raise


def _is_path_text_valid(rendered: str) -> bool:
    """Whether a raw path string is well-formed (leading slash, size, no control/space)."""
    return (
        rendered.startswith("/")
        and 1 <= len(rendered.encode("utf-8")) <= _MAX_PATH_BYTES
        and not _invalid_url_text(rendered)
    )


def _is_relative_path_structure_valid(parsed: Any) -> bool:
    """Whether a parsed path carries no authority/query/fragment/traversal segment."""
    if parsed.scheme or parsed.netloc or parsed.query or parsed.fragment:
        return False
    return not any(segment in {".", ".."} for segment in parsed.path.split("/"))


def _is_valid_relative_path(rendered: str, parsed: Any) -> bool:
    """Whether ``rendered``/its pre-parsed form is a safe same-authority relative path."""
    return _is_path_text_valid(rendered) and _is_relative_path_structure_valid(parsed)


def _raise_for_status(response: requests.Response) -> None:
    """Close+raise the right typed error for an unsuccessful response; no-op on 2xx."""
    if response.status_code == 401:
        response.close()
        raise AuthError("Audiobookshelf rejected the active credential")
    if response.status_code == 403:
        response.close()
        raise UnauthorizedError("Audiobookshelf denied the requested operation")
    if not 200 <= response.status_code < 300:
        status = response.status_code
        response.close()
        raise ApiError(f"Audiobookshelf API returned HTTP {status}")


class ApiClientBase:
    """Base client used by every Audiobookshelf API domain mixin."""

    def __init__(
        self,
        base_url: str,
        token: str,
        tls_profile: ResolvedTLSProfile | None = None,
        max_retries: int = 3,
    ) -> None:
        _validate_max_retries(max_retries)
        host = _validate_base_url(base_url)
        credential = _validate_token(token)

        self.base_url = host
        self.max_retries = max_retries
        self.tls_profile = tls_profile or resolve_tls_profile("audiobookshelf")
        self.session = _configure_authenticated_session(self.tls_profile, credential)

    def close(self) -> None:
        """Release the HTTP session and temporary TLS material."""
        self.session.headers.pop("Authorization", None)
        self.session.close()
        self.tls_profile.cleanup()

    @staticmethod
    def _path(*segments: Any) -> str:
        """Encode untrusted path segments without allowing authority or path escape."""
        encoded: list[str] = []
        for segment in segments:
            rendered = str(segment)
            if not 1 <= len(
                rendered.encode("utf-8")
            ) <= _MAX_SEGMENT_BYTES or _has_controls(rendered):
                raise ParameterError("API path parameter is invalid")
            encoded.append(quote(rendered, safe=""))
        return "/" + "/".join(encoded)

    def _resolve_url(self, path: str) -> str:
        rendered = str(path or "")
        parsed = urlsplit(rendered)
        if not _is_valid_relative_path(rendered, parsed):
            raise ParameterError("API path is invalid")
        resolved = f"{self.base_url}{rendered}"
        configured = urlsplit(self.base_url)
        target = urlsplit(resolved)
        if target.scheme != configured.scheme or target.netloc != configured.netloc:
            raise ParameterError("API request authority differs from configuration")
        return resolved

    def _send_once(
        self,
        method: str,
        url: str,
        params: dict[str, Any] | None,
        json: Any | None,
    ) -> requests.Response:
        try:
            return self.session.request(
                method,
                url,
                params=params or None,
                json=json,
                timeout=60.0,
                allow_redirects=False,
                stream=True,
            )
        except requests.RequestException:
            raise ApiError("Audiobookshelf API request failed") from None

    def _should_retry(self, response: requests.Response, attempt: int) -> bool:
        return (
            response.status_code in _TRANSIENT_STATUSES and attempt < self.max_retries
        )

    def _finish_response(self, response: requests.Response) -> Any:
        _raise_for_status(response)
        try:
            return self._decode(response)
        except requests.RequestException:
            raise ApiError("Audiobookshelf API response failed") from None
        finally:
            response.close()

    def request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
    ) -> Any:
        """Issue one same-authority request with bounded retries and output."""
        normalized_method = str(method or "").upper()
        if normalized_method not in _ALLOWED_METHODS:
            raise ParameterError("Unsupported HTTP method")
        url = self._resolve_url(path)

        attempt = 0
        while True:
            response = self._send_once(normalized_method, url, params, json)
            if self._should_retry(response, attempt):
                delay = self._retry_delay(response, attempt)
                response.close()
                time.sleep(delay)
                attempt += 1
                continue
            return self._finish_response(response)

    @staticmethod
    def _retry_delay(response: requests.Response, attempt: int) -> float:
        retry_after = response.headers.get("Retry-After")
        if retry_after:
            try:
                parsed = float(retry_after)
                if math.isfinite(parsed):
                    return min(max(parsed, 0.0), 60.0)
            except ValueError:
                pass
        return min(2.0**attempt, 30.0)

    @staticmethod
    def _decode(response: requests.Response) -> Any:
        declared_length = response.headers.get("Content-Length")
        if declared_length:
            try:
                if int(declared_length) > _MAX_RESPONSE_BYTES:
                    raise ApiError(
                        "Audiobookshelf response exceeded the connector limit"
                    )
            except ValueError:
                pass

        content = bytearray()
        for chunk in response.iter_content(chunk_size=64 * 1024):
            if not chunk:
                continue
            content.extend(chunk)
            if len(content) > _MAX_RESPONSE_BYTES:
                raise ApiError("Audiobookshelf response exceeded the connector limit")
        if not content:
            return None
        if "application/json" in response.headers.get("Content-Type", ""):
            try:
                return json_module.loads(content)
            except (UnicodeDecodeError, ValueError):
                raise ApiError("Audiobookshelf returned invalid JSON") from None
        return bytes(content)
