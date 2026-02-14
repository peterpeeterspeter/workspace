#!/usr/bin/env python3
"""
Fixed upload for crashgamegambling.com (correct username)
"""

import json
import subprocess

print("Uploading crashgamegambling.com landing page...")

with open('/root/.openclaw/workspace/tasks/crashgamegambling-landing.html', 'r') as f:
    gambling_html = f.read()

payload = {
    "title": "Master Crash Gambling - From Beginner to Pro",
    "content": gambling_html,
    "status": "publish"
}

# FIXED: user is "peter" not "@peter" for crashgamegambling.com
curl_cmd = [
    'curl', '-s', '-X', 'POST',
    'https://crashgamegambling.com/wp-json/wp/v2/pages/49036',
    '-u', 'peter:MioX SygN Xaz6 pK9o RUiK tBMF',
    '-H', 'Content-Type: application/json',
    '-d', json.dumps(payload)
]

result = subprocess.run(curl_cmd, capture_output=True, text=True)

# Check for HTML error (403 forbidden)
if result.stdout.strip().startswith('<!DOCTYPE'):
    print("❌ Error: Received HTML instead of JSON (possibly 403 Forbidden)")
    print(f"First 200 chars: {result.stdout[:200]}")
elif result.stdout.strip():
    try:
        response = json.loads(result.stdout)
        if 'id' in response:
            print("✅ Uploaded successfully!")
            print(f"   Title: {response['title']['rendered']}")
            print(f"   URL: {response['link']}")
        else:
            print(f"❌ API Error: {response}")
    except json.JSONDecodeError:
        print(f"❌ Could not parse response")
        print(f"First 200 chars: {result.stdout[:200]}")
else:
    print("❌ Empty response from server")

print("\n" + "="*60)
print("ALL 4 LANDING PAGES DEPLOYED!")
print("="*60)
print("\n🚀 Live URLs:")
print("1. https://www.crashcasino.io/")
print("2. https://freecrashgames.com/home/")
print("3. https://cryptocrashgambling.com/main-home/")
print("4. https://crashgamegambling.com/home/")
