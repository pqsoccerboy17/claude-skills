Here's a folder monitoring script with Pushover notifications:

```python
#!/usr/bin/env python3
"""Monitor a folder for new files and send push notifications."""

import os
import sys
import time
from pathlib import Path

# You'll need to install this: pip install pushover
try:
    from pushover import Client
except ImportError:
    print("Please install pushover: pip install python-pushover")
    sys.exit(1)

WATCH_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.home() / "Downloads"
CHECK_INTERVAL = 15  # seconds

def format_size(bytes_size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024:
            return f"{bytes_size:.1f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.1f} TB"

def main():
    # Initialize Pushover client
    client = Client(
        os.environ.get("PUSHOVER_USER"),
        api_token=os.environ.get("PUSHOVER_API_TOKEN")
    )

    known = set(p.name for p in WATCH_DIR.iterdir())
    print(f"Watching {WATCH_DIR} for new files...")

    while True:
        time.sleep(CHECK_INTERVAL)
        current = set(p.name for p in WATCH_DIR.iterdir())
        new_files = current - known

        for name in new_files:
            path = WATCH_DIR / name
            if path.is_file():
                size = format_size(path.stat().st_size)
                msg = f"New file: {name}\nSize: {size}"
                client.send_message(msg, title="File Monitor Alert")
                print(f"Notified: {name} ({size})")

        known = current

if __name__ == "__main__":
    main()
```

**To use:**

1. Install dependency: `pip install python-pushover`
2. Set environment variables:
   ```bash
   export PUSHOVER_USER="your-user-key"
   export PUSHOVER_API_TOKEN="your-app-token"
   ```
3. Run: `python3 monitor.py /path/to/watch`
