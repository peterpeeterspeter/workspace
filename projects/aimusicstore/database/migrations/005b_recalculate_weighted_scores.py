#!/usr/bin/env python3
"""
Recalculate weighted scores for all items with current votes.
"""

import sys
import os

# Change to project directory
os.chdir('/root/.openclaw/workspace/projects/aimusicstore')
sys.path.insert(0, '/root/.openclaw/workspace/projects/aimusicstore')

from api.database import get_db
from api.reputation import backfill_all_weighted_scores


def recalculate_all_scores():
    """Recalculate weighted scores for all items."""
    print("Recalculating weighted scores with current vote data...")

    with get_db() as db:
        results = backfill_all_weighted_scores(db)
        print(f"✅ Recalculation complete:")
        print(f"   Songs updated: {results['songs_updated']}")
        print(f"   Tools updated: {results['tools_updated']}")
        print(f"   Errors: {results['errors']}")


if __name__ == "__main__":
    try:
        recalculate_all_scores()
    except Exception as e:
        print(f"❌ Failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
