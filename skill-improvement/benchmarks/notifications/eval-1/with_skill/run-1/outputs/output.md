# File Monitor with Pushover Notifications

Read the notifications SKILL.md. Using the send_notification() function from ~/scripts/notify.py per the skill's integration pattern.

```python
import sys
import os
import time
from pathlib import Path
from datetime import datetime

# Import notification module per skill pattern
sys.path.insert(0, str(Path.home() / "scripts"))

try:
    from notify import send_notification
    NOTIFICATIONS_AVAILABLE = True
except ImportError:
    NOTIFICATIONS_AVAILABLE = False
    print("Warning: notify.py not found at ~/scripts/notify.py")

# Verify Pushover environment variables
pushover_user = os.environ.get("PUSHOVER_USER_KEY")
pushover_token = os.environ.get("PUSHOVER_APP_TOKEN")

if not pushover_user or not pushover_token:
    print("Warning: PUSHOVER_USER_KEY and/or PUSHOVER_APP_TOKEN not set")
    print("Pushover notifications will not work without these.")

def format_size(size_bytes):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024

def monitor_folder(watch_dir, poll_interval=5):
    """Monitor a folder for new files and send Pushover notifications."""
    watch_path = Path(watch_dir)
    if not watch_path.exists():
        print(f"Directory not found: {watch_dir}")
        return
    
    known_files = set(f.name for f in watch_path.iterdir() if f.is_file())
    print(f"Monitoring {watch_dir} for new files...")
    
    while True:
        current_files = set(f.name for f in watch_path.iterdir() if f.is_file())
        new_files = current_files - known_files
        
        for filename in new_files:
            filepath = watch_path / filename
            size = format_size(filepath.stat().st_size)
            
            print(f"New file: {filename} ({size})")
            
            if NOTIFICATIONS_AVAILABLE:
                send_notification(
                    title="New File Detected",
                    message=f"File: {filename}\nSize: {size}\nFolder: {watch_dir}",
                    priority=0  # Normal priority for file monitoring
                )
        
        known_files = current_files
        time.sleep(poll_interval)

if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else str(Path.home() / "Downloads")
    monitor_folder(folder)
```
