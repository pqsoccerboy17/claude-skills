Here's a folder monitoring script integrated with your ecosystem's notification system.

**Tool call: Write** (~/scripts/folder_watcher.py)

```python
#!/usr/bin/env python3
"""Watch a folder for new files and notify via Pushover."""

import sys
import time
from pathlib import Path

# Ecosystem notify.py integration
sys.path.insert(0, str(Path.home() / "scripts"))

try:
    from notify import send_notification
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False
    print("notify.py not available - install at ~/scripts/notify.py")

def human_size(nbytes):
    for unit in ("B", "KB", "MB", "GB"):
        if nbytes < 1024:
            return f"{nbytes:.0f} {unit}"
        nbytes /= 1024
    return f"{nbytes:.0f} TB"

def main():
    watch_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "Downloads"

    if not watch_path.is_dir():
        print(f"Error: {watch_path} is not a directory")
        sys.exit(1)

    # Snapshot current files
    seen = set(p.name for p in watch_path.iterdir() if p.is_file())
    print(f"Monitoring {watch_path} for new files...")

    while True:
        time.sleep(5)
        current = set(p.name for p in watch_path.iterdir() if p.is_file())
        added = current - seen

        for name in sorted(added):
            fpath = watch_path / name
            size = human_size(fpath.stat().st_size)
            print(f"Detected: {name} ({size})")

            if NOTIFICATIONS_AVAILABLE:
                send_notification(
                    "New File",
                    f"{name} - {size}",
                    priority=0
                )

        seen = current

if __name__ == "__main__":
    main()
```

The script follows the ecosystem integration pattern from the skill:
- Adds `~/scripts` to the Python path and imports `send_notification()` from `notify.py`
- `notify.py` handles reading `PUSHOVER_USER_KEY` and `PUSHOVER_APP_TOKEN` from your environment (set in `~/scripts/ecosystem.env`)
- Uses priority 0 (normal) for each new file notification
- Includes filename and human-readable size in the message
- Gracefully handles missing notify.py with a fallback message

To run:
```bash
python3 ~/scripts/folder_watcher.py ~/Documents/incoming
```
