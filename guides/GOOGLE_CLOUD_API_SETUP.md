# Google Cloud API Setup Guide

A step-by-step guide for enabling Gmail API and Google Drive API access for Treehouse LLC automation projects.

**Time required:** 15-20 minutes
**Difficulty:** Beginner-friendly
**Browser:** Chrome recommended

---

## Table of Contents

1. [Create Google Cloud Project](#1-create-google-cloud-project)
2. [Enable APIs](#2-enable-apis)
3. [Configure OAuth Consent Screen](#3-configure-oauth-consent-screen)
4. [Create OAuth2 Credentials](#4-create-oauth2-credentials)
5. [Download and Save Credentials](#5-download-and-save-credentials)
6. [Understanding Scopes](#6-understanding-scopes)
7. [Local Setup](#7-local-setup)
8. [First-Time Authorization](#8-first-time-authorization)
9. [Security Best Practices](#9-security-best-practices)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Create Google Cloud Project

### Step 1.1: Open Google Cloud Console

1. Open Chrome browser
2. Go to: **https://console.cloud.google.com/**
3. Sign in with your Google account (if not already signed in)

### Step 1.2: Create New Project

1. Look at the top-left of the page, next to "Google Cloud"
2. Click on the **project dropdown** (it may say "Select a project" or show an existing project name)
3. In the popup window, click **"NEW PROJECT"** button (top-right of the popup)

### Step 1.3: Configure Project Details

Fill in the following:

| Field | Value |
|-------|-------|
| **Project name** | `treehouse-automation` |
| **Organization** | Leave as "No organization" (for personal accounts) |
| **Location** | Leave as default |

4. Click **"CREATE"** button
5. Wait 10-30 seconds for the project to be created
6. You will see a notification in the top-right when complete

### Step 1.4: Select Your New Project

1. Click the **notification bell** icon (top-right) and click "SELECT PROJECT"

   **OR**

2. Click the project dropdown again and select **"treehouse-automation"**

**Verify:** The project dropdown should now display "treehouse-automation"

---

## 2. Enable APIs

You need to enable two APIs: Gmail API and Google Drive API.

### Step 2.1: Navigate to API Library

1. Click the **hamburger menu** (three horizontal lines, top-left)
2. Scroll down and click **"APIs & Services"**
3. Click **"Library"**

**Direct URL:** https://console.cloud.google.com/apis/library?project=treehouse-automation

### Step 2.2: Enable Gmail API

1. In the search bar, type: `Gmail API`
2. Click on **"Gmail API"** (by Google) in the results
3. Click the blue **"ENABLE"** button
4. Wait for the API to be enabled (you will be redirected to the API dashboard)

### Step 2.3: Enable Google Drive API

1. Click **"APIs & Services"** in the left sidebar
2. Click **"Library"**
3. In the search bar, type: `Google Drive API`
4. Click on **"Google Drive API"** (by Google) in the results
5. Click the blue **"ENABLE"** button
6. Wait for the API to be enabled

### Step 2.4: Verify APIs are Enabled

1. Go to **"APIs & Services"** > **"Enabled APIs & services"**
2. You should see both APIs listed:
   - Gmail API
   - Google Drive API

**Direct URL:** https://console.cloud.google.com/apis/dashboard?project=treehouse-automation

---

## 3. Configure OAuth Consent Screen

Before creating credentials, you must configure the OAuth consent screen. This defines what users see when authorizing your application.

### Step 3.1: Navigate to OAuth Consent Screen

1. In the left sidebar, click **"APIs & Services"**
2. Click **"OAuth consent screen"**

**Direct URL:** https://console.cloud.google.com/apis/credentials/consent?project=treehouse-automation

### Step 3.2: Choose User Type

You will see two options:

| Type | Description | When to Use |
|------|-------------|-------------|
| **Internal** | Only available for Google Workspace accounts | If you have a business Google Workspace account |
| **External** | Available to any Google account | For personal Gmail accounts |

**For most users:** Select **"External"** and click **"CREATE"**

### Step 3.3: App Information

Fill in the following fields:

| Field | Value |
|-------|-------|
| **App name** | `Treehouse Automation` |
| **User support email** | Your email address |
| **App logo** | Skip (leave empty) |

### Step 3.4: App Domain (Optional)

Leave all fields in this section **empty**:
- Application home page
- Application privacy policy link
- Application terms of service link

### Step 3.5: Developer Contact Information

| Field | Value |
|-------|-------|
| **Email addresses** | Your email address |

Click **"SAVE AND CONTINUE"**

### Step 3.6: Scopes Configuration

1. Click **"ADD OR REMOVE SCOPES"**
2. In the search/filter box, search for each scope and check the box:

   **Gmail scope:**
   - Search: `gmail.readonly`
   - Check: `https://www.googleapis.com/auth/gmail.readonly`

   **Drive scope:**
   - Search: `drive.file`
   - Check: `https://www.googleapis.com/auth/drive.file`

3. Click **"UPDATE"** at the bottom of the scope list
4. Click **"SAVE AND CONTINUE"**

### Step 3.7: Test Users

Since this is an "External" app in testing mode, you must add test users:

1. Click **"+ ADD USERS"**
2. Enter your Google email address
3. Click **"ADD"**
4. Click **"SAVE AND CONTINUE"**

### Step 3.8: Summary

1. Review your configuration
2. Click **"BACK TO DASHBOARD"**

**Note:** Your app will remain in "Testing" mode, which is fine for personal automation. Only test users (you) can authorize the app.

---

## 4. Create OAuth2 Credentials

Now create the actual credentials your application will use.

### Step 4.1: Navigate to Credentials

1. In the left sidebar, click **"APIs & Services"**
2. Click **"Credentials"**

**Direct URL:** https://console.cloud.google.com/apis/credentials?project=treehouse-automation

### Step 4.2: Create OAuth Client ID

1. Click **"+ CREATE CREDENTIALS"** (top of page)
2. Select **"OAuth client ID"**

### Step 4.3: Configure Application Type

| Field | Value |
|-------|-------|
| **Application type** | `Desktop app` |
| **Name** | `Treehouse Desktop Client` |

3. Click **"CREATE"**

### Step 4.4: Credentials Created

A popup will appear with:
- **Your Client ID** (long string ending in `.apps.googleusercontent.com`)
- **Your Client Secret** (shorter string)

**Important:** Click **"DOWNLOAD JSON"** to save your credentials file.

Click **"OK"** to close the popup.

---

## 5. Download and Save Credentials

### Step 5.1: Locate Downloaded File

The file will be in your Downloads folder with a name like:
```
client_secret_XXXXX.apps.googleusercontent.com.json
```

### Step 5.2: Rename and Move the File

1. Rename the file to: `credentials.json`
2. Create a secure location for the file:

**On Mac/Linux:**
```bash
mkdir -p ~/.config/treehouse
mv ~/Downloads/client_secret_*.json ~/.config/treehouse/credentials.json
```

**On Windows:**
```cmd
mkdir %USERPROFILE%\.config\treehouse
move %USERPROFILE%\Downloads\client_secret_*.json %USERPROFILE%\.config\treehouse\credentials.json
```

### Step 5.3: Verify File Location

The credentials file should now be at:
- **Mac/Linux:** `~/.config/treehouse/credentials.json`
- **Windows:** `C:\Users\YourName\.config\treehouse\credentials.json`

---

## 6. Understanding Scopes

Scopes define what permissions your application has. Here are the scopes we configured:

### gmail.readonly

**Full scope URL:** `https://www.googleapis.com/auth/gmail.readonly`

| What it CAN do | What it CANNOT do |
|----------------|-------------------|
| Read email messages | Send emails |
| Read email metadata (subject, from, to, date) | Delete emails |
| Search emails | Modify emails |
| List emails and threads | Create drafts |
| Access labels | Manage settings |

**Use case:** Reading confirmation emails, extracting information from receipts, monitoring for specific messages.

### drive.file

**Full scope URL:** `https://www.googleapis.com/auth/drive.file`

| What it CAN do | What it CANNOT do |
|----------------|-------------------|
| Create new files | Access existing files it did not create |
| Read files the app created | Delete files it did not create |
| Edit files the app created | Access shared drives |
| Organize files the app created | See your entire Drive |

**Use case:** Creating reports, saving processed documents, generating spreadsheets. This is the most privacy-respecting Drive scope.

### Why These Scopes?

These scopes follow the **principle of least privilege**:
- `gmail.readonly` gives read-only access (safer than full access)
- `drive.file` only accesses files your app creates (cannot see other files)

---

## 7. Local Setup

### Step 7.1: Set Environment Variables

Your application needs to know where to find the credentials.

**On Mac/Linux (add to ~/.bashrc or ~/.zshrc):**
```bash
# Google Cloud credentials for Treehouse automation
export GOOGLE_APPLICATION_CREDENTIALS="$HOME/.config/treehouse/credentials.json"
export TREEHOUSE_CREDENTIALS_PATH="$HOME/.config/treehouse/credentials.json"
export TREEHOUSE_TOKEN_PATH="$HOME/.config/treehouse/token.json"
```

After adding, reload your shell:
```bash
source ~/.bashrc  # or source ~/.zshrc
```

**On Windows (PowerShell - run as Administrator):**
```powershell
[Environment]::SetEnvironmentVariable("GOOGLE_APPLICATION_CREDENTIALS", "$env:USERPROFILE\.config\treehouse\credentials.json", "User")
[Environment]::SetEnvironmentVariable("TREEHOUSE_CREDENTIALS_PATH", "$env:USERPROFILE\.config\treehouse\credentials.json", "User")
[Environment]::SetEnvironmentVariable("TREEHOUSE_TOKEN_PATH", "$env:USERPROFILE\.config\treehouse\token.json", "User")
```

### Step 7.2: Install Python Google Libraries

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

### Step 7.3: Verify Installation

```bash
python -c "from google.oauth2.credentials import Credentials; print('Google libraries installed successfully')"
```

---

## 8. First-Time Authorization

The first time your application runs, it needs to complete an OAuth flow.

### What Happens

1. Your application reads `credentials.json`
2. A browser window opens automatically
3. You see Google's consent screen asking to authorize "Treehouse Automation"
4. You click "Allow"
5. A `token.json` file is created (contains your access/refresh tokens)
6. Future runs use `token.json` (no browser needed)

### Sample Authorization Code

Here is a Python example to test the authorization flow:

```python
#!/usr/bin/env python3
"""Test Google API authorization flow."""

import os
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Scopes for Gmail read and Drive file access
SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/drive.file'
]

# Paths (use environment variables or defaults)
CREDENTIALS_PATH = os.environ.get(
    'TREEHOUSE_CREDENTIALS_PATH',
    os.path.expanduser('~/.config/treehouse/credentials.json')
)
TOKEN_PATH = os.environ.get(
    'TREEHOUSE_TOKEN_PATH',
    os.path.expanduser('~/.config/treehouse/token.json')
)

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
            # Run full authorization flow
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

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
```

Save this as `test_google_auth.py` and run:
```bash
python test_google_auth.py
```

### During First Run

1. Chrome will open with Google sign-in
2. Select your Google account
3. You may see a warning: "Google hasn't verified this app"
   - Click **"Advanced"**
   - Click **"Go to Treehouse Automation (unsafe)"**
4. Review permissions and click **"Allow"**
5. You can close the browser window
6. Check terminal for success message

---

## 9. Security Best Practices

### Never Commit Credentials to Git

Add these lines to your `.gitignore`:

```gitignore
# Google API credentials - NEVER commit these
credentials.json
token.json
client_secret*.json
*_credentials.json

# Config directory (may contain secrets)
.config/
```

### Protect Your Files

**On Mac/Linux:**
```bash
chmod 600 ~/.config/treehouse/credentials.json
chmod 600 ~/.config/treehouse/token.json
```

### Token Refresh Handling

- Access tokens expire after 1 hour
- The Google client library automatically refreshes tokens using the refresh token
- Refresh tokens do not expire unless revoked
- Your code should handle `google.auth.exceptions.RefreshError` for revoked tokens

### Revoking Access

If you need to revoke access (security concern, testing, etc.):

**Method 1: Google Account Settings**
1. Go to: https://myaccount.google.com/permissions
2. Find "Treehouse Automation"
3. Click on it
4. Click **"Remove Access"**

**Method 2: Delete Token File**
```bash
rm ~/.config/treehouse/token.json
```
Next run will require re-authorization.

**Method 3: Google Cloud Console**
1. Go to Credentials page
2. Delete the OAuth 2.0 Client ID
3. Create a new one if needed

### Credential Rotation

For enhanced security, periodically:
1. Delete existing OAuth credentials in Google Cloud Console
2. Create new credentials
3. Download new `credentials.json`
4. Delete old `token.json`
5. Re-authorize

---

## 10. Troubleshooting

### Error: "Access blocked: Authorization Error"

**Cause:** App not in testing mode or user not added as test user.

**Fix:**
1. Go to OAuth consent screen in Cloud Console
2. Ensure app is in "Testing" status
3. Add your email as a test user

### Error: "redirect_uri_mismatch"

**Cause:** Application type mismatch.

**Fix:**
1. Delete existing credentials
2. Create new OAuth client ID
3. Select "Desktop app" as application type

### Error: "invalid_client"

**Cause:** Corrupted or wrong credentials file.

**Fix:**
1. Re-download credentials.json from Cloud Console
2. Ensure no extra characters/formatting in file
3. Delete token.json and re-authorize

### Error: "Access Not Configured"

**Cause:** API not enabled for project.

**Fix:**
1. Go to API Library
2. Search for the API (Gmail or Drive)
3. Click Enable

### Browser Does Not Open

**Cause:** Running in headless environment or port blocked.

**Fix for headless:**
```python
# Use console-based flow instead
flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
creds = flow.run_console()  # Instead of run_local_server()
```

### Error: "Quota exceeded"

**Cause:** Too many API requests.

**Default quotas:**
- Gmail API: 1 billion quota units/day
- Drive API: 1 billion quota units/day

For personal use, you will not hit these limits.

---

## Quick Reference

### Important URLs

| Purpose | URL |
|---------|-----|
| Cloud Console | https://console.cloud.google.com/ |
| API Library | https://console.cloud.google.com/apis/library |
| Credentials | https://console.cloud.google.com/apis/credentials |
| OAuth Consent | https://console.cloud.google.com/apis/credentials/consent |
| Revoke Access | https://myaccount.google.com/permissions |

### File Locations

| File | Purpose | Location |
|------|---------|----------|
| `credentials.json` | OAuth client ID/secret | `~/.config/treehouse/credentials.json` |
| `token.json` | Access/refresh tokens | `~/.config/treehouse/token.json` |

### Environment Variables

| Variable | Purpose |
|----------|---------|
| `GOOGLE_APPLICATION_CREDENTIALS` | Standard Google Cloud credential path |
| `TREEHOUSE_CREDENTIALS_PATH` | Path to credentials.json |
| `TREEHOUSE_TOKEN_PATH` | Path to token.json |

### Scopes Summary

| Scope | Allows |
|-------|--------|
| `gmail.readonly` | Read emails (no send/delete) |
| `drive.file` | Create/edit app-created files only |

---

## Next Steps

After completing this setup:

1. Test authorization with the sample script
2. Integrate with your automation scripts
3. Review the [Gmail API documentation](https://developers.google.com/gmail/api)
4. Review the [Drive API documentation](https://developers.google.com/drive/api)

---

*Last updated: January 2026*
*For: Treehouse LLC Property Management Automation*
