"""Tests for the ecosystem status module."""

import sys
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add the ecosystem-status script to the path
STATUS_DIR = Path(__file__).resolve().parent.parent / "productivity" / "ecosystem-status" / "scripts"
sys.path.insert(0, str(STATUS_DIR))

import ecosystem_status


class TestFormatTimeAgo:
    """Tests for format_time_ago function."""

    def test_just_now(self):
        now = datetime.now()
        result = ecosystem_status.format_time_ago(now)
        assert result == "just now"

    def test_minutes_ago(self):
        dt = datetime.now() - timedelta(minutes=5)
        result = ecosystem_status.format_time_ago(dt)
        assert "5 minutes ago" == result

    def test_single_minute(self):
        dt = datetime.now() - timedelta(minutes=1, seconds=30)
        result = ecosystem_status.format_time_ago(dt)
        assert "1 minute ago" == result

    def test_hours_ago(self):
        dt = datetime.now() - timedelta(hours=3)
        result = ecosystem_status.format_time_ago(dt)
        assert "3 hours ago" == result

    def test_single_hour(self):
        dt = datetime.now() - timedelta(hours=1, minutes=30)
        result = ecosystem_status.format_time_ago(dt)
        assert "1 hour ago" == result

    def test_days_ago(self):
        dt = datetime.now() - timedelta(days=7)
        result = ecosystem_status.format_time_ago(dt)
        assert "7 days ago" == result

    def test_single_day(self):
        dt = datetime.now() - timedelta(days=1, hours=5)
        result = ecosystem_status.format_time_ago(dt)
        assert "1 day ago" == result


class TestGetFileMtime:
    """Tests for get_file_mtime function."""

    def test_nonexistent_file(self):
        result = ecosystem_status.get_file_mtime(Path("/nonexistent/path/file.txt"))
        assert result is None

    def test_existing_file(self, tmp_path):
        test_file = tmp_path / "test.txt"
        test_file.write_text("test")
        result = ecosystem_status.get_file_mtime(test_file)
        assert isinstance(result, datetime)


class TestCountFilesInDownloads:
    """Tests for count_files_in_downloads function."""

    def test_with_mocked_empty_downloads(self, tmp_path):
        with patch.object(ecosystem_status, "HOME", tmp_path):
            downloads = tmp_path / "Downloads"
            downloads.mkdir()
            count = ecosystem_status.count_files_in_downloads(["pdf"])
            assert count == 0

    def test_counts_matching_files(self, tmp_path):
        with patch.object(ecosystem_status, "HOME", tmp_path):
            downloads = tmp_path / "Downloads"
            downloads.mkdir()
            (downloads / "file1.pdf").write_text("test")
            (downloads / "file2.pdf").write_text("test")
            (downloads / "file3.txt").write_text("test")
            count = ecosystem_status.count_files_in_downloads(["pdf"])
            assert count == 2
