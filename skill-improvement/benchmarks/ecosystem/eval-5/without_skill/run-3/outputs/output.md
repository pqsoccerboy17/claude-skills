Here's a script that monitors a folder and sends Pushover notifications for new files:

```python
#!/usr/bin/env python3
"""Watch a directory for new files and notify via Pushover."""

import os
import time
import http.client
import urllib.parse

WATCH_FOLDER = os.path.expanduser("~/Downloads")  # adjust as needed

def send_notification(title, message):
    """Send a Pushover notification using the HTTP API."""
    conn = http.client.HTTPSConnection("api.pushover.net:443")
    conn.request("POST", "/1/messages.json",
        urllib.parse.urlencode({
            "token": os.environ["PUSHOVER_TOKEN"],
            "user": os.environ["PUSHOVER_USER"],
            "title": title,
            "message": message,
        }),
        {"Content-type": "application/x-www-form-urlencoded"})
    response = conn.getresponse()
    if response.status != 200:
        print(f"Notification failed: {response.status}")
    conn.close()

def human_size(nbytes):
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    i = 0
    while nbytes >= 1024 and i < len(suffixes) - 1:
        nbytes /= 1024.0
        i += 1
    return f"{nbytes:.1f} {suffixes[i]}"

if __name__ == "__main__":
    seen = set(os.listdir(WATCH_FOLDER))
    print(f"Watching {WATCH_FOLDER}...")

    while True:
        time.sleep(5)
        current = set(os.listdir(WATCH_FOLDER))
        new = current - seen
        for f in new:
            full_path = os.path.join(WATCH_FOLDER, f)
            if os.path.isfile(full_path):
                sz = human_size(os.path.getsize(full_path))
                send_notification(
                    "New File Detected",
                    f"{f} - {sz}"
                )
                print(f"Sent notification for: {f}")
        seen = current
```

**Usage:**
1. Set your Pushover environment variables (`PUSHOVER_TOKEN` and `PUSHOVER_USER`)
2. Run: `python3 file_monitor.py`

No external dependencies needed - uses only the Python standard library.
