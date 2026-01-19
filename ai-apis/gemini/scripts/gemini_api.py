#!/usr/bin/env python3
"""
Gemini API Helper Script

Provides easy access to Google's Gemini API for common automation tasks.
Designed to be used by Claude Code, n8n, or standalone scripts.

Usage:
    # Categorize a transaction
    python gemini_api.py categorize "COSTCO WHOLESALE" -89.47

    # Summarize text
    python gemini_api.py summarize "Long text to summarize..."

    # Research a company
    python gemini_api.py research "Acme Corp"

    # Extract data from receipt image
    python gemini_api.py receipt /path/to/receipt.jpg
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Optional


def get_api_key() -> str:
    """Get Gemini API key from environment or config."""
    key = os.environ.get("GEMINI_API_KEY")
    if key:
        return key

    # Try ecosystem.env
    env_file = Path.home() / "scripts/ecosystem.env"
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip('"').strip("'")

    raise ValueError(
        "GEMINI_API_KEY not found. Set it in environment or ~/scripts/ecosystem.env"
    )


def call_gemini(prompt: str, model: str = "gemini-2.0-flash") -> str:
    """
    Make a request to Gemini API.

    Args:
        prompt: The prompt to send
        model: Model to use (default: gemini-1.5-flash)

    Returns:
        Generated text response
    """
    import urllib.request
    import urllib.error

    api_key = get_api_key()
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"

    data = {
        "contents": [
            {
                "parts": [
                    {"text": prompt}
                ]
            }
        ]
    }

    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
            return result["candidates"][0]["content"]["parts"][0]["text"]
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        raise Exception(f"Gemini API error {e.code}: {error_body}")


def categorize_transaction(description: str, amount: float) -> Dict[str, Any]:
    """
    Categorize a financial transaction.

    Args:
        description: Transaction description
        amount: Transaction amount

    Returns:
        Dictionary with category and confidence
    """
    prompt = f"""Categorize this financial transaction into exactly one of these categories:
- Utilities
- Insurance
- Repairs & Maintenance
- Property Tax
- Mortgage
- HOA
- Rental Income
- Groceries
- Dining
- Transportation
- Entertainment
- Shopping
- Healthcare
- Other

Transaction: {description}
Amount: ${amount:.2f}

Respond with ONLY the category name, nothing else."""

    category = call_gemini(prompt).strip()

    # Clean up response
    category = category.replace("*", "").strip()

    return {
        "description": description,
        "amount": amount,
        "category": category
    }


def summarize_text(text: str, max_words: int = 100) -> str:
    """
    Summarize text.

    Args:
        text: Text to summarize
        max_words: Maximum words in summary

    Returns:
        Summary text
    """
    prompt = f"""Summarize the following text in {max_words} words or less:

{text}

Be concise and capture the key points."""

    return call_gemini(prompt).strip()


def research_company(company_name: str) -> Dict[str, Any]:
    """
    Research a company for lead enrichment.

    Args:
        company_name: Name of the company

    Returns:
        Dictionary with research findings
    """
    prompt = f"""Research the company "{company_name}" and provide the following information:

1. Industry/Sector
2. Estimated company size (employees, revenue range if known)
3. Key products or services
4. Headquarters location
5. Brief description of what they do
6. Potential AI/automation opportunities

Be concise and factual. If you're uncertain about something, say so."""

    research = call_gemini(prompt).strip()

    return {
        "company": company_name,
        "research": research,
        "timestamp": __import__("datetime").datetime.now().isoformat()
    }


def extract_receipt(image_path: str) -> Dict[str, Any]:
    """
    Extract data from a receipt image using Gemini's multimodal capabilities.

    Note: This requires the google-generativeai package for image handling.

    Args:
        image_path: Path to receipt image

    Returns:
        Dictionary with extracted receipt data
    """
    try:
        import google.generativeai as genai
        import PIL.Image
    except ImportError:
        return {
            "error": "google-generativeai and Pillow packages required. Run: pip install google-generativeai Pillow"
        }

    api_key = get_api_key()
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel("gemini-1.5-flash")
    image = PIL.Image.open(image_path)

    prompt = """Extract the following information from this receipt:
- Store/Merchant name
- Date
- Total amount
- Tax amount (if shown)
- Payment method (if shown)
- List of items with prices

Return as JSON with these fields: merchant, date, total, tax, payment_method, items (array of {name, price})"""

    response = model.generate_content([prompt, image])

    try:
        # Try to parse as JSON
        text = response.text.strip()
        # Remove markdown code blocks if present
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(text)
    except json.JSONDecodeError:
        return {"raw_text": response.text}


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Gemini API Helper")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Categorize command
    cat_parser = subparsers.add_parser("categorize", help="Categorize a transaction")
    cat_parser.add_argument("description", help="Transaction description")
    cat_parser.add_argument("amount", type=float, help="Transaction amount")

    # Summarize command
    sum_parser = subparsers.add_parser("summarize", help="Summarize text")
    sum_parser.add_argument("text", help="Text to summarize")
    sum_parser.add_argument("--max-words", type=int, default=100, help="Max words")

    # Research command
    res_parser = subparsers.add_parser("research", help="Research a company")
    res_parser.add_argument("company", help="Company name")

    # Receipt command
    rec_parser = subparsers.add_parser("receipt", help="Extract receipt data")
    rec_parser.add_argument("image_path", help="Path to receipt image")

    # Raw prompt command
    raw_parser = subparsers.add_parser("prompt", help="Send raw prompt")
    raw_parser.add_argument("prompt", help="Prompt text")

    args = parser.parse_args()

    if args.command == "categorize":
        result = categorize_transaction(args.description, args.amount)
        print(json.dumps(result, indent=2))

    elif args.command == "summarize":
        result = summarize_text(args.text, args.max_words)
        print(result)

    elif args.command == "research":
        result = research_company(args.company)
        print(json.dumps(result, indent=2))

    elif args.command == "receipt":
        result = extract_receipt(args.image_path)
        print(json.dumps(result, indent=2))

    elif args.command == "prompt":
        result = call_gemini(args.prompt)
        print(result)

    else:
        parser.print_help()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
