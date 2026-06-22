from typing import Any

import requests


class ApiClientBase:
    """Base HTTP API client wrapper for the Audiobookshelf REST API.

    Authentication is a Bearer API token issued from the user account settings
    (Config -> API Keys). All requests are sent against ``{base_url}/api/...``.
    """

    def __init__(self, base_url: str, token: str, verify: bool = True):
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.verify = verify
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    def request(
        self,
        method: str,
        path: str,
        params: dict[str, Any] | None = None,
        json: Any | None = None,
        **kwargs,
    ) -> dict[str, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        response = self.session.request(
            method,
            url,
            params=params,
            json=json,
            verify=self.verify,
            **kwargs,
        )
        response.raise_for_status()
        try:
            return response.json()
        except ValueError:
            return {"status": response.status_code, "text": response.text}
