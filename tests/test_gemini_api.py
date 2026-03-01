"""Tests for the Gemini API helper module."""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add the gemini-api script to the path
GEMINI_DIR = Path(__file__).resolve().parent.parent / "ai-apis" / "gemini" / "scripts"
sys.path.insert(0, str(GEMINI_DIR))

import gemini_api


class TestGetApiKey:
    """Tests for get_api_key function."""

    def test_reads_from_env(self):
        with patch.dict("os.environ", {"GEMINI_API_KEY": "test-key-123"}):
            key = gemini_api.get_api_key()
            assert key == "test-key-123"

    def test_raises_when_no_key(self):
        with patch.dict("os.environ", {}, clear=True):
            # Also mock the ecosystem.env file to not exist
            with patch.object(Path, "exists", return_value=False):
                with pytest.raises(ValueError, match="GEMINI_API_KEY not found"):
                    gemini_api.get_api_key()


class TestCategorizeTransaction:
    """Tests for categorize_transaction function (mocked API)."""

    @patch("gemini_api.call_gemini", return_value="Groceries")
    def test_returns_dict_with_category(self, mock_call):
        result = gemini_api.categorize_transaction("COSTCO WHOLESALE", -89.47)
        assert result["description"] == "COSTCO WHOLESALE"
        assert result["amount"] == -89.47
        assert result["category"] == "Groceries"

    @patch("gemini_api.call_gemini", return_value="  **Dining**  ")
    def test_cleans_asterisks_from_response(self, mock_call):
        result = gemini_api.categorize_transaction("RESTAURANT", -45.00)
        assert result["category"] == "Dining"


class TestResearchCompany:
    """Tests for research_company function (mocked API)."""

    @patch("gemini_api.call_gemini", return_value="A technology company...")
    def test_returns_research_dict(self, mock_call):
        result = gemini_api.research_company("Acme Corp")
        assert result["company"] == "Acme Corp"
        assert result["research"] == "A technology company..."
        assert "timestamp" in result

    @patch("gemini_api.call_gemini", return_value="Research results")
    def test_prompt_includes_company_name(self, mock_call):
        gemini_api.research_company("Test Company")
        prompt = mock_call.call_args[0][0]
        assert "Test Company" in prompt


class TestSummarizeText:
    """Tests for summarize_text function (mocked API)."""

    @patch("gemini_api.call_gemini", return_value="A brief summary.")
    def test_returns_summary_string(self, mock_call):
        result = gemini_api.summarize_text("Long text here...")
        assert result == "A brief summary."

    @patch("gemini_api.call_gemini", return_value="Summary")
    def test_passes_max_words_in_prompt(self, mock_call):
        gemini_api.summarize_text("Text", max_words=50)
        prompt = mock_call.call_args[0][0]
        assert "50" in prompt
