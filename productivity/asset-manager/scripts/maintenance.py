#!/usr/bin/env python3
"""
Maintenance Tracking for Asset Management

Log maintenance activities and check for due maintenance.

Usage:
    # Log maintenance
    python3 maintenance.py log --asset-id "TH-HVAC-01" --type "Preventive" \
        --description "Replaced air filter" --cost 25

    # Check what's due
    python3 maintenance.py due

    # Check what's due in the next N days
    python3 maintenance.py due --days 14

    # Get maintenance history for an asset
    python3 maintenance.py history --asset-id "TH-HVAC-01"

    # Get all maintenance for a time period
    python3 maintenance.py history --since "2024-01-01"

Environment Variables:
    NOTION_TOKEN - Notion integration token
    NOTION_ASSETS_DB_ID - Asset Inventory database ID
    NOTION_MAINTENANCE_DB_ID - Maintenance Log database ID
"""

import argparse
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
NOTION_MAINTENANCE_DB_ID = os.environ.get("NOTION_MAINTENANCE_DB_ID")

NOTION_API_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

# Valid maintenance types
MAINTENANCE_TYPES = ["Preventive", "Repair", "Inspection", "Emergency"]


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
# Maintenance Operations
# =============================================================================

def get_asset_page_id(asset_id: str) -> Optional[str]:
    """Get the Notion page ID for an asset."""
    if not NOTION_ASSETS_DB_ID:
        raise ValueError("NOTION_ASSETS_DB_ID environment variable not set")

    data = {
        "filter": {
            "property": "Asset ID",
            "title": {"equals": asset_id}
        }
    }

    result = notion_request("POST", f"/databases/{NOTION_ASSETS_DB_ID}/query", data)

    if result.get("results"):
        return result["results"][0]["id"]
    return None


def generate_log_id() -> str:
    """Generate a maintenance log ID."""
    year = datetime.now().year

    if not NOTION_MAINTENANCE_DB_ID:
        raise ValueError("NOTION_MAINTENANCE_DB_ID environment variable not set")

    # Query to find highest log ID for this year
    data = {
        "filter": {
            "property": "Log ID",
            "title": {"starts_with": f"ML-{year}-"}
        },
        "sorts": [
            {"property": "Log ID", "direction": "descending"}
        ],
        "page_size": 1
    }

    result = notion_request("POST", f"/databases/{NOTION_MAINTENANCE_DB_ID}/query", data)

    if result.get("results"):
        last_id = result["results"][0]["properties"]["Log ID"]["title"][0]["text"]["content"]
        # Extract sequence number
        seq = int(last_id.split("-")[-1])
        return f"ML-{year}-{seq + 1:03d}"
    else:
        return f"ML-{year}-001"


def log_maintenance(
    asset_id: str,
    maintenance_type: str,
    description: str,
    cost: float = 0,
    vendor: str = "",
    date: str = None,
    notes: str = ""
) -> dict:
    """Log a maintenance entry."""

    if not NOTION_MAINTENANCE_DB_ID:
        raise ValueError("NOTION_MAINTENANCE_DB_ID environment variable not set")

    if maintenance_type not in MAINTENANCE_TYPES:
        raise ValueError(f"Invalid type: {maintenance_type}. Must be one of: {MAINTENANCE_TYPES}")

    # Get asset page ID
    asset_page_id = get_asset_page_id(asset_id)
    if not asset_page_id:
        raise ValueError(f"Asset not found: {asset_id}")

    # Generate log ID
    log_id = generate_log_id()

    # Use today if no date provided
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    # Build properties
    properties = {
        "Log ID": {"title": [{"text": {"content": log_id}}]},
        "Asset": {"relation": [{"id": asset_page_id}]},
        "Date": {"date": {"start": date}},
        "Type": {"select": {"name": maintenance_type}},
        "Description": {"rich_text": [{"text": {"content": description}}]},
    }

    if cost > 0:
        properties["Cost"] = {"number": cost}

    if vendor:
        properties["Vendor/Tech"] = {"rich_text": [{"text": {"content": vendor}}]}

    if notes:
        properties["Notes"] = {"rich_text": [{"text": {"content": notes}}]}

    data = {
        "parent": {"database_id": NOTION_MAINTENANCE_DB_ID},
        "properties": properties
    }

    result = notion_request("POST", "/pages", data)

    # Also update the asset's Last Service date
    update_data = {
        "properties": {
            "Last Service": {"date": {"start": date}}
        }
    }
    notion_request("PATCH", f"/pages/{asset_page_id}", update_data)

    print(f"Logged maintenance: {log_id}")
    print(f"Asset: {asset_id}")
    print(f"Type: {maintenance_type}")
    print(f"Description: {description}")
    if cost > 0:
        print(f"Cost: ${cost:.2f}")
    print(f"Updated Last Service date to: {date}")

    return result


def get_due_maintenance(days_ahead: int = 7) -> list:
    """Get assets with maintenance due within the specified days."""

    if not NOTION_ASSETS_DB_ID:
        raise ValueError("NOTION_ASSETS_DB_ID environment variable not set")

    # We need to check where Next Service Due <= today + days_ahead
    # Since Next Service Due is a formula, we need to query all active assets
    # and filter client-side

    data = {
        "filter": {
            "and": [
                {
                    "property": "Status",
                    "select": {"equals": "Active"}
                },
                {
                    "property": "Service Interval",
                    "number": {"is_not_empty": True}
                }
            ]
        }
    }

    result = notion_request("POST", f"/databases/{NOTION_ASSETS_DB_ID}/query", data)

    due_assets = []
    today = datetime.now().date()
    cutoff = today + timedelta(days=days_ahead)

    for page in result.get("results", []):
        props = page.get("properties", {})

        # Get Last Service and Service Interval
        last_service_prop = props.get("Last Service", {}).get("date")
        service_interval = props.get("Service Interval", {}).get("number")

        if not last_service_prop or not service_interval:
            continue

        last_service = datetime.strptime(last_service_prop["start"], "%Y-%m-%d").date()
        next_due = last_service + timedelta(days=service_interval)

        if next_due <= cutoff:
            # Get asset details
            asset_id = ""
            title = props.get("Asset ID", {}).get("title", [])
            if title:
                asset_id = title[0]["text"]["content"]

            name = ""
            name_text = props.get("Name", {}).get("rich_text", [])
            if name_text:
                name = name_text[0]["text"]["content"]

            category = ""
            cat_select = props.get("Category", {}).get("select")
            if cat_select:
                category = cat_select["name"]

            days_until = (next_due - today).days

            due_assets.append({
                "asset_id": asset_id,
                "name": name,
                "category": category,
                "next_due": next_due.strftime("%Y-%m-%d"),
                "days_until": days_until,
                "overdue": days_until < 0,
                "url": page.get("url", "")
            })

    # Sort by days until due (most urgent first)
    due_assets.sort(key=lambda x: x["days_until"])

    return due_assets


def get_maintenance_history(asset_id: str = None, since: str = None, limit: int = 50) -> list:
    """Get maintenance history, optionally filtered by asset or date."""

    if not NOTION_MAINTENANCE_DB_ID:
        raise ValueError("NOTION_MAINTENANCE_DB_ID environment variable not set")

    filters = []

    if asset_id:
        # Get asset page ID
        asset_page_id = get_asset_page_id(asset_id)
        if not asset_page_id:
            raise ValueError(f"Asset not found: {asset_id}")
        filters.append({
            "property": "Asset",
            "relation": {"contains": asset_page_id}
        })

    if since:
        filters.append({
            "property": "Date",
            "date": {"on_or_after": since}
        })

    data = {
        "sorts": [{"property": "Date", "direction": "descending"}],
        "page_size": limit
    }

    if filters:
        if len(filters) == 1:
            data["filter"] = filters[0]
        else:
            data["filter"] = {"and": filters}

    result = notion_request("POST", f"/databases/{NOTION_MAINTENANCE_DB_ID}/query", data)

    history = []
    for page in result.get("results", []):
        props = page.get("properties", {})

        log_id = ""
        title = props.get("Log ID", {}).get("title", [])
        if title:
            log_id = title[0]["text"]["content"]

        date = ""
        date_prop = props.get("Date", {}).get("date")
        if date_prop:
            date = date_prop["start"]

        maint_type = ""
        type_select = props.get("Type", {}).get("select")
        if type_select:
            maint_type = type_select["name"]

        description = ""
        desc_text = props.get("Description", {}).get("rich_text", [])
        if desc_text:
            description = desc_text[0]["text"]["content"]

        cost = props.get("Cost", {}).get("number") or 0

        vendor = ""
        vendor_text = props.get("Vendor/Tech", {}).get("rich_text", [])
        if vendor_text:
            vendor = vendor_text[0]["text"]["content"]

        history.append({
            "log_id": log_id,
            "date": date,
            "type": maint_type,
            "description": description,
            "cost": cost,
            "vendor": vendor
        })

    return history


def print_due_maintenance(assets: list):
    """Print due maintenance in a nice format."""
    if not assets:
        print("No maintenance due.")
        return

    print(f"\n{'='*70}")
    print("MAINTENANCE DUE")
    print(f"{'='*70}")

    overdue = [a for a in assets if a["overdue"]]
    upcoming = [a for a in assets if not a["overdue"]]

    if overdue:
        print("\nOVERDUE:")
        print("-" * 70)
        for asset in overdue:
            print(f"  {asset['asset_id']:<15} {asset['name'][:30]:<30} ({abs(asset['days_until'])} days overdue)")

    if upcoming:
        print("\nUPCOMING:")
        print("-" * 70)
        for asset in upcoming:
            due_text = "TODAY" if asset['days_until'] == 0 else f"in {asset['days_until']} days"
            print(f"  {asset['asset_id']:<15} {asset['name'][:30]:<30} ({due_text})")

    print(f"\nTotal: {len(overdue)} overdue, {len(upcoming)} upcoming")


def print_maintenance_history(history: list):
    """Print maintenance history."""
    if not history:
        print("No maintenance history found.")
        return

    print(f"\n{'Log ID':<15} {'Date':<12} {'Type':<12} {'Cost':>8}  Description")
    print("-" * 80)

    total_cost = 0
    for entry in history:
        cost_str = f"${entry['cost']:.0f}" if entry['cost'] else "-"
        total_cost += entry['cost']
        print(f"{entry['log_id']:<15} {entry['date']:<12} {entry['type']:<12} {cost_str:>8}  {entry['description'][:35]}")

    print("-" * 80)
    print(f"Total entries: {len(history)}, Total cost: ${total_cost:,.2f}")


# =============================================================================
# Notification Integration
# =============================================================================

def send_maintenance_notification(assets: list):
    """Send notification for due maintenance via notify.py."""
    try:
        # Try to import from the notifications skill
        sys.path.insert(0, os.path.expanduser("~/claude-skills/productivity/notifications/scripts"))
        from notify import send_notification
    except ImportError:
        print("Warning: notify.py not available, skipping notification")
        return

    if not assets:
        return

    overdue = [a for a in assets if a["overdue"]]
    upcoming = [a for a in assets if not a["overdue"]]

    if overdue:
        title = f"Overdue Maintenance ({len(overdue)})"
        message = "\n".join([f"{a['asset_id']}: {a['name']}" for a in overdue[:5]])
        if len(overdue) > 5:
            message += f"\n... and {len(overdue) - 5} more"
        send_notification(title, message, priority=1)  # High priority

    elif upcoming:
        title = f"Maintenance Due ({len(upcoming)})"
        message = "\n".join([f"{a['asset_id']}: {a['name']} ({a['days_until']}d)" for a in upcoming[:5]])
        send_notification(title, message, priority=0)


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Maintenance Tracking")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Log command
    log_parser = subparsers.add_parser("log", help="Log maintenance")
    log_parser.add_argument("--asset-id", required=True, help="Asset ID (e.g., TH-HVAC-01)")
    log_parser.add_argument("--type", required=True, choices=MAINTENANCE_TYPES, help="Maintenance type")
    log_parser.add_argument("--description", required=True, help="Description of work done")
    log_parser.add_argument("--cost", type=float, default=0, help="Cost of maintenance")
    log_parser.add_argument("--vendor", default="", help="Vendor or technician")
    log_parser.add_argument("--date", help="Date (YYYY-MM-DD), defaults to today")
    log_parser.add_argument("--notes", default="", help="Additional notes")

    # Due command
    due_parser = subparsers.add_parser("due", help="Check due maintenance")
    due_parser.add_argument("--days", type=int, default=7, help="Days ahead to check")
    due_parser.add_argument("--notify", action="store_true", help="Send notification")

    # History command
    history_parser = subparsers.add_parser("history", help="Get maintenance history")
    history_parser.add_argument("--asset-id", help="Filter by asset ID")
    history_parser.add_argument("--since", help="Filter by date (YYYY-MM-DD)")
    history_parser.add_argument("--limit", type=int, default=50, help="Max entries to return")

    args = parser.parse_args()

    if args.command == "log":
        log_maintenance(
            asset_id=args.asset_id,
            maintenance_type=args.type,
            description=args.description,
            cost=args.cost,
            vendor=args.vendor,
            date=args.date,
            notes=args.notes
        )

    elif args.command == "due":
        assets = get_due_maintenance(days_ahead=args.days)
        print_due_maintenance(assets)

        if args.notify:
            send_maintenance_notification(assets)

    elif args.command == "history":
        history = get_maintenance_history(
            asset_id=args.asset_id,
            since=args.since,
            limit=args.limit
        )
        print_maintenance_history(history)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
