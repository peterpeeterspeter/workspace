#!/usr/bin/env python3
"""
Manual upload for cryptocrash and crashgamegambling
"""

import json
import subprocess

# Cryptocrash
print("Uploading cryptocrashgambling.com...")
with open('/root/.openclaw/workspace/tasks/cryptocrash-landing.html', 'r') as f:
    crypto_html = f.read()

payload = {
    "title": "Crypto Crash Gambling - Bitcoin, ETH, USDT",
    "content": crypto_html,
    "status": "publish"
}

curl_cmd = [
    'curl', '-s', '-X', 'POST',
    'https://cryptocrashgambling.com/wp-json/wp/v2/pages/17869',
    '-u', '@peter:R3kQ 6vRA UwYd x7Cn KEtT Pk83',
    '-H', 'Content-Type: application/json',
    '-d', json.dumps(payload)
]

result = subprocess.run(curl_cmd, capture_output=True, text=True)
response = json.loads(result.stdout)
print(f"✓ Uploaded! URL: {response['link']}")

# Crashgamegambling
print("\nUploading crashgamegambling.com...")
with open('/root/.openclaw/workspace/tasks/crashgamegambling-landing.html', 'r') as f:
    gambling_html = f.read()

payload = {
    "title": "Master Crash Gambling - From Beginner to Pro",
    "content": gambling_html,
    "status": "publish"
}

curl_cmd = [
    'curl', '-s', '-X', 'POST',
    'https://crashgamegambling.com/wp-json/wp/v2/pages/49036',
    '-u', 'peter:MioX SygN Xaz6 pK9o RUiK tBMF',
    '-H', 'Content-Type: application/json',
    '-d', json.dumps(payload)
]

result = subprocess.run(curl_cmd, capture_output=True, text=True)
response = json.loads(result.stdout)
print(f"✓ Uploaded! URL: {response['link']}")

print("\n" + "="*60)
print("All 4 landing pages deployed!")
print("="*60)
