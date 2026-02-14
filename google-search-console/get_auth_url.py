#!/usr/bin/env python3
"""
Generate Google Search Console OAuth URL (Manual Flow)
"""

import json
import urllib.parse

# Load credentials
with open('credentials.json', 'r') as f:
    creds = json.load(f)

web_creds = creds['web']
client_id = web_creds['client_id']
redirect_uri = 'http://localhost:8081'
scope = 'https://www.googleapis.com/auth/webmasters.readonly'

# Build authorization URL
params = {
    'client_id': client_id,
    'redirect_uri': redirect_uri,
    'scope': scope,
    'response_type': 'code',
    'access_type': 'offline',
    'include_granted_scopes': 'true'
}

auth_url = f"https://accounts.google.com/o/oauth2/auth?{urllib.parse.urlencode(params)}"

print("=" * 80)
print("GOOGLE SEARCH CONSOLE AUTHORIZATION URL")
print("=" * 80)
print("\n1. Visit this URL in your browser:\n")
print(auth_url)
print("\n2. Authorize the application")
print("3. Copy the 'code' parameter from the redirect URL")
print("4. Run: python exchange_code.py <code>")
print("\n" + "=" * 80)
