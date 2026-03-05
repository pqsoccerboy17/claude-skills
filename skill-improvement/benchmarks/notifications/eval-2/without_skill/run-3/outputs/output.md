# Test Notification

```python
import requests
import os

def send_test():
    token = os.environ.get("PUSHOVER_APP_TOKEN")
    user = os.environ.get("PUSHOVER_USER_KEY")
    
    response = requests.post("https://api.pushover.net/1/messages.json", data={
        "token": token,
        "user": user,
        "message": "Test notification",
        "priority": 0
    })
    
    if response.status_code == 200:
        print("Sent!")
    else:
        print(f"Failed: {response.text}")

send_test()
```
