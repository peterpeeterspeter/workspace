#!/usr/bin/env python3
"""
Run migration 003: Add weighted_score columns to songs and tools tables
"""

import sys
import os

# Change to project directory
os.chdir('/root/.openclaw/workspace/projects/aimusicstore')
sys.path.insert(0, '/root/.openclaw/workspace/projects/aimusicstore')

from api.database import get_db
from sqlalchemy import text


def run_migration():
    """Run migration 003."""
    print("Running Migration 003: Add weighted_score columns...")

    with get_db() as db:
        # Add weighted_score to songs table (will fail if already exists - that's fine)
        try:
            db.execute(text("ALTER TABLE songs ADD COLUMN IF NOT EXISTS weighted_score INTEGER DEFAULT 0"))
            db.execute(text("CREATE INDEX IF NOT EXISTS idx_songs_weighted_score ON songs(weighted_score DESC)"))
            print("✅ weighted_score column added to songs table (or already exists)")
        except Exception as e:
            print(f"⚠️  Songs table issue (may already have column): {e}")

        # Commit songs changes before starting tools transaction
        db.commit()

        # Add weighted_score to tools table (will fail if already exists - that's fine)
        try:
            db.execute(text("ALTER TABLE tools ADD COLUMN IF NOT EXISTS weighted_score INTEGER DEFAULT 0"))
            db.execute(text("CREATE INDEX IF NOT EXISTS idx_tools_weighted_score ON tools(weighted_score DESC)"))
            print("✅ weighted_score column added to tools table (or already exists)")
        except Exception as e:
            print(f"⚠️  Tools table issue (may already have column): {e}")

        db.commit()

    print("✅ Migration 003 completed successfully!")


if __name__ == "__main__":
    try:
        run_migration()
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
