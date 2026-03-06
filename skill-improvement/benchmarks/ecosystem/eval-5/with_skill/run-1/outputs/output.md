Here's a Python script that monitors a folder and sends Pushover notifications via your ecosystem's `notify.py` module when new files appear.

**Tool call: Write** (creating ~/scripts/watch_folder.py)

```python
#!/usr/bin/env python3
"""Watch a folder for new files and send Pushover notifications."""

import sys
import time
import os
from pathlib import Path

# Add scripts directory to path for notify.py
sys.path.insert(0, str(Path.home() / "scripts"))

try:
    from notify import send_notification
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False
    print("Warning: notify.py not found. Notifications disabled.")

WATCH_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "Downloads"
POLL_INTERVAL = 5  # seconds

def get_file_size_str(size_bytes):
    """Return human-readable file size."""
    for unit in ["B", "KB", "MB", "GB"]:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def main():
    seen_files = set(WATCH_DIR.iterdir()) if WATCH_DIR.exists() else set()
    print(f"Monitoring {WATCH_DIR} for new files...")

    while True:
        time.sleep(POLL_INTERVAL)
        current_files = set(WATCH_DIR.iterdir())
        new_files = current_files - seen_files

        for filepath in new_files:
            if filepath.is_file():
                size = get_file_size_str(filepath.stat().st_size)
                title = "New File Detected"
                message = f"{filepath.name} ({size})"
                print(f"New file: {message}")

                if NOTIFICATIONS_AVAILABLE:
                    send_notification(title, message, priority=0)

        seen_files = current_files

if __name__ == "__main__":
    main()
```

This script:
- Imports `send_notification()` from `~/scripts/notify.py` using the ecosystem's standard import pattern
- Uses Pushover as the notification backend (via notify.py which reads `PUSHOVER_USER_KEY` and `PUSHOVER_APP_TOKEN` from environment)
- Sends notifications with the filename and human-readable file size
- Uses priority 0 (normal) for file monitoring events
- Falls back gracefully if notify.py is not available

Run it with:
```bash
python3 ~/scripts/watch_folder.py /path/to/folder
```
