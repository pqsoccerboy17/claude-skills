# Receipt Data Extraction

```python
import base64
import requests
import json

def extract_receipt(image_path):
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()
    
    # Using a generic vision API approach
    response = requests.post(
        "https://api.openai.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.environ['OPENAI_API_KEY']}"},
        json={
            "model": "gpt-4-vision-preview",
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": "Extract merchant, date, total, and line items from this receipt. Return JSON."},
                    {"type": "image_url", "url": {"url": f"data:image/jpeg;base64,{image_data}"}}
                ]
            }]
        }
    )
    
    return json.loads(response.json()["choices"][0]["message"]["content"])

result = extract_receipt("receipt.jpg")
print(json.dumps(result, indent=2))
```
