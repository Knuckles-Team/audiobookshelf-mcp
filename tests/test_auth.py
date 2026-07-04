from unittest.mock import patch

import pytest

import audiobookshelf_mcp.auth as auth_module
from audiobookshelf_mcp.auth import get_client


@pytest.mark.concept("AS-OS.identity.abs")
def test_get_client_auth_error():
    """Auth failure surfaces a clear error. CONCEPT:AS-OS.identity.abs"""
    auth_module._client = None
    with patch("audiobookshelf_mcp.auth.ApiClientSystem") as mock_client_cls:
        mock_client_cls.side_effect = Exception("Auth Failure")
        with pytest.raises(RuntimeError) as exc_info:
            get_client()
        assert "AUTHENTICATION ERROR" in str(exc_info.value)
    auth_module._client = None
