from typing import Any

from .api_client_base import ApiClientBase


class ApiClientSeries(ApiClientBase):
    """Series operations (Audiobookshelf ``Series`` tag)."""

    def get_series(self, id: str, **params: Any) -> dict[str, Any]:
        """Get a single series by id (supports include params)."""
        return self.request(
            "GET", self._path("api", "series", id), params=params or None
        )

    def update_series(self, id: str, **body: Any) -> dict[str, Any]:
        """Update a series by id."""
        return self.request("PATCH", self._path("api", "series", id), json=body)
