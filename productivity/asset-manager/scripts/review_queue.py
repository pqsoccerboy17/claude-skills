#!/usr/bin/env python3
"""
Review Queue Module for Treehouse Asset Manager

Manage items needing human review before processing into the asset inventory.
Items are added by automated scanners (Gmail, manual finder) and approved by humans
before being synced to Notion.

Usage:
    # List pending items
    python3 review_queue.py --list

    # List all items (including approved/rejected)
    python3 review_queue.py --list --all

    # Filter by type
    python3 review_queue.py --list --type purchase

    # Show item details
    python3 review_queue.py --show abc123

    # Approve an item
    python3 review_queue.py --approve abc123

    # Reject an item with reason
    python3 review_queue.py --reject abc123 --reason "Duplicate entry"

    # Modify an item before approval
    python3 review_queue.py --modify abc123 --json '{"property": "DAL"}'

    # Add a new item manually
    python3 review_queue.py --add --type purchase --json '{"vendor": "Amazon", "item": "Refrigerator"}'

    # Export approved items
    python3 review_queue.py --export approved_items.json

    # Show queue statistics
    python3 review_queue.py --stats

    # Clear approved items (archive them)
    python3 review_queue.py --clear-approved

Storage:
    Active queue: ~/.config/treehouse/review_queue.json
    Archive: ~/.config/treehouse/review_queue_archive.json
"""

import argparse
import fcntl
import json
import os
import sys
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# =============================================================================
# Configuration
# =============================================================================

CONFIG_DIR = Path.home() / ".config" / "treehouse"
QUEUE_FILE = CONFIG_DIR / "review_queue.json"
ARCHIVE_FILE = CONFIG_DIR / "review_queue_archive.json"

# Valid item types
ITEM_TYPES = ["purchase", "manual", "property_match", "warranty", "service"]

# Valid statuses
STATUSES = ["pending", "approved", "rejected", "modified"]


# =============================================================================
# Data Types
# =============================================================================

class ReviewItem:
    """Represents an item in the review queue."""

    def __init__(
        self,
        item_type: str,
        data: Dict[str, Any],
        suggested_action: str = "",
        notes: str = "",
        item_id: Optional[str] = None,
        created_at: Optional[str] = None,
        status: str = "pending"
    ):
        self.id = item_id or str(uuid.uuid4())[:8]
        self.type = item_type
        self.created_at = created_at or datetime.now().isoformat()
        self.data = data
        self.suggested_action = suggested_action
        self.notes = notes
        self.status = status

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "id": self.id,
            "type": self.type,
            "created_at": self.created_at,
            "data": self.data,
            "suggested_action": self.suggested_action,
            "notes": self.notes,
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ReviewItem":
        """Create ReviewItem from dictionary."""
        return cls(
            item_id=data.get("id"),
            item_type=data.get("type", "manual"),
            created_at=data.get("created_at"),
            data=data.get("data", {}),
            suggested_action=data.get("suggested_action", ""),
            notes=data.get("notes", ""),
            status=data.get("status", "pending")
        )

    def get_summary(self) -> str:
        """Generate a human-readable summary of the item."""
        data = self.data

        if self.type == "purchase":
            vendor = data.get("vendor", "Unknown")
            item = data.get("item", data.get("name", "Unknown item"))
            return f"{vendor}: {item}"

        elif self.type == "manual":
            asset_id = data.get("asset_id", "Unknown")
            return f"Manual not found: {asset_id}"

        elif self.type == "property_match":
            location = data.get("location", "Unknown")
            match_type = data.get("match_type", "asset")
            return f"Property match: {match_type} at {location}"

        elif self.type == "warranty":
            asset_id = data.get("asset_id", "Unknown")
            return f"Warranty update: {asset_id}"

        elif self.type == "service":
            asset_id = data.get("asset_id", "Unknown")
            return f"Service record: {asset_id}"

        else:
            # Generic fallback
            if "name" in data:
                return data["name"]
            if "item" in data:
                return data["item"]
            return f"{self.type} item"


# =============================================================================
# File Storage with Locking
# =============================================================================

class QueueStorage:
    """Handle JSON file storage with file locking for safe concurrent access."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self._ensure_directory()

    def _ensure_directory(self):
        """Ensure the config directory exists."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)

    def _read_file(self) -> Dict[str, Any]:
        """Read the JSON file."""
        if not self.file_path.exists():
            return {"items": [], "metadata": {"version": "1.0", "last_modified": None}}

        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print(f"Warning: Corrupted JSON file at {self.file_path}, starting fresh")
            return {"items": [], "metadata": {"version": "1.0", "last_modified": None}}

    def _write_file(self, data: Dict[str, Any]):
        """Write data to the JSON file with atomic write."""
        data["metadata"]["last_modified"] = datetime.now().isoformat()

        # Write to temp file first, then rename (atomic on POSIX)
        temp_path = self.file_path.with_suffix(".tmp")
        with open(temp_path, "w") as f:
            json.dump(data, f, indent=2, default=str)

        temp_path.rename(self.file_path)

    def load_items(self) -> List[ReviewItem]:
        """Load all items from the queue file."""
        data = self._read_file()
        return [ReviewItem.from_dict(item) for item in data.get("items", [])]

    def save_items(self, items: List[ReviewItem]):
        """Save all items to the queue file."""
        data = self._read_file()
        data["items"] = [item.to_dict() for item in items]
        self._write_file(data)

    def with_lock(self, operation):
        """Execute an operation with file locking."""
        self._ensure_directory()

        # Create lock file
        lock_path = self.file_path.with_suffix(".lock")

        try:
            with open(lock_path, "w") as lock_file:
                # Acquire exclusive lock
                fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
                try:
                    return operation()
                finally:
                    # Release lock
                    fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
        except IOError as e:
            print(f"Error acquiring lock: {e}")
            raise


# =============================================================================
# Queue Operations
# =============================================================================

class ReviewQueue:
    """Main review queue manager."""

    def __init__(self):
        self.storage = QueueStorage(QUEUE_FILE)
        self.archive_storage = QueueStorage(ARCHIVE_FILE)

    def add_item(
        self,
        item_type: str,
        data: Dict[str, Any],
        suggested_action: str = "",
        notes: str = ""
    ) -> ReviewItem:
        """Add a new item to the review queue."""
        if item_type not in ITEM_TYPES:
            raise ValueError(f"Invalid item type: {item_type}. Must be one of: {ITEM_TYPES}")

        item = ReviewItem(
            item_type=item_type,
            data=data,
            suggested_action=suggested_action,
            notes=notes
        )

        def operation():
            items = self.storage.load_items()
            items.append(item)
            self.storage.save_items(items)
            return item

        return self.storage.with_lock(operation)

    def get_item(self, item_id: str) -> Optional[ReviewItem]:
        """Get an item by ID."""
        items = self.storage.load_items()
        for item in items:
            if item.id == item_id or item.id.startswith(item_id):
                return item
        return None

    def list_items(
        self,
        include_all: bool = False,
        status_filter: Optional[str] = None,
        type_filter: Optional[str] = None
    ) -> List[ReviewItem]:
        """List items with optional filtering."""
        items = self.storage.load_items()

        # Filter by status
        if not include_all and status_filter is None:
            items = [i for i in items if i.status == "pending"]
        elif status_filter:
            items = [i for i in items if i.status == status_filter]

        # Filter by type
        if type_filter:
            items = [i for i in items if i.type == type_filter]

        # Sort by created_at (newest first)
        items.sort(key=lambda x: x.created_at, reverse=True)

        return items

    def approve_item(self, item_id: str, notes: str = "") -> Optional[ReviewItem]:
        """Approve an item for processing."""
        def operation():
            items = self.storage.load_items()
            for item in items:
                if item.id == item_id or item.id.startswith(item_id):
                    item.status = "approved"
                    if notes:
                        item.notes = (item.notes + "\n" + notes).strip() if item.notes else notes
                    self.storage.save_items(items)
                    return item
            return None

        return self.storage.with_lock(operation)

    def reject_item(self, item_id: str, reason: str = "") -> Optional[ReviewItem]:
        """Reject an item."""
        def operation():
            items = self.storage.load_items()
            for item in items:
                if item.id == item_id or item.id.startswith(item_id):
                    item.status = "rejected"
                    if reason:
                        item.notes = (item.notes + f"\nRejection reason: {reason}").strip() if item.notes else f"Rejection reason: {reason}"
                    self.storage.save_items(items)
                    return item
            return None

        return self.storage.with_lock(operation)

    def modify_item(self, item_id: str, modifications: Dict[str, Any]) -> Optional[ReviewItem]:
        """Modify an item's data."""
        def operation():
            items = self.storage.load_items()
            for item in items:
                if item.id == item_id or item.id.startswith(item_id):
                    # Deep merge modifications into data
                    item.data.update(modifications)
                    item.status = "modified"
                    self.storage.save_items(items)
                    return item
            return None

        return self.storage.with_lock(operation)

    def get_statistics(self) -> Dict[str, Any]:
        """Get queue statistics."""
        items = self.storage.load_items()

        stats = {
            "total": len(items),
            "by_status": {},
            "by_type": {},
            "oldest_pending": None,
            "newest_item": None
        }

        # Count by status
        for status in STATUSES:
            count = len([i for i in items if i.status == status])
            stats["by_status"][status] = count

        # Count by type
        for item_type in ITEM_TYPES:
            count = len([i for i in items if i.type == item_type])
            if count > 0:
                stats["by_type"][item_type] = count

        # Find oldest pending
        pending = [i for i in items if i.status == "pending"]
        if pending:
            pending.sort(key=lambda x: x.created_at)
            stats["oldest_pending"] = pending[0].created_at

        # Find newest item
        if items:
            items_sorted = sorted(items, key=lambda x: x.created_at, reverse=True)
            stats["newest_item"] = items_sorted[0].created_at

        return stats

    def export_approved(self, output_path: str) -> int:
        """Export approved items to a JSON file."""
        items = self.storage.load_items()
        approved = [i for i in items if i.status == "approved"]

        export_data = {
            "exported_at": datetime.now().isoformat(),
            "count": len(approved),
            "items": [item.to_dict() for item in approved]
        }

        with open(output_path, "w") as f:
            json.dump(export_data, f, indent=2, default=str)

        return len(approved)

    def clear_approved(self) -> int:
        """Archive approved and rejected items, keeping only pending/modified."""
        def operation():
            items = self.storage.load_items()

            # Separate items to archive and keep
            to_archive = [i for i in items if i.status in ("approved", "rejected")]
            to_keep = [i for i in items if i.status not in ("approved", "rejected")]

            # Archive items
            if to_archive:
                archive_items = self.archive_storage.load_items()
                archive_items.extend(to_archive)
                self.archive_storage.save_items(archive_items)

            # Save remaining items
            self.storage.save_items(to_keep)

            return len(to_archive)

        return self.storage.with_lock(operation)


# =============================================================================
# Display Functions
# =============================================================================

def print_item_table(items: List[ReviewItem]):
    """Print items in a table format."""
    if not items:
        print("No items found.")
        return

    # Header
    print()
    print(f"{'ID':<12} {'Type':<16} {'Created':<12} {'Status':<10} {'Summary'}")
    print("\u2500" * 80)

    # Rows
    for item in items:
        # Format date
        try:
            created_dt = datetime.fromisoformat(item.created_at.replace("Z", "+00:00"))
            created_str = created_dt.strftime("%Y-%m-%d")
        except (ValueError, AttributeError):
            created_str = "Unknown"

        # Truncate summary
        summary = item.get_summary()
        if len(summary) > 35:
            summary = summary[:32] + "..."

        print(f"{item.id:<12} {item.type:<16} {created_str:<12} {item.status:<10} {summary}")

    print()
    print(f"Total: {len(items)} item(s)")


def print_item_details(item: ReviewItem):
    """Pretty print a single item's details."""
    print()
    print("=" * 60)
    print(f"Review Item: {item.id}")
    print("=" * 60)
    print()

    print(f"  Type:             {item.type}")
    print(f"  Status:           {item.status}")
    print(f"  Created:          {item.created_at}")
    print()

    if item.suggested_action:
        print(f"  Suggested Action: {item.suggested_action}")
        print()

    print("  Data:")
    print("  " + "-" * 40)
    for key, value in item.data.items():
        if isinstance(value, dict):
            print(f"    {key}:")
            for k, v in value.items():
                print(f"      {k}: {v}")
        elif isinstance(value, list):
            print(f"    {key}: [{len(value)} items]")
            for i, v in enumerate(value[:3]):  # Show first 3
                print(f"      - {v}")
            if len(value) > 3:
                print(f"      ... and {len(value) - 3} more")
        else:
            print(f"    {key}: {value}")
    print()

    if item.notes:
        print("  Notes:")
        print("  " + "-" * 40)
        for line in item.notes.split("\n"):
            print(f"    {line}")
        print()

    print("=" * 60)


def print_statistics(stats: Dict[str, Any]):
    """Print queue statistics."""
    print()
    print("=" * 50)
    print("Review Queue Statistics")
    print("=" * 50)
    print()

    print(f"  Total Items: {stats['total']}")
    print()

    print("  By Status:")
    print("  " + "-" * 30)
    for status, count in stats["by_status"].items():
        bar = "#" * min(count, 20)
        print(f"    {status:<12} {count:>4}  {bar}")
    print()

    if stats["by_type"]:
        print("  By Type:")
        print("  " + "-" * 30)
        for item_type, count in stats["by_type"].items():
            print(f"    {item_type:<16} {count:>4}")
        print()

    if stats["oldest_pending"]:
        try:
            oldest_dt = datetime.fromisoformat(stats["oldest_pending"].replace("Z", "+00:00"))
            age_days = (datetime.now() - oldest_dt.replace(tzinfo=None)).days
            print(f"  Oldest Pending: {stats['oldest_pending'][:10]} ({age_days} days ago)")
        except (ValueError, AttributeError):
            print(f"  Oldest Pending: {stats['oldest_pending']}")

    if stats["newest_item"]:
        print(f"  Newest Item:    {stats['newest_item'][:10]}")

    print()
    print("=" * 50)


# =============================================================================
# CLI Interface
# =============================================================================

def parse_json_arg(json_str: str) -> Dict[str, Any]:
    """Parse and validate JSON string argument."""
    try:
        data = json.loads(json_str)
        if not isinstance(data, dict):
            raise ValueError("JSON must be an object (dictionary)")
        return data
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Review Queue Manager for Treehouse Asset Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --list                              Show pending items
  %(prog)s --list --all                        Show all items
  %(prog)s --list --type purchase              Filter by type
  %(prog)s --show abc123                       Show item details
  %(prog)s --approve abc123                    Approve item
  %(prog)s --reject abc123 --reason "Dup"      Reject with reason
  %(prog)s --modify abc123 --json '{"x": 1}'   Modify item data
  %(prog)s --add --type purchase --json '{}'   Add new item
  %(prog)s --export out.json                   Export approved items
  %(prog)s --stats                             Show statistics
  %(prog)s --clear-approved                    Archive approved items
        """
    )

    # Action arguments (mutually exclusive)
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument("--list", action="store_true", help="List review items")
    action_group.add_argument("--show", metavar="ID", help="Show item details")
    action_group.add_argument("--approve", metavar="ID", help="Approve an item")
    action_group.add_argument("--reject", metavar="ID", help="Reject an item")
    action_group.add_argument("--modify", metavar="ID", help="Modify an item's data")
    action_group.add_argument("--add", action="store_true", help="Add a new item")
    action_group.add_argument("--export", metavar="FILE", help="Export approved items to file")
    action_group.add_argument("--stats", action="store_true", help="Show queue statistics")
    action_group.add_argument("--clear-approved", action="store_true", help="Archive approved/rejected items")

    # Modifier arguments
    parser.add_argument("--all", action="store_true", help="Include all statuses (with --list)")
    parser.add_argument("--status", choices=STATUSES, help="Filter by status (with --list)")
    parser.add_argument("--type", choices=ITEM_TYPES, dest="item_type", help="Filter by type (with --list/--add)")
    parser.add_argument("--reason", help="Rejection reason (with --reject)")
    parser.add_argument("--json", dest="json_data", help="JSON data (with --add/--modify)")
    parser.add_argument("--suggested-action", help="Suggested action (with --add)")
    parser.add_argument("--notes", help="Notes (with --add)")

    # Output format
    parser.add_argument("--output-json", action="store_true", help="Output in JSON format")

    args = parser.parse_args()

    # Initialize queue
    queue = ReviewQueue()

    try:
        # Handle each action
        if args.list:
            items = queue.list_items(
                include_all=args.all,
                status_filter=args.status,
                type_filter=args.item_type
            )

            if args.output_json:
                print(json.dumps([i.to_dict() for i in items], indent=2, default=str))
            else:
                print_item_table(items)

        elif args.show:
            item = queue.get_item(args.show)
            if item:
                if args.output_json:
                    print(json.dumps(item.to_dict(), indent=2, default=str))
                else:
                    print_item_details(item)
            else:
                print(f"Error: Item not found: {args.show}")
                sys.exit(1)

        elif args.approve:
            item = queue.approve_item(args.approve, notes=args.notes or "")
            if item:
                print(f"Approved: {item.id}")
                print(f"Summary: {item.get_summary()}")
            else:
                print(f"Error: Item not found: {args.approve}")
                sys.exit(1)

        elif args.reject:
            item = queue.reject_item(args.reject, reason=args.reason or "")
            if item:
                print(f"Rejected: {item.id}")
                print(f"Summary: {item.get_summary()}")
                if args.reason:
                    print(f"Reason: {args.reason}")
            else:
                print(f"Error: Item not found: {args.reject}")
                sys.exit(1)

        elif args.modify:
            if not args.json_data:
                print("Error: --json is required with --modify")
                sys.exit(1)

            try:
                modifications = parse_json_arg(args.json_data)
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)

            item = queue.modify_item(args.modify, modifications)
            if item:
                print(f"Modified: {item.id}")
                print(f"Status changed to: modified")
                if args.output_json:
                    print(json.dumps(item.to_dict(), indent=2, default=str))
            else:
                print(f"Error: Item not found: {args.modify}")
                sys.exit(1)

        elif args.add:
            if not args.item_type:
                print("Error: --type is required with --add")
                sys.exit(1)

            if not args.json_data:
                print("Error: --json is required with --add")
                sys.exit(1)

            try:
                data = parse_json_arg(args.json_data)
            except ValueError as e:
                print(f"Error: {e}")
                sys.exit(1)

            item = queue.add_item(
                item_type=args.item_type,
                data=data,
                suggested_action=args.suggested_action or "",
                notes=args.notes or ""
            )

            print(f"Added: {item.id}")
            print(f"Type: {item.type}")
            print(f"Summary: {item.get_summary()}")

        elif args.export:
            count = queue.export_approved(args.export)
            print(f"Exported {count} approved item(s) to: {args.export}")

        elif args.stats:
            stats = queue.get_statistics()
            if args.output_json:
                print(json.dumps(stats, indent=2, default=str))
            else:
                print_statistics(stats)

        elif args.clear_approved:
            count = queue.clear_approved()
            print(f"Archived {count} item(s) (approved + rejected)")
            print(f"Archive location: {ARCHIVE_FILE}")

    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


# =============================================================================
# Programmatic API (for use by other modules)
# =============================================================================

def add_to_queue(
    item_type: str,
    data: Dict[str, Any],
    suggested_action: str = "",
    notes: str = "",
    confidence: float = 1.0
) -> str:
    """
    Add an item to the review queue programmatically.

    Used by:
    - Gmail scanner when confidence < 0.8
    - Manual finder when manual not found
    - Property matcher for uncertain matches

    Args:
        item_type: Type of item (purchase, manual, property_match, etc.)
        data: The item data dictionary
        suggested_action: What the system recommends
        notes: Additional notes
        confidence: Confidence score (items with < 0.8 should be reviewed)

    Returns:
        The item ID
    """
    queue = ReviewQueue()

    # Add confidence to notes if provided
    if confidence < 1.0:
        conf_note = f"Confidence: {confidence:.2f}"
        notes = f"{notes}\n{conf_note}".strip() if notes else conf_note

    item = queue.add_item(
        item_type=item_type,
        data=data,
        suggested_action=suggested_action,
        notes=notes
    )

    return item.id


def get_approved_items(item_type: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Get all approved items, optionally filtered by type.

    Used by notion_sync.py to pick up approved items for syncing.

    Args:
        item_type: Optional type filter

    Returns:
        List of approved item dictionaries
    """
    queue = ReviewQueue()
    items = queue.list_items(include_all=True, status_filter="approved", type_filter=item_type)
    return [item.to_dict() for item in items]


def mark_item_processed(item_id: str) -> bool:
    """
    Mark an approved item as processed (archive it).

    Called after notion_sync.py successfully syncs an item.

    Args:
        item_id: The item ID

    Returns:
        True if successful, False if item not found
    """
    queue = ReviewQueue()
    item = queue.get_item(item_id)

    if item and item.status == "approved":
        # Add to archive directly
        def operation():
            items = queue.storage.load_items()
            remaining = []
            archived = None

            for i in items:
                if i.id == item_id or i.id.startswith(item_id):
                    i.notes = (i.notes + "\nProcessed: " + datetime.now().isoformat()).strip()
                    archived = i
                else:
                    remaining.append(i)

            if archived:
                archive_items = queue.archive_storage.load_items()
                archive_items.append(archived)
                queue.archive_storage.save_items(archive_items)
                queue.storage.save_items(remaining)
                return True

            return False

        return queue.storage.with_lock(operation)

    return False


if __name__ == "__main__":
    main()
