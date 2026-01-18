#!/usr/bin/env python3
"""
Google Drive Uploader for Treehouse Asset Manager

Upload files to Google Drive with proper organization, naming, and folder structure.

Usage:
    # Upload a single file
    python3 drive_uploader.py --file manual.pdf --folder "Dallas/Manuals" --asset-id "DAL-HVAC-01"

    # Upload with explicit doc type and date
    python3 drive_uploader.py --file hvac-guide.pdf --folder "Dallas/Manuals" \
        --asset-id "DAL-HVAC-01" --doc-type manual --date 2024-01-15

    # Batch upload from JSON
    python3 drive_uploader.py --batch uploads.json --create-folders

    # List folder structure
    python3 drive_uploader.py --list-folders

    # Setup initial folder structure
    python3 drive_uploader.py --setup

    # Dry run (preview without uploading)
    python3 drive_uploader.py --file manual.pdf --folder "Dallas/Manuals" --dry-run

Environment Variables:
    TREEHOUSE_TOKEN_PATH - Path to OAuth token (default: ~/.config/treehouse/token.json)
    TREEHOUSE_CREDENTIALS_PATH - Path to credentials (default: ~/.config/treehouse/credentials.json)

Credentials:
    Token path: ~/.config/treehouse/token.json
    Credentials path: ~/.config/treehouse/credentials.json
    Scope: drive.file
"""

import argparse
import json
import os
import sys
import hashlib
import mimetypes
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

try:
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
except ImportError:
    print("Error: Google API libraries required. Install with:")
    print("  pip install google-api-python-client google-auth-httplib2 google-auth-oauthlib")
    sys.exit(1)


# =============================================================================
# Configuration
# =============================================================================

# Default paths for credentials
DEFAULT_TOKEN_PATH = os.path.expanduser("~/.config/treehouse/token.json")
DEFAULT_CREDENTIALS_PATH = os.path.expanduser("~/.config/treehouse/credentials.json")

# Environment variable overrides
TOKEN_PATH = os.environ.get("TREEHOUSE_TOKEN_PATH", DEFAULT_TOKEN_PATH)
CREDENTIALS_PATH = os.environ.get("TREEHOUSE_CREDENTIALS_PATH", DEFAULT_CREDENTIALS_PATH)

# OAuth scopes - drive.file allows access to files created by this app
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

# Root folder name in Google Drive
ROOT_FOLDER_NAME = "Treehouse-Assets"

# Folder structure definition
FOLDER_STRUCTURE = {
    "Dallas": ["Manuals", "Warranties", "Receipts", "Service-Records"],
    "Austin-A": ["Manuals", "Warranties", "Receipts", "Service-Records"],
    "Austin-B": ["Manuals", "Warranties", "Receipts", "Service-Records"],
    "Austin-C": ["Manuals", "Warranties", "Receipts", "Service-Records"],
    "Treehouse-General": ["Insurance", "LLC-Documents", "Multi-Property"],
}

# Property code mapping (asset ID prefix -> folder name)
PROPERTY_MAP = {
    "DAL": "Dallas",
    "ATX-A": "Austin-A",
    "ATX-B": "Austin-B",
    "ATX-C": "Austin-C",
    "TH": "Treehouse-General",
}

# Document type to folder mapping
DOCTYPE_FOLDER_MAP = {
    "manual": "Manuals",
    "warranty": "Warranties",
    "receipt": "Receipts",
    "invoice": "Service-Records",
    "service": "Service-Records",
    "insurance": "Insurance",
    "llc": "LLC-Documents",
    "multi": "Multi-Property",
}

# Cache file for folder IDs
CACHE_PATH = os.path.expanduser("~/.config/treehouse/drive_cache.json")


# =============================================================================
# Google Drive Authentication
# =============================================================================

class DriveAuthError(Exception):
    """Error during Google Drive authentication."""
    pass


class DriveUploadError(Exception):
    """Error during file upload."""
    pass


def get_credentials() -> Credentials:
    """
    Get or create Google Drive API credentials.

    Returns:
        Credentials: Authenticated Google credentials

    Raises:
        DriveAuthError: If authentication fails
    """
    creds = None

    # Check for existing token
    if os.path.exists(TOKEN_PATH):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
        except Exception as e:
            print(f"Warning: Could not load existing token: {e}")

    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Warning: Could not refresh token: {e}")
                creds = None

        if not creds:
            if not os.path.exists(CREDENTIALS_PATH):
                raise DriveAuthError(
                    f"Credentials file not found: {CREDENTIALS_PATH}\n"
                    "Please download OAuth 2.0 credentials from Google Cloud Console\n"
                    "and save to this path."
                )

            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_PATH, SCOPES
                )
                creds = flow.run_local_server(port=0)
            except Exception as e:
                raise DriveAuthError(f"Authentication failed: {e}")

        # Save credentials for next run
        os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
        os.chmod(TOKEN_PATH, 0o600)  # Secure the token file

    return creds


def get_drive_service():
    """
    Get authenticated Google Drive service.

    Returns:
        Resource: Google Drive API service
    """
    creds = get_credentials()
    return build("drive", "v3", credentials=creds)


# =============================================================================
# Folder ID Cache
# =============================================================================

class FolderCache:
    """Cache for Google Drive folder IDs to improve performance."""

    def __init__(self, cache_path: str = CACHE_PATH):
        self.cache_path = cache_path
        self.cache: Dict[str, str] = {}
        self._load()

    def _load(self):
        """Load cache from disk."""
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, "r") as f:
                    self.cache = json.load(f)
            except (json.JSONDecodeError, IOError):
                self.cache = {}

    def _save(self):
        """Save cache to disk."""
        os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
        with open(self.cache_path, "w") as f:
            json.dump(self.cache, f, indent=2)

    def get(self, folder_path: str) -> Optional[str]:
        """Get folder ID from cache."""
        return self.cache.get(folder_path)

    def set(self, folder_path: str, folder_id: str):
        """Set folder ID in cache."""
        self.cache[folder_path] = folder_id
        self._save()

    def clear(self):
        """Clear the cache."""
        self.cache = {}
        if os.path.exists(self.cache_path):
            os.remove(self.cache_path)


# =============================================================================
# Drive Operations
# =============================================================================

class DriveUploader:
    """Google Drive uploader with folder management and caching."""

    def __init__(self, dry_run: bool = False):
        """
        Initialize the uploader.

        Args:
            dry_run: If True, don't actually upload (preview mode)
        """
        self.dry_run = dry_run
        self.service = None
        self.cache = FolderCache()
        self._root_id: Optional[str] = None

    def _get_service(self):
        """Get or create the Drive service."""
        if self.service is None:
            self.service = get_drive_service()
        return self.service

    def _find_folder(self, name: str, parent_id: Optional[str] = None) -> Optional[str]:
        """
        Find a folder by name, optionally within a parent.

        Args:
            name: Folder name to find
            parent_id: Parent folder ID (None for root)

        Returns:
            str or None: Folder ID if found
        """
        service = self._get_service()

        query = f"name = '{name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
        if parent_id:
            query += f" and '{parent_id}' in parents"

        try:
            results = service.files().list(
                q=query,
                spaces="drive",
                fields="files(id, name)",
                pageSize=10
            ).execute()

            files = results.get("files", [])
            if files:
                return files[0]["id"]
        except HttpError as e:
            print(f"Error finding folder '{name}': {e}")

        return None

    def _create_folder(self, name: str, parent_id: Optional[str] = None) -> str:
        """
        Create a folder in Google Drive.

        Args:
            name: Folder name
            parent_id: Parent folder ID (None for root)

        Returns:
            str: Created folder ID
        """
        if self.dry_run:
            print(f"  [DRY RUN] Would create folder: {name}")
            return f"dry-run-{name}"

        service = self._get_service()

        file_metadata = {
            "name": name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_id:
            file_metadata["parents"] = [parent_id]

        try:
            folder = service.files().create(
                body=file_metadata,
                fields="id"
            ).execute()
            return folder["id"]
        except HttpError as e:
            raise DriveUploadError(f"Failed to create folder '{name}': {e}")

    def _get_or_create_folder(self, name: str, parent_id: Optional[str] = None) -> str:
        """
        Get existing folder or create if it doesn't exist.

        Args:
            name: Folder name
            parent_id: Parent folder ID

        Returns:
            str: Folder ID
        """
        folder_id = self._find_folder(name, parent_id)
        if folder_id:
            return folder_id
        return self._create_folder(name, parent_id)

    def get_root_folder_id(self) -> str:
        """
        Get or create the root Treehouse-Assets folder.

        Returns:
            str: Root folder ID
        """
        if self._root_id:
            return self._root_id

        # Check cache first
        cached_id = self.cache.get(ROOT_FOLDER_NAME)
        if cached_id:
            # Verify it still exists
            if not self.dry_run:
                service = self._get_service()
                try:
                    service.files().get(fileId=cached_id, fields="id").execute()
                    self._root_id = cached_id
                    return cached_id
                except HttpError:
                    # Folder was deleted, clear cache entry
                    pass

        # Find or create root folder
        self._root_id = self._get_or_create_folder(ROOT_FOLDER_NAME)
        if not self.dry_run:
            self.cache.set(ROOT_FOLDER_NAME, self._root_id)

        return self._root_id

    def get_folder_id(self, folder_path: str, create: bool = True) -> str:
        """
        Get folder ID for a path like "Dallas/Manuals".

        Args:
            folder_path: Path relative to Treehouse-Assets (e.g., "Dallas/Manuals")
            create: If True, create folders that don't exist

        Returns:
            str: Folder ID
        """
        # Check cache first
        full_path = f"{ROOT_FOLDER_NAME}/{folder_path}"
        cached_id = self.cache.get(full_path)
        if cached_id and not self.dry_run:
            # Verify it still exists
            service = self._get_service()
            try:
                service.files().get(fileId=cached_id, fields="id").execute()
                return cached_id
            except HttpError:
                pass

        # Navigate/create folder hierarchy
        parent_id = self.get_root_folder_id()
        parts = folder_path.strip("/").split("/")

        for part in parts:
            if create:
                folder_id = self._get_or_create_folder(part, parent_id)
            else:
                folder_id = self._find_folder(part, parent_id)
                if not folder_id:
                    raise DriveUploadError(f"Folder not found: {part} in {folder_path}")
            parent_id = folder_id

        # Cache the result
        if not self.dry_run:
            self.cache.set(full_path, parent_id)

        return parent_id

    def check_duplicate(self, filename: str, folder_id: str) -> Optional[Dict[str, str]]:
        """
        Check if a file with the same name exists in the folder.

        Args:
            filename: File name to check
            folder_id: Folder ID to check in

        Returns:
            dict or None: File info if duplicate exists, None otherwise
        """
        if self.dry_run:
            return None

        service = self._get_service()

        query = (
            f"name = '{filename}' and "
            f"'{folder_id}' in parents and "
            f"trashed = false"
        )

        try:
            results = service.files().list(
                q=query,
                spaces="drive",
                fields="files(id, name, webViewLink, md5Checksum)",
                pageSize=1
            ).execute()

            files = results.get("files", [])
            if files:
                return {
                    "id": files[0]["id"],
                    "name": files[0]["name"],
                    "url": files[0].get("webViewLink", ""),
                    "md5": files[0].get("md5Checksum", ""),
                }
        except HttpError as e:
            print(f"Warning: Error checking for duplicates: {e}")

        return None

    def get_file_md5(self, file_path: str) -> str:
        """Calculate MD5 hash of a local file."""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def upload_file(
        self,
        local_path: str,
        drive_folder: str,
        filename: Optional[str] = None,
        asset_id: Optional[str] = None,
        doc_type: Optional[str] = None,
        date: Optional[str] = None,
        skip_duplicates: bool = True
    ) -> Dict[str, Any]:
        """
        Upload a file to Google Drive.

        Args:
            local_path: Path to local file
            drive_folder: Drive folder path (e.g., "Dallas/Manuals")
            filename: Optional custom filename (otherwise generates from conventions)
            asset_id: Asset ID for naming convention
            doc_type: Document type for naming convention
            date: Date for naming convention (YYYY-MM-DD)
            skip_duplicates: If True, skip if identical file exists

        Returns:
            dict: UploadResult with status, drive_id, drive_url, etc.
        """
        result = {
            "local_path": local_path,
            "drive_id": None,
            "drive_url": None,
            "folder_path": drive_folder,
            "status": "pending",
            "message": "",
        }

        # Validate local file exists
        if not os.path.exists(local_path):
            result["status"] = "failed"
            result["message"] = f"Local file not found: {local_path}"
            return result

        # Generate filename if not provided
        if not filename:
            filename = self._generate_filename(local_path, asset_id, doc_type, date)

        result["filename"] = filename

        # Get folder ID
        try:
            folder_id = self.get_folder_id(drive_folder, create=True)
        except DriveUploadError as e:
            result["status"] = "failed"
            result["message"] = str(e)
            return result

        # Check for duplicates
        if skip_duplicates:
            existing = self.check_duplicate(filename, folder_id)
            if existing:
                # Check if content is identical
                if existing.get("md5"):
                    local_md5 = self.get_file_md5(local_path)
                    if local_md5 == existing["md5"]:
                        result["status"] = "exists"
                        result["drive_id"] = existing["id"]
                        result["drive_url"] = existing["url"]
                        result["message"] = "Identical file already exists"
                        return result

                # File exists but content differs
                result["status"] = "exists"
                result["drive_id"] = existing["id"]
                result["drive_url"] = existing["url"]
                result["message"] = "File with same name exists (content may differ)"
                return result

        # Dry run mode
        if self.dry_run:
            result["status"] = "dry_run"
            result["message"] = f"Would upload {filename} to {drive_folder}"
            print(f"  [DRY RUN] Would upload: {local_path} -> {drive_folder}/{filename}")
            return result

        # Perform upload
        service = self._get_service()

        # Detect MIME type
        mime_type, _ = mimetypes.guess_type(local_path)
        if not mime_type:
            mime_type = "application/octet-stream"

        file_metadata = {
            "name": filename,
            "parents": [folder_id],
        }

        try:
            media = MediaFileUpload(local_path, mimetype=mime_type, resumable=True)
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields="id, webViewLink"
            ).execute()

            result["status"] = "uploaded"
            result["drive_id"] = file["id"]
            result["drive_url"] = file.get("webViewLink", "")
            result["message"] = "Upload successful"

        except HttpError as e:
            result["status"] = "failed"
            result["message"] = f"Upload failed: {e}"

        return result

    def _generate_filename(
        self,
        local_path: str,
        asset_id: Optional[str] = None,
        doc_type: Optional[str] = None,
        date: Optional[str] = None
    ) -> str:
        """
        Generate a filename following naming conventions.

        Format: {asset_id}_{doc_type}_{date}.{ext}
        """
        # Get extension from original file
        _, ext = os.path.splitext(local_path)
        ext = ext.lower()

        # Use current date if not provided
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        # If we have asset_id and doc_type, use convention
        if asset_id and doc_type:
            return f"{asset_id}_{doc_type}_{date}{ext}"

        # Otherwise, use original filename
        return os.path.basename(local_path)

    def batch_upload(
        self,
        requests: List[Dict[str, Any]],
        create_folders: bool = True
    ) -> List[Dict[str, Any]]:
        """
        Upload multiple files from a list of upload requests.

        Args:
            requests: List of UploadRequest dicts
            create_folders: If True, create folders that don't exist

        Returns:
            list: List of UploadResult dicts
        """
        results = []

        for i, req in enumerate(requests, 1):
            print(f"Processing {i}/{len(requests)}: {req.get('local_path', 'unknown')}")

            result = self.upload_file(
                local_path=req.get("local_path", ""),
                drive_folder=req.get("drive_folder", ""),
                filename=req.get("filename"),
                asset_id=req.get("asset_id"),
                doc_type=req.get("doc_type"),
            )
            results.append(result)

            # Print status
            status_icon = {
                "uploaded": "[OK]",
                "exists": "[SKIP]",
                "failed": "[FAIL]",
                "dry_run": "[DRY]",
            }.get(result["status"], "[?]")

            print(f"  {status_icon} {result.get('message', '')}")

        return results

    def setup_folder_structure(self) -> Dict[str, Any]:
        """
        Create the complete folder structure in Google Drive.

        Returns:
            dict: Report of created/existing folders
        """
        report = {
            "created": [],
            "existed": [],
            "errors": [],
        }

        print(f"Setting up folder structure under '{ROOT_FOLDER_NAME}'...")

        # Create root folder
        root_id = self.get_root_folder_id()
        if not self.dry_run:
            print(f"  Root folder: {ROOT_FOLDER_NAME}")

        # Create property folders and subfolders
        for property_name, subfolders in FOLDER_STRUCTURE.items():
            print(f"  Creating {property_name}/...")

            try:
                property_id = self._get_or_create_folder(property_name, root_id)

                # Check if it was just created or already existed
                full_path = f"{ROOT_FOLDER_NAME}/{property_name}"
                if self.cache.get(full_path):
                    report["existed"].append(full_path)
                else:
                    report["created"].append(full_path)
                    if not self.dry_run:
                        self.cache.set(full_path, property_id)

                # Create subfolders
                for subfolder in subfolders:
                    try:
                        subfolder_id = self._get_or_create_folder(subfolder, property_id)
                        subfolder_path = f"{full_path}/{subfolder}"

                        if self.cache.get(subfolder_path):
                            report["existed"].append(subfolder_path)
                        else:
                            report["created"].append(subfolder_path)
                            if not self.dry_run:
                                self.cache.set(subfolder_path, subfolder_id)

                        print(f"    {subfolder}/")

                    except DriveUploadError as e:
                        report["errors"].append(f"{property_name}/{subfolder}: {e}")
                        print(f"    [ERROR] {subfolder}: {e}")

            except DriveUploadError as e:
                report["errors"].append(f"{property_name}: {e}")
                print(f"  [ERROR] {property_name}: {e}")

        return report

    def list_folders(self, parent_path: str = "") -> List[Dict[str, str]]:
        """
        List all folders in the Drive structure.

        Args:
            parent_path: Path to list from (empty for root)

        Returns:
            list: List of folder info dicts
        """
        folders = []

        if self.dry_run:
            print("[DRY RUN] Cannot list folders without connecting to Drive")
            return folders

        service = self._get_service()

        # Get starting folder ID
        if parent_path:
            try:
                parent_id = self.get_folder_id(parent_path, create=False)
            except DriveUploadError:
                print(f"Folder not found: {parent_path}")
                return folders
        else:
            parent_id = self.get_root_folder_id()
            parent_path = ROOT_FOLDER_NAME

        def list_recursive(folder_id: str, path: str, depth: int = 0):
            """Recursively list folder contents."""
            query = (
                f"'{folder_id}' in parents and "
                f"mimeType = 'application/vnd.google-apps.folder' and "
                f"trashed = false"
            )

            try:
                results = service.files().list(
                    q=query,
                    spaces="drive",
                    fields="files(id, name)",
                    orderBy="name"
                ).execute()

                for file in results.get("files", []):
                    folder_path = f"{path}/{file['name']}"
                    folders.append({
                        "path": folder_path,
                        "id": file["id"],
                        "depth": depth,
                    })
                    # Recurse into subfolders
                    list_recursive(file["id"], folder_path, depth + 1)

            except HttpError as e:
                print(f"Error listing folder: {e}")

        # Add root to list
        folders.append({
            "path": parent_path,
            "id": parent_id,
            "depth": 0,
        })

        list_recursive(parent_id, parent_path, 1)

        return folders


# =============================================================================
# Utility Functions
# =============================================================================

def infer_folder_from_asset_id(asset_id: str, doc_type: str) -> Optional[str]:
    """
    Infer the Drive folder path from asset ID and document type.

    Args:
        asset_id: Asset ID (e.g., "DAL-HVAC-01")
        doc_type: Document type (e.g., "manual")

    Returns:
        str or None: Folder path (e.g., "Dallas/Manuals")
    """
    # Extract property code from asset ID
    parts = asset_id.upper().split("-")
    if len(parts) < 2:
        return None

    # Handle multi-part property codes (e.g., ATX-A)
    if parts[0] == "ATX" and len(parts) >= 2:
        property_code = f"{parts[0]}-{parts[1]}"
    else:
        property_code = parts[0]

    # Map to folder name
    property_folder = PROPERTY_MAP.get(property_code)
    if not property_folder:
        return None

    # Map doc type to subfolder
    doc_folder = DOCTYPE_FOLDER_MAP.get(doc_type.lower())
    if not doc_folder:
        doc_folder = "Manuals"  # Default

    return f"{property_folder}/{doc_folder}"


def parse_upload_request(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Parse and validate an upload request.

    Args:
        data: Raw upload request data

    Returns:
        dict: Validated upload request
    """
    request = {
        "local_path": data.get("local_path", ""),
        "drive_folder": data.get("drive_folder", ""),
        "filename": data.get("filename"),
        "asset_id": data.get("asset_id"),
        "doc_type": data.get("doc_type"),
    }

    # Infer drive_folder if not provided but asset_id and doc_type are
    if not request["drive_folder"] and request["asset_id"] and request["doc_type"]:
        request["drive_folder"] = infer_folder_from_asset_id(
            request["asset_id"],
            request["doc_type"]
        )

    return request


# =============================================================================
# CLI Interface
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Upload files to Google Drive for Treehouse Asset Manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Upload a single file
  python3 drive_uploader.py --file manual.pdf --folder "Dallas/Manuals" --asset-id "DAL-HVAC-01"

  # Upload with explicit doc type
  python3 drive_uploader.py --file receipt.pdf --folder "Dallas/Receipts" \\
      --asset-id "DAL-HVAC-01" --doc-type receipt

  # Batch upload from JSON
  python3 drive_uploader.py --batch uploads.json

  # List current folder structure
  python3 drive_uploader.py --list-folders

  # Create initial folder structure
  python3 drive_uploader.py --setup

  # Preview upload without actually uploading
  python3 drive_uploader.py --file manual.pdf --folder "Dallas/Manuals" --dry-run

Folder paths:
  Dallas/Manuals, Dallas/Warranties, Dallas/Receipts, Dallas/Service-Records
  Austin-A/Manuals, Austin-A/Warranties, Austin-A/Receipts, Austin-A/Service-Records
  Austin-B/Manuals, Austin-B/Warranties, Austin-B/Receipts, Austin-B/Service-Records
  Austin-C/Manuals, Austin-C/Warranties, Austin-C/Receipts, Austin-C/Service-Records
  Treehouse-General/Insurance, Treehouse-General/LLC-Documents, Treehouse-General/Multi-Property
        """
    )

    # Action arguments
    action_group = parser.add_mutually_exclusive_group(required=True)
    action_group.add_argument(
        "--file",
        metavar="PATH",
        help="Upload a single file"
    )
    action_group.add_argument(
        "--batch",
        metavar="JSON_FILE",
        help="Batch upload from JSON file"
    )
    action_group.add_argument(
        "--list-folders",
        action="store_true",
        help="List folder structure in Google Drive"
    )
    action_group.add_argument(
        "--setup",
        action="store_true",
        help="Create initial folder structure"
    )
    action_group.add_argument(
        "--clear-cache",
        action="store_true",
        help="Clear folder ID cache"
    )

    # Upload options
    parser.add_argument(
        "--folder",
        metavar="PATH",
        help="Drive folder path (e.g., 'Dallas/Manuals')"
    )
    parser.add_argument(
        "--asset-id",
        metavar="ID",
        help="Asset ID for naming convention (e.g., 'DAL-HVAC-01')"
    )
    parser.add_argument(
        "--doc-type",
        metavar="TYPE",
        choices=list(DOCTYPE_FOLDER_MAP.keys()),
        help="Document type (manual, warranty, receipt, invoice, service, insurance, llc, multi)"
    )
    parser.add_argument(
        "--date",
        metavar="YYYY-MM-DD",
        help="Date for filename (default: today)"
    )
    parser.add_argument(
        "--filename",
        metavar="NAME",
        help="Custom filename (overrides naming convention)"
    )

    # Batch options
    parser.add_argument(
        "--create-folders",
        action="store_true",
        help="Create folders if they don't exist (default for batch)"
    )

    # General options
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview actions without making changes"
    )
    parser.add_argument(
        "--output",
        "-o",
        metavar="FILE",
        help="Output results to JSON file"
    )
    parser.add_argument(
        "--quiet",
        "-q",
        action="store_true",
        help="Suppress progress output"
    )

    args = parser.parse_args()

    # Handle clear cache
    if args.clear_cache:
        cache = FolderCache()
        cache.clear()
        print("Folder ID cache cleared.")
        return

    # Create uploader instance
    uploader = DriveUploader(dry_run=args.dry_run)

    # Handle setup
    if args.setup:
        print("Setting up Google Drive folder structure...")
        if args.dry_run:
            print("[DRY RUN MODE]")
        report = uploader.setup_folder_structure()
        print(f"\nCreated: {len(report['created'])} folders")
        print(f"Existed: {len(report['existed'])} folders")
        if report["errors"]:
            print(f"Errors: {len(report['errors'])}")
            for err in report["errors"]:
                print(f"  - {err}")
        return

    # Handle list folders
    if args.list_folders:
        print("Listing Google Drive folder structure...\n")
        folders = uploader.list_folders()
        if folders:
            for folder in folders:
                indent = "  " * folder["depth"]
                name = folder["path"].split("/")[-1] if "/" in folder["path"] else folder["path"]
                print(f"{indent}{name}/")
            print(f"\nTotal: {len(folders)} folders")
        return

    # Handle single file upload
    if args.file:
        # Validate required arguments
        if not args.folder and not (args.asset_id and args.doc_type):
            parser.error("--folder is required, or both --asset-id and --doc-type to infer folder")

        # Infer folder if needed
        folder = args.folder
        if not folder and args.asset_id and args.doc_type:
            folder = infer_folder_from_asset_id(args.asset_id, args.doc_type)
            if not folder:
                parser.error(f"Could not infer folder from asset ID: {args.asset_id}")

        print(f"Uploading: {args.file}")
        print(f"To folder: {folder}")
        if args.dry_run:
            print("[DRY RUN MODE]")

        result = uploader.upload_file(
            local_path=args.file,
            drive_folder=folder,
            filename=args.filename,
            asset_id=args.asset_id,
            doc_type=args.doc_type,
            date=args.date,
        )

        # Print result
        print(f"\nStatus: {result['status']}")
        print(f"Message: {result['message']}")
        if result.get("drive_url"):
            print(f"Drive URL: {result['drive_url']}")
        if result.get("filename"):
            print(f"Filename: {result['filename']}")

        # Output to file if requested
        if args.output:
            with open(args.output, "w") as f:
                json.dump(result, f, indent=2)
            print(f"Results saved to: {args.output}")

        # Exit with error code if failed
        if result["status"] == "failed":
            sys.exit(1)

        return

    # Handle batch upload
    if args.batch:
        if not os.path.exists(args.batch):
            print(f"Error: Batch file not found: {args.batch}")
            sys.exit(1)

        with open(args.batch, "r") as f:
            try:
                batch_data = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error: Invalid JSON in batch file: {e}")
                sys.exit(1)

        # Handle both list and dict with "uploads" key
        if isinstance(batch_data, dict):
            uploads = batch_data.get("uploads", [])
        else:
            uploads = batch_data

        if not uploads:
            print("No uploads found in batch file.")
            return

        print(f"Processing {len(uploads)} uploads...")
        if args.dry_run:
            print("[DRY RUN MODE]")

        # Parse and validate requests
        requests = [parse_upload_request(u) for u in uploads]

        # Perform uploads
        results = uploader.batch_upload(requests, create_folders=args.create_folders)

        # Summary
        uploaded = sum(1 for r in results if r["status"] == "uploaded")
        skipped = sum(1 for r in results if r["status"] == "exists")
        failed = sum(1 for r in results if r["status"] == "failed")

        print(f"\nSummary:")
        print(f"  Uploaded: {uploaded}")
        print(f"  Skipped (exists): {skipped}")
        print(f"  Failed: {failed}")

        # Output to file if requested
        if args.output:
            with open(args.output, "w") as f:
                json.dump(results, f, indent=2)
            print(f"Results saved to: {args.output}")

        # Exit with error code if any failed
        if failed > 0:
            sys.exit(1)

        return


if __name__ == "__main__":
    main()
