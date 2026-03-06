I'll create a folder watcher script that uses your ecosystem's notification system. Following the integration pattern from the skill docs:

**Tool call: Write** (creating the script)

```python
#!/usr/bin/env python3
"""Monitor a directory for new files and send push notifications."""

import sys
import time
import os
from pathlib import Path

# Import ecosystem notification module
sys.path.insert(0, str(Path.home() / "scripts"))

try:
    from notify import send_notification
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False

def format_size(bytes_val):
    """Format bytes into readable size string."""
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024 * 1024:
        return f"{bytes_val / 1024:.1f} KB"
    elif bytes_val < 1024 * 1024 * 1024:
        return f"{bytes_val / (1024 * 1024):.1f} MB"
    return f"{bytes_val / (1024 * 1024 * 1024):.1f} GB"

def watch_directory(target_dir):
    """Poll directory and notify on new files."""
    target = Path(target_dir)
    if not target.exists():
        print(f"Error: {target} does not exist")
        return

    known_files = {f for f in target.iterdir() if f.is_file()}
    print(f"Watching {target} ({len(known_files)} existing files)")

    while True:
        time.sleep(3)
        current_files = {f for f in target.iterdir() if f.is_file()}
        new_files = current_files - known_files

        for f in new_files:
            size = format_size(f.stat().st_size)
            msg = f"New file: {f.name}\nSize: {size}"
            print(msg)

            if NOTIFICATIONS_AVAILABLE:
                send_notification("File Monitor", msg, priority=1)

        known_files = current_files

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else str(Path.home() / "Downloads")
    watch_directory(folder)
```

Key points:
- Uses the ecosystem import pattern (`sys.path.insert` for `~/scripts`) to access `send_notification()`
- Pushover delivers the notifications since `notify.py` reads `PUSHOVER_USER_KEY` and `PUSHOVER_APP_TOKEN` from your environment variables
- Each notification includes the filename and size
- Priority is set to 1 (high) since you probably want to know about new files promptly
- If Pushover credentials are missing, `notify.py` falls back to macOS notifications
