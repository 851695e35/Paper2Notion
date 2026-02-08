#!/usr/bin/env python3
"""
One-time setup script for Gmail authentication.
Run this once to authenticate and save your Gmail token.
"""

from gmail_auth import setup_gmail_credentials

if __name__ == "__main__":
    try:
        setup_gmail_credentials()
        print("\n[OK] Gmail authentication setup complete!")
        print("You can now run main.py without browser interaction.")
    except Exception as e:
        print(f"[ERROR] Setup failed: {e}")
        exit(1)
