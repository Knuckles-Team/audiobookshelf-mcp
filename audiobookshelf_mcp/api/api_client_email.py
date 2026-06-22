from typing import Any

from .api_client_base import ApiClientBase


class ApiClientEmail(ApiClientBase):
    """Email settings and e-reader delivery operations (``Email`` tag)."""

    def get_email_settings(self) -> dict[str, Any]:
        """Get the server email settings."""
        return self.request("GET", "/api/emails/settings")

    def update_email_settings(self, **body: Any) -> dict[str, Any]:
        """Update the server email settings."""
        return self.request("PATCH", "/api/emails/settings", json=body)

    def update_ereader_devices(self, **body: Any) -> dict[str, Any]:
        """Update the configured e-reader devices."""
        return self.request("POST", "/api/emails/ereader-devices", json=body)

    def send_ebook_to_device(self, **body: Any) -> dict[str, Any]:
        """Send an ebook to a configured e-reader device."""
        return self.request("POST", "/api/emails/send-ebook-to-device", json=body)

    def send_test_email(self, **body: Any) -> dict[str, Any]:
        """Send a test email using the configured settings."""
        return self.request("POST", "/api/emails/test", json=body)
