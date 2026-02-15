#!/usr/bin/env python3
"""
Migration 007: Update schema for auth dependency + enhanced votes

This migration adds the following features:
1. api_keys table: Change is_active BOOLEAN → status TEXT ('active'|'revoked')
2. agents table: Add status TEXT default 'active'
3. votes table: Add reasoning, confidence, weight_applied, vote_source
4. votes table: Update unique constraint to include item_type

This enables:
- Proper API key status management
- Agent suspension capability
- Enhanced vote tracking with reasoning and confidence
- Vote source tracking (external vs bootstrap vs internal)
- Unique constraint prevents duplicate votes per item type

Author: Carlottta
Date: 2026-02-15
Phase: 1 - Step 5: Auth Dependency + Enhanced Votes
"""

import sys
import os

# Change to project directory
os.chdir('/root/.openclaw/workspace/projects/aimusicstore')
sys.path.insert(0, '/root/.openclaw/workspace/projects/aimusicstore')

from api.database import get_db
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def upgrade():
    """
    Update schema for auth dependency + enhanced votes.
    """
    logger.info("Running migration 007: Update schema for auth dependency + enhanced votes")
    
    try:
        with get_db() as db:
            # ============================================
            # 1. Update api_keys table
            # ============================================
            logger.info("Step 1: Updating api_keys table (is_active → status)")
            
            # Add status column
            db.execute(text("ALTER TABLE api_keys ADD COLUMN IF NOT EXISTS status TEXT"))
            
            # Backfill status from is_active
            db.execute(text("UPDATE api_keys SET status = 'active' WHERE is_active = TRUE"))
            db.execute(text("UPDATE api_keys SET status = 'revoked' WHERE is_active = FALSE OR is_active IS NULL"))
            
            # Set NOT NULL and default
            db.execute(text("ALTER TABLE api_keys ALTER COLUMN status SET NOT NULL"))
            db.execute(text("ALTER TABLE api_keys ALTER COLUMN status SET DEFAULT 'active'"))
            
            # Add check constraint (use DO block for IF NOT EXISTS)
            db.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'check_api_keys_status'
                    ) THEN
                        ALTER TABLE api_keys ADD CONSTRAINT check_api_keys_status 
                        CHECK (status IN ('active', 'revoked'));
                    END IF;
                END $$;
            """))
            
            logger.info("✅ api_keys.status column added and populated")
            
            # ============================================
            # 2. Update agents table
            # ============================================
            logger.info("Step 2: Updating agents table (add status)")
            
            db.execute(text("ALTER TABLE agents ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'active'"))
            
            # Add check constraint (use DO block for IF NOT EXISTS)
            db.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'check_agents_status'
                    ) THEN
                        ALTER TABLE agents ADD CONSTRAINT check_agents_status 
                        CHECK (status IN ('active', 'suspended'));
                    END IF;
                END $$;
            """))
            
            logger.info("✅ agents.status column added")
            
            # ============================================
            # 3. Update votes table
            # ============================================
            logger.info("Step 3: Updating votes table (add reasoning, confidence, weight_applied, vote_source)")
            
            # Add new columns
            db.execute(text("ALTER TABLE votes ADD COLUMN IF NOT EXISTS reasoning TEXT"))
            db.execute(text("ALTER TABLE votes ADD COLUMN IF NOT EXISTS confidence REAL"))
            db.execute(text("ALTER TABLE votes ADD COLUMN IF NOT EXISTS weight_applied REAL DEFAULT 0"))
            db.execute(text("ALTER TABLE votes ADD COLUMN IF NOT EXISTS vote_source TEXT DEFAULT 'external'"))
            
            # Add confidence check constraint (use DO block for IF NOT EXISTS)
            db.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'check_votes_confidence'
                    ) THEN
                        ALTER TABLE votes ADD CONSTRAINT check_votes_confidence 
                        CHECK (confidence IS NULL OR (confidence >= 0 AND confidence <= 1));
                    END IF;
                END $$;
            """))
            
            # Backfill vote_source for existing votes (BEFORE adding constraint)
            db.execute(text("UPDATE votes SET vote_source = 'bootstrap' WHERE vote_source IS NULL OR vote_source NOT IN ('external', 'bootstrap', 'internal')"))
            
            # Add vote_source check constraint (use DO block for IF NOT EXISTS)
            db.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'check_votes_vote_source'
                    ) THEN
                        ALTER TABLE votes ADD CONSTRAINT check_votes_vote_source 
                        CHECK (vote_source IN ('external', 'bootstrap', 'internal'));
                    END IF;
                END $$;
            """))
            
            logger.info("✅ votes columns added (reasoning, confidence, weight_applied, vote_source)")
            
            # ============================================
            # 4. Update votes unique constraint
            # ============================================
            logger.info("Step 4: Updating votes unique constraint (add item_type)")
            
            # Drop old unique constraint if it exists
            # PostgreSQL doesn't support "IF EXISTS" for constraint drops
            db.execute(text("""
                DO $$
                BEGIN
                    IF EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'votes_agent_id_item_id_key'
                    ) THEN
                        ALTER TABLE votes DROP CONSTRAINT votes_agent_id_item_id_key;
                    END IF;
                    
                    IF EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'unique_vote_per_agent'
                    ) THEN
                        ALTER TABLE votes DROP CONSTRAINT unique_vote_per_agent;
                    END IF;
                END $$;
            """))
            
            # Add new unique constraint with item_type (use DO block for IF NOT EXISTS)
            db.execute(text("""
                DO $$
                BEGIN
                    IF NOT EXISTS (
                        SELECT 1 FROM pg_constraint 
                        WHERE conname = 'unique_vote_per_agent_and_type'
                    ) THEN
                        ALTER TABLE votes ADD CONSTRAINT unique_vote_per_agent_and_type 
                        UNIQUE (agent_id, item_id, item_type);
                    END IF;
                END $$;
            """))
            
            logger.info("✅ votes unique constraint updated (agent_id, item_id, item_type)")
            
            # ============================================
            # 5. Create indexes
            # ============================================
            logger.info("Step 5: Creating indexes for new columns")
            
            db.execute(text("CREATE INDEX IF NOT EXISTS idx_api_keys_status ON api_keys(status)"))
            db.execute(text("CREATE INDEX IF NOT EXISTS idx_agents_status ON agents(status)"))
            db.execute(text("CREATE INDEX IF NOT EXISTS idx_votes_vote_source ON votes(vote_source)"))
            db.execute(text("CREATE INDEX IF NOT EXISTS idx_votes_confidence ON votes(confidence) WHERE confidence IS NOT NULL"))
            
            logger.info("✅ Indexes created")
            
            # Commit all changes
            db.commit()
            logger.info("✅ Migration 007 completed successfully")
            
            # ============================================
            # Verification
            # ============================================
            logger.info("\n📊 Verification:")
            
            # Check api_keys
            result = db.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'api_keys' 
                AND column_name IN ('status', 'is_active')
                ORDER BY column_name
            """)).fetchall()
            logger.info(f"   api_keys columns: {[row[0] for row in result]}")
            
            # Check agents
            result = db.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'agents' 
                AND column_name = 'status'
            """)).fetchall()
            logger.info(f"   agents columns: {[row[0] for row in result]}")
            
            # Check votes
            result = db.execute(text("""
                SELECT column_name, data_type 
                FROM information_schema.columns 
                WHERE table_name = 'votes' 
                AND column_name IN ('reasoning', 'confidence', 'weight_applied', 'vote_source')
                ORDER BY column_name
            """)).fetchall()
            logger.info(f"   votes columns: {[row[0] for row in result]}")
            
            # Check unique constraint
            result = db.execute(text("""
                SELECT conname 
                FROM pg_constraint 
                WHERE conname LIKE '%unique_vote%' 
                AND conrelid = 'votes'::regclass
            """)).fetchall()
            logger.info(f"   votes unique constraints: {[row[0] for row in result]}")
            
            return True
        
    except Exception as e:
        logger.error(f"❌ Migration 007 failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def downgrade():
    """
    Rollback migration 007.
    """
    logger.info("Rolling back migration 007")
    
    try:
        with get_db() as db:
            # Drop indexes
            db.execute(text("DROP INDEX IF EXISTS idx_api_keys_status"))
            db.execute(text("DROP INDEX IF EXISTS idx_agents_status"))
            db.execute(text("DROP INDEX IF EXISTS idx_votes_vote_source"))
            db.execute(text("DROP INDEX IF EXISTS idx_votes_confidence"))
            
            # Drop votes columns
            db.execute(text("ALTER TABLE votes DROP CONSTRAINT IF EXISTS check_votes_vote_source"))
            db.execute(text("ALTER TABLE votes DROP CONSTRAINT IF EXISTS check_votes_confidence"))
            db.execute(text("ALTER TABLE votes DROP COLUMN IF EXISTS vote_source"))
            db.execute(text("ALTER TABLE votes DROP COLUMN IF EXISTS weight_applied"))
            db.execute(text("ALTER TABLE votes DROP COLUMN IF EXISTS confidence"))
            db.execute(text("ALTER TABLE votes DROP COLUMN IF EXISTS reasoning"))
            
            # Restore old unique constraint
            db.execute(text("ALTER TABLE votes DROP CONSTRAINT IF EXISTS unique_vote_per_agent_and_type"))
            db.execute(text("""
                ALTER TABLE votes ADD CONSTRAINT IF NOT EXISTS unique_vote_per_agent 
                UNIQUE (agent_id, item_id)
            """))
            
            # Drop agents column
            db.execute(text("ALTER TABLE agents DROP CONSTRAINT IF EXISTS check_agents_status"))
            db.execute(text("ALTER TABLE agents DROP COLUMN IF EXISTS status"))
            
            # Drop api_keys columns
            db.execute(text("ALTER TABLE api_keys DROP CONSTRAINT IF EXISTS check_api_keys_status"))
            db.execute(text("ALTER TABLE api_keys DROP COLUMN IF EXISTS status"))
            
            db.commit()
            logger.info("✅ Rollback completed")
            return True
            
    except Exception as e:
        logger.error(f"❌ Rollback failed: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migration 007: Auth Dependency + Enhanced Votes")
    parser.add_argument('--downgrade', action='store_true', help='Rollback migration')
    args = parser.parse_args()
    
    if args.downgrade:
        success = downgrade()
    else:
        success = upgrade()
    
    sys.exit(0 if success else 1)
