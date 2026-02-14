#!/usr/bin/env python3
"""
Send email via AgentMail to Peter
"""

import os
import sys
from pathlib import Path

# Add workspace to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables
from dotenv import load_dotenv
load_dotenv('/root/.openclaw/workspace/.env.email')

# Import AgentMail SDK
try:
    from agentmail import AgentMail
except ImportError:
    print("❌ AgentMail SDK not installed")
    os.system("pip install --break-system-packages agentmail")
    from agentmail import AgentMail

# Initialize client
api_key = os.getenv("AGENTMAIL_API_KEY")
if not api_key:
    print("❌ AGENTMAIL_API_KEY not found")
    sys.exit(1)

print(f"📧 Sending email via AgentMail...")

client = AgentMail(api_key=api_key)

# Send email to Peter
try:
    result = client.inboxes.messages.send(
        inbox_id="carlotta@agentmail.to",
        to="peterpeeterspeter@gmail.com",
        subject="Carlottta AgentMail Test 👋",
        text="""Hello Peter!

This is a test email from Carlottta via AgentMail.

🎭 Carlottta - Digital Familiar & Coordinator
OpenClaw Multi-Agent System

---
✅ Email Integration: Complete
✅ AgentMail SDK: Installed
✅ API Key: Configured
✅ Test Email: Sending

If you're seeing this, AgentMail is working perfectly!

Best regards,
Carlottta 🎭
"""
    )
    print(f"✅ Email sent successfully!")
    print(f"Message ID: {result.id}")
except Exception as e:
    print(f"❌ Error sending email: {e}")
    sys.exit(1)
