#!/usr/bin/env python3
"""
Ecosystem Status Script

Shows status of all automation systems at a glance:
- Tax PDF Organizer (LaunchAgent + watcher)
- Media Organizer
- Monarch Money MCP Server
- Treehouse Context Sync
- Notion Rules (Tax OCR)

Usage:
    python3 ~/scripts/ecosystem_status.py
"""

import os
import subprocess
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple


# =============================================================================
# Configuration
# =============================================================================

HOME = Path.home()
DOCUMENTS = HOME / "Documents"

# Repository paths
REPOS = {
    "tax_organizer": DOCUMENTS / "tax-pdf-organizer",
    "media_organizer": DOCUMENTS / "media-organizer",
    "monarch_mcp": DOCUMENTS / "monarch-mcp-server",
    "context_sync": DOCUMENTS / "treehouse-context-sync",
    "notion_rules": DOCUMENTS / "notion-rules",
}

# Log files
LOGS = {
    "tax_schedule": HOME / "tax_organizer_schedule.log",
    "tax_watcher": HOME / "tax_organizer_watcher.log",
}

# Session files
MONARCH_SESSION = HOME / "Library/Application Support/monarch-mcp-server/mm_session.pickle"

# LaunchAgent identifiers
LAUNCHAGENTS = {
    "tax_schedule": "com.taxorganizer.schedule",
    "tax_watcher": "com.taxorganizer.watcher",
    "tax_healthcheck": "com.taxorganizer.healthcheck",
}


# =============================================================================
# Utility Functions
# =============================================================================

def format_time_ago(dt: datetime) -> str:
    """Format a datetime as 'X minutes/hours/days ago'."""
    now = datetime.now()
    delta = now - dt

    if delta.total_seconds() < 60:
        return "just now"
    elif delta.total_seconds() < 3600:
        mins = int(delta.total_seconds() / 60)
        return f"{mins} minute{'s' if mins != 1 else ''} ago"
    elif delta.total_seconds() < 86400:
        hours = int(delta.total_seconds() / 3600)
        return f"{hours} hour{'s' if hours != 1 else ''} ago"
    else:
        days = int(delta.total_seconds() / 86400)
        return f"{days} day{'s' if days != 1 else ''} ago"


def get_file_mtime(path: Path) -> Optional[datetime]:
    """Get file modification time."""
    try:
        if path.exists():
            return datetime.fromtimestamp(path.stat().st_mtime)
    except Exception:
        pass
    return None


def get_launchctl_status(label: str) -> Tuple[bool, Optional[int]]:
    """Check if a LaunchAgent is loaded and get its PID."""
    try:
        result = subprocess.run(
            ["launchctl", "list"],
            capture_output=True,
            text=True,
            timeout=5
        )
        for line in result.stdout.splitlines():
            if label in line:
                parts = line.split()
                if len(parts) >= 2:
                    pid = parts[0]
                    if pid != "-" and pid.isdigit():
                        return True, int(pid)
                    return True, None
        return False, None
    except Exception:
        return False, None


def count_files_in_downloads(extensions: List[str]) -> int:
    """Count files with given extensions in Downloads."""
    downloads = HOME / "Downloads"
    count = 0
    try:
        for ext in extensions:
            count += len(list(downloads.glob(f"*.{ext}")))
            count += len(list(downloads.glob(f"*.{ext.upper()}")))
    except Exception:
        pass
    return count


def get_last_log_entry(log_path: Path) -> Optional[datetime]:
    """Get timestamp of last log entry."""
    try:
        if log_path.exists():
            # Read last few lines
            result = subprocess.run(
                ["tail", "-20", str(log_path)],
                capture_output=True,
                text=True,
                timeout=5
            )
            # Look for timestamp patterns like "2026-01-17" or "[2026-01-17"
            import re
            for line in reversed(result.stdout.splitlines()):
                match = re.search(r'(\d{4}-\d{2}-\d{2}[T\s]\d{2}:\d{2}:\d{2})', line)
                if match:
                    try:
                        ts = match.group(1).replace('T', ' ')
                        return datetime.strptime(ts, "%Y-%m-%d %H:%M:%S")
                    except ValueError:
                        pass
            # Fall back to file modification time
            return get_file_mtime(log_path)
    except Exception:
        pass
    return None


# =============================================================================
# Status Checkers
# =============================================================================

def check_tax_organizer() -> Dict[str, Any]:
    """Check tax-pdf-organizer status."""
    status = {
        "name": "Tax PDF Organizer",
        "icon": "📁",
        "status": "unknown",
        "details": [],
        "attention": [],
    }

    # Check LaunchAgents
    watcher_loaded, watcher_pid = get_launchctl_status(LAUNCHAGENTS["tax_watcher"])
    schedule_loaded, _ = get_launchctl_status(LAUNCHAGENTS["tax_schedule"])

    if watcher_loaded and watcher_pid:
        status["status"] = "watching"
        status["details"].append(f"Watcher running (PID {watcher_pid})")
    elif watcher_loaded:
        status["status"] = "loaded"
        status["details"].append("Watcher loaded but not running")
    else:
        status["status"] = "not_running"
        status["details"].append("Watcher not loaded")

    if schedule_loaded:
        status["details"].append("Scheduler loaded")

    # Check last activity
    last_activity = get_last_log_entry(LOGS["tax_watcher"])
    if last_activity:
        status["last_activity"] = last_activity
        status["details"].append(f"Last activity: {format_time_ago(last_activity)}")

    # Check pending PDFs in Downloads
    pending = count_files_in_downloads(["pdf"])
    if pending > 0:
        status["pending"] = pending
        status["attention"].append(f"{pending} PDF files in Downloads")

    return status


def check_media_organizer() -> Dict[str, Any]:
    """Check media-organizer status."""
    status = {
        "name": "Media Organizer",
        "icon": "📷",
        "status": "unknown",
        "details": [],
        "attention": [],
    }

    repo = REPOS["media_organizer"]
    if not repo.exists():
        status["status"] = "not_installed"
        status["details"].append("Repository not found")
        return status

    # Check if run.sh exists (indicates setup)
    if (repo / "run.sh").exists():
        status["status"] = "installed"
        status["details"].append("Installed (manual run)")
    else:
        status["status"] = "not_configured"
        status["details"].append("Not configured")

    # Check for pending media in Downloads
    media_exts = ["jpg", "jpeg", "png", "heic", "mov", "mp4", "mp3"]
    pending = count_files_in_downloads(media_exts)
    if pending > 0:
        status["pending"] = pending
        status["attention"].append(f"{pending} media files in Downloads")

    return status


def check_monarch_money() -> Dict[str, Any]:
    """Check Monarch Money MCP Server status."""
    status = {
        "name": "Monarch Money",
        "icon": "💰",
        "status": "unknown",
        "details": [],
        "attention": [],
    }

    # Check session file
    if MONARCH_SESSION.exists():
        mtime = get_file_mtime(MONARCH_SESSION)
        if mtime:
            age_days = (datetime.now() - mtime).days
            status["last_activity"] = mtime
            status["details"].append(f"Session: {format_time_ago(mtime)}")

            if age_days > 7:
                status["status"] = "stale"
                status["attention"].append("Session may need refresh (>7 days old)")
            else:
                status["status"] = "connected"
    else:
        status["status"] = "not_authenticated"
        status["attention"].append("Run login_setup.py to authenticate")

    return status


def check_context_sync() -> Dict[str, Any]:
    """Check treehouse-context-sync status."""
    status = {
        "name": "Context Sync",
        "icon": "🔄",
        "status": "unknown",
        "details": [],
        "attention": [],
    }

    repo = REPOS["context_sync"]
    if not repo.exists():
        status["status"] = "not_installed"
        status["details"].append("Repository not found")
        return status

    # Check CHANGELOG.md for last sync
    changelog = repo / "docs/context/CHANGELOG.md"
    if changelog.exists():
        mtime = get_file_mtime(changelog)
        if mtime:
            status["last_activity"] = mtime
            age_hours = (datetime.now() - mtime).total_seconds() / 3600
            status["details"].append(f"Last sync: {format_time_ago(mtime)}")

            if age_hours > 36:  # More than 1.5 days
                status["status"] = "stale"
                status["attention"].append("Sync may be stale (>36 hours)")
            else:
                status["status"] = "synced"
    else:
        status["status"] = "not_configured"
        status["details"].append("CHANGELOG.md not found")

    return status


def check_notion_rules() -> Dict[str, Any]:
    """Check notion-rules (Tax OCR) status."""
    status = {
        "name": "Notion Rules (Tax OCR)",
        "icon": "📄",
        "status": "idle",
        "details": [],
        "attention": [],
    }

    repo = REPOS["notion_rules"]
    if not repo.exists():
        status["status"] = "not_installed"
        status["details"].append("Repository not found")
        return status

    # Check checkpoint file
    checkpoint = repo / "tax-years/data/processing_checkpoint.json"
    if checkpoint.exists():
        mtime = get_file_mtime(checkpoint)
        if mtime:
            status["last_activity"] = mtime
            status["details"].append(f"Last run: {format_time_ago(mtime)}")

        # Try to read checkpoint for pending items
        try:
            with open(checkpoint) as f:
                data = json.load(f)
                # Check for items needing review
                if "results" in data:
                    needs_review = sum(
                        1 for r in data["results"]
                        if r.get("needs_review", False)
                    )
                    if needs_review > 0:
                        status["attention"].append(f"{needs_review} documents need review")
        except Exception:
            pass

    return status


# =============================================================================
# Main Output
# =============================================================================

def print_status():
    """Print ecosystem status to console."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    print(f"\n📊 ECOSYSTEM STATUS - {now}")
    print("━" * 50)

    # Collect all statuses
    checks = [
        check_tax_organizer(),
        check_media_organizer(),
        check_monarch_money(),
        check_context_sync(),
        check_notion_rules(),
    ]

    all_attention = []

    for check in checks:
        icon = check["icon"]
        name = check["name"]
        status = check["status"]

        # Status indicator
        if status in ["watching", "connected", "synced"]:
            status_icon = "✅"
            status_text = status.title()
        elif status in ["loaded", "installed", "idle"]:
            status_icon = "⏸️"
            status_text = status.title()
        elif status in ["stale"]:
            status_icon = "⚠️"
            status_text = "Stale"
        else:
            status_icon = "❌"
            status_text = status.replace("_", " ").title()

        print(f"\n{icon} {name}")
        print(f"   Status: {status_icon} {status_text}")

        for detail in check.get("details", []):
            print(f"   {detail}")

        if check.get("pending"):
            print(f"   Pending: {check['pending']} files")

        # Collect attention items
        for item in check.get("attention", []):
            all_attention.append(f"{icon} {item}")

    # Attention section
    if all_attention:
        print("\n" + "━" * 50)
        print("⚠️  ATTENTION NEEDED:")
        for item in all_attention:
            print(f"   • {item}")
    else:
        print("\n" + "━" * 50)
        print("✅ All systems nominal")

    print()


if __name__ == "__main__":
    print_status()
