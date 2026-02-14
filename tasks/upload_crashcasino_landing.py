#!/usr/bin/env python3
"""
Upload new landing page to crashcasino.io via WordPress REST API
"""

import json
import subprocess

# WordPress credentials
CRASHCASINO_URL = "https://crashcasino.io/wp-json"
CRASHCASINO_USER = "peter"
CRASHCASINO_PASS = "3vRhtTs2khfdLtTiDFqkdeXI"

# Read the HTML file
with open('/root/.openclaw/workspace/tasks/crashcasino-landing/standalone.html', 'r') as f:
    html_content = f.read()

# Update the home page (ID 309 is the homepage)
payload = {
    "title": "Is Crash Gambling Rigged? We Tested 50 Sites for Fairness",
    "content": html_content,
    "status": "publish"
}

print("Updating crashcasino.io homepage...")
print(f"URL: {CRASHCASINO_URL}")
print(f"Title: {payload['title']}")
print(f"Content length: {len(html_content)} characters")

curl_command = [
    'curl', '-s', '-X', 'POST',
    f"{CRASHCASINO_URL}/wp/v2/pages/309",
    '-u', f"{CRASHCASINO_USER}:{CRASHCASINO_PASS}",
    '-H', 'Content-Type: application/json',
    '-d', json.dumps(payload)
]

try:
    result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
    response = json.loads(result.stdout)

    if 'code' in response:
        print(f"\n❌ Error: {response['message']}")
        print(f"Details: {response}")
    else:
        print(f"\n✓ Success!")
        print(f"Page ID: {response.get('id')}")
        print(f"Title: {response.get('title', {}).get('rendered')}")
        print(f"Link: {response.get('link')}")

except subprocess.CalledProcessError as e:
    print(f"\n❌ Error executing curl: {e}")
    print(f"stderr: {e.stderr}")
except Exception as e:
    print(f"\n❌ Error: {e}")
