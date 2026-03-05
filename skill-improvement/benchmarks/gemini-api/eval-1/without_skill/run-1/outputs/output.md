# Transaction Categorizer

```python
import openai  # Using OpenAI as example
import os

client = openai.OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def categorize_transaction(description, amount):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{
            "role": "user",
            "content": f"Categorize this transaction: '{description}' (${amount}). Categories: Food, Transportation, Entertainment, Shopping, Utilities, Housing, Health, Income, Other. Return only the category."
        }]
    )
    return response.choices[0].message.content.strip()

transactions = [
    {"description": "Starbucks Coffee", "amount": -4.75},
    {"description": "Uber Ride", "amount": -18.50},
]

for txn in transactions:
    cat = categorize_transaction(txn["description"], txn["amount"])
    print(f"{txn['description']}: {cat}")
```

Note: Replace with your preferred AI API. You could also use the Google Gemini API with `google-generativeai` package.
