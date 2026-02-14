#!/usr/bin/env python3
"""
Migration 006: Create api_keys table for API authentication

This migration adds the api_keys table to support:
- API key authentication (US-010)
- Tier-based access control (Free, Pro, Enterprise)
- Usage tracking and expiration
- Key management (create, revoke, update tier)
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
    Create api_keys table.
    """
    logger.info("Running migration 006: Create api_keys table")
    
    try:
        with get_db() as db:
            # Create api_keys table
            db.execute(text("""
                CREATE TABLE IF NOT EXISTS api_keys (
                    key_id VARCHAR(255) PRIMARY KEY,
                    name VARCHAR(500) NOT NULL,
                    key_hash VARCHAR(64) NOT NULL UNIQUE,
                    tier VARCHAR(20) NOT NULL DEFAULT 'free',
                    agent_id VARCHAR(255) REFERENCES agents(id) ON DELETE SET NULL,
                    is_active BOOLEAN NOT NULL DEFAULT TRUE,
                    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    last_used TIMESTAMP,
                    expires_at TIMESTAMP,
                    revoked_at TIMESTAMP
                )
            """))
            
            # Create indexes
            db.execute(text("CREATE INDEX IF NOT EXISTS idx_api_keys_key_hash ON api_keys(key_hash)"))
            db.execute(text("CREATE INDEX IF NOT EXISTS idx_api_keys_tier ON api_keys(tier)"))
            db.execute(text("CREATE INDEX IF NOT EXISTS idx_api_keys_agent_id ON api_keys(agent_id)"))
            db.execute(text("CREATE INDEX IF NOT EXISTS idx_api_keys_is_active ON api_keys(is_active)"))
            
            db.commit()
            logger.info("✅ Created api_keys table with indexes")
            
            # Verify table was created
            result = db.execute(text(
                "SELECT COUNT(*) as count FROM information_schema.tables "
                "WHERE table_name = 'api_keys'"
            ))
            count = result.fetchone()[0]
            
            if count > 0:
                logger.info("✅ Migration 006 completed successfully")
                logger.info("   Table: api_keys")
                logger.info("   Columns: key_id, name, key_hash, tier, agent_id, is_active, created_at, last_used, expires_at, revoked_at")
                logger.info("   Indexes: key_hash, tier, agent_id, is_active")
            else:
                logger.error("❌ Migration 006 failed: table not created")
                return False
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Migration 006 failed: {e}")
        return False


def downgrade():
    """
    Drop api_keys table (rollback).
    """
    logger.info("Rolling back migration 006: Drop api_keys table")
    
    try:
        with get_db() as db:
            db.execute(text("DROP TABLE IF EXISTS api_keys CASCADE"))
            db.commit()
            logger.info("✅ Dropped api_keys table")
        return True
    except Exception as e:
        logger.error(f"❌ Rollback failed: {e}")
        return False


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Migration 006: API Keys Table")
    parser.add_argument('--downgrade', action='store_true', help='Rollback migration')
    args = parser.parse_args()
    
    if args.downgrade:
        success = downgrade()
    else:
        success = upgrade()
    
    sys.exit(0 if success else 1)
