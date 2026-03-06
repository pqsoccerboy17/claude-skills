Let me send a test notification via Pushover. First I'll write a quick Python script:

```python
import os
import requests

user_key = os.environ.get("PUSHOVER_USER_KEY")
app_token = os.environ.get("PUSHOVER_APP_TOKEN")

if not user_key or not app_token:
    print("Error: PUSHOVER_USER_KEY and PUSHOVER_APP_TOKEN must be set")
else:
    response = requests.post("https://api.pushover.net/1/messages.json", data={
        "token": app_token,
        "user": user_key,
        "message": "This is a test notification to verify Pushover is configured correctly.",
        "title": "Pushover Test",
        "priority": 0
    })
    if response.status_code == 200 and response.json().get("status") == 1:
        print("Success! Test notification sent.")
    else:
        print(f"Failed: {response.text}")
```

```bash
python3 -c "
import os, requests
user_key = os.environ.get('PUSHOVER_USER_KEY')
app_token = os.environ.get('PUSHOVER_APP_TOKEN')
if not user_key or not app_token:
    print('Error: Pushover credentials not found in environment')
else:
    r = requests.post('https://api.pushover.net/1/messages.json', data={'token': app_token, 'user': user_key, 'message': 'Test notification - Pushover setup verified', 'title': 'Test', 'priority': 0})
    print('Success!' if r.ok else f'Failed: {r.text}')
"
```

This will send a normal priority (0) test notification. Check your phone - you should see it appear momentarily if everything is configured correctly.
