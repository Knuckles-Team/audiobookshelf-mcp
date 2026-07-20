from typing import Any

from .api_client_base import ApiClientBase


class ApiClientPodcasts(ApiClientBase):
    """Podcast operations (Audiobookshelf ``Podcasts`` tag)."""

    def create_podcast(self, **body: Any) -> dict[str, Any]:
        """Create a new podcast library item."""
        return self.request("POST", "/api/podcasts", json=body)

    def get_podcast_feed(self, **body: Any) -> dict[str, Any]:
        """Fetch a podcast RSS feed by URL."""
        return self.request("POST", "/api/podcasts/feed", json=body)

    def bulk_create_podcasts_from_opml_feed(self, **body: Any) -> dict[str, Any]:
        """Bulk create podcasts from an OPML feed."""
        return self.request("POST", "/api/podcasts/opml/create", json=body)

    def get_feeds_from_opml_text(self, **body: Any) -> dict[str, Any]:
        """Parse feeds from raw OPML text."""
        return self.request("POST", "/api/podcasts/opml/parse", json=body)

    def check_new_episodes(self, id: str) -> dict[str, Any]:
        """Check for new episodes for a podcast by id."""
        return self.request("GET", self._path("api", "podcasts", id, "checknew"))

    def clear_episode_download_queue(self, id: str) -> dict[str, Any]:
        """Clear the episode download queue for a podcast by id."""
        return self.request("GET", self._path("api", "podcasts", id, "clear-queue"))

    def download_episodes(self, id: str, **body: Any) -> dict[str, Any]:
        """Queue episodes for download for a podcast by id."""
        return self.request(
            "POST", self._path("api", "podcasts", id, "download-episodes"), json=body
        )

    def get_episode_downloads(self, id: str) -> dict[str, Any]:
        """Get the current episode download queue for a podcast by id."""
        return self.request("GET", self._path("api", "podcasts", id, "downloads"))

    def get_episode(self, id: str, episode_id: str) -> dict[str, Any]:
        """Get a single podcast episode by id."""
        return self.request(
            "GET", self._path("api", "podcasts", id, "episode", episode_id)
        )

    def update_episode(self, id: str, episode_id: str, **body: Any) -> dict[str, Any]:
        """Update a podcast episode by id."""
        return self.request(
            "PATCH", self._path("api", "podcasts", id, "episode", episode_id), json=body
        )

    def remove_episode(self, id: str, episode_id: str) -> dict[str, Any]:
        """Remove a podcast episode by id."""
        return self.request(
            "DELETE", self._path("api", "podcasts", id, "episode", episode_id)
        )

    def quick_match_episodes(self, id: str, **body: Any) -> dict[str, Any]:
        """Quick-match a podcast's episodes against a feed by id."""
        return self.request(
            "POST", self._path("api", "podcasts", id, "match-episodes"), json=body
        )

    def find_episode(self, id: str, **params: Any) -> dict[str, Any]:
        """Search for a podcast episode by id."""
        return self.request(
            "GET",
            self._path("api", "podcasts", id, "search-episode"),
            params=params or None,
        )
