#!/usr/bin/env python3
"""
Gmail Scanner for Treehouse Asset Manager

Extracts purchase information from Gmail emails for asset tracking.
Supports multiple vendors and provides structured output for the review queue.

Usage:
    # Scan last 365 days for all vendors
    python3 gmail_scanner.py --days 365 --output purchases.json

    # Scan specific vendors only
    python3 gmail_scanner.py --days 30 --vendors amazon,homedepot --output purchases.json

    # Preview only (dry-run mode)
    python3 gmail_scanner.py --dry-run --days 30

    # Process a single email by ID
    python3 gmail_scanner.py --email-id <gmail_message_id>

    # Verbose output with debug logging
    python3 gmail_scanner.py --days 30 --verbose

Environment Variables:
    TREEHOUSE_CREDENTIALS_PATH - Path to credentials.json (default: ~/.config/treehouse/credentials.json)
    TREEHOUSE_TOKEN_PATH - Path to token.json (default: ~/.config/treehouse/token.json)
"""

import argparse
import base64
import hashlib
import json
import logging
import os
import re
import sys
from dataclasses import dataclass, field, asdict
from datetime import datetime, timedelta
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
from pathlib import Path
from typing import Optional, Dict, List, Any, Tuple

# =============================================================================
# Configuration
# =============================================================================

DEFAULT_CONFIG_DIR = Path.home() / ".config" / "treehouse"
DEFAULT_CREDENTIALS_PATH = DEFAULT_CONFIG_DIR / "credentials.json"
DEFAULT_TOKEN_PATH = DEFAULT_CONFIG_DIR / "token.json"
DEFAULT_LOG_DIR = DEFAULT_CONFIG_DIR / "logs"

# Gmail API scopes required
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# Supported vendors with their email patterns and domains
VENDOR_CONFIG = {
    "amazon": {
        "name": "Amazon",
        "domains": ["amazon.com", "amazon.co.uk", "amazon.ca"],
        "from_patterns": [
            r"auto-confirm@amazon\.com",
            r"ship-confirm@amazon\.com",
            r"order-update@amazon\.com",
            r"digital-no-reply@amazon\.com",
        ],
        "subject_patterns": [
            r"Your Amazon\.com order",
            r"Your order.*has shipped",
            r"Your Amazon order",
            r"Shipped:",
            r"Delivery",
        ],
    },
    "homedepot": {
        "name": "Home Depot",
        "domains": ["homedepot.com"],
        "from_patterns": [
            r"@homedepot\.com",
            r"@emails\.homedepot\.com",
        ],
        "subject_patterns": [
            r"Your Home Depot Order",
            r"Order Confirmation",
            r"Your order.*shipped",
            r"Your order is ready",
            r"Thank you for your purchase",
        ],
    },
    "lowes": {
        "name": "Lowe's",
        "domains": ["lowes.com"],
        "from_patterns": [
            r"@lowes\.com",
            r"@email\.lowes\.com",
        ],
        "subject_patterns": [
            r"Your Lowe's Order",
            r"Order Confirmation",
            r"Your order.*shipped",
            r"Receipt",
        ],
    },
    "bestbuy": {
        "name": "Best Buy",
        "domains": ["bestbuy.com"],
        "from_patterns": [
            r"@bestbuy\.com",
            r"@emailinfo\.bestbuy\.com",
        ],
        "subject_patterns": [
            r"Your Best Buy Order",
            r"Order Confirmation",
            r"Your order.*shipped",
            r"Thanks for your order",
        ],
    },
    "costco": {
        "name": "Costco",
        "domains": ["costco.com"],
        "from_patterns": [
            r"@costco\.com",
            r"@online\.costco\.com",
        ],
        "subject_patterns": [
            r"Your Costco",
            r"Order Confirmation",
            r"Your order.*shipped",
            r"Receipt",
        ],
    },
    "walmart": {
        "name": "Walmart",
        "domains": ["walmart.com"],
        "from_patterns": [
            r"@walmart\.com",
            r"@email\.walmart\.com",
        ],
        "subject_patterns": [
            r"Your Walmart",
            r"Order Confirmation",
            r"Your order.*shipped",
            r"Thanks for your order",
        ],
    },
    "target": {
        "name": "Target",
        "domains": ["target.com"],
        "from_patterns": [
            r"@target\.com",
            r"@em\.target\.com",
        ],
        "subject_patterns": [
            r"Your Target",
            r"Order Confirmation",
            r"Your order.*shipped",
            r"Thanks for your order",
        ],
    },
    "wayfair": {
        "name": "Wayfair",
        "domains": ["wayfair.com"],
        "from_patterns": [
            r"@wayfair\.com",
            r"@email\.wayfair\.com",
        ],
        "subject_patterns": [
            r"Your Wayfair",
            r"Order Confirmation",
            r"Your order.*shipped",
            r"Order Details",
        ],
    },
    "ikea": {
        "name": "IKEA",
        "domains": ["ikea.com", "ikea.us"],
        "from_patterns": [
            r"@ikea\.com",
            r"@info\.ikea\.com",
        ],
        "subject_patterns": [
            r"Your IKEA",
            r"Order Confirmation",
            r"Your order.*shipped",
            r"Order Details",
        ],
    },
    "menards": {
        "name": "Menards",
        "domains": ["menards.com"],
        "from_patterns": [
            r"@menards\.com",
            r"@email\.menards\.com",
        ],
        "subject_patterns": [
            r"Your Menards",
            r"Order Confirmation",
            r"Your order.*shipped",
            r"Receipt",
        ],
    },
    "acehardware": {
        "name": "Ace Hardware",
        "domains": ["acehardware.com"],
        "from_patterns": [
            r"@acehardware\.com",
            r"@email\.acehardware\.com",
        ],
        "subject_patterns": [
            r"Your Ace Hardware",
            r"Order Confirmation",
            r"Your order.*shipped",
            r"Receipt",
        ],
    },
}

# Property detection keywords based on shipping address
PROPERTY_KEYWORDS = {
    "DAL": ["dallas", "dal", "75", "tx 75"],  # Dallas area zip codes start with 75
    "ATX-A": ["austin", "main", "unit a", "78"],  # Austin zip codes start with 78
    "ATX-B": ["adu", "unit b", "casita"],
    "ATX-C": ["unit c", "adu c"],
}

# Category detection keywords from product names
CATEGORY_KEYWORDS = {
    "HVAC": [
        "air conditioner", "ac unit", "hvac", "furnace", "heat pump",
        "thermostat", "mini split", "condenser", "air handler", "ductless",
        "heating", "cooling", "climate", "nest", "ecobee",
    ],
    "APPL": [
        "refrigerator", "fridge", "freezer", "washer", "dryer",
        "dishwasher", "microwave", "oven", "range", "stove",
        "garbage disposal", "trash compactor", "ice maker",
    ],
    "PLMB": [
        "water heater", "tankless", "toilet", "faucet", "sink",
        "shower", "bathtub", "pipe", "valve", "drain", "plumbing",
        "sump pump", "water softener", "water filter",
    ],
    "ELEC": [
        "electrical panel", "breaker", "outlet", "switch", "light",
        "fixture", "ceiling fan", "chandelier", "sconce", "dimmer",
        "surge protector", "generator", "inverter", "solar",
    ],
    "TOOL": [
        "drill", "saw", "hammer", "wrench", "screwdriver", "pliers",
        "ladder", "level", "measuring", "power tool", "cordless",
        "compressor", "pressure washer", "shop vac",
    ],
    "TECH": [
        "computer", "laptop", "monitor", "keyboard", "mouse",
        "router", "modem", "wifi", "network", "camera", "security",
        "smart home", "hub", "speaker", "television", "tv",
    ],
    "FURN": [
        "desk", "chair", "table", "sofa", "couch", "bed", "mattress",
        "dresser", "cabinet", "shelf", "bookcase", "ottoman",
    ],
    "LAND": [
        "mower", "lawn", "trimmer", "blower", "edger", "sprinkler",
        "irrigation", "hose", "garden", "outdoor", "patio",
    ],
    "SAFE": [
        "smoke detector", "carbon monoxide", "co detector", "fire",
        "extinguisher", "alarm", "sensor", "detector", "safe",
    ],
}


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class PurchaseRecord:
    """Represents a purchase extracted from an email."""
    id: str                          # Unique ID (hash of email)
    vendor: str                      # Amazon, Home Depot, etc.
    product_name: str                # Extracted product name
    model_number: str = ""           # If available
    purchase_date: str = ""          # ISO format
    price: Optional[float] = None    # If available
    email_id: str = ""               # Gmail message ID
    email_subject: str = ""          # For reference
    confidence: float = 0.0          # 0.0-1.0 extraction confidence
    raw_snippet: str = ""            # Original text for review
    suggested_property: str = ""     # DAL, ATX-A, etc.
    suggested_category: str = ""     # HVAC, APPL, etc.
    status: str = "pending_review"   # pending_review, approved, rejected
    extraction_notes: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return asdict(self)


# =============================================================================
# HTML Parser
# =============================================================================

class EmailHTMLParser(HTMLParser):
    """Simple HTML parser to extract text from email bodies."""

    def __init__(self):
        super().__init__()
        self.text_parts = []
        self.skip_tags = {"script", "style", "head", "title", "meta"}
        self.current_tag = None
        self.skip_content = False

    def handle_starttag(self, tag, attrs):
        self.current_tag = tag.lower()
        if self.current_tag in self.skip_tags:
            self.skip_content = True

    def handle_endtag(self, tag):
        if tag.lower() in self.skip_tags:
            self.skip_content = False
        self.current_tag = None

    def handle_data(self, data):
        if not self.skip_content:
            text = data.strip()
            if text:
                self.text_parts.append(text)

    def get_text(self) -> str:
        return " ".join(self.text_parts)


def html_to_text(html_content: str) -> str:
    """Convert HTML to plain text."""
    parser = EmailHTMLParser()
    try:
        parser.feed(html_content)
        return parser.get_text()
    except Exception:
        # Fallback: strip tags with regex
        clean = re.sub(r"<[^>]+>", " ", html_content)
        return " ".join(clean.split())


# =============================================================================
# Gmail API Integration
# =============================================================================

class GmailScanner:
    """Scans Gmail for purchase emails and extracts product information."""

    def __init__(
        self,
        credentials_path: Optional[Path] = None,
        token_path: Optional[Path] = None,
        verbose: bool = False,
    ):
        self.credentials_path = credentials_path or Path(
            os.environ.get("TREEHOUSE_CREDENTIALS_PATH", DEFAULT_CREDENTIALS_PATH)
        )
        self.token_path = token_path or Path(
            os.environ.get("TREEHOUSE_TOKEN_PATH", DEFAULT_TOKEN_PATH)
        )
        self.verbose = verbose
        self.service = None
        self.logger = self._setup_logging()

    def _setup_logging(self) -> logging.Logger:
        """Configure logging."""
        logger = logging.getLogger("gmail_scanner")
        logger.setLevel(logging.DEBUG if self.verbose else logging.INFO)

        # Console handler
        console = logging.StreamHandler()
        console.setLevel(logging.DEBUG if self.verbose else logging.INFO)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        console.setFormatter(formatter)
        logger.addHandler(console)

        # File handler (if log directory exists)
        try:
            DEFAULT_LOG_DIR.mkdir(parents=True, exist_ok=True)
            log_file = DEFAULT_LOG_DIR / f"gmail_scanner_{datetime.now().strftime('%Y%m%d')}.log"
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"Could not create log file: {e}")

        return logger

    def authenticate(self) -> bool:
        """Authenticate with Gmail API."""
        try:
            from google.auth.transport.requests import Request
            from google.oauth2.credentials import Credentials
            from google_auth_oauthlib.flow import InstalledAppFlow
            from googleapiclient.discovery import build
        except ImportError:
            self.logger.error(
                "Google API libraries not installed. Install with:\n"
                "pip install google-auth google-auth-oauthlib google-auth-httplib2 "
                "google-api-python-client"
            )
            return False

        creds = None

        # Load existing token
        if self.token_path.exists():
            try:
                creds = Credentials.from_authorized_user_file(str(self.token_path), SCOPES)
                self.logger.debug(f"Loaded credentials from {self.token_path}")
            except Exception as e:
                self.logger.warning(f"Failed to load token: {e}")

        # Refresh or get new credentials
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                    self.logger.info("Refreshed expired credentials")
                except Exception as e:
                    self.logger.warning(f"Failed to refresh credentials: {e}")
                    creds = None

            if not creds:
                if not self.credentials_path.exists():
                    self.logger.error(
                        f"Credentials file not found: {self.credentials_path}\n"
                        "Please download OAuth credentials from Google Cloud Console\n"
                        "and save them to this location."
                    )
                    return False

                try:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        str(self.credentials_path), SCOPES
                    )
                    creds = flow.run_local_server(port=0)
                    self.logger.info("Completed OAuth flow")
                except Exception as e:
                    self.logger.error(f"OAuth flow failed: {e}")
                    return False

            # Save token
            try:
                self.token_path.parent.mkdir(parents=True, exist_ok=True)
                with open(self.token_path, "w") as token_file:
                    token_file.write(creds.to_json())
                self.logger.debug(f"Saved token to {self.token_path}")
            except Exception as e:
                self.logger.warning(f"Failed to save token: {e}")

        # Build service
        try:
            self.service = build("gmail", "v1", credentials=creds)
            self.logger.info("Gmail API service initialized successfully")
            return True
        except Exception as e:
            self.logger.error(f"Failed to build Gmail service: {e}")
            return False

    def _build_search_query(
        self,
        vendors: Optional[List[str]] = None,
        days: int = 365,
    ) -> str:
        """Build Gmail search query for purchase emails."""
        # Date filter
        after_date = (datetime.now() - timedelta(days=days)).strftime("%Y/%m/%d")
        query_parts = [f"after:{after_date}"]

        # Vendor filter
        if vendors:
            vendor_queries = []
            for vendor_key in vendors:
                if vendor_key in VENDOR_CONFIG:
                    config = VENDOR_CONFIG[vendor_key]
                    for domain in config["domains"]:
                        vendor_queries.append(f"from:{domain}")
            if vendor_queries:
                query_parts.append("(" + " OR ".join(vendor_queries) + ")")
        else:
            # All vendors
            all_domains = []
            for config in VENDOR_CONFIG.values():
                all_domains.extend(config["domains"])
            query_parts.append("(" + " OR ".join(f"from:{d}" for d in all_domains) + ")")

        # Common purchase keywords
        keywords = [
            "order confirmation",
            "order shipped",
            "your order",
            "thank you for your purchase",
            "receipt",
            "invoice",
        ]
        query_parts.append("(" + " OR ".join(f'"{k}"' for k in keywords) + ")")

        return " ".join(query_parts)

    def search_emails(
        self,
        vendors: Optional[List[str]] = None,
        days: int = 365,
        max_results: int = 500,
    ) -> List[Dict[str, Any]]:
        """Search for purchase emails."""
        if not self.service:
            self.logger.error("Gmail service not initialized. Call authenticate() first.")
            return []

        query = self._build_search_query(vendors, days)
        self.logger.info(f"Search query: {query}")

        messages = []
        page_token = None

        try:
            while len(messages) < max_results:
                results = self.service.users().messages().list(
                    userId="me",
                    q=query,
                    maxResults=min(100, max_results - len(messages)),
                    pageToken=page_token,
                ).execute()

                batch = results.get("messages", [])
                messages.extend(batch)

                self.logger.debug(f"Fetched {len(batch)} messages (total: {len(messages)})")

                page_token = results.get("nextPageToken")
                if not page_token:
                    break

            self.logger.info(f"Found {len(messages)} potential purchase emails")
            return messages

        except Exception as e:
            self.logger.error(f"Error searching emails: {e}")
            return []

    def get_email(self, email_id: str) -> Optional[Dict[str, Any]]:
        """Fetch a single email by ID."""
        if not self.service:
            self.logger.error("Gmail service not initialized. Call authenticate() first.")
            return None

        try:
            message = self.service.users().messages().get(
                userId="me",
                id=email_id,
                format="full",
            ).execute()
            return message
        except Exception as e:
            self.logger.error(f"Error fetching email {email_id}: {e}")
            return None

    def _get_email_body(self, message: Dict[str, Any]) -> str:
        """Extract email body text from message."""
        payload = message.get("payload", {})

        def extract_body(part: Dict[str, Any]) -> str:
            """Recursively extract body from message parts."""
            if "body" in part and "data" in part["body"]:
                data = part["body"]["data"]
                decoded = base64.urlsafe_b64decode(data).decode("utf-8", errors="ignore")
                mime_type = part.get("mimeType", "")
                if "html" in mime_type:
                    return html_to_text(decoded)
                return decoded

            if "parts" in part:
                texts = []
                for subpart in part["parts"]:
                    text = extract_body(subpart)
                    if text:
                        texts.append(text)
                return " ".join(texts)

            return ""

        return extract_body(payload)

    def _get_email_headers(self, message: Dict[str, Any]) -> Dict[str, str]:
        """Extract email headers."""
        headers = {}
        for header in message.get("payload", {}).get("headers", []):
            name = header.get("name", "").lower()
            value = header.get("value", "")
            headers[name] = value
        return headers

    def _identify_vendor(
        self,
        from_addr: str,
        subject: str,
    ) -> Tuple[Optional[str], str]:
        """Identify vendor from email headers."""
        from_lower = from_addr.lower()
        subject_lower = subject.lower()

        for vendor_key, config in VENDOR_CONFIG.items():
            # Check from address patterns
            for pattern in config["from_patterns"]:
                if re.search(pattern, from_lower, re.IGNORECASE):
                    return vendor_key, config["name"]

            # Check domain in from address
            for domain in config["domains"]:
                if domain in from_lower:
                    return vendor_key, config["name"]

        return None, ""

    def _extract_products_amazon(self, body: str, subject: str) -> List[Dict[str, Any]]:
        """Extract product info from Amazon emails."""
        products = []

        # Product name patterns
        patterns = [
            # "Item: Product Name"
            r"(?:Item|Product):\s*([^\n\r$]+)",
            # Look for product descriptions
            r"(?:^|\n)\s*([A-Z][^$\n]{10,80})\s*(?:\n|$)",
            # Order item format
            r"Order #[^\n]+\n+([^\n$]+)",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, body, re.IGNORECASE | re.MULTILINE)
            for match in matches[:5]:  # Limit to 5 products
                name = match.strip()
                if len(name) > 10 and not any(skip in name.lower() for skip in [
                    "click here", "view order", "track", "http", "www",
                    "customer service", "amazon.com", "total",
                ]):
                    products.append({
                        "name": name[:200],
                        "confidence": 0.6,
                    })

        # Model number pattern
        model_pattern = r"(?:Model|Part|SKU|Item)[#:\s]+([A-Z0-9][A-Z0-9\-]+)"
        model_matches = re.findall(model_pattern, body, re.IGNORECASE)

        # Price pattern
        price_pattern = r"\$\s*([\d,]+\.?\d{0,2})"
        price_matches = re.findall(price_pattern, body)

        # Enhance products with model/price if found
        for i, product in enumerate(products):
            if i < len(model_matches):
                product["model"] = model_matches[i]
                product["confidence"] += 0.1
            if i < len(price_matches):
                try:
                    product["price"] = float(price_matches[i].replace(",", ""))
                    product["confidence"] += 0.1
                except ValueError:
                    pass

        return products

    def _extract_products_homedepot(self, body: str, subject: str) -> List[Dict[str, Any]]:
        """Extract product info from Home Depot emails."""
        products = []

        patterns = [
            r"Item:\s*([^\n\r$]+)",
            r"Product:\s*([^\n\r$]+)",
            r"(?:SKU|Model):\s*(\S+)\s+([^\n\r$]+)",
            r"(?:^|\n)([A-Z][^\n$]{15,100})\s*\$",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, body, re.IGNORECASE | re.MULTILINE)
            for match in matches[:5]:
                if isinstance(match, tuple):
                    model = match[0].strip()
                    name = match[1].strip() if len(match) > 1 else ""
                else:
                    name = match.strip()
                    model = ""

                if len(name) > 5:
                    products.append({
                        "name": name[:200],
                        "model": model,
                        "confidence": 0.65,
                    })

        # Extract prices
        price_pattern = r"\$\s*([\d,]+\.?\d{0,2})"
        price_matches = re.findall(price_pattern, body)

        for i, product in enumerate(products):
            if i < len(price_matches):
                try:
                    product["price"] = float(price_matches[i].replace(",", ""))
                except ValueError:
                    pass

        return products

    def _extract_products_generic(self, body: str, subject: str, vendor: str) -> List[Dict[str, Any]]:
        """Generic product extraction for any vendor."""
        products = []

        # Common patterns across vendors
        patterns = [
            r"(?:Item|Product|Order Item):\s*([^\n\r$]{10,150})",
            r"(?:^|\n)\s*(\d+)\s+([^\n\r$]{10,100})\s+\$",
            r"Description:\s*([^\n\r$]{10,150})",
        ]

        for pattern in patterns:
            matches = re.findall(pattern, body, re.IGNORECASE | re.MULTILINE)
            for match in matches[:5]:
                if isinstance(match, tuple):
                    name = match[-1].strip()  # Take the last group (usually the name)
                else:
                    name = match.strip()

                if len(name) > 5 and not any(skip in name.lower() for skip in [
                    "click", "view", "track", "http", "www", "help", "contact",
                ]):
                    products.append({
                        "name": name[:200],
                        "confidence": 0.5,
                    })

        # Model numbers
        model_pattern = r"(?:Model|Part|SKU|Item)\s*[#:\s]+([A-Z0-9][A-Z0-9\-]{3,20})"
        model_matches = re.findall(model_pattern, body, re.IGNORECASE)

        for i, product in enumerate(products):
            if i < len(model_matches):
                product["model"] = model_matches[i]
                product["confidence"] += 0.1

        # Prices
        price_pattern = r"\$\s*([\d,]+\.?\d{0,2})"
        price_matches = re.findall(price_pattern, body)

        for i, product in enumerate(products):
            if i < len(price_matches):
                try:
                    product["price"] = float(price_matches[i].replace(",", ""))
                except ValueError:
                    pass

        return products

    def _extract_date(self, headers: Dict[str, str], body: str) -> str:
        """Extract purchase date from email."""
        # Try to parse Date header
        date_str = headers.get("date", "")
        if date_str:
            try:
                dt = parsedate_to_datetime(date_str)
                return dt.strftime("%Y-%m-%d")
            except Exception:
                pass

        # Look for date in body
        date_patterns = [
            r"(?:Order|Purchase)\s*Date:\s*(\w+\s+\d{1,2},?\s+\d{4})",
            r"(\d{1,2}/\d{1,2}/\d{2,4})",
            r"(\d{4}-\d{2}-\d{2})",
        ]

        for pattern in date_patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                try:
                    date_text = match.group(1)
                    # Try various formats
                    for fmt in ["%B %d, %Y", "%b %d, %Y", "%m/%d/%Y", "%m/%d/%y", "%Y-%m-%d"]:
                        try:
                            dt = datetime.strptime(date_text, fmt)
                            return dt.strftime("%Y-%m-%d")
                        except ValueError:
                            continue
                except Exception:
                    pass

        return datetime.now().strftime("%Y-%m-%d")

    def _detect_property(self, body: str, subject: str) -> str:
        """Detect property from shipping address or keywords."""
        text = (body + " " + subject).lower()

        # Check each property's keywords
        matches = {}
        for prop_code, keywords in PROPERTY_KEYWORDS.items():
            count = sum(1 for kw in keywords if kw in text)
            if count > 0:
                matches[prop_code] = count

        if matches:
            # Return property with most keyword matches
            return max(matches, key=matches.get)

        return ""

    def _detect_category(self, product_name: str) -> str:
        """Detect category from product name."""
        name_lower = product_name.lower()

        matches = {}
        for category, keywords in CATEGORY_KEYWORDS.items():
            count = sum(1 for kw in keywords if kw in name_lower)
            if count > 0:
                matches[category] = count

        if matches:
            return max(matches, key=matches.get)

        return "MISC"

    def _generate_record_id(self, email_id: str, product_name: str) -> str:
        """Generate unique ID for a purchase record."""
        content = f"{email_id}:{product_name}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def extract_purchases(self, message: Dict[str, Any]) -> List[PurchaseRecord]:
        """Extract purchase records from an email message."""
        records = []

        email_id = message.get("id", "")
        headers = self._get_email_headers(message)
        body = self._get_email_body(message)

        from_addr = headers.get("from", "")
        subject = headers.get("subject", "")

        # Identify vendor
        vendor_key, vendor_name = self._identify_vendor(from_addr, subject)
        if not vendor_key:
            self.logger.debug(f"Unknown vendor for email: {subject}")
            return records

        self.logger.debug(f"Processing {vendor_name} email: {subject[:50]}")

        # Extract products based on vendor
        if vendor_key == "amazon":
            products = self._extract_products_amazon(body, subject)
        elif vendor_key == "homedepot":
            products = self._extract_products_homedepot(body, subject)
        else:
            products = self._extract_products_generic(body, subject, vendor_key)

        # Extract common fields
        purchase_date = self._extract_date(headers, body)
        suggested_property = self._detect_property(body, subject)

        # Create records for each product
        for product in products:
            product_name = product.get("name", "Unknown Product")
            suggested_category = self._detect_category(product_name)

            # Calculate confidence
            confidence = product.get("confidence", 0.5)
            if product.get("model"):
                confidence += 0.1
            if product.get("price"):
                confidence += 0.1
            if suggested_property:
                confidence += 0.05
            if suggested_category != "MISC":
                confidence += 0.05
            confidence = min(confidence, 1.0)

            # Extraction notes
            notes = []
            if not product.get("model"):
                notes.append("Model number not found")
            if not product.get("price"):
                notes.append("Price not extracted")
            if not suggested_property:
                notes.append("Property not detected from shipping address")

            record = PurchaseRecord(
                id=self._generate_record_id(email_id, product_name),
                vendor=vendor_name,
                product_name=product_name,
                model_number=product.get("model", ""),
                purchase_date=purchase_date,
                price=product.get("price"),
                email_id=email_id,
                email_subject=subject[:200],
                confidence=round(confidence, 2),
                raw_snippet=body[:500],
                suggested_property=suggested_property,
                suggested_category=suggested_category,
                status="pending_review",
                extraction_notes=notes,
            )
            records.append(record)

        if not records:
            # Create placeholder record if no products extracted
            record = PurchaseRecord(
                id=self._generate_record_id(email_id, "unknown"),
                vendor=vendor_name,
                product_name="[Extraction failed - manual review needed]",
                purchase_date=purchase_date,
                email_id=email_id,
                email_subject=subject[:200],
                confidence=0.1,
                raw_snippet=body[:500],
                suggested_property=suggested_property,
                suggested_category="MISC",
                status="pending_review",
                extraction_notes=["Product extraction failed - manual review required"],
            )
            records.append(record)

        return records

    def scan(
        self,
        vendors: Optional[List[str]] = None,
        days: int = 365,
        max_results: int = 500,
    ) -> List[PurchaseRecord]:
        """Scan Gmail for purchases and return records."""
        all_records = []

        messages = self.search_emails(vendors, days, max_results)

        for i, msg_ref in enumerate(messages):
            email_id = msg_ref.get("id", "")

            if self.verbose:
                self.logger.debug(f"Processing email {i+1}/{len(messages)}: {email_id}")

            message = self.get_email(email_id)
            if message:
                records = self.extract_purchases(message)
                all_records.extend(records)

                if records:
                    self.logger.debug(f"  Extracted {len(records)} product(s)")

        # Deduplicate by ID
        seen = set()
        unique_records = []
        for record in all_records:
            if record.id not in seen:
                seen.add(record.id)
                unique_records.append(record)

        self.logger.info(
            f"Extracted {len(unique_records)} unique purchase records "
            f"from {len(messages)} emails"
        )

        return unique_records

    def scan_single_email(self, email_id: str) -> List[PurchaseRecord]:
        """Scan a single email by ID."""
        message = self.get_email(email_id)
        if message:
            return self.extract_purchases(message)
        return []


# =============================================================================
# Output Functions
# =============================================================================

def save_records(records: List[PurchaseRecord], output_path: Path) -> bool:
    """Save purchase records to JSON file."""
    try:
        data = {
            "generated_at": datetime.now().isoformat(),
            "count": len(records),
            "records": [r.to_dict() for r in records],
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w") as f:
            json.dump(data, f, indent=2)

        return True
    except Exception as e:
        logging.error(f"Failed to save records: {e}")
        return False


def print_summary(records: List[PurchaseRecord]):
    """Print summary of extracted records."""
    print("\n" + "=" * 70)
    print("GMAIL SCANNER RESULTS")
    print("=" * 70)

    if not records:
        print("\nNo purchase records found.")
        return

    # Summary by vendor
    vendors = {}
    for r in records:
        vendors[r.vendor] = vendors.get(r.vendor, 0) + 1

    print(f"\nTotal Records: {len(records)}")
    print("\nBy Vendor:")
    for vendor, count in sorted(vendors.items()):
        print(f"  {vendor}: {count}")

    # Summary by confidence
    high_conf = sum(1 for r in records if r.confidence >= 0.8)
    med_conf = sum(1 for r in records if 0.5 <= r.confidence < 0.8)
    low_conf = sum(1 for r in records if r.confidence < 0.5)

    print("\nBy Confidence Level:")
    print(f"  High (>=0.8): {high_conf}")
    print(f"  Medium (0.5-0.8): {med_conf}")
    print(f"  Low (<0.5): {low_conf}")

    # Summary by property
    properties = {}
    for r in records:
        prop = r.suggested_property or "Unknown"
        properties[prop] = properties.get(prop, 0) + 1

    print("\nBy Suggested Property:")
    for prop, count in sorted(properties.items()):
        print(f"  {prop}: {count}")

    # Sample records
    print("\n" + "-" * 70)
    print("SAMPLE RECORDS (first 5)")
    print("-" * 70)

    for i, record in enumerate(records[:5]):
        print(f"\n[{i+1}] {record.product_name[:60]}")
        print(f"    Vendor: {record.vendor}")
        print(f"    Date: {record.purchase_date}")
        if record.price:
            print(f"    Price: ${record.price:,.2f}")
        if record.model_number:
            print(f"    Model: {record.model_number}")
        print(f"    Property: {record.suggested_property or 'Unknown'}")
        print(f"    Category: {record.suggested_category}")
        print(f"    Confidence: {record.confidence:.0%}")
        print(f"    Email: {record.email_subject[:50]}...")

    print("\n" + "=" * 70)


def print_records_table(records: List[PurchaseRecord]):
    """Print records in table format."""
    print(f"\n{'Product':<40} {'Vendor':<15} {'Date':<12} {'Price':>10} {'Conf':>6}")
    print("-" * 90)

    for record in records:
        name = record.product_name[:38] + ".." if len(record.product_name) > 40 else record.product_name
        price = f"${record.price:,.2f}" if record.price else "N/A"
        print(f"{name:<40} {record.vendor:<15} {record.purchase_date:<12} {price:>10} {record.confidence:>5.0%}")


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Gmail Scanner for Treehouse Asset Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python gmail_scanner.py --days 365 --output purchases.json
  python gmail_scanner.py --days 30 --vendors amazon,homedepot --dry-run
  python gmail_scanner.py --email-id 18abc123def
  python gmail_scanner.py --days 90 --verbose
        """
    )

    parser.add_argument(
        "--days",
        type=int,
        default=365,
        help="Number of days to scan (default: 365)"
    )

    parser.add_argument(
        "--vendors",
        type=str,
        help="Comma-separated list of vendors to scan (e.g., amazon,homedepot). "
             f"Available: {', '.join(VENDOR_CONFIG.keys())}"
    )

    parser.add_argument(
        "--output", "-o",
        type=str,
        help="Output JSON file path"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview results without saving to file"
    )

    parser.add_argument(
        "--email-id",
        type=str,
        help="Process a single email by Gmail message ID"
    )

    parser.add_argument(
        "--max-results",
        type=int,
        default=500,
        help="Maximum number of emails to process (default: 500)"
    )

    parser.add_argument(
        "--credentials",
        type=str,
        help=f"Path to credentials.json (default: {DEFAULT_CREDENTIALS_PATH})"
    )

    parser.add_argument(
        "--token",
        type=str,
        help=f"Path to token.json (default: {DEFAULT_TOKEN_PATH})"
    )

    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Enable verbose output"
    )

    parser.add_argument(
        "--list-vendors",
        action="store_true",
        help="List all supported vendors and exit"
    )

    parser.add_argument(
        "--table",
        action="store_true",
        help="Display results in table format"
    )

    args = parser.parse_args()

    # List vendors and exit
    if args.list_vendors:
        print("\nSupported Vendors:")
        print("-" * 40)
        for key, config in VENDOR_CONFIG.items():
            print(f"  {key:<15} - {config['name']}")
        print()
        return

    # Parse vendors
    vendors = None
    if args.vendors:
        vendors = [v.strip().lower() for v in args.vendors.split(",")]
        invalid = [v for v in vendors if v not in VENDOR_CONFIG]
        if invalid:
            print(f"Error: Unknown vendor(s): {', '.join(invalid)}")
            print(f"Available vendors: {', '.join(VENDOR_CONFIG.keys())}")
            sys.exit(1)

    # Initialize scanner
    scanner = GmailScanner(
        credentials_path=Path(args.credentials) if args.credentials else None,
        token_path=Path(args.token) if args.token else None,
        verbose=args.verbose,
    )

    # Authenticate
    print("Authenticating with Gmail API...")
    if not scanner.authenticate():
        print("Authentication failed. Please check your credentials.")
        sys.exit(1)

    # Scan emails
    if args.email_id:
        print(f"Processing single email: {args.email_id}")
        records = scanner.scan_single_email(args.email_id)
    else:
        print(f"Scanning emails from the last {args.days} days...")
        if vendors:
            print(f"Filtering by vendors: {', '.join(vendors)}")
        records = scanner.scan(
            vendors=vendors,
            days=args.days,
            max_results=args.max_results,
        )

    # Display results
    if args.table:
        print_records_table(records)
    else:
        print_summary(records)

    # Save results
    if not args.dry_run and args.output:
        output_path = Path(args.output)
        print(f"\nSaving {len(records)} records to {output_path}...")
        if save_records(records, output_path):
            print(f"Successfully saved to {output_path}")
        else:
            print("Failed to save records")
            sys.exit(1)
    elif args.dry_run:
        print("\n[DRY RUN] Results not saved.")
    elif not args.output and records:
        print("\nNote: Use --output to save results to a file.")


if __name__ == "__main__":
    main()
