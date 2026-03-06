Here's a Python script that monitors a folder for new files and sends Pushover notifications:

```python
import os
import time
import requests

# Pushover configuration
PUSHOVER_API_URL = "https://api.pushover.net/1/messages.json"
PUSHOVER_USER_KEY = os.environ.get("PUSHOVER_USER_KEY")
PUSHOVER_APP_TOKEN = os.environ.get("PUSHOVER_APP_TOKEN")

WATCH_DIR = "/path/to/watch"  # Change this to your target directory
POLL_INTERVAL = 10  # seconds

def send_pushover_notification(message, title="File Monitor"):
    """Send a notification via Pushover API."""
    if not PUSHOVER_USER_KEY or not PUSHOVER_APP_TOKEN:
        print("Error: Pushover credentials not set in environment")
        return False

    data = {
        "token": PUSHOVER_APP_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": message,
        "title": title,
        "priority": 0
    }

    response = requests.post(PUSHOVER_API_URL, data=data)
    return response.status_code == 200

def get_file_size_str(size_bytes):
    """Convert bytes to human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.1f} TB"

def monitor_folder(directory):
    """Watch a directory for new files."""
    known_files = set(os.listdir(directory))
    print(f"Monitoring {directory} for new files...")

    while True:
        time.sleep(POLL_INTERVAL)
        current_files = set(os.listdir(directory))
        new_files = current_files - known_files

        for filename in new_files:
            filepath = os.path.join(directory, filename)
            if os.path.isfile(filepath):
                size = os.path.getsize(filepath)
                size_str = get_file_size_str(size)
                message = f"New file detected: {filename} ({size_str})"
                print(message)
                send_pushover_notification(message)

        known_files = current_files

if __name__ == "__main__":
    monitor_folder(WATCH_DIR)
```

**Setup:**

1. Install requests: `pip install requests`
2. Set your Pushover credentials:
   ```bash
   export PUSHOVER_USER_KEY="your-user-key"
   export PUSHOVER_APP_TOKEN="your-app-token"
   ```
3. Update `WATCH_DIR` to the folder you want to monitor
4. Run: `python monitor.py`

The script polls the directory every 10 seconds and sends a Pushover notification with the filename and size when a new file appears.
