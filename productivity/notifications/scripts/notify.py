#!/usr/bin/env python3
"""
Unified Notification Module for Ecosystem Tools

Supports:
- Pushover (primary, requires PUSHOVER_USER_KEY and PUSHOVER_APP_TOKEN)
- macOS notifications (fallback, no config needed)

Usage:
    from notify import send_notification
    send_notification("Title", "Message body", priority=0)

Or from command line:
    python3 ~/scripts/notify.py "Title" "Message"

Environment Variables:
    PUSHOVER_USER_KEY   - Your Pushover user key
    PUSHOVER_APP_TOKEN  - Your Pushover application token
    NOTIFY_ENABLED      - Set to "false" to disable all notifications
"""

import os
import subprocess
import urllib.request
import urllib.parse
import json
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# =============================================================================
# Configuration
# =============================================================================

def get_config() -> dict:
    """Get notification configuration from environment."""
    return {
        "enabled": os.getenv("NOTIFY_ENABLED", "true").lower() != "false",
        "pushover_user": os.getenv("PUSHOVER_USER_KEY"),
        "pushover_token": os.getenv("PUSHOVER_APP_TOKEN"),
    }


# =============================================================================
# Notification Backends
# =============================================================================

def send_pushover(
    title: str,
    message: str,
    priority: int = 0,
    url: Optional[str] = None,
    url_title: Optional[str] = None,
) -> bool:
    """
    Send notification via Pushover.

    Args:
        title: Notification title
        message: Notification body
        priority: -2 (silent) to 2 (emergency), default 0
        url: Optional URL to include
        url_title: Optional title for the URL

    Returns:
        True if successful, False otherwise
    """
    config = get_config()
    user_key = config["pushover_user"]
    app_token = config["pushover_token"]

    if not user_key or not app_token:
        logger.debug("Pushover not configured (missing credentials)")
        return False

    try:
        data = {
            "token": app_token,
            "user": user_key,
            "title": title,
            "message": message,
            "priority": priority,
        }

        if url:
            data["url"] = url
        if url_title:
            data["url_title"] = url_title

        encoded_data = urllib.parse.urlencode(data).encode("utf-8")
        req = urllib.request.Request(
            "https://api.pushover.net/1/messages.json",
            data=encoded_data,
            method="POST"
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            if response.status == 200:
                logger.info("Pushover notification sent successfully")
                return True
            else:
                logger.warning(f"Pushover returned status {response.status}")
                return False

    except Exception as e:
        logger.warning(f"Pushover notification failed: {e}")
        return False


def send_macos_notification(title: str, message: str) -> bool:
    """
    Send notification via macOS Notification Center.

    Args:
        title: Notification title
        message: Notification body

    Returns:
        True if successful, False otherwise
    """
    try:
        # Use osascript to send notification
        script = f'''
        display notification "{message}" with title "{title}"
        '''
        result = subprocess.run(
            ["osascript", "-e", script],
            capture_output=True,
            timeout=5
        )
        if result.returncode == 0:
            logger.info("macOS notification sent successfully")
            return True
        else:
            logger.warning(f"macOS notification failed: {result.stderr.decode()}")
            return False

    except Exception as e:
        logger.warning(f"macOS notification failed: {e}")
        return False


# =============================================================================
# Main API
# =============================================================================

def send_notification(
    title: str,
    message: str,
    priority: int = 0,
    url: Optional[str] = None,
    url_title: Optional[str] = None,
) -> bool:
    """
    Send notification using best available method.

    Tries Pushover first, falls back to macOS notifications.

    Args:
        title: Notification title
        message: Notification body
        priority: -2 (silent) to 2 (emergency), default 0
        url: Optional URL to include (Pushover only)
        url_title: Optional title for the URL (Pushover only)

    Returns:
        True if notification was sent successfully
    """
    config = get_config()

    if not config["enabled"]:
        logger.info("Notifications disabled via NOTIFY_ENABLED=false")
        return False

    # Try Pushover first
    if send_pushover(title, message, priority, url, url_title):
        return True

    # Fall back to macOS notification
    return send_macos_notification(title, message)


def notify_organization_complete(
    organizer_name: str,
    files_organized: int,
    categories: Optional[dict] = None,
    pending_review: int = 0,
    errors: int = 0,
) -> bool:
    """
    Send notification about completed file organization.

    Args:
        organizer_name: Name of the organizer (e.g., "Tax Organizer")
        files_organized: Total number of files organized
        categories: Optional dict of category -> count
        pending_review: Number of files pending review
        errors: Number of errors encountered

    Returns:
        True if notification was sent
    """
    # Determine icon based on organizer
    if "tax" in organizer_name.lower():
        icon = "📁"
    elif "media" in organizer_name.lower():
        icon = "📷"
    else:
        icon = "✅"

    title = f"{icon} {organizer_name} Complete"

    # Build message
    lines = []

    if files_organized > 0:
        lines.append(f"Organized: {files_organized} file{'s' if files_organized != 1 else ''}")

        # Add category breakdown if provided
        if categories:
            for cat, count in categories.items():
                lines.append(f"  • {count} {cat}")

    if pending_review > 0:
        lines.append(f"⚠️ Pending review: {pending_review}")

    if errors > 0:
        lines.append(f"❌ Errors: {errors}")

    if not lines:
        lines.append("No files to organize")

    message = "\n".join(lines)

    # Determine priority
    if errors > 0:
        priority = 1  # High priority for errors
    elif pending_review > 0:
        priority = 0  # Normal for pending review
    else:
        priority = -1  # Low priority for routine success

    return send_notification(title, message, priority)


# =============================================================================
# CLI
# =============================================================================

def main():
    """Command-line interface for sending notifications."""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python3 notify.py <title> <message> [priority]")
        print()
        print("Environment variables:")
        print("  PUSHOVER_USER_KEY   - Pushover user key")
        print("  PUSHOVER_APP_TOKEN  - Pushover application token")
        print("  NOTIFY_ENABLED      - Set to 'false' to disable")
        sys.exit(1)

    title = sys.argv[1]
    message = sys.argv[2]
    priority = int(sys.argv[3]) if len(sys.argv) > 3 else 0

    # Configure logging for CLI
    logging.basicConfig(level=logging.INFO, format="%(message)s")

    config = get_config()
    print(f"Pushover configured: {bool(config['pushover_user'] and config['pushover_token'])}")
    print(f"Notifications enabled: {config['enabled']}")

    success = send_notification(title, message, priority)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
