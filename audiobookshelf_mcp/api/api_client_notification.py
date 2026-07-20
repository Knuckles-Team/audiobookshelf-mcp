from typing import Any

from .api_client_base import ApiClientBase


class ApiClientNotification(ApiClientBase):
    """Notification operations (Audiobookshelf ``Notification`` tag)."""

    def get_notification_event_data(self) -> dict[str, Any]:
        """Get the available notification event data."""
        return self.request("GET", "/api/notificationdata")

    def get_notifications(self) -> dict[str, Any]:
        """Get the configured notification settings and notifications."""
        return self.request("GET", "/api/notifications")

    def configure_notification_settings(self, **body: Any) -> dict[str, Any]:
        """Update the global notification settings."""
        return self.request("PATCH", "/api/notifications", json=body)

    def create_notification(self, **body: Any) -> dict[str, Any]:
        """Create a new notification."""
        return self.request("POST", "/api/notifications", json=body)

    def send_default_test_notification(self) -> dict[str, Any]:
        """Send a default test notification."""
        return self.request("GET", "/api/notifications/test")

    def delete_notification(self, id: str) -> dict[str, Any]:
        """Delete a notification by id."""
        return self.request("DELETE", self._path("api", "notifications", id))

    def update_notification(self, id: str, **body: Any) -> dict[str, Any]:
        """Update a notification by id."""
        return self.request("PATCH", self._path("api", "notifications", id), json=body)

    def send_test_notification(self, id: str) -> dict[str, Any]:
        """Send a test notification for a specific notification by id."""
        return self.request("GET", self._path("api", "notifications", id, "test"))
