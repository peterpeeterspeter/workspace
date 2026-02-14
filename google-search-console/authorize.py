#!/usr/bin/env python3
"""
OAuth 2.0 Authorization Flow for Google Search Console API
Run this first to authorize the application
"""

import os
from pathlib import Path

try:
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    import google.oauth2.credentials
except ImportError:
    print("❌ Missing required packages")
    print("Run: pip install -r requirements.txt")
    exit(1)

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

def authorize():
    """Run OAuth flow and save credentials"""
    
    creds_file = Path('credentials.json')
    
    if not creds_file.exists():
        print("❌ credentials.json not found")
        print("\n📋 Setup Instructions:")
        print("1. Go to: https://console.cloud.google.com/")
        print("2. Create project or use existing")
        print("3. Enable Search Console API")
        print("4. Create OAuth 2.0 Client ID (Web application)")
        print("5. Add http://localhost:8080 to authorized URIs")
        print("6. Download credentials.json to this directory")
        return False
    
    print("🔐 Google Search Console API Authorization")
    print("=" * 50)
    print("\nOpening browser for authorization...\n")
    
    try:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json',
            SCOPES
        )
        
        # Use console flow for headless server environment
        creds = flow.run_console(
            authorization_prompt_message='Please visit this URL to authorize the application:\n{url}\n\n'
        )
        
        # Save credentials for future use
        with open('token.json', 'w') as token:
            token.write(creds.json)
        
        print("\n✅ Authorization successful!")
        print("📁 Token saved to: token.json")
        print("\nYou can now run: python setup.py")
        return True
        
    except Exception as e:
        print(f"\n❌ Authorization failed: {e}")
        print("\nTroubleshooting:")
        print("1. Verify credentials.json is valid")
        print("2. Check that Search Console API is enabled")
        print("3. Ensure OAuth consent screen is configured")
        return False

if __name__ == '__main__':
    success = authorize()
    exit(0 if success else 1)
