import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from config import GMAIL_CREDENTIALS_FILE, GMAIL_TOKEN_FILE

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

def setup_gmail_credentials():
    """Initial setup - run this once to authenticate and save token."""
    print("Starting Gmail authentication setup...")
    flow = InstalledAppFlow.from_client_secrets_file(
        GMAIL_CREDENTIALS_FILE, SCOPES)
    creds = flow.run_local_server(port=8080, open_browser=True)

    # Save token for future use
    with open(GMAIL_TOKEN_FILE, 'wb') as token:
        pickle.dump(creds, token)
    print(f"[OK] Credentials saved to {GMAIL_TOKEN_FILE}")
    return creds

def get_gmail_service():
    """Authenticate and return Gmail service (no browser interaction needed after setup)."""
    creds = None

    # Load existing token
    if os.path.exists(GMAIL_TOKEN_FILE):
        with open(GMAIL_TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)

    # Refresh expired token
    if creds and creds.expired and creds.refresh_token:
        print("Token expired, refreshing...")
        try:
            creds.refresh(Request())
            # Save refreshed token
            with open(GMAIL_TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        except Exception as e:
            print(f"Failed to refresh token: {e}")
            print("Please run: python -c 'from gmail_auth import setup_gmail_credentials; setup_gmail_credentials()'")
            raise
    elif not creds or not creds.valid:
        print(f"No valid credentials found. Please run setup first:")
        print("python -c 'from gmail_auth import setup_gmail_credentials; setup_gmail_credentials()'")
        raise ValueError("Gmail credentials not found. Run setup_gmail_credentials() first.")

    from googleapiclient.discovery import build
    return build('gmail', 'v1', credentials=creds)
