"""Gmail OAuth2 authentication module.

This module handles the OAuth2 authentication flow for accessing Gmail API.
It manages token storage, refresh, and provides authenticated credentials.
"""

import logging
import os
import pickle
from glob import glob
from typing import Optional

from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Load environment variables
load_dotenv()

# Gmail API scopes - modify read-only to full access if needed
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# File paths for credentials and tokens
TOKEN_FILE = os.getenv("TOKEN_FILE", "token.json")


def find_credentials_file() -> str:
    """Find the OAuth2 credentials file.

    Searches for credentials in the following order:
    1. CREDENTIALS_FILE environment variable
    2. Any client_secret*.json file in project root

    Returns:
        str: Path to credentials file

    Raises:
        FileNotFoundError: If no credentials file is found
    """
    # Check environment variable first
    env_creds = os.getenv("CREDENTIALS_FILE")
    if env_creds and os.path.exists(env_creds):
        return env_creds

    # Auto-detect client_secret*.json files in project root
    logging.info("Searching for OAuth2 credentials file...")
    cred_files = glob("client_secret*.json")
    if cred_files:
        return cred_files[0]  # Use the first match

    raise FileNotFoundError(
        "No OAuth2 credentials file found.\n"
        "Please download your credentials from Google Cloud Console and save as 'client_secret_*.json' in the project root.\n"
        "Alternatively, set CREDENTIALS_FILE environment variable."
    )


def get_credentials() -> Credentials:
    """Get valid Gmail API credentials.
    ref: https://developers.google.com/workspace/admin/directory/v1/quickstart/python?hl=en

    This function handles the complete OAuth2 flow:
    1. Loads existing credentials from token file if available
    2. Refreshes expired credentials if possible
    3. Initiates new OAuth flow if no valid credentials exist

    Returns:
        Credentials: Valid Google OAuth2 credentials

    Raises:
        FileNotFoundError: If credentials file doesn't exist
    """
    creds: Optional[Credentials] = None

    # Load existing credentials from token file
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            creds = pickle.load(token)

    # Check if credentials are valid or can be refreshed
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # Refresh expired credentials
            print("Refreshing expired credentials...")
            creds.refresh(Request())
        else:
            # No valid credentials - run OAuth flow
            # find_credentials_file() raises FileNotFoundError with helpful message if not found
            credentials_file = find_credentials_file()

            print("Starting OAuth2 authentication flow...")
            print("A browser window will open for you to authorize the application.")

            flow = InstalledAppFlow.from_client_secrets_file(credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)

            print("Authentication successful!")

        # Save credentials for future runs
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(creds, token)
            print(f"Credentials saved to {TOKEN_FILE}")

    return creds


def get_gmail_service():
    """Create and return an authenticated Gmail API service.

    Returns:
        googleapiclient.discovery.Resource: Authenticated Gmail API service
    """
    creds = get_credentials()
    service = build("gmail", "v1", credentials=creds)
    return service


def revoke_credentials() -> None:
    """Revoke stored credentials and delete token file.

    This is useful for testing or when you need to re-authenticate.
    """
    if os.path.exists(TOKEN_FILE):
        os.remove(TOKEN_FILE)
        print(f"Removed {TOKEN_FILE}")
    else:
        print(f"No token file found at {TOKEN_FILE}")
