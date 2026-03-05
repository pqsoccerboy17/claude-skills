# File Monitor with Notifications

```python
import os
import time
import subprocess
from pathlib import Path

def monitor_folder(watch_dir):
    watch_path = Path(watch_dir)
    known = set(f.name for f in watch_path.iterdir() if f.is_file())
    
    while True:
        current = set(f.name for f in watch_path.iterdir() if f.is_file())
        new = current - known
        
        for f in new:
            size = (watch_path / f).stat().st_size
            print(f"New file: {f} ({size} bytes)")
            
            # macOS notification
            subprocess.run([
                "osascript", "-e",
                f'display notification "New file: {f}" with title "File Monitor"'
            ])
        
        known = current
        time.sleep(5)

if __name__ == "__main__":
    monitor_folder(os.path.expanduser("~/Downloads"))
```

This script monitors a folder and sends macOS notifications when new files appear.
