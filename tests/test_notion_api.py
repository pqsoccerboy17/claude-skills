"""Basic tests for the Notion API client module."""

import sys
import json
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

# Add the notion-api script to the path
NOTION_DIR = Path(__file__).resolve().parent.parent / "productivity" / "notion-api" / "scripts"
sys.path.insert(0, str(NOTION_DIR))

import notion_api


class TestGetConfig:
    def test_returns_dict(self):
        config = notion_api.get_config()
        assert isinstance(config, dict)
        assert "token" in config
        assert "automation_db_id" in config

    def test_reads_env_token(self):
        with patch.dict("os.environ", {"NOTION_TOKEN": "test-token-123"}):
            config = notion_api.get_config()
            assert config["token"] == "test-token-123"


class TestNotionClient:
    def test_requires_token(self):
        with patch.dict("os.environ", {}, clear=True):
            with patch.object(notion_api, "get_config", return_value={"token": None, "automation_db_id": None}):
                with pytest.raises(ValueError, match="Notion token not found"):
                    notion_api.NotionClient()

    def test_initializes_with_token(self):
        client = notion_api.NotionClient(token="test-token")
        assert client.token == "test-token"
        assert "Bearer test-token" in client._headers["Authorization"]

    def test_headers_include_api_version(self):
        client = notion_api.NotionClient(token="test-token")
        assert client._headers["Notion-Version"] == notion_api.NOTION_API_VERSION
        assert client._headers["Content-Type"] == "application/json"


class TestNotionAPIError:
    def test_error_message(self):
        err = notion_api.NotionAPIError(404, "Not found")
        assert err.status_code == 404
        assert err.message == "Not found"
        assert "404" in str(err)
        assert "Not found" in str(err)


class TestQueryDatabase:
    @patch.object(notion_api.NotionClient, "_request")
    def test_basic_query(self, mock_request):
        mock_request.return_value = {"results": [], "has_more": False}
        client = notion_api.NotionClient(token="test-token")
        result = client.query_database("db-123")
        mock_request.assert_called_once_with(
            "POST", "/databases/db-123/query", {"page_size": 100}
        )
        assert result == {"results": [], "has_more": False}

    @patch.object(notion_api.NotionClient, "_request")
    def test_query_with_filter(self, mock_request):
        mock_request.return_value = {"results": []}
        client = notion_api.NotionClient(token="test-token")
        test_filter = {"property": "Status", "select": {"equals": "Done"}}
        client.query_database("db-123", filter=test_filter)
        call_body = mock_request.call_args[0][2]
        assert call_body["filter"] == test_filter


class TestSearch:
    @patch.object(notion_api.NotionClient, "_request")
    def test_basic_search(self, mock_request):
        mock_request.return_value = {"results": []}
        client = notion_api.NotionClient(token="test-token")
        client.search("test query")
        mock_request.assert_called_once_with(
            "POST", "/search", {"query": "test query", "page_size": 100}
        )

    @patch.object(notion_api.NotionClient, "_request")
    def test_search_with_filter(self, mock_request):
        mock_request.return_value = {"results": []}
        client = notion_api.NotionClient(token="test-token")
        client.search("test", filter_type="page")
        call_body = mock_request.call_args[0][2]
        assert call_body["filter"] == {"property": "object", "value": "page"}
