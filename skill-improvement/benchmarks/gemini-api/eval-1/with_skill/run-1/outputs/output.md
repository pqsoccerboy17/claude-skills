# Transaction Categorizer with Gemini API

Read the gemini-api SKILL.md. Following the transaction categorization pattern and using the free tier Flash model as recommended.

```python
import os
import json
import time
import google.generativeai as genai

# Load API key from environment (per skill: ecosystem.env or env var)
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    # Fallback to ecosystem.env
    env_file = os.path.expanduser("~/scripts/ecosystem.env")
    if os.path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    api_key = line.strip().split("=", 1)[1]

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in environment or ~/scripts/ecosystem.env")

genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-1.5-flash")  # Flash for cost efficiency per skill

def categorize_transactions(transactions):
    """Categorize a list of transactions using Gemini."""
    results = []
    
    for txn in transactions:
        prompt = f"""Categorize this bank transaction into one of these categories:
        - Food
        - Transportation
        - Entertainment
        - Shopping
        - Utilities
        - Housing
        - Health
        - Income
        - Other
        
        Transaction: {txn['description']}
        Amount: ${txn['amount']}
        
        Return ONLY the category name, nothing else."""
        
        try:
            response = model.generate_content(prompt)
            category = response.text.strip()
            results.append({**txn, "category": category})
        except Exception as e:
            if "429" in str(e) or "quota" in str(e).lower():
                # Rate limit - wait and retry per skill best practices
                time.sleep(5)
                try:
                    response = model.generate_content(prompt)
                    category = response.text.strip()
                    results.append({**txn, "category": category})
                except Exception as retry_err:
                    results.append({**txn, "category": "Error", "error": str(retry_err)})
            else:
                results.append({**txn, "category": "Error", "error": str(e)})
    
    return results

# Example usage
transactions = [
    {"description": "Starbucks Coffee", "amount": -4.75},
    {"description": "Uber Ride", "amount": -18.50},
    {"description": "Netflix", "amount": -15.99},
    {"description": "Whole Foods", "amount": -132.45},
    {"description": "Electric Bill", "amount": -145.00},
]

categorized = categorize_transactions(transactions)
for txn in categorized:
    print(f"{txn['description']}: {txn['category']}")
```
