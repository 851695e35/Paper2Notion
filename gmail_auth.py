import json
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
    # Force consent screen to get refresh_token
    creds = flow.run_local_server(port=8080, open_browser=True, prompt='consent')

    # Save token for future use (as JSON)
    token_data = json.loads(creds.to_json())
    with open(GMAIL_TOKEN_FILE, 'w') as token_file:
        json.dump(token_data, token_file, indent=2)
    print(f"[OK] Credentials saved to {GMAIL_TOKEN_FILE}")
    return creds

def get_gmail_service():
    """Authenticate and return Gmail service (no browser interaction needed after setup)."""
    creds = None

    # Load existing token
    if os.path.exists(GMAIL_TOKEN_FILE):
        try:
            with open(GMAIL_TOKEN_FILE, 'r') as token_file:
                token_data = json.load(token_file)
                creds = Credentials.from_authorized_user_info(token_data, SCOPES)
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Error loading token file: {e}")
            print("Token file may be corrupted. Please re-authenticate.")
            creds = None

    # Refresh expired token
    if creds and creds.expired and creds.refresh_token:
        print("Token expired, refreshing...")
        try:
            creds.refresh(Request())
            # Save refreshed token
            token_data = json.loads(creds.to_json())
            with open(GMAIL_TOKEN_FILE, 'w') as token_file:
                json.dump(token_data, token_file, indent=2)
            print("[OK] Token refreshed and saved")
        except Exception as e:
            print(f"Failed to refresh token: {e}")
            print("Please run: python setup_gmail.py")
            raise
    elif not creds or not creds.valid or not getattr(creds, 'refresh_token', None):
        print(f"No valid credentials found. Please re-authenticate:")
        print("python setup_gmail.py")
        raise ValueError("Gmail credentials not found. Run setup_gmail.py first.")

    from googleapiclient.discovery import build
    return build('gmail', 'v1', credentials=creds)
