#!/usr/bin/env python3
"""
Initialize database with test data.
Run this from the project root directory.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent / 'api'))

# Load environment variables
load_dotenv()

# Import and run initialization
from database import init_db

if __name__ == "__main__":
    print("Initializing aimusicstore database...")
    print(f"DATABASE_URL: {os.getenv('DATABASE_URL', 'Not set')}")
    
    try:
        init_db(seed_data=True)
        print("\n✅ Database initialization complete!")
    except Exception as e:
        print(f"\n❌ Database initialization failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
