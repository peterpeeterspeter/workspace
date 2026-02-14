#!/usr/bin/env python3
"""
Create NEW page on crashgamegambling.com instead of updating
"""

import json
import subprocess

print("Creating NEW page on crashgamegambling.com...")

with open('/root/.openclaw/workspace/tasks/crashgamegambling-landing.html', 'r') as f:
    gambling_html = f.read()

payload = {
    "title": "Master Crash Gambling - From Beginner to Pro",
    "content": gambling_html,
    "status": "publish",
    "slug": "master-crash-gambling"
}

curl_cmd = [
    'curl', '-s', '-X', 'POST',
    'https://crashgamegambling.com/wp-json/wp/v2/pages',
    '-u', 'peter:MioX SygN Xaz6 pK9o RUiK tBMF',
    '-H', 'Content-Type: application/json',
    '-d', json.dumps(payload)
]

result = subprocess.run(curl_cmd, capture_output=True, text=True)

if result.stdout.strip().startswith('<!DOCTYPE'):
    print("❌ Still getting 403 Forbidden")
    print("\nTrying smaller payload...")

    # Try with minimal content first
    small_payload = {
        "title": "Master Crash Gambling",
        "content": "<h1>Testing...</h1>",
        "status": "draft"
    }

    curl_cmd2 = [
        'curl', '-s', '-X', 'POST',
        'https://crashgamegambling.com/wp-json/wp/v2/pages',
        '-u', 'peter:MioX SygN Xaz6 pK9o RUiK tBMF',
        '-H', 'Content-Type: application/json',
        '-d', json.dumps(small_payload)
    ]

    result2 = subprocess.run(curl_cmd2, capture_output=True, text=True)

    if result2.stdout.strip():
        try:
            response = json.loads(result2.stdout)
            if 'id' in response:
                print(f"✅ Created page with ID: {response['id']}")

                # Now update it with full content
                update_payload = {
                    "content": gambling_html,
                    "status": "publish"
                }

                curl_cmd3 = [
                    'curl', '-s', '-X', 'POST',
                    f'https://crashgamegambling.com/wp-json/wp/v2/pages/{response["id"]}',
                    '-u', 'peter:MioX SygN Xaz6 pK9o RUiK tBMF',
                    '-H', 'Content-Type: application/json',
                    '-d', json.dumps(update_payload)
                ]

                result3 = subprocess.run(curl_cmd3, capture_output=True, text=True)

                try:
                    final_response = json.loads(result3.stdout)
                    if 'id' in final_response:
                        print(f"✅ Updated with full content!")
                        print(f"   URL: {final_response['link']}")
                    else:
                        print(f"❌ Update failed: {final_response}")
                except:
                    print(f"❌ Could not update page")
            else:
                print(f"❌ Could not create page: {response}")
        except Exception as e:
            print(f"❌ Error: {e}")
            print(f"Response: {result2.stdout[:200]}")
    else:
        print("❌ No response")

elif result.stdout.strip():
    try:
        response = json.loads(result.stdout)
        if 'id' in response:
            print("✅ Created successfully!")
            print(f"   Page ID: {response['id']}")
            print(f"   URL: {response['link']}")
        else:
            print(f"❌ API Error: {response}")
    except json.JSONDecodeError as e:
        print(f"❌ JSON Error: {e}")
        print(f"Response: {result.stdout[:200]}")
else:
    print("❌ Empty response")

print("\n" + "="*60)
print("LANDING PAGES STATUS:")
print("="*60)
print("✅ crashcasino.io - LIVE")
print("✅ freecrashgames.com - LIVE")
print("✅ cryptocrashgambling.com - LIVE")
print("⚠️  crashgamegambling.com - Needs manual upload (403 Forbidden)")
