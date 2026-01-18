#!/usr/bin/env python3
"""
Asset CRUD Operations for Notion Database

Create, read, update, and delete assets in the Notion Asset Inventory database.

Usage:
    # Create a new asset
    python3 asset_crud.py create --id "TH-HVAC-01" --name "Primary AC Unit" \
        --category "HVAC" --location "123 Main St" --cost 3500 \
        --purchase-date "2024-01-15" --warranty-years 5 --service-interval 90

    # Get asset details
    python3 asset_crud.py get --id "TH-HVAC-01"

    # List all assets
    python3 asset_crud.py list

    # List assets by category
    python3 asset_crud.py list --category "HVAC"

    # Update an asset
    python3 asset_crud.py update --id "TH-HVAC-01" --status "Needs Service"

    # Search assets
    python3 asset_crud.py search --query "AC"

Environment Variables:
    NOTION_TOKEN - Notion integration token
    NOTION_ASSETS_DB_ID - Asset Inventory database ID
"""

import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Optional

try:
    import requests
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)


# =============================================================================
# Configuration
# =============================================================================

NOTION_TOKEN = os.environ.get("NOTION_TOKEN")
NOTION_ASSETS_DB_ID = os.environ.get("NOTION_ASSETS_DB_ID")

NOTION_API_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

# Valid category options
CATEGORIES = [
    "HVAC", "APPL", "PLMB", "ELEC", "TOOL",
    "TECH", "FURN", "LAND", "SAFE", "MISC"
]

# Valid status options
STATUSES = ["Active", "Needs Service", "Retired"]

# Depreciation categories
DEPRECIATION_CATEGORIES = ["5-year", "7-year", "27.5-year"]


# =============================================================================
# Notion API Helpers
# =============================================================================

def get_headers() -> dict:
    """Get headers for Notion API requests."""
    if not NOTION_TOKEN:
        raise ValueError("NOTION_TOKEN environment variable not set")
    return {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Content-Type": "application/json",
        "Notion-Version": NOTION_VERSION
    }


def notion_request(method: str, endpoint: str, data: Optional[dict] = None) -> dict:
    """Make a request to the Notion API."""
    url = f"{NOTION_API_URL}{endpoint}"
    headers = get_headers()

    if method == "GET":
        response = requests.get(url, headers=headers)
    elif method == "POST":
        response = requests.post(url, headers=headers, json=data)
    elif method == "PATCH":
        response = requests.patch(url, headers=headers, json=data)
    else:
        raise ValueError(f"Unsupported method: {method}")

    if not response.ok:
        print(f"Error: {response.status_code} - {response.text}")
        sys.exit(1)

    return response.json()


# =============================================================================
# Asset Operations
# =============================================================================

def create_asset(
    asset_id: str,
    name: str,
    category: str,
    location: str,
    purchase_cost: float,
    purchase_date: str,
    warranty_years: int = 0,
    service_interval: int = 0,
    vendor: str = "",
    depreciation_category: str = "",
    notes: str = ""
) -> dict:
    """Create a new asset in the Notion database."""

    if not NOTION_ASSETS_DB_ID:
        raise ValueError("NOTION_ASSETS_DB_ID environment variable not set")

    if category not in CATEGORIES:
        raise ValueError(f"Invalid category: {category}. Must be one of: {CATEGORIES}")

    # Calculate warranty expiry
    warranty_expiry = None
    if warranty_years > 0:
        purchase = datetime.strptime(purchase_date, "%Y-%m-%d")
        warranty_expiry = (purchase + timedelta(days=warranty_years * 365)).strftime("%Y-%m-%d")

    # Build properties
    properties = {
        "Asset ID": {"title": [{"text": {"content": asset_id}}]},
        "Name": {"rich_text": [{"text": {"content": name}}]},
        "Category": {"select": {"name": category}},
        "Location": {"select": {"name": location}},
        "Status": {"select": {"name": "Active"}},
        "Purchase Date": {"date": {"start": purchase_date}},
        "Purchase Cost": {"number": purchase_cost},
    }

    if vendor:
        properties["Vendor"] = {"rich_text": [{"text": {"content": vendor}}]}

    if warranty_expiry:
        properties["Warranty Expiry"] = {"date": {"start": warranty_expiry}}

    if service_interval > 0:
        properties["Service Interval"] = {"number": service_interval}
        # Set Last Service to purchase date initially
        properties["Last Service"] = {"date": {"start": purchase_date}}

    if depreciation_category and depreciation_category in DEPRECIATION_CATEGORIES:
        properties["Depreciation Category"] = {"select": {"name": depreciation_category}}

    if notes:
        properties["Notes"] = {"rich_text": [{"text": {"content": notes}}]}

    data = {
        "parent": {"database_id": NOTION_ASSETS_DB_ID},
        "properties": properties
    }

    result = notion_request("POST", "/pages", data)
    print(f"Created asset: {asset_id}")
    print(f"Notion URL: {result.get('url', 'N/A')}")
    return result


def get_asset(asset_id: str) -> Optional[dict]:
    """Get an asset by its ID."""

    if not NOTION_ASSETS_DB_ID:
        raise ValueError("NOTION_ASSETS_DB_ID environment variable not set")

    # Query database for the asset
    data = {
        "filter": {
            "property": "Asset ID",
            "title": {"equals": asset_id}
        }
    }

    result = notion_request("POST", f"/databases/{NOTION_ASSETS_DB_ID}/query", data)

    if result.get("results"):
        asset = result["results"][0]
        return parse_asset(asset)

    return None


def list_assets(category: Optional[str] = None, status: Optional[str] = None) -> list:
    """List all assets, optionally filtered by category or status."""

    if not NOTION_ASSETS_DB_ID:
        raise ValueError("NOTION_ASSETS_DB_ID environment variable not set")

    # Build filter
    filters = []
    if category:
        filters.append({
            "property": "Category",
            "select": {"equals": category}
        })
    if status:
        filters.append({
            "property": "Status",
            "select": {"equals": status}
        })

    data = {}
    if filters:
        if len(filters) == 1:
            data["filter"] = filters[0]
        else:
            data["filter"] = {"and": filters}

    # Add sorting
    data["sorts"] = [
        {"property": "Category", "direction": "ascending"},
        {"property": "Asset ID", "direction": "ascending"}
    ]

    result = notion_request("POST", f"/databases/{NOTION_ASSETS_DB_ID}/query", data)

    assets = []
    for page in result.get("results", []):
        assets.append(parse_asset(page))

    return assets


def update_asset(asset_id: str, **updates) -> dict:
    """Update an asset's properties."""

    # First, find the asset's page ID
    if not NOTION_ASSETS_DB_ID:
        raise ValueError("NOTION_ASSETS_DB_ID environment variable not set")

    data = {
        "filter": {
            "property": "Asset ID",
            "title": {"equals": asset_id}
        }
    }

    result = notion_request("POST", f"/databases/{NOTION_ASSETS_DB_ID}/query", data)

    if not result.get("results"):
        raise ValueError(f"Asset not found: {asset_id}")

    page_id = result["results"][0]["id"]

    # Build update properties
    properties = {}

    if "status" in updates:
        if updates["status"] not in STATUSES:
            raise ValueError(f"Invalid status: {updates['status']}. Must be one of: {STATUSES}")
        properties["Status"] = {"select": {"name": updates["status"]}}

    if "last_service" in updates:
        properties["Last Service"] = {"date": {"start": updates["last_service"]}}

    if "notes" in updates:
        properties["Notes"] = {"rich_text": [{"text": {"content": updates["notes"]}}]}

    if "documentation_url" in updates:
        properties["Documentation"] = {"url": updates["documentation_url"]}

    if not properties:
        print("No valid updates provided")
        return {}

    update_data = {"properties": properties}
    result = notion_request("PATCH", f"/pages/{page_id}", update_data)

    print(f"Updated asset: {asset_id}")
    return result


def search_assets(query: str) -> list:
    """Search assets by name or ID."""

    if not NOTION_ASSETS_DB_ID:
        raise ValueError("NOTION_ASSETS_DB_ID environment variable not set")

    # Search in both Asset ID and Name
    data = {
        "filter": {
            "or": [
                {
                    "property": "Asset ID",
                    "title": {"contains": query}
                },
                {
                    "property": "Name",
                    "rich_text": {"contains": query}
                }
            ]
        }
    }

    result = notion_request("POST", f"/databases/{NOTION_ASSETS_DB_ID}/query", data)

    assets = []
    for page in result.get("results", []):
        assets.append(parse_asset(page))

    return assets


def parse_asset(page: dict) -> dict:
    """Parse a Notion page into a clean asset dict."""
    props = page.get("properties", {})

    def get_title(prop):
        title = prop.get("title", [])
        return title[0]["text"]["content"] if title else ""

    def get_text(prop):
        text = prop.get("rich_text", [])
        return text[0]["text"]["content"] if text else ""

    def get_select(prop):
        select = prop.get("select")
        return select["name"] if select else ""

    def get_number(prop):
        return prop.get("number")

    def get_date(prop):
        date = prop.get("date")
        return date["start"] if date else ""

    def get_url(prop):
        return prop.get("url", "")

    return {
        "id": page.get("id"),
        "url": page.get("url"),
        "asset_id": get_title(props.get("Asset ID", {})),
        "name": get_text(props.get("Name", {})),
        "category": get_select(props.get("Category", {})),
        "location": get_select(props.get("Location", {})),
        "status": get_select(props.get("Status", {})),
        "purchase_date": get_date(props.get("Purchase Date", {})),
        "purchase_cost": get_number(props.get("Purchase Cost", {})),
        "vendor": get_text(props.get("Vendor", {})),
        "warranty_expiry": get_date(props.get("Warranty Expiry", {})),
        "depreciation_category": get_select(props.get("Depreciation Category", {})),
        "service_interval": get_number(props.get("Service Interval", {})),
        "last_service": get_date(props.get("Last Service", {})),
        "documentation": get_url(props.get("Documentation", {})),
        "notes": get_text(props.get("Notes", {})),
    }


def print_asset(asset: dict):
    """Pretty print an asset."""
    print(f"\n{'='*50}")
    print(f"Asset ID: {asset['asset_id']}")
    print(f"Name: {asset['name']}")
    print(f"Category: {asset['category']}")
    print(f"Location: {asset['location']}")
    print(f"Status: {asset['status']}")
    print(f"Purchase Date: {asset['purchase_date']}")
    print(f"Purchase Cost: ${asset['purchase_cost']:,.2f}" if asset['purchase_cost'] else "Purchase Cost: N/A")
    if asset['vendor']:
        print(f"Vendor: {asset['vendor']}")
    if asset['warranty_expiry']:
        print(f"Warranty Expiry: {asset['warranty_expiry']}")
    if asset['service_interval']:
        print(f"Service Interval: {asset['service_interval']} days")
    if asset['last_service']:
        print(f"Last Service: {asset['last_service']}")
    if asset['documentation']:
        print(f"Documentation: {asset['documentation']}")
    if asset['notes']:
        print(f"Notes: {asset['notes']}")
    print(f"Notion URL: {asset['url']}")
    print(f"{'='*50}")


def print_asset_table(assets: list):
    """Print assets in a table format."""
    if not assets:
        print("No assets found.")
        return

    print(f"\n{'Asset ID':<15} {'Name':<25} {'Category':<8} {'Status':<15} {'Cost':>10}")
    print("-" * 80)
    for asset in assets:
        cost = f"${asset['purchase_cost']:,.0f}" if asset['purchase_cost'] else "N/A"
        print(f"{asset['asset_id']:<15} {asset['name'][:25]:<25} {asset['category']:<8} {asset['status']:<15} {cost:>10}")
    print(f"\nTotal: {len(assets)} assets")


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Asset CRUD Operations")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Create command
    create_parser = subparsers.add_parser("create", help="Create a new asset")
    create_parser.add_argument("--id", required=True, help="Asset ID (e.g., TH-HVAC-01)")
    create_parser.add_argument("--name", required=True, help="Asset name")
    create_parser.add_argument("--category", required=True, choices=CATEGORIES, help="Asset category")
    create_parser.add_argument("--location", required=True, help="Asset location")
    create_parser.add_argument("--cost", type=float, required=True, help="Purchase cost")
    create_parser.add_argument("--purchase-date", required=True, help="Purchase date (YYYY-MM-DD)")
    create_parser.add_argument("--warranty-years", type=int, default=0, help="Warranty period in years")
    create_parser.add_argument("--service-interval", type=int, default=0, help="Service interval in days")
    create_parser.add_argument("--vendor", default="", help="Vendor/store name")
    create_parser.add_argument("--depreciation", choices=DEPRECIATION_CATEGORIES, help="Depreciation category")
    create_parser.add_argument("--notes", default="", help="Additional notes")

    # Get command
    get_parser = subparsers.add_parser("get", help="Get asset details")
    get_parser.add_argument("--id", required=True, help="Asset ID")

    # List command
    list_parser = subparsers.add_parser("list", help="List assets")
    list_parser.add_argument("--category", choices=CATEGORIES, help="Filter by category")
    list_parser.add_argument("--status", choices=STATUSES, help="Filter by status")

    # Update command
    update_parser = subparsers.add_parser("update", help="Update an asset")
    update_parser.add_argument("--id", required=True, help="Asset ID")
    update_parser.add_argument("--status", choices=STATUSES, help="New status")
    update_parser.add_argument("--last-service", help="Last service date (YYYY-MM-DD)")
    update_parser.add_argument("--notes", help="Notes to add/update")
    update_parser.add_argument("--documentation-url", help="Documentation URL")

    # Search command
    search_parser = subparsers.add_parser("search", help="Search assets")
    search_parser.add_argument("--query", required=True, help="Search query")

    args = parser.parse_args()

    if args.command == "create":
        create_asset(
            asset_id=args.id,
            name=args.name,
            category=args.category,
            location=args.location,
            purchase_cost=args.cost,
            purchase_date=args.purchase_date,
            warranty_years=args.warranty_years,
            service_interval=args.service_interval,
            vendor=args.vendor,
            depreciation_category=args.depreciation or "",
            notes=args.notes
        )

    elif args.command == "get":
        asset = get_asset(args.id)
        if asset:
            print_asset(asset)
        else:
            print(f"Asset not found: {args.id}")

    elif args.command == "list":
        assets = list_assets(category=args.category, status=args.status)
        print_asset_table(assets)

    elif args.command == "update":
        updates = {}
        if args.status:
            updates["status"] = args.status
        if args.last_service:
            updates["last_service"] = args.last_service
        if args.notes:
            updates["notes"] = args.notes
        if args.documentation_url:
            updates["documentation_url"] = args.documentation_url

        if updates:
            update_asset(args.id, **updates)
        else:
            print("No updates specified")

    elif args.command == "search":
        assets = search_assets(args.query)
        print_asset_table(assets)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
