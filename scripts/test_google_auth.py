#!/usr/bin/env python3
"""Test Google API authorization flow."""

import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Scopes for Gmail read and Drive file access
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.file'
]

# Paths
CREDENTIALS_PATH = os.path.expanduser('~/.config/treehouse/credentials.json')
TOKEN_PATH = os.path.expanduser('~/.config/treehouse/token.json')

def get_credentials():
    """Get or refresh Google API credentials."""
    creds = None

    # Load existing token if available
    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    # If no valid credentials, run authorization flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh expired token
            creds.refresh(Request())
        else:
            # Run authorization flow - try local server first, fall back to console
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            try:
                creds = flow.run_local_server(port=0, open_browser=False)
            except Exception:
                # Fall back to console-based flow
                creds = flow.run_console()

        # Save credentials for next run
        os.makedirs(os.path.dirname(TOKEN_PATH), exist_ok=True)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())

    return creds

def test_gmail(creds):
    """Test Gmail API access."""
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().labels().list(userId='me').execute()
    labels = results.get('labels', [])
    print(f"Gmail API: Found {len(labels)} labels")
    return True

def test_drive(creds):
    """Test Drive API access."""
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(pageSize=10).execute()
    files = results.get('files', [])
    print(f"Drive API: Access confirmed (found {len(files)} app-created files)")
    return True

if __name__ == '__main__':
    print("Testing Google API Authorization...")
    print(f"Credentials file: {CREDENTIALS_PATH}")
    print(f"Token file: {TOKEN_PATH}")
    print()

    try:
        creds = get_credentials()
        print("Authorization successful!")
        print()
        test_gmail(creds)
        test_drive(creds)
        print()
        print("All APIs working correctly!")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
