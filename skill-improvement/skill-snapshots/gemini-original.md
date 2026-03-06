---
name: gemini-api
description: Google Gemini API integration for AI-powered automation
---

# Gemini API Skill

Direct access to Google's Gemini API for AI-powered automation tasks.

## Why This Exists

Gemini provides a generous free tier (1M tokens/min, no credit card required) making it ideal for:
- Transaction categorization
- Document analysis
- Text summarization
- Data extraction from receipts
- Research and lead enrichment

## Free Tier Limits (as of Jan 2026)

| Model | Requests/Min | Tokens/Min | Daily Limit |
|-------|--------------|------------|-------------|
| Gemini 1.5 Flash | 15 | 1,000,000 | 1,500 |
| Gemini 1.5 Pro | 2 | 32,000 | 50 |
| Gemini 2.0 Flash | 10 | 4,000,000 | Varies |

## Setup

### 1. Get API Key (Free)

1. Go to https://aistudio.google.com/
2. Sign in with Google account
3. Click "Get API Key" → "Create API key"
4. Copy the key

### 2. Configure Environment

Add to `~/scripts/ecosystem.env`:

```bash
GEMINI_API_KEY=your_api_key_here
```

Or set in shell:

```bash
export GEMINI_API_KEY="AIzaSy..."
```

## Usage Examples

### Basic Text Generation

```python
import google.generativeai as genai

genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-1.5-flash")

response = model.generate_content("Summarize this document...")
print(response.text)
```

### Transaction Categorization

```python
def categorize_transaction(description: str, amount: float) -> str:
    """Use Gemini to categorize a financial transaction."""
    prompt = f"""Categorize this transaction into one of these categories:
    - Utilities
    - Insurance
    - Repairs & Maintenance
    - Taxes
    - Mortgage
    - HOA
    - Rental Income
    - Other

    Transaction: {description}
    Amount: ${amount}

    Return ONLY the category name, nothing else."""

    response = model.generate_content(prompt)
    return response.text.strip()
```

### Receipt OCR (Multimodal)

```python
import PIL.Image

def extract_receipt_data(image_path: str) -> dict:
    """Extract data from a receipt image."""
    image = PIL.Image.open(image_path)

    prompt = """Extract the following from this receipt:
    - Store name
    - Date
    - Total amount
    - List of items with prices

    Return as JSON."""

    response = model.generate_content([prompt, image])
    return json.loads(response.text)
```

### Lead Research

```python
def research_company(company_name: str) -> dict:
    """Research a company for consulting lead enrichment."""
    prompt = f"""Research {company_name} and provide:
    - Industry
    - Company size (estimate)
    - Key products/services
    - Recent news or developments
    - Potential pain points that AI/consulting could address

    Be concise. Return as structured text."""

    response = model.generate_content(prompt)
    return {"company": company_name, "research": response.text}
```

## Integration with n8n

### HTTP Request Node Configuration

In n8n, use an HTTP Request node:

**URL**: `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent`

**Method**: POST

**Query Parameters**:
- `key`: `{{$env.GEMINI_API_KEY}}`

**Body** (JSON):
```json
{
  "contents": [
    {
      "parts": [
        {
          "text": "Your prompt here"
        }
      ]
    }
  ]
}
```

### n8n Code Node Example

```javascript
// Categorize transactions using Gemini
const apiKey = $env.GEMINI_API_KEY;
const description = $input.item.json.description;
const amount = $input.item.json.amount;

const response = await fetch(
  `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${apiKey}`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      contents: [{
        parts: [{
          text: `Categorize this transaction: "${description}" ($${amount}). Reply with only the category.`
        }]
      }]
    })
  }
);

const data = await response.json();
const category = data.candidates[0].content.parts[0].text.trim();

return { category };
```

## Python Helper Script

A helper script is available at:

```
~/dev/tools/claude-skills/ai-apis/gemini/scripts/gemini_api.py
```

## Best Practices

1. **Use Flash for high-volume tasks** - It's faster and has higher limits
2. **Batch requests when possible** - Reduce API calls
3. **Cache responses** - Store results to avoid redundant calls
4. **Handle rate limits gracefully** - Implement exponential backoff
5. **Keep prompts concise** - Shorter prompts = lower token usage

## Troubleshooting

### "API key not valid"
- Verify key at https://aistudio.google.com/
- Check for extra spaces in the key
- Ensure key is enabled for Generative Language API

### Rate limit errors
- Wait and retry with exponential backoff
- Use Flash model for higher limits
- Spread requests over time

### Empty responses
- Check prompt clarity
- Verify content isn't being blocked by safety filters
- Try rephrasing the prompt
