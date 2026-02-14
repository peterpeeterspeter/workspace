#!/usr/bin/env python3
"""
Exchange OAuth authorization code for access token
"""

import json
import sys
import urllib.request
import urllib.parse

def exchange_code(auth_code):
    """Exchange authorization code for access token"""

    # Load credentials
    with open('credentials.json', 'r') as f:
        creds = json.load(f)

    web_creds = creds['web']

    # Prepare token exchange request
    token_url = 'https://oauth2.googleapis.com/token'
    data = {
        'code': auth_code,
        'client_id': web_creds['client_id'],
        'client_secret': web_creds['client_secret'],
        'redirect_uri': 'http://localhost:8081',
        'grant_type': 'authorization_code'
    }

    print("🔄 Exchanging authorization code for tokens...")

    try:
        req = urllib.request.Request(
            token_url,
            data=urllib.parse.urlencode(data).encode('utf-8'),
            method='POST'
        )

        with urllib.request.urlopen(req) as response:
            tokens = json.loads(response.read().decode('utf-8'))

        # Save tokens
        with open('token.json', 'w') as f:
            json.dump(tokens, f, indent=2)

        print("\n✅ Authorization successful!")
        print("📁 Token saved to: token.json")
        print(f"\nAccess Token: {tokens['access_token'][:20]}...")
        print(f"Refresh Token: {tokens.get('refresh_token', 'N/A')[:20]}...")
        print(f"Expires in: {tokens['expires_in']} seconds")
        print("\n✅ You can now run: python setup.py")

        return True

    except urllib.error.HTTPError as e:
        print(f"\n❌ Token exchange failed: {e.code}")
        error_response = e.read().decode('utf-8')
        print(f"Error: {error_response}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python exchange_code.py <authorization_code>")
        print("\nExample:")
        print("python exchange_code.py 4/0AeanS0...")
        sys.exit(1)

    auth_code = sys.argv[1]
    success = exchange_code(auth_code)
    sys.exit(0 if success else 1)
