#!/usr/bin/env python3
"""
Test AgentMail Integration for Carlottta
"""

import os
import sys
from pathlib import Path

# Add workspace to path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv('/root/.openclaw/workspace/.env.email')

# Import AgentMail SDK
try:
    from agentmail import AgentMail
    print("✅ AgentMail SDK installed")
except ImportError:
    print("❌ AgentMail SDK not installed. Installing...")
    os.system("pip install agentmail python-dotenv")
    from agentmail import AgentMail

# Initialize client
api_key = os.getenv("AGENTMAIL_API_KEY")
if not api_key:
    print("❌ AGENTMAIL_API_KEY not found in .env.email")
    sys.exit(1)

print(f"✅ API Key loaded: {api_key[:20]}...")

client = AgentMail(api_key=api_key)
print("✅ AgentMail client initialized")

# Test: List inboxes
print("\n📋 Listing inboxes...")
try:
    inboxes = client.inboxes.list()
    print(f"Found {len(inboxes)} inbox(es)")
    for inbox in inboxes:
        print(f"  - {inbox.email}")
except Exception as e:
    print(f"❌ Error listing inboxes: {e}")

# Test: Send test email
print("\n📧 Sending test email...")
try:
    result = client.inboxes.messages.send(
        inbox_id="carlotta@agentmail.to",
        to="peter@agentmail.to",  # Test recipient
        subject="Carlottta Email Integration Test ✅",
        text="Hello from Carlottta! This is a test email from the OpenClaw Multi-Agent System.\n\n-- \nCarlottta 🎭\nDigital Familiar & Coordinator\nOpenClaw Multi-Agent System"
    )
    print(f"✅ Email sent successfully!")
    print(f"Message ID: {result.get('id', 'N/A')}")
except Exception as e:
    print(f"❌ Error sending email: {e}")

print("\n✅ AgentMail integration test complete!")
