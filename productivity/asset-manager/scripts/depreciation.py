#!/usr/bin/env python3
"""
Depreciation Calculator for Asset Management

Calculate and track depreciation for tax purposes.

Usage:
    # Calculate depreciation for a single asset
    python3 depreciation.py calculate --asset-id "TH-HVAC-01" --tax-year 2024

    # Calculate depreciation for all assets
    python3 depreciation.py calculate --all --tax-year 2024

    # Generate tax report
    python3 depreciation.py report --tax-year 2024 --output depreciation_2024.csv

    # Show depreciation schedule for an asset
    python3 depreciation.py schedule --asset-id "TH-HVAC-01"

Environment Variables:
    NOTION_TOKEN - Notion integration token
    NOTION_ASSETS_DB_ID - Asset Inventory database ID
    NOTION_DEPRECIATION_DB_ID - Depreciation Schedule database ID

Depreciation Methods:
    - Straight-line: (Cost - Salvage) / Useful Life
    - MACRS 5-year: IRS percentage tables for 5-year property
    - MACRS 7-year: IRS percentage tables for 7-year property
    - 27.5-year: Residential rental property (straight-line)
"""

import argparse
import csv
import os
import sys
from datetime import datetime
from decimal import Decimal, ROUND_HALF_UP
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
NOTION_DEPRECIATION_DB_ID = os.environ.get("NOTION_DEPRECIATION_DB_ID")

NOTION_API_URL = "https://api.notion.com/v1"
NOTION_VERSION = "2022-06-28"

# MACRS depreciation tables (half-year convention)
# Source: IRS Publication 946
MACRS_5_YEAR = {
    1: Decimal("0.2000"),
    2: Decimal("0.3200"),
    3: Decimal("0.1920"),
    4: Decimal("0.1152"),
    5: Decimal("0.1152"),
    6: Decimal("0.0576"),
}

MACRS_7_YEAR = {
    1: Decimal("0.1429"),
    2: Decimal("0.2449"),
    3: Decimal("0.1749"),
    4: Decimal("0.1249"),
    5: Decimal("0.0893"),
    6: Decimal("0.0892"),
    7: Decimal("0.0893"),
    8: Decimal("0.0446"),
}

# Mapping of depreciation categories to methods and years
DEPRECIATION_METHODS = {
    "5-year": {"method": "MACRS", "years": 5, "table": MACRS_5_YEAR},
    "7-year": {"method": "MACRS", "years": 7, "table": MACRS_7_YEAR},
    "27.5-year": {"method": "straight-line", "years": Decimal("27.5"), "table": None},
}


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
# Depreciation Calculations
# =============================================================================

def calculate_depreciation(
    cost: Decimal,
    purchase_date: str,
    depreciation_category: str,
    tax_year: int,
    salvage_value: Decimal = Decimal("0")
) -> dict:
    """
    Calculate depreciation for a specific tax year.

    Args:
        cost: Original purchase cost
        purchase_date: Date of purchase (YYYY-MM-DD)
        depreciation_category: Category (5-year, 7-year, 27.5-year)
        tax_year: Year to calculate depreciation for
        salvage_value: Estimated salvage value (default 0)

    Returns:
        Dict with depreciation details
    """
    if depreciation_category not in DEPRECIATION_METHODS:
        raise ValueError(f"Unknown category: {depreciation_category}")

    method_info = DEPRECIATION_METHODS[depreciation_category]
    purchase_year = int(purchase_date[:4])

    # Calculate year in service (1-indexed)
    year_in_service = tax_year - purchase_year + 1

    if year_in_service < 1:
        return {
            "year": tax_year,
            "depreciation": Decimal("0"),
            "method": method_info["method"],
            "note": "Asset not yet in service"
        }

    depreciable_basis = cost - salvage_value

    if method_info["method"] == "MACRS":
        table = method_info["table"]
        max_year = len(table)

        if year_in_service > max_year:
            return {
                "year": tax_year,
                "depreciation": Decimal("0"),
                "method": "MACRS",
                "note": "Fully depreciated"
            }

        rate = table[year_in_service]
        depreciation = (depreciable_basis * rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

        return {
            "year": tax_year,
            "year_in_service": year_in_service,
            "depreciation": depreciation,
            "rate": float(rate),
            "method": f"MACRS {method_info['years']}-year",
            "note": None
        }

    elif method_info["method"] == "straight-line":
        useful_life = method_info["years"]

        # For 27.5 year property, use mid-month convention for first year
        if depreciation_category == "27.5-year":
            if year_in_service == 1:
                # Mid-month convention: assume placed in service mid-month
                purchase_month = int(purchase_date[5:7])
                months_in_service = 12 - purchase_month + 0.5  # Mid-month
                annual_depreciation = depreciable_basis / useful_life
                depreciation = (annual_depreciation * Decimal(str(months_in_service)) / 12).quantize(
                    Decimal("0.01"), rounding=ROUND_HALF_UP
                )
            else:
                # Check if fully depreciated
                total_years = int(useful_life) + 1  # Extra year due to mid-month
                if year_in_service > total_years:
                    return {
                        "year": tax_year,
                        "depreciation": Decimal("0"),
                        "method": "Straight-line 27.5-year",
                        "note": "Fully depreciated"
                    }
                depreciation = (depreciable_basis / useful_life).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

            return {
                "year": tax_year,
                "year_in_service": year_in_service,
                "depreciation": depreciation,
                "method": "Straight-line 27.5-year",
                "note": None
            }

    return {
        "year": tax_year,
        "depreciation": Decimal("0"),
        "method": "Unknown",
        "note": "Could not calculate"
    }


def calculate_cumulative_depreciation(
    cost: Decimal,
    purchase_date: str,
    depreciation_category: str,
    through_year: int
) -> Decimal:
    """Calculate total depreciation through a given year."""
    purchase_year = int(purchase_date[:4])
    total = Decimal("0")

    for year in range(purchase_year, through_year + 1):
        result = calculate_depreciation(
            cost=cost,
            purchase_date=purchase_date,
            depreciation_category=depreciation_category,
            tax_year=year
        )
        total += result["depreciation"]

    return total


def get_book_value(
    cost: Decimal,
    purchase_date: str,
    depreciation_category: str,
    as_of_year: int
) -> Decimal:
    """Calculate book value (cost - accumulated depreciation)."""
    cumulative = calculate_cumulative_depreciation(
        cost=cost,
        purchase_date=purchase_date,
        depreciation_category=depreciation_category,
        through_year=as_of_year
    )
    return cost - cumulative


# =============================================================================
# Asset Operations
# =============================================================================

def get_depreciable_assets() -> list:
    """Get all assets with depreciation categories."""
    if not NOTION_ASSETS_DB_ID:
        raise ValueError("NOTION_ASSETS_DB_ID environment variable not set")

    data = {
        "filter": {
            "and": [
                {
                    "property": "Depreciation Category",
                    "select": {"is_not_empty": True}
                },
                {
                    "property": "Status",
                    "select": {"does_not_equal": "Retired"}
                }
            ]
        },
        "sorts": [{"property": "Asset ID", "direction": "ascending"}]
    }

    result = notion_request("POST", f"/databases/{NOTION_ASSETS_DB_ID}/query", data)

    assets = []
    for page in result.get("results", []):
        props = page.get("properties", {})

        asset_id = ""
        title = props.get("Asset ID", {}).get("title", [])
        if title:
            asset_id = title[0]["text"]["content"]

        name = ""
        name_text = props.get("Name", {}).get("rich_text", [])
        if name_text:
            name = name_text[0]["text"]["content"]

        cost = props.get("Purchase Cost", {}).get("number") or 0

        purchase_date = ""
        date_prop = props.get("Purchase Date", {}).get("date")
        if date_prop:
            purchase_date = date_prop["start"]

        category = ""
        cat_select = props.get("Depreciation Category", {}).get("select")
        if cat_select:
            category = cat_select["name"]

        if asset_id and cost and purchase_date and category:
            assets.append({
                "page_id": page.get("id"),
                "asset_id": asset_id,
                "name": name,
                "cost": Decimal(str(cost)),
                "purchase_date": purchase_date,
                "depreciation_category": category
            })

    return assets


def get_asset_for_depreciation(asset_id: str) -> Optional[dict]:
    """Get a single asset for depreciation calculation."""
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
        return None

    page = result["results"][0]
    props = page.get("properties", {})

    cost = props.get("Purchase Cost", {}).get("number") or 0

    purchase_date = ""
    date_prop = props.get("Purchase Date", {}).get("date")
    if date_prop:
        purchase_date = date_prop["start"]

    category = ""
    cat_select = props.get("Depreciation Category", {}).get("select")
    if cat_select:
        category = cat_select["name"]

    name = ""
    name_text = props.get("Name", {}).get("rich_text", [])
    if name_text:
        name = name_text[0]["text"]["content"]

    if not (cost and purchase_date and category):
        return None

    return {
        "page_id": page.get("id"),
        "asset_id": asset_id,
        "name": name,
        "cost": Decimal(str(cost)),
        "purchase_date": purchase_date,
        "depreciation_category": category
    }


# =============================================================================
# Report Generation
# =============================================================================

def generate_depreciation_report(tax_year: int, output_file: str = None) -> list:
    """Generate depreciation report for all assets."""
    assets = get_depreciable_assets()

    report = []
    total_depreciation = Decimal("0")
    total_cost = Decimal("0")

    for asset in assets:
        result = calculate_depreciation(
            cost=asset["cost"],
            purchase_date=asset["purchase_date"],
            depreciation_category=asset["depreciation_category"],
            tax_year=tax_year
        )

        cumulative = calculate_cumulative_depreciation(
            cost=asset["cost"],
            purchase_date=asset["purchase_date"],
            depreciation_category=asset["depreciation_category"],
            through_year=tax_year
        )

        book_value = asset["cost"] - cumulative

        entry = {
            "asset_id": asset["asset_id"],
            "name": asset["name"],
            "cost": float(asset["cost"]),
            "purchase_date": asset["purchase_date"],
            "method": result["method"],
            "depreciation": float(result["depreciation"]),
            "cumulative": float(cumulative),
            "book_value": float(book_value),
            "note": result.get("note", "")
        }
        report.append(entry)

        total_depreciation += result["depreciation"]
        total_cost += asset["cost"]

    # Print report
    print(f"\n{'='*90}")
    print(f"DEPRECIATION REPORT - TAX YEAR {tax_year}")
    print(f"{'='*90}")
    print(f"\n{'Asset ID':<15} {'Name':<20} {'Cost':>12} {'Method':<20} {'Depreciation':>12}")
    print("-" * 90)

    for entry in report:
        print(f"{entry['asset_id']:<15} {entry['name'][:20]:<20} ${entry['cost']:>10,.0f} {entry['method']:<20} ${entry['depreciation']:>10,.2f}")

    print("-" * 90)
    print(f"{'TOTAL':<15} {'':<20} ${float(total_cost):>10,.0f} {'':<20} ${float(total_depreciation):>10,.2f}")
    print(f"\nAssets: {len(report)}")

    # Export to CSV if requested
    if output_file:
        with open(output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=[
                "asset_id", "name", "cost", "purchase_date", "method",
                "depreciation", "cumulative", "book_value", "note"
            ])
            writer.writeheader()
            writer.writerows(report)
        print(f"\nExported to: {output_file}")

    return report


def show_depreciation_schedule(asset_id: str):
    """Show full depreciation schedule for an asset."""
    asset = get_asset_for_depreciation(asset_id)

    if not asset:
        print(f"Asset not found or missing depreciation info: {asset_id}")
        return

    purchase_year = int(asset["purchase_date"][:4])
    current_year = datetime.now().year

    # Determine end year based on method
    method_info = DEPRECIATION_METHODS.get(asset["depreciation_category"], {})
    years = method_info.get("years", 5)
    if isinstance(years, Decimal):
        end_year = purchase_year + int(years) + 1
    else:
        end_year = purchase_year + years

    # Show at least through current year
    end_year = max(end_year, current_year)

    print(f"\n{'='*70}")
    print(f"DEPRECIATION SCHEDULE: {asset_id}")
    print(f"{'='*70}")
    print(f"Name: {asset['name']}")
    print(f"Cost: ${float(asset['cost']):,.2f}")
    print(f"Purchase Date: {asset['purchase_date']}")
    print(f"Method: {asset['depreciation_category']}")
    print(f"\n{'Year':<8} {'Depreciation':>15} {'Cumulative':>15} {'Book Value':>15}")
    print("-" * 70)

    cumulative = Decimal("0")
    for year in range(purchase_year, end_year + 1):
        result = calculate_depreciation(
            cost=asset["cost"],
            purchase_date=asset["purchase_date"],
            depreciation_category=asset["depreciation_category"],
            tax_year=year
        )

        cumulative += result["depreciation"]
        book_value = asset["cost"] - cumulative

        marker = " <--" if year == current_year else ""
        print(f"{year:<8} ${float(result['depreciation']):>13,.2f} ${float(cumulative):>13,.2f} ${float(book_value):>13,.2f}{marker}")

    print("-" * 70)


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    parser = argparse.ArgumentParser(description="Depreciation Calculator")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Calculate command
    calc_parser = subparsers.add_parser("calculate", help="Calculate depreciation")
    calc_parser.add_argument("--asset-id", help="Asset ID (or --all for all assets)")
    calc_parser.add_argument("--all", action="store_true", help="Calculate for all assets")
    calc_parser.add_argument("--tax-year", type=int, required=True, help="Tax year")

    # Report command
    report_parser = subparsers.add_parser("report", help="Generate tax report")
    report_parser.add_argument("--tax-year", type=int, required=True, help="Tax year")
    report_parser.add_argument("--output", help="Output CSV file path")

    # Schedule command
    schedule_parser = subparsers.add_parser("schedule", help="Show depreciation schedule")
    schedule_parser.add_argument("--asset-id", required=True, help="Asset ID")

    args = parser.parse_args()

    if args.command == "calculate":
        if args.all:
            generate_depreciation_report(args.tax_year)
        elif args.asset_id:
            asset = get_asset_for_depreciation(args.asset_id)
            if asset:
                result = calculate_depreciation(
                    cost=asset["cost"],
                    purchase_date=asset["purchase_date"],
                    depreciation_category=asset["depreciation_category"],
                    tax_year=args.tax_year
                )
                print(f"\nAsset: {args.asset_id}")
                print(f"Tax Year: {args.tax_year}")
                print(f"Method: {result['method']}")
                print(f"Depreciation: ${float(result['depreciation']):,.2f}")
                if result.get("note"):
                    print(f"Note: {result['note']}")
            else:
                print(f"Asset not found or missing depreciation info: {args.asset_id}")
        else:
            print("Specify --asset-id or --all")

    elif args.command == "report":
        output = args.output or f"depreciation_{args.tax_year}.csv"
        generate_depreciation_report(args.tax_year, output)

    elif args.command == "schedule":
        show_depreciation_schedule(args.asset_id)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
