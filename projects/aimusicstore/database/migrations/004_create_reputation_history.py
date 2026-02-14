#!/usr/bin/env python3
"""
Run migration 004: Create reputation_history table
"""

import sys
import os

# Change to project directory
os.chdir('/root/.openclaw/workspace/projects/aimusicstore')
sys.path.insert(0, '/root/.openclaw/workspace/projects/aimusicstore')

from api.database import get_db
from sqlalchemy import text


def run_migration():
    """Run migration 004."""
    print("Running Migration 004: Create reputation_history table...")

    with get_db() as db:
        # Create reputation_history table
        try:
            db.execute(text("""
                CREATE TABLE IF NOT EXISTS reputation_history (
                    id SERIAL PRIMARY KEY,
                    agent_id VARCHAR(255) NOT NULL,
                    old_score INTEGER NOT NULL,
                    new_score INTEGER NOT NULL,
                    change_reason TEXT,
                    timestamp TIMESTAMP DEFAULT NOW(),

                    -- Foreign key constraint
                    CONSTRAINT fk_reputation_history_agent
                        FOREIGN KEY (agent_id)
                        REFERENCES agents(id)
                        ON DELETE CASCADE
                )
            """))
            print("✅ reputation_history table created")
        except Exception as e:
            print(f"⚠️  Table creation issue (may already exist): {e}")

        # Create indexes for performance
        try:
            db.execute(text("CREATE INDEX IF NOT EXISTS idx_reputation_history_agent_id ON reputation_history(agent_id)"))
            db.execute(text("CREATE INDEX IF NOT EXISTS idx_reputation_history_timestamp ON reputation_history(timestamp DESC)"))
            db.execute(text("CREATE INDEX IF NOT EXISTS idx_reputation_history_agent_timestamp ON reputation_history(agent_id, timestamp DESC)"))
            print("✅ Indexes created for reputation_history table")
        except Exception as e:
            print(f"⚠️  Index creation issue: {e}")

        db.commit()

    print("✅ Migration 004 completed successfully!")


if __name__ == "__main__":
    try:
        run_migration()
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
