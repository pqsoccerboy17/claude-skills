"""Basic tests for the notifications module."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add the notify script to the path
NOTIFY_DIR = Path(__file__).resolve().parent.parent / "productivity" / "notifications" / "scripts"
sys.path.insert(0, str(NOTIFY_DIR))

import notify


class TestGetConfig:
    def test_returns_dict(self):
        config = notify.get_config()
        assert isinstance(config, dict)
        assert "enabled" in config
        assert "pushover_user" in config
        assert "pushover_token" in config

    def test_disabled_via_env(self):
        with patch.dict("os.environ", {"NOTIFY_ENABLED": "false"}):
            config = notify.get_config()
            assert config["enabled"] is False

    def test_enabled_by_default(self):
        with patch.dict("os.environ", {}, clear=True):
            config = notify.get_config()
            assert config["enabled"] is True


class TestSendNotification:
    def test_disabled_returns_false(self):
        with patch.dict("os.environ", {"NOTIFY_ENABLED": "false"}):
            result = notify.send_notification("Test", "Body")
            assert result is False

    @patch("notify.send_pushover", return_value=True)
    def test_tries_pushover_first(self, mock_pushover):
        with patch.dict("os.environ", {"NOTIFY_ENABLED": "true"}):
            result = notify.send_notification("Title", "Message", priority=1)
            mock_pushover.assert_called_once_with("Title", "Message", 1, None, None)
            assert result is True

    @patch("notify.send_macos_notification", return_value=True)
    @patch("notify.send_pushover", return_value=False)
    def test_falls_back_to_macos(self, mock_pushover, mock_macos):
        with patch.dict("os.environ", {"NOTIFY_ENABLED": "true"}):
            result = notify.send_notification("Title", "Message")
            mock_macos.assert_called_once_with("Title", "Message")
            assert result is True


class TestNotifyOrganizationComplete:
    @patch("notify.send_notification", return_value=True)
    def test_basic_call(self, mock_send):
        result = notify.notify_organization_complete(
            organizer_name="Tax Organizer",
            files_organized=3,
        )
        assert result is True
        mock_send.assert_called_once()
        title = mock_send.call_args[0][0]
        assert "Tax Organizer" in title

    @patch("notify.send_notification", return_value=True)
    def test_error_priority(self, mock_send):
        notify.notify_organization_complete(
            organizer_name="Test",
            files_organized=1,
            errors=2,
        )
        priority = mock_send.call_args[0][2]
        assert priority == 1  # High priority for errors
