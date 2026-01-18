#!/usr/bin/env python3
"""
Manual Finder for Treehouse Asset Manager

Find and download product manuals from the web using multiple search strategies.

Usage:
    # Single product search
    python3 manual_finder.py --product "LG Refrigerator" --model "LRMVS3006S"
    python3 manual_finder.py --product "Carrier AC" --model "24ACC636A003" --brand "Carrier"

    # Batch processing
    python3 manual_finder.py --input purchases.json --output manuals.json

    # Download manuals
    python3 manual_finder.py --input purchases.json --download --output-dir ./manuals/

    # Search only (no download)
    python3 manual_finder.py --product "Samsung Washer" --model "WF45R6100AW" --no-download

Design Principles:
    - Pure Python, no AI dependencies
    - Standalone CLI operation
    - Respectful rate limiting (1 req/sec)
    - Comprehensive error handling
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.parse
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any
import logging

try:
    import requests
    from requests.adapters import HTTPAdapter
    from urllib3.util.retry import Retry
except ImportError:
    print("Error: requests library required. Install with: pip install requests")
    sys.exit(1)

try:
    from bs4 import BeautifulSoup
except ImportError:
    print("Error: beautifulsoup4 library required. Install with: pip install beautifulsoup4")
    sys.exit(1)


# =============================================================================
# Configuration
# =============================================================================

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Rate limiting (seconds between requests)
RATE_LIMIT_DELAY = 1.0

# Request timeout (seconds)
REQUEST_TIMEOUT = 30

# Maximum file size to download (50 MB)
MAX_FILE_SIZE = 50 * 1024 * 1024

# Minimum valid PDF size (1 KB)
MIN_PDF_SIZE = 1024

# PDF magic bytes
PDF_MAGIC_BYTES = b'%PDF'

# User agent for requests
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/120.0.0.0 Safari/537.36"
)

# Manufacturer support URLs and patterns
MANUFACTURER_PATTERNS: Dict[str, Dict[str, Any]] = {
    "lg": {
        "domain": "support.lg.com",
        "search_url": "https://www.lg.com/us/support/products",
        "manual_patterns": [
            r"https://.*\.lg\.com/.*\.pdf",
            r"https://gscs.*\.lge\.com/.*\.pdf",
        ]
    },
    "samsung": {
        "domain": "samsung.com",
        "search_url": "https://www.samsung.com/us/support/model/{model}/",
        "manual_patterns": [
            r"https://.*samsung.*\.pdf",
            r"https://downloadcenter\.samsung\.com/.*\.pdf",
        ]
    },
    "ge": {
        "domain": "geappliances.com",
        "search_url": "https://www.geappliances.com/ge/search.htm?searchTerm={model}",
        "manual_patterns": [
            r"https://.*geappliances\.com/.*\.pdf",
            r"https://products\.geappliances\.com/.*\.pdf",
        ]
    },
    "whirlpool": {
        "domain": "whirlpool.com",
        "search_url": "https://www.whirlpool.com/services/manuals.html",
        "manual_patterns": [
            r"https://.*whirlpool.*\.pdf",
        ]
    },
    "frigidaire": {
        "domain": "frigidaire.com",
        "search_url": "https://www.frigidaire.com/Owner-Center/Product-Support-Resources/",
        "manual_patterns": [
            r"https://.*frigidaire.*\.pdf",
            r"https://.*electrolux.*\.pdf",
        ]
    },
    "carrier": {
        "domain": "carrier.com",
        "search_url": "https://www.carrier.com/residential/en/us/products/",
        "manual_patterns": [
            r"https://.*carrier\.com/.*\.pdf",
        ]
    },
    "trane": {
        "domain": "trane.com",
        "search_url": "https://www.trane.com/residential/en/resources/",
        "manual_patterns": [
            r"https://.*trane\.com/.*\.pdf",
        ]
    },
    "lennox": {
        "domain": "lennox.com",
        "search_url": "https://www.lennox.com/owners/resources/library",
        "manual_patterns": [
            r"https://.*lennox\.com/.*\.pdf",
        ]
    },
    "bosch": {
        "domain": "bosch-home.com",
        "search_url": "https://www.bosch-home.com/us/support",
        "manual_patterns": [
            r"https://.*bosch.*\.pdf",
        ]
    },
    "kitchenaid": {
        "domain": "kitchenaid.com",
        "search_url": "https://www.kitchenaid.com/owners.html",
        "manual_patterns": [
            r"https://.*kitchenaid.*\.pdf",
        ]
    },
    "maytag": {
        "domain": "maytag.com",
        "search_url": "https://www.maytag.com/services/manuals.html",
        "manual_patterns": [
            r"https://.*maytag.*\.pdf",
        ]
    },
    "honeywell": {
        "domain": "honeywellhome.com",
        "search_url": "https://www.honeywellhome.com/support/",
        "manual_patterns": [
            r"https://.*honeywell.*\.pdf",
        ]
    },
    "nest": {
        "domain": "nest.com",
        "search_url": "https://support.google.com/googlenest/",
        "manual_patterns": [
            r"https://.*nest.*\.pdf",
            r"https://.*google.*nest.*\.pdf",
        ]
    },
    "ecobee": {
        "domain": "ecobee.com",
        "search_url": "https://support.ecobee.com/",
        "manual_patterns": [
            r"https://.*ecobee.*\.pdf",
        ]
    },
}

# Third-party manual sites
MANUAL_SITES = [
    {
        "name": "ManualsLib",
        "domain": "manualslib.com",
        "search_url": "https://www.manualslib.com/search?q={query}",
        "confidence": 0.8
    },
    {
        "name": "ManualsOnline",
        "domain": "manualsonline.com",
        "search_url": "https://www.manualsonline.com/search?q={query}",
        "confidence": 0.7
    },
]


# =============================================================================
# Data Classes
# =============================================================================

@dataclass
class ProductQuery:
    """Input format for manual search."""
    product_name: str
    model_number: Optional[str] = None
    brand: Optional[str] = None
    purchase_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ProductQuery':
        return cls(
            product_name=data.get("product_name", ""),
            model_number=data.get("model_number"),
            brand=data.get("brand"),
            purchase_id=data.get("purchase_id")
        )

    def get_search_query(self) -> str:
        """Generate a search query string from the product info."""
        parts = []
        if self.brand:
            parts.append(self.brand)
        parts.append(self.product_name)
        if self.model_number:
            parts.append(self.model_number)
        return " ".join(parts)


@dataclass
class ManualResult:
    """Output format for manual search results."""
    purchase_id: Optional[str]
    manual_url: str
    manual_path: Optional[str] = None
    source: str = "search"  # "manufacturer", "manualslib", "manualsonline", "search"
    confidence: float = 0.0
    file_size: int = 0
    status: str = "not_found"  # "found", "not_found", "downloaded", "review_needed"
    error: Optional[str] = None
    search_query: Optional[str] = None
    timestamp: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ManualResult':
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


# =============================================================================
# HTTP Session Management
# =============================================================================

class RateLimitedSession:
    """HTTP session with rate limiting and retry logic."""

    def __init__(self, rate_limit: float = RATE_LIMIT_DELAY):
        self.rate_limit = rate_limit
        self.last_request_time = 0.0
        self.session = self._create_session()

    def _create_session(self) -> requests.Session:
        """Create a requests session with retry logic."""
        session = requests.Session()

        # Configure retries
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        # Set default headers
        session.headers.update({
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        })

        return session

    def _wait_for_rate_limit(self):
        """Enforce rate limiting between requests."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            sleep_time = self.rate_limit - elapsed
            logger.debug(f"Rate limiting: sleeping {sleep_time:.2f}s")
            time.sleep(sleep_time)
        self.last_request_time = time.time()

    def get(self, url: str, **kwargs) -> Optional[requests.Response]:
        """Make a rate-limited GET request."""
        self._wait_for_rate_limit()

        kwargs.setdefault("timeout", REQUEST_TIMEOUT)

        try:
            response = self.session.get(url, **kwargs)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            logger.warning(f"Request failed for {url}: {e}")
            return None

    def head(self, url: str, **kwargs) -> Optional[requests.Response]:
        """Make a rate-limited HEAD request."""
        self._wait_for_rate_limit()

        kwargs.setdefault("timeout", REQUEST_TIMEOUT)

        try:
            response = self.session.head(url, **kwargs)
            return response
        except requests.exceptions.RequestException as e:
            logger.warning(f"HEAD request failed for {url}: {e}")
            return None

    def download_file(self, url: str, dest_path: Path) -> bool:
        """Download a file with progress tracking."""
        self._wait_for_rate_limit()

        try:
            response = self.session.get(url, stream=True, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            # Check content length
            content_length = int(response.headers.get("content-length", 0))
            if content_length > MAX_FILE_SIZE:
                logger.warning(f"File too large: {content_length} bytes")
                return False

            # Download with progress
            downloaded = 0
            with open(dest_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        if downloaded > MAX_FILE_SIZE:
                            logger.warning("Download exceeded max size, aborting")
                            f.close()
                            dest_path.unlink(missing_ok=True)
                            return False

            return True

        except requests.exceptions.RequestException as e:
            logger.error(f"Download failed for {url}: {e}")
            dest_path.unlink(missing_ok=True)
            return False


# =============================================================================
# PDF Validation
# =============================================================================

def validate_pdf(file_path: Path) -> bool:
    """
    Validate that a file is a valid PDF.

    Checks:
    - File exists
    - File size is within acceptable range
    - Magic bytes indicate PDF format
    """
    if not file_path.exists():
        return False

    file_size = file_path.stat().st_size

    # Check minimum size
    if file_size < MIN_PDF_SIZE:
        logger.warning(f"PDF too small: {file_size} bytes")
        return False

    # Check maximum size
    if file_size > MAX_FILE_SIZE:
        logger.warning(f"PDF too large: {file_size} bytes")
        return False

    # Check magic bytes
    try:
        with open(file_path, "rb") as f:
            header = f.read(8)
            if not header.startswith(PDF_MAGIC_BYTES):
                logger.warning(f"Invalid PDF magic bytes: {header[:4]}")
                return False
    except IOError as e:
        logger.error(f"Error reading PDF: {e}")
        return False

    return True


def get_pdf_info(file_path: Path) -> Dict[str, Any]:
    """Get basic info about a PDF file."""
    info = {
        "valid": False,
        "size": 0,
        "path": str(file_path)
    }

    if not file_path.exists():
        return info

    info["size"] = file_path.stat().st_size
    info["valid"] = validate_pdf(file_path)

    return info


# =============================================================================
# Search Strategies
# =============================================================================

class ManualFinder:
    """Main class for finding and downloading product manuals."""

    def __init__(self, output_dir: Optional[Path] = None):
        self.session = RateLimitedSession()
        self.output_dir = output_dir or Path("./manuals")
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def find_manual(self, query: ProductQuery, download: bool = False) -> ManualResult:
        """
        Find a manual for the given product.

        Search order:
        1. Manufacturer website (highest confidence)
        2. ManualsLib.com
        3. ManualsOnline.com
        4. DuckDuckGo search
        """
        result = ManualResult(
            purchase_id=query.purchase_id,
            manual_url="",
            search_query=query.get_search_query(),
            timestamp=datetime.now().isoformat()
        )

        logger.info(f"Searching for manual: {query.get_search_query()}")

        # Try manufacturer first
        brand = self._detect_brand(query)
        if brand:
            logger.info(f"Detected brand: {brand}")
            manufacturer_result = self._search_manufacturer(query, brand)
            if manufacturer_result:
                result.manual_url = manufacturer_result["url"]
                result.source = "manufacturer"
                result.confidence = manufacturer_result["confidence"]
                result.status = "found"
                logger.info(f"Found on manufacturer site: {result.manual_url}")

        # Try ManualsLib
        if result.status == "not_found":
            manualslib_result = self._search_manualslib(query)
            if manualslib_result:
                result.manual_url = manualslib_result["url"]
                result.source = "manualslib"
                result.confidence = manualslib_result["confidence"]
                result.status = "found"
                logger.info(f"Found on ManualsLib: {result.manual_url}")

        # Try ManualsOnline
        if result.status == "not_found":
            manualsonline_result = self._search_manualsonline(query)
            if manualsonline_result:
                result.manual_url = manualsonline_result["url"]
                result.source = "manualsonline"
                result.confidence = manualsonline_result["confidence"]
                result.status = "found"
                logger.info(f"Found on ManualsOnline: {result.manual_url}")

        # Try DuckDuckGo search
        if result.status == "not_found":
            search_result = self._search_duckduckgo(query)
            if search_result:
                result.manual_url = search_result["url"]
                result.source = "search"
                result.confidence = search_result["confidence"]
                result.status = "found" if search_result["confidence"] >= 0.5 else "review_needed"
                logger.info(f"Found via search: {result.manual_url}")

        # Download if requested and found
        if download and result.status in ("found", "review_needed") and result.manual_url:
            download_result = self._download_manual(result.manual_url, query)
            if download_result:
                result.manual_path = download_result["path"]
                result.file_size = download_result["size"]
                result.status = "downloaded"
                logger.info(f"Downloaded to: {result.manual_path}")
            else:
                result.error = "Download failed"

        return result

    def _detect_brand(self, query: ProductQuery) -> Optional[str]:
        """Detect the brand from the query."""
        # First check explicit brand
        if query.brand:
            brand_lower = query.brand.lower()
            for key in MANUFACTURER_PATTERNS:
                if key in brand_lower or brand_lower in key:
                    return key

        # Check product name
        product_lower = query.product_name.lower()
        for brand in MANUFACTURER_PATTERNS:
            if brand in product_lower:
                return brand

        return None

    def _search_manufacturer(self, query: ProductQuery, brand: str) -> Optional[Dict[str, Any]]:
        """Search the manufacturer's website for the manual."""
        if brand not in MANUFACTURER_PATTERNS:
            return None

        config = MANUFACTURER_PATTERNS[brand]

        # Build search URL
        model = query.model_number or ""
        search_url = config["search_url"].format(model=urllib.parse.quote(model))

        # Try direct search on manufacturer site
        response = self.session.get(search_url)
        if not response:
            return None

        # Parse HTML and look for PDF links
        soup = BeautifulSoup(response.text, "html.parser")

        # Find all links
        pdf_links = []
        for link in soup.find_all("a", href=True):
            href = link["href"]

            # Check if it's a PDF link
            if ".pdf" in href.lower():
                # Make absolute URL
                if href.startswith("/"):
                    href = f"https://{config['domain']}{href}"
                elif not href.startswith("http"):
                    href = f"https://{config['domain']}/{href}"

                # Check against patterns
                for pattern in config.get("manual_patterns", []):
                    if re.search(pattern, href, re.IGNORECASE):
                        # Score based on relevance
                        score = self._score_manual_link(href, link.get_text(), query)
                        pdf_links.append({"url": href, "score": score})

        # Also search for model-specific pages
        if query.model_number and not pdf_links:
            model_search_results = self._search_manufacturer_model(query, brand)
            if model_search_results:
                pdf_links.extend(model_search_results)

        if pdf_links:
            # Sort by score and return best match
            pdf_links.sort(key=lambda x: x["score"], reverse=True)
            best = pdf_links[0]
            return {
                "url": best["url"],
                "confidence": min(0.95, 0.7 + best["score"] * 0.25)
            }

        return None

    def _search_manufacturer_model(self, query: ProductQuery, brand: str) -> List[Dict[str, Any]]:
        """Search for model-specific manual page on manufacturer site."""
        results = []
        config = MANUFACTURER_PATTERNS[brand]

        # Try common URL patterns for model support pages
        model = query.model_number
        if not model:
            return results

        model_encoded = urllib.parse.quote(model)
        patterns = [
            f"https://www.{config['domain']}/support/{model_encoded}",
            f"https://www.{config['domain']}/products/{model_encoded}",
            f"https://support.{config['domain']}/product/{model_encoded}",
        ]

        for url in patterns:
            response = self.session.get(url, allow_redirects=True)
            if response and response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                for link in soup.find_all("a", href=True):
                    href = link["href"]
                    text = link.get_text().lower()

                    if ".pdf" in href.lower() and any(kw in text for kw in ["manual", "guide", "instruction"]):
                        if href.startswith("/"):
                            href = f"https://www.{config['domain']}{href}"
                        elif not href.startswith("http"):
                            href = f"https://www.{config['domain']}/{href}"

                        score = self._score_manual_link(href, text, query)
                        results.append({"url": href, "score": score})

        return results

    def _search_manualslib(self, query: ProductQuery) -> Optional[Dict[str, Any]]:
        """Search ManualsLib for the manual."""
        search_query = query.get_search_query()
        encoded_query = urllib.parse.quote(search_query)
        search_url = f"https://www.manualslib.com/?q={encoded_query}"

        response = self.session.get(search_url)
        if not response:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        # Find manual links
        manual_links = []

        # Look for search results
        for result in soup.find_all(class_=re.compile(r"search-result|product-item|manual-item")):
            links = result.find_all("a", href=True)
            for link in links:
                href = link["href"]
                text = link.get_text().lower()

                # ManualsLib specific patterns
                if "/manual" in href or "/pdf" in href:
                    if not href.startswith("http"):
                        href = f"https://www.manualslib.com{href}"

                    score = self._score_manual_link(href, text, query)

                    # Boost if model number appears in URL or text
                    if query.model_number:
                        model_lower = query.model_number.lower()
                        if model_lower in href.lower() or model_lower in text:
                            score += 0.3

                    manual_links.append({"url": href, "score": score})

        # Also look for direct PDF links
        for link in soup.find_all("a", href=True):
            href = link["href"]
            if ".pdf" in href.lower() or "download" in href.lower():
                if not href.startswith("http"):
                    href = f"https://www.manualslib.com{href}"

                score = self._score_manual_link(href, link.get_text(), query)
                manual_links.append({"url": href, "score": score})

        if manual_links:
            manual_links.sort(key=lambda x: x["score"], reverse=True)
            best = manual_links[0]
            return {
                "url": best["url"],
                "confidence": min(0.85, 0.6 + best["score"] * 0.25)
            }

        return None

    def _search_manualsonline(self, query: ProductQuery) -> Optional[Dict[str, Any]]:
        """Search ManualsOnline for the manual."""
        search_query = query.get_search_query()
        encoded_query = urllib.parse.quote(search_query)
        search_url = f"https://www.manualsonline.com/search?q={encoded_query}"

        response = self.session.get(search_url)
        if not response:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        manual_links = []

        # Look for manual links
        for link in soup.find_all("a", href=True):
            href = link["href"]
            text = link.get_text().lower()

            if any(kw in href.lower() for kw in ["manual", "pdf", "download"]):
                if not href.startswith("http"):
                    href = f"https://www.manualsonline.com{href}"

                score = self._score_manual_link(href, text, query)
                manual_links.append({"url": href, "score": score})

        if manual_links:
            manual_links.sort(key=lambda x: x["score"], reverse=True)
            best = manual_links[0]
            return {
                "url": best["url"],
                "confidence": min(0.75, 0.5 + best["score"] * 0.25)
            }

        return None

    def _search_duckduckgo(self, query: ProductQuery) -> Optional[Dict[str, Any]]:
        """Search DuckDuckGo for the manual."""
        search_query = f"{query.get_search_query()} user manual PDF"
        encoded_query = urllib.parse.quote(search_query)

        # Use DuckDuckGo HTML version
        search_url = f"https://html.duckduckgo.com/html/?q={encoded_query}"

        response = self.session.get(search_url)
        if not response:
            return None

        soup = BeautifulSoup(response.text, "html.parser")

        results = []

        # Find search result links
        for result in soup.find_all(class_="result"):
            link = result.find("a", class_="result__url") or result.find("a", href=True)
            if not link:
                continue

            href = link.get("href", "")

            # DuckDuckGo uses redirects, try to get actual URL
            if "duckduckgo.com" in href:
                # Parse redirect URL
                parsed = urllib.parse.urlparse(href)
                params = urllib.parse.parse_qs(parsed.query)
                if "uddg" in params:
                    href = params["uddg"][0]

            if not href.startswith("http"):
                continue

            # Get title/snippet
            title_elem = result.find(class_="result__title") or result.find("a")
            text = title_elem.get_text().lower() if title_elem else ""

            snippet_elem = result.find(class_="result__snippet")
            snippet = snippet_elem.get_text().lower() if snippet_elem else ""

            # Score the result
            score = 0.0

            # Boost for PDF links
            if ".pdf" in href.lower():
                score += 0.4

            # Boost for manual keywords
            combined_text = text + " " + snippet
            if "manual" in combined_text:
                score += 0.2
            if "user guide" in combined_text or "owner" in combined_text:
                score += 0.15
            if "instruction" in combined_text:
                score += 0.1

            # Boost for model number match
            if query.model_number:
                model_lower = query.model_number.lower()
                if model_lower in href.lower() or model_lower in combined_text:
                    score += 0.3

            # Boost for manufacturer sites
            for brand in MANUFACTURER_PATTERNS:
                if brand in href.lower():
                    score += 0.2
                    break

            # Boost for known manual sites
            if "manualslib" in href.lower() or "manualsonline" in href.lower():
                score += 0.15

            if score > 0:
                results.append({"url": href, "score": score})

        if results:
            results.sort(key=lambda x: x["score"], reverse=True)
            best = results[0]
            return {
                "url": best["url"],
                "confidence": min(0.7, 0.3 + best["score"])
            }

        return None

    def _score_manual_link(self, url: str, text: str, query: ProductQuery) -> float:
        """Score a manual link based on relevance."""
        score = 0.0
        url_lower = url.lower()
        text_lower = text.lower()
        combined = url_lower + " " + text_lower

        # Check for model number
        if query.model_number:
            model_lower = query.model_number.lower()
            # Exact match in URL is strongest signal
            if model_lower in url_lower:
                score += 0.5
            # Match in text is also good
            elif model_lower in text_lower:
                score += 0.3
            # Partial match (common for model variations)
            elif model_lower[:6] in combined:  # First 6 chars
                score += 0.2

        # Check for manual keywords
        if "user" in combined and "manual" in combined:
            score += 0.2
        elif "manual" in combined:
            score += 0.15
        elif "guide" in combined:
            score += 0.1
        elif "instruction" in combined:
            score += 0.1

        # Check for product type keywords
        product_words = query.product_name.lower().split()
        for word in product_words:
            if len(word) > 3 and word in combined:
                score += 0.05

        # Penalize non-English, non-PDF
        if any(lang in url_lower for lang in ["/fr/", "/de/", "/es/", "/it/", "/jp/", "/cn/"]):
            score -= 0.2

        return max(0.0, score)

    def _download_manual(self, url: str, query: ProductQuery) -> Optional[Dict[str, Any]]:
        """Download a manual PDF."""
        # Generate filename
        filename = self._generate_filename(url, query)
        dest_path = self.output_dir / filename

        # Check if already downloaded
        if dest_path.exists() and validate_pdf(dest_path):
            logger.info(f"Manual already downloaded: {dest_path}")
            return {
                "path": str(dest_path),
                "size": dest_path.stat().st_size
            }

        # Download the file
        logger.info(f"Downloading: {url}")

        if self.session.download_file(url, dest_path):
            # Validate the downloaded file
            if validate_pdf(dest_path):
                return {
                    "path": str(dest_path),
                    "size": dest_path.stat().st_size
                }
            else:
                logger.warning(f"Downloaded file is not a valid PDF: {dest_path}")
                dest_path.unlink(missing_ok=True)

        return None

    def _generate_filename(self, url: str, query: ProductQuery) -> str:
        """Generate a filename for the downloaded manual."""
        parts = []

        # Add brand if known
        if query.brand:
            parts.append(self._sanitize_filename(query.brand))

        # Add product name (truncated)
        product = query.product_name.split()[0]  # First word
        parts.append(self._sanitize_filename(product))

        # Add model number
        if query.model_number:
            parts.append(self._sanitize_filename(query.model_number))
        else:
            # Use hash of URL as identifier
            url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
            parts.append(url_hash)

        # Add "manual" suffix
        parts.append("manual")

        return "_".join(parts) + ".pdf"

    def _sanitize_filename(self, name: str) -> str:
        """Sanitize a string for use as a filename."""
        # Remove or replace invalid characters
        sanitized = re.sub(r'[<>:"/\\|?*]', '', name)
        sanitized = re.sub(r'\s+', '_', sanitized)
        sanitized = sanitized.strip('._')
        return sanitized[:50]  # Truncate to reasonable length

    def process_batch(self, queries: List[ProductQuery], download: bool = False) -> List[ManualResult]:
        """Process multiple queries in batch."""
        results = []
        total = len(queries)

        for i, query in enumerate(queries, 1):
            logger.info(f"Processing {i}/{total}: {query.get_search_query()}")
            result = self.find_manual(query, download=download)
            results.append(result)

            # Log progress
            if result.status == "downloaded":
                logger.info(f"  -> Downloaded: {result.manual_path}")
            elif result.status == "found":
                logger.info(f"  -> Found: {result.manual_url} (confidence: {result.confidence:.2f})")
            elif result.status == "review_needed":
                logger.info(f"  -> Needs review: {result.manual_url}")
            else:
                logger.info(f"  -> Not found")

        return results


# =============================================================================
# CLI Interface
# =============================================================================

def load_queries_from_json(file_path: str) -> List[ProductQuery]:
    """Load product queries from a JSON file."""
    with open(file_path, "r") as f:
        data = json.load(f)

    queries = []

    # Handle different input formats
    if isinstance(data, list):
        for item in data:
            queries.append(ProductQuery.from_dict(item))
    elif isinstance(data, dict):
        # Could be a single query or a dict with a "products" key
        if "products" in data:
            for item in data["products"]:
                queries.append(ProductQuery.from_dict(item))
        elif "product_name" in data:
            queries.append(ProductQuery.from_dict(data))
        else:
            # Try to extract from purchase records
            for key, value in data.items():
                if isinstance(value, dict) and "product_name" in value:
                    value["purchase_id"] = key
                    queries.append(ProductQuery.from_dict(value))

    return queries


def save_results_to_json(results: List[ManualResult], file_path: str):
    """Save results to a JSON file."""
    data = [r.to_dict() for r in results]
    with open(file_path, "w") as f:
        json.dump(data, f, indent=2)
    logger.info(f"Results saved to: {file_path}")


def print_results(results: List[ManualResult]):
    """Print results in a human-readable format."""
    print("\n" + "=" * 80)
    print("MANUAL FINDER RESULTS")
    print("=" * 80)

    found = [r for r in results if r.status in ("found", "downloaded")]
    review = [r for r in results if r.status == "review_needed"]
    not_found = [r for r in results if r.status == "not_found"]

    print(f"\nSummary: {len(found)} found, {len(review)} need review, {len(not_found)} not found")
    print("-" * 80)

    for result in results:
        print(f"\nQuery: {result.search_query}")
        print(f"Status: {result.status}")
        if result.manual_url:
            print(f"URL: {result.manual_url}")
            print(f"Source: {result.source}")
            print(f"Confidence: {result.confidence:.2f}")
        if result.manual_path:
            print(f"Downloaded: {result.manual_path}")
            print(f"Size: {result.file_size:,} bytes")
        if result.error:
            print(f"Error: {result.error}")

    print("\n" + "=" * 80)


def main():
    parser = argparse.ArgumentParser(
        description="Find and download product manuals from the web",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Single product search
  %(prog)s --product "LG Refrigerator" --model "LRMVS3006S"

  # With brand specified
  %(prog)s --product "AC Unit" --model "24ACC636A003" --brand "Carrier"

  # Batch processing from JSON
  %(prog)s --input purchases.json --output manuals.json

  # Download manuals
  %(prog)s --input purchases.json --download --output-dir ./manuals/

  # Single product with download
  %(prog)s --product "Samsung Washer" --model "WF45R6100AW" --download
"""
    )

    # Single product arguments
    parser.add_argument("--product", "-p", help="Product name (e.g., 'LG Refrigerator')")
    parser.add_argument("--model", "-m", help="Model number (e.g., 'LRMVS3006S')")
    parser.add_argument("--brand", "-b", help="Brand name (e.g., 'LG')")

    # Batch processing arguments
    parser.add_argument("--input", "-i", help="Input JSON file with product queries")
    parser.add_argument("--output", "-o", help="Output JSON file for results")

    # Download options
    parser.add_argument("--download", "-d", action="store_true", help="Download found manuals")
    parser.add_argument("--no-download", action="store_true", help="Search only, don't download")
    parser.add_argument("--output-dir", default="./manuals", help="Directory for downloaded manuals")

    # Output options
    parser.add_argument("--quiet", "-q", action="store_true", help="Minimal output")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    # Configure logging
    if args.quiet:
        logging.getLogger().setLevel(logging.WARNING)
    elif args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Validate arguments
    if not args.product and not args.input:
        parser.error("Either --product or --input is required")

    # Determine if we should download
    should_download = args.download and not args.no_download

    # Create finder
    output_dir = Path(args.output_dir) if should_download else None
    finder = ManualFinder(output_dir=output_dir)

    # Process queries
    if args.input:
        # Batch processing
        logger.info(f"Loading queries from: {args.input}")
        queries = load_queries_from_json(args.input)
        logger.info(f"Loaded {len(queries)} queries")

        results = finder.process_batch(queries, download=should_download)
    else:
        # Single product
        query = ProductQuery(
            product_name=args.product,
            model_number=args.model,
            brand=args.brand
        )
        result = finder.find_manual(query, download=should_download)
        results = [result]

    # Output results
    if args.output:
        save_results_to_json(results, args.output)

    if args.json:
        print(json.dumps([r.to_dict() for r in results], indent=2))
    elif not args.quiet:
        print_results(results)

    # Exit with appropriate code
    found_count = sum(1 for r in results if r.status in ("found", "downloaded"))
    if found_count == 0:
        sys.exit(1)
    elif found_count < len(results):
        sys.exit(2)  # Partial success
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
