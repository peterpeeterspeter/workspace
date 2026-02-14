#!/usr/bin/env python3
"""
Run migration 005: Backfill weighted scores for all existing items
"""

import sys
import os

# Change to project directory
os.chdir('/root/.openclaw/workspace/projects/aimusicstore')
sys.path.insert(0, '/root/.openclaw/workspace/projects/aimusicstore')

from api.database import get_db
from api.reputation import backfill_all_weighted_scores


def run_migration():
    """Run migration 005."""
    print("Running Migration 005: Backfill weighted scores...")

    with get_db() as db:
        results = backfill_all_weighted_scores(db)
        print(f"✅ Backfill complete:")
        print(f"   Songs updated: {results['songs_updated']}")
        print(f"   Tools updated: {results['tools_updated']}")
        print(f"   Errors: {results['errors']}")

    print("✅ Migration 005 completed successfully!")


if __name__ == "__main__":
    try:
        run_migration()
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
