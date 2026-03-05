# Receipt OCR with Gemini Multimodal

Read the gemini-api SKILL.md. Using the Receipt OCR multimodal pattern from the skill with Flash model.

```python
import os
import json
import google.generativeai as genai
import PIL.Image

# Load API key
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    env_file = os.path.expanduser("~/scripts/ecosystem.env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    api_key = line.strip().split("=", 1)[1]

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")  # Free tier per skill recommendation

def extract_receipt_data(image_path: str) -> dict:
    """Extract structured data from a receipt image using Gemini vision."""
    image = PIL.Image.open(image_path)
    
    prompt = """Extract the following from this receipt image and return as JSON:
    {
        "merchant": "store name",
        "date": "YYYY-MM-DD",
        "total": 0.00,
        "line_items": [
            {"item": "item name", "price": 0.00}
        ]
    }
    
    Return ONLY valid JSON, no other text."""
    
    response = model.generate_content([prompt, image])
    
    # Parse JSON from response
    text = response.text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    
    return json.loads(text)

# Example usage
if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python receipt_ocr.py <image_path>")
        sys.exit(1)
    
    result = extract_receipt_data(sys.argv[1])
    print(json.dumps(result, indent=2))
```
