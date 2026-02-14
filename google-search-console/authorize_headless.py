#!/usr/bin/env python3
"""
OAuth 2.0 Authorization Flow for Google Search Console API (Headless)
Generates authorization URL and waits for manual callback
"""

import json
import urllib.parse
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

try:
    from google_auth_oauthlib.flow import Flow
    from google.auth.transport.requests import Request
except ImportError:
    print("❌ Missing required packages")
    print("Run: pip install -r requirements.txt")
    exit(1)

SCOPES = ['https://www.googleapis.com/auth/webmasters.readonly']

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/?code='):
            # Extract authorization code
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
            code = params.get('code', [None])[0]

            if code:
                self.server.auth_code = code
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(b'<h1>Authorization successful! You can close this window.</h1>')
                print("\n✅ Authorization code received!")
                return

        self.send_response(400)
        self.end_headers()

    def log_message(self, format, *args):
        pass  # Suppress logs

def authorize():
    """Run OAuth flow in headless mode"""

    creds_file = Path('credentials.json')

    if not creds_file.exists():
        print("❌ credentials.json not found")
        return False

    print("🔐 Google Search Console API Authorization (Headless)")
    print("=" * 60)

    try:
        # Create flow
        flow = Flow.from_client_secrets_file(
            'credentials.json',
            scopes=SCOPES
        )

        # Set redirect URI
        flow.redirect_uri = 'http://localhost:8080'

        # Generate authorization URL
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )

        print("\n📋 Step 1: Visit this URL to authorize:\n")
        print(auth_url)
        print("\n" + "=" * 60)

        # Start local server to receive callback
        print("\n📋 Step 2: Starting local server on port 8080...")
        server = HTTPServer(('localhost', 8080), CallbackHandler)
        server.auth_code = None
        server_thread = threading.Thread(target=server.handle_request)
        server_thread.daemon = True
        server_thread.start()

        print("⏳ Waiting for authorization callback...")

        # Wait for callback (max 5 minutes)
        for i in range(300):
            time.sleep(1)
            if hasattr(server, 'auth_code') and server.auth_code:
                break
            if i % 10 == 0:
                print(f"⏳ Still waiting... ({i//10}/30)")

        # Exchange code for credentials
        if hasattr(server, 'auth_code') and server.auth_code:
            print("\n📋 Step 3: Exchanging authorization code for tokens...")
            flow.fetch_token(code=server.auth_code)
            creds = flow.credentials

            # Save credentials
            with open('token.json', 'w') as token:
                token.write(creds.json)

            print("\n✅ Authorization successful!")
            print("📁 Token saved to: token.json")
            print("\nYou can now run: python setup.py")
            return True
        else:
            print("\n❌ Timeout - no authorization received within 5 minutes")
            return False

    except Exception as e:
        print(f"\n❌ Authorization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = authorize()
    exit(0 if success else 1)
