"""Tests for the Excel recalculation module."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add the xlsx script to the path
XLSX_DIR = Path(__file__).resolve().parent.parent / "document-processing" / "xlsx"
sys.path.insert(0, str(XLSX_DIR))

import recalc


class TestRecalcNonexistentFile:
    """Tests for recalc with non-existent file."""

    def test_returns_error_for_missing_file(self):
        result = recalc.recalc("/nonexistent/path/file.xlsx")
        assert "error" in result
        assert "does not exist" in result["error"]


class TestHasGtimeout:
    """Tests for has_gtimeout function."""

    @patch("subprocess.run")
    def test_returns_true_when_available(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        assert recalc.has_gtimeout() is True

    @patch("subprocess.run", side_effect=FileNotFoundError)
    def test_returns_false_when_not_found(self, mock_run):
        assert recalc.has_gtimeout() is False


class TestSetupLibreofficeMacro:
    """Tests for setup_libreoffice_macro function."""

    @patch("recalc.Path.read_text", return_value="RecalculateAndSave")
    @patch("os.path.exists", return_value=True)
    def test_returns_true_when_macro_exists(self, mock_exists, mock_read):
        result = recalc.setup_libreoffice_macro()
        assert result is True
