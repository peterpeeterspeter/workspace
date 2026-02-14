#!/usr/bin/env python3
"""
Upload redesigned landing page to crashcasino.io
"""

import json
import subprocess

# Read the redesigned HTML
with open('/root/.openclaw/workspace/tasks/crashcasino-landing-redesigned.html', 'r') as f:
    html_content = f.read()

# Update crashcasino.io homepage
payload = {
    "title": "Is Crash Gambling Rigged? We Tested 50 Sites for Fairness",
    "content": html_content,
    "status": "publish"
}

print("Uploading redesigned landing page to crashcasino.io...")
print(f"HTML length: {len(html_content)} chars")
print()

curl_command = [
    'curl', '-s', '-X', 'POST',
    'https://crashcasino.io/wp-json/wp/v2/pages/309',
    '-u', 'peter:3vRhtTs2khfdLtTiDFqkdeXI',
    '-H', 'Content-Type: application/json',
    '-d', json.dumps(payload)
]

try:
    result = subprocess.run(curl_command, capture_output=True, text=True, check=True)
    response = json.loads(result.stdout)

    if 'code' in response:
        print(f"❌ Error: {response['message']}")
        print(f"Details: {response}")
    else:
        print("✅ SUCCESS!")
        print(f"   Page ID: {response.get('id')}")
        print(f"   URL: {response.get('link')}")
        print()
        print("🎨 Design improvements:")
        print("   • Professional gradient backgrounds")
        print("   • Animated grid overlay")
        print("   • Floating badge with pulse animation")
        print("   • Stats section (50 sites, 12 verified)")
        print("   • Modern card designs with hover effects")
        print("   • Inter font family")
        print("   • Smooth animations throughout")
        print("   • Better mobile spacing")
        print("   • Fixed header with backdrop blur")
        print("   • Professional footer")

except Exception as e:
    print(f"❌ Error: {e}")
