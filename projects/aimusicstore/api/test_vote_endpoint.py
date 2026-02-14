#!/usr/bin/env python3
"""
Test script for aimusicstore.com vote endpoint (US-001)

Run this to verify the vote endpoint is working correctly.
Requires: PostgreSQL and Redis running (docker-compose up)
"""

import os
import sys
import json
import logging
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Test configuration
API_HOST = os.getenv('API_HOST', 'localhost')
API_PORT = os.getenv('API_PORT', '8000')
BASE_URL = f"http://{API_HOST}:{API_PORT}"


def test_health_endpoint():
    """Test the /health endpoint."""
    print("\n" + "="*60)
    print("TEST 1: Health Endpoint")
    print("="*60)
    
    try:
        import requests
        
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check successful")
            print(f"   Status: {data.get('status')}")
            print(f"   Version: {data.get('version')}")
            print(f"   Database: {data.get('database', {}).get('status', 'unknown')}")
            print(f"   Redis: {data.get('redis', 'unknown')}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False


def test_vote_endpoint():
    """Test the POST /api/v1/vote endpoint."""
    print("\n" + "="*60)
    print("TEST 2: Vote Endpoint")
    print("="*60)
    
    try:
        import requests
        
        # Test data
        vote_data = {
            "agent_id": "test-agent-001",
            "item_type": "song",
            "item_id": "song-1",
            "vote": "up",
            "comment": "Great track!"
        }
        
        print(f"Sending vote request...")
        print(f"  Agent: {vote_data['agent_id']}")
        print(f"  Item: {vote_data['item_type']}:{vote_data['item_id']}")
        print(f"  Vote: {vote_data['vote']}")
        
        response = requests.post(
            f"{BASE_URL}/api/v1/vote",
            json=vote_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        
        print(f"\nResponse status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Vote recorded successfully")
            print(f"   Status: {data.get('status')}")
            print(f"   Message: {data.get('message')}")
            print(f"   Data: {json.dumps(data.get('data'), indent=2)}")
            return True
        elif response.status_code == 400:
            data = response.json()
            print(f"⚠️  Bad request: {data.get('detail')}")
            return None  # Expected if item doesn't exist
        elif response.status_code == 404:
            data = response.json()
            print(f"⚠️  Item not found: {data.get('detail')}")
            print(f"   This is expected if test data hasn't been seeded")
            return None
        else:
            print(f"❌ Unexpected response: {response.status_code}")
            print(f"   Detail: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Vote endpoint error: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_duplicate_vote():
    """Test that duplicate votes are rejected."""
    print("\n" + "="*60)
    print("TEST 3: Duplicate Vote Prevention")
    print("="*60)
    
    try:
        import requests
        
        vote_data = {
            "agent_id": "test-agent-002",
            "item_type": "song",
            "item_id": "song-1",
            "vote": "up"
        }
        
        # First vote
        print(f"Sending first vote...")
        response1 = requests.post(
            f"{BASE_URL}/api/v1/vote",
            json=vote_data,
            timeout=10
        )
        
        print(f"First vote response: {response1.status_code}")
        
        # Second vote (should fail)
        print(f"Sending duplicate vote...")
        response2 = requests.post(
            f"{BASE_URL}/api/v1/vote",
            json=vote_data,
            timeout=10
        )
        
        print(f"Duplicate vote response: {response2.status_code}")
        
        if response2.status_code == 400:
            data = response2.json()
            if "already voted" in data.get('detail', '').lower():
                print(f"✅ Duplicate vote correctly rejected")
                print(f"   Detail: {data.get('detail')}")
                return True
            else:
                print(f"⚠️  Wrong error message: {data.get('detail')}")
                return False
        else:
            print(f"❌ Duplicate vote should have been rejected")
            return False
            
    except Exception as e:
        print(f"❌ Duplicate vote test error: {e}")
        return False


def test_validation():
    """Test input validation."""
    print("\n" + "="*60)
    print("TEST 4: Input Validation")
    print("="*60)
    
    try:
        import requests
        
        test_cases = [
            {
                "name": "Invalid vote type",
                "data": {
                    "agent_id": "test-agent",
                    "item_type": "song",
                    "item_id": "song-1",
                    "vote": "invalid"  # Should be 'up' or 'down'
                },
                "expected_status": 422  # Pydantic validation error
            },
            {
                "name": "Invalid item type",
                "data": {
                    "agent_id": "test-agent",
                    "item_type": "invalid",  # Should be 'song' or 'tool'
                    "item_id": "song-1",
                    "vote": "up"
                },
                "expected_status": 422
            },
            {
                "name": "Missing required field",
                "data": {
                    "agent_id": "test-agent",
                    "item_type": "song",
                    "vote": "up"
                    # Missing item_id
                },
                "expected_status": 422
            }
        ]
        
        all_passed = True
        for test_case in test_cases:
            print(f"\nTesting: {test_case['name']}")
            response = requests.post(
                f"{BASE_URL}/api/v1/vote",
                json=test_case['data'],
                timeout=10
            )
            
            if response.status_code == test_case['expected_status']:
                print(f"  ✅ Correctly rejected with status {response.status_code}")
            else:
                print(f"  ❌ Expected status {test_case['expected_status']}, got {response.status_code}")
                all_passed = False
        
        return all_passed
            
    except Exception as e:
        print(f"❌ Validation test error: {e}")
        return False


def main():
    """Run all tests."""
    print("\n" + "="*60)
    print("aimusicstore.com - Vote Endpoint Test Suite")
    print(f"Testing API at: {BASE_URL}")
    print(f"Timestamp: {datetime.utcnow().isoformat()}")
    print("="*60)
    
    # Check if API is running
    print("\n⚠️  Note: Make sure API is running before running tests")
    print("   Start with: cd /root/.openclaw/workspace/projects/aimusicstore && python -m api.main")
    print("   Or: uvicorn api.main:app --reload")
    
    input("\nPress Enter to continue...")
    
    # Run tests
    results = {
        "health": test_health_endpoint(),
        "vote": test_vote_endpoint(),
        "duplicate": test_duplicate_vote(),
        "validation": test_validation()
    }
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, result in results.items():
        if result is True:
            status = "✅ PASS"
        elif result is False:
            status = "❌ FAIL"
        else:
            status = "⚠️  SKIP"
        
        print(f"{test_name.capitalize():20} {status}")
    
    # Overall result
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    total = len(results)
    
    print(f"\nResult: {passed}/{total} tests passed")
    
    if failed == 0 and passed > 0:
        print("🎉 All critical tests passed!")
        return 0
    else:
        print("⚠️  Some tests failed or were skipped")
        return 1


if __name__ == "__main__":
    sys.exit(main())
