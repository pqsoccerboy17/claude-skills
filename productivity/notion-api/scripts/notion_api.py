#!/usr/bin/env python3
"""
Notion API Client for Claude Code Sessions

Provides direct Notion API access for Code mode sessions where MCP servers
aren't available. Mirrors functionality from ecosystem-mcp-server.

Usage:
    from notion_api import NotionClient
    notion = NotionClient()
    results = notion.query_database("db-id")

Or from command line:
    python3 notion_api.py query <database-id>
    python3 notion_api.py search "query"
    python3 notion_api.py status

Environment Variables:
    NOTION_TOKEN              - Notion integration token (required)
    NOTION_AUTOMATION_DB_ID   - Default automation requests database ID
"""

import os
import json
import time
import logging
import urllib.request
import urllib.parse
import urllib.error
from pathlib import Path
from typing import Optional, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# =============================================================================
# Configuration
# =============================================================================

NOTION_API_VERSION = "2022-06-28"
NOTION_API_BASE = "https://api.notion.com/v1"

CONFIG_PATHS = [
    Path.home() / ".config" / "notion" / "config.json",
    Path.home() / ".notion" / "config.json",
    Path.home() / "Library" / "Application Support" / "ecosystem-mcp-server" / "notion_config.json",
]


def get_config() -> dict:
    """
    Get Notion configuration from environment or config file.

    Priority:
    1. Environment variables
    2. Config files (checked in order)
    """
    config = {
        "token": os.getenv("NOTION_TOKEN"),
        "automation_db_id": os.getenv("NOTION_AUTOMATION_DB_ID"),
    }

    # If no token in env, check config files
    if not config["token"]:
        for config_path in CONFIG_PATHS:
            if config_path.exists():
                try:
                    with open(config_path) as f:
                        file_config = json.load(f)
                        config["token"] = file_config.get("token") or file_config.get("notion_token")
                        config["automation_db_id"] = config["automation_db_id"] or file_config.get("automation_db_id") or file_config.get("database_id")
                        if config["token"]:
                            logger.debug(f"Loaded config from {config_path}")
                            break
                except Exception as e:
                    logger.warning(f"Failed to read {config_path}: {e}")

    return config


# =============================================================================
# Notion API Client
# =============================================================================

class NotionClient:
    """
    Direct Notion API client for Code mode sessions.

    Provides database queries, page operations, and search functionality
    without requiring MCP infrastructure.
    """

    def __init__(self, token: Optional[str] = None):
        """
        Initialize the Notion client.

        Args:
            token: Notion integration token. If not provided, will be read
                   from NOTION_TOKEN env var or config file.
        """
        config = get_config()
        self.token = token or config["token"]
        self.automation_db_id = config["automation_db_id"]

        if not self.token:
            raise ValueError(
                "Notion token not found. Set NOTION_TOKEN environment variable "
                "or create a config file at ~/.config/notion/config.json"
            )

        self._headers = {
            "Authorization": f"Bearer {self.token}",
            "Notion-Version": NOTION_API_VERSION,
            "Content-Type": "application/json",
        }

    def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict] = None,
        retries: int = 3,
    ) -> dict:
        """
        Make an API request to Notion.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint (e.g., "/databases/xxx/query")
            data: Request body for POST/PATCH
            retries: Number of retries for rate limiting

        Returns:
            API response as dict
        """
        url = f"{NOTION_API_BASE}{endpoint}"

        for attempt in range(retries):
            try:
                body = json.dumps(data).encode() if data else None
                req = urllib.request.Request(
                    url,
                    data=body,
                    headers=self._headers,
                    method=method,
                )

                with urllib.request.urlopen(req, timeout=30) as response:
                    return json.loads(response.read().decode())

            except urllib.error.HTTPError as e:
                error_body = e.read().decode() if e.fp else ""

                # Rate limited - retry with backoff
                if e.code == 429 and attempt < retries - 1:
                    wait_time = 2 ** attempt
                    logger.warning(f"Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue

                # Parse error message
                try:
                    error_data = json.loads(error_body)
                    message = error_data.get("message", str(e))
                except json.JSONDecodeError:
                    message = error_body or str(e)

                raise NotionAPIError(e.code, message) from e

            except urllib.error.URLError as e:
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)
                    continue
                raise NotionAPIError(0, f"Network error: {e}") from e

        raise NotionAPIError(0, "Max retries exceeded")

    # =========================================================================
    # Database Operations
    # =========================================================================

    def query_database(
        self,
        database_id: str,
        filter: Optional[dict] = None,
        sorts: Optional[list] = None,
        page_size: int = 100,
        start_cursor: Optional[str] = None,
    ) -> dict:
        """
        Query a Notion database.

        Args:
            database_id: The database ID to query
            filter: Notion filter object
            sorts: List of sort objects
            page_size: Number of results per page (max 100)
            start_cursor: Cursor for pagination

        Returns:
            Query results with 'results' list and pagination info
        """
        body = {"page_size": min(page_size, 100)}

        if filter:
            body["filter"] = filter
        if sorts:
            body["sorts"] = sorts
        if start_cursor:
            body["start_cursor"] = start_cursor

        return self._request("POST", f"/databases/{database_id}/query", body)

    def get_database(self, database_id: str) -> dict:
        """Get database metadata and schema."""
        return self._request("GET", f"/databases/{database_id}")

    # =========================================================================
    # Page Operations
    # =========================================================================

    def get_page(self, page_id: str) -> dict:
        """
        Get a page by ID.

        Args:
            page_id: The page ID

        Returns:
            Page object with properties
        """
        return self._request("GET", f"/pages/{page_id}")

    def create_page(
        self,
        database_id: str,
        properties: dict,
        children: Optional[list] = None,
    ) -> dict:
        """
        Create a new page in a database.

        Args:
            database_id: Parent database ID
            properties: Page properties matching database schema
            children: Optional content blocks

        Returns:
            Created page object
        """
        body = {
            "parent": {"database_id": database_id},
            "properties": properties,
        }

        if children:
            body["children"] = children

        return self._request("POST", "/pages", body)

    def update_page(self, page_id: str, properties: dict) -> dict:
        """
        Update a page's properties.

        Args:
            page_id: The page ID to update
            properties: Properties to update

        Returns:
            Updated page object
        """
        return self._request("PATCH", f"/pages/{page_id}", {"properties": properties})

    def get_page_content(self, page_id: str) -> list:
        """
        Get all blocks (content) from a page.

        Args:
            page_id: The page ID

        Returns:
            List of block objects
        """
        blocks = []
        cursor = None

        while True:
            endpoint = f"/blocks/{page_id}/children"
            if cursor:
                endpoint += f"?start_cursor={cursor}"

            response = self._request("GET", endpoint)
            blocks.extend(response.get("results", []))

            if not response.get("has_more"):
                break
            cursor = response.get("next_cursor")

        return blocks

    # =========================================================================
    # Search
    # =========================================================================

    def search(
        self,
        query: str,
        filter_type: Optional[str] = None,
        page_size: int = 100,
    ) -> dict:
        """
        Search Notion for pages and databases.

        Args:
            query: Search query text
            filter_type: "page" or "database" to filter results
            page_size: Number of results

        Returns:
            Search results
        """
        body = {"query": query, "page_size": min(page_size, 100)}

        if filter_type in ("page", "database"):
            body["filter"] = {"property": "object", "value": filter_type}

        return self._request("POST", "/search", body)

    # =========================================================================
    # Automation Requests (mirrors ecosystem-mcp-server)
    # =========================================================================

    def get_pending_requests(self, database_id: Optional[str] = None) -> list:
        """
        Get pending automation requests from the control plane database.

        Args:
            database_id: Automation requests database ID (uses default if not provided)

        Returns:
            List of pending request pages
        """
        db_id = database_id or self.automation_db_id
        if not db_id:
            raise ValueError("No automation database ID configured")

        response = self.query_database(
            db_id,
            filter={"property": "Status", "select": {"equals": "queued"}},
            sorts=[{"property": "Created", "direction": "ascending"}],
        )

        return [self._parse_request(page) for page in response.get("results", [])]

    def _parse_request(self, page: dict) -> dict:
        """Parse automation request from page properties."""
        props = page.get("properties", {})

        def get_title(prop):
            title = prop.get("title", [])
            return title[0]["text"]["content"] if title else ""

        def get_select(prop):
            select = prop.get("select")
            return select["name"] if select else None

        def get_text(prop):
            rich_text = prop.get("rich_text", [])
            return rich_text[0]["text"]["content"] if rich_text else ""

        return {
            "id": page["id"],
            "name": get_title(props.get("Name", {})),
            "command": get_select(props.get("Command", {})),
            "arguments": get_text(props.get("Arguments", {})),
            "status": get_select(props.get("Status", {})),
            "created": page.get("created_time"),
        }

    def update_request_status(
        self,
        page_id: str,
        status: str,
        result: Optional[str] = None,
    ) -> dict:
        """
        Update automation request status.

        Args:
            page_id: Request page ID
            status: New status (queued, running, done, failed)
            result: Optional result text

        Returns:
            Updated page object
        """
        properties = {
            "Status": {"select": {"name": status}},
        }

        if status in ("done", "failed"):
            properties["Processed"] = {"date": {"start": datetime.now().isoformat()}}

        if result:
            # Truncate result to Notion's limit
            truncated = result[:2000] if len(result) > 2000 else result
            properties["Result"] = {"rich_text": [{"text": {"content": truncated}}]}

        return self.update_page(page_id, properties)

    # =========================================================================
    # Utilities
    # =========================================================================

    def test_connection(self) -> dict:
        """
        Test the API connection and return user info.

        Returns:
            Dict with connection status and user info
        """
        try:
            response = self._request("GET", "/users/me")
            return {
                "connected": True,
                "user": response.get("name"),
                "type": response.get("type"),
                "bot": response.get("bot", {}),
            }
        except NotionAPIError as e:
            return {
                "connected": False,
                "error": str(e),
            }


class NotionAPIError(Exception):
    """Notion API error with status code and message."""

    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"Notion API Error ({status_code}): {message}")


# =============================================================================
# Helper Functions (for use without class instantiation)
# =============================================================================

def query_database(database_id: str, **kwargs) -> dict:
    """Query a database. See NotionClient.query_database for args."""
    return NotionClient().query_database(database_id, **kwargs)


def search(query: str, **kwargs) -> dict:
    """Search Notion. See NotionClient.search for args."""
    return NotionClient().search(query, **kwargs)


def get_page(page_id: str) -> dict:
    """Get a page by ID."""
    return NotionClient().get_page(page_id)


def create_page(database_id: str, properties: dict, **kwargs) -> dict:
    """Create a page. See NotionClient.create_page for args."""
    return NotionClient().create_page(database_id, properties, **kwargs)


def update_page(page_id: str, properties: dict) -> dict:
    """Update a page's properties."""
    return NotionClient().update_page(page_id, properties)


def get_pending_requests(database_id: Optional[str] = None) -> list:
    """Get pending automation requests."""
    return NotionClient().get_pending_requests(database_id)


# =============================================================================
# CLI
# =============================================================================

def main():
    """Command-line interface."""
    import sys

    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
    )

    if len(sys.argv) < 2:
        print("Notion API Client for Claude Code Sessions")
        print()
        print("Usage:")
        print("  python3 notion_api.py status              - Test connection")
        print("  python3 notion_api.py search <query>      - Search for pages")
        print("  python3 notion_api.py query <db-id>       - Query a database")
        print("  python3 notion_api.py get <page-id>       - Get a page")
        print("  python3 notion_api.py pending             - Get pending automation requests")
        print()
        print("Environment:")
        print("  NOTION_TOKEN              - Integration token (required)")
        print("  NOTION_AUTOMATION_DB_ID   - Default automation database")
        sys.exit(1)

    command = sys.argv[1]

    try:
        client = NotionClient()

        if command == "status":
            result = client.test_connection()
            if result["connected"]:
                print(f"Connected as: {result['user']}")
                print(f"Type: {result['type']}")
                if result.get("bot"):
                    print(f"Workspace: {result['bot'].get('workspace_name', 'N/A')}")
            else:
                print(f"Connection failed: {result['error']}")
                sys.exit(1)

        elif command == "search":
            if len(sys.argv) < 3:
                print("Usage: notion_api.py search <query>")
                sys.exit(1)
            query = " ".join(sys.argv[2:])
            results = client.search(query)
            print(f"Found {len(results.get('results', []))} results:")
            for item in results.get("results", [])[:10]:
                obj_type = item.get("object")
                title = ""
                if obj_type == "page":
                    props = item.get("properties", {})
                    for prop in props.values():
                        if prop.get("type") == "title":
                            title_arr = prop.get("title", [])
                            title = title_arr[0]["text"]["content"] if title_arr else ""
                            break
                elif obj_type == "database":
                    title_arr = item.get("title", [])
                    title = title_arr[0]["text"]["content"] if title_arr else ""
                print(f"  [{obj_type}] {title or '(untitled)'} - {item['id']}")

        elif command == "query":
            if len(sys.argv) < 3:
                print("Usage: notion_api.py query <database-id>")
                sys.exit(1)
            db_id = sys.argv[2]
            results = client.query_database(db_id)
            print(f"Found {len(results.get('results', []))} entries")
            print(json.dumps(results, indent=2, default=str))

        elif command == "get":
            if len(sys.argv) < 3:
                print("Usage: notion_api.py get <page-id>")
                sys.exit(1)
            page_id = sys.argv[2]
            page = client.get_page(page_id)
            print(json.dumps(page, indent=2, default=str))

        elif command == "pending":
            requests = client.get_pending_requests()
            if not requests:
                print("No pending automation requests")
            else:
                print(f"Found {len(requests)} pending requests:")
                for req in requests:
                    print(f"  [{req['command']}] {req['name']} - {req['id']}")

        else:
            print(f"Unknown command: {command}")
            sys.exit(1)

    except ValueError as e:
        print(f"Configuration error: {e}")
        sys.exit(1)
    except NotionAPIError as e:
        print(f"API error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
