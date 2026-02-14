# api/database.py
"""
Database connection and session management for aimusicstore.com

Provides:
- SQLAlchemy engine with connection pooling
- Session factory for database operations
- Database initialization function
- Context manager for safe session handling
"""

import os
import logging
from contextlib import contextmanager
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
# Look for .env in parent directories (project root)
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import QueuePool

from models import Base, init_database, seed_test_data

logger = logging.getLogger(__name__)

# Database URL from environment variable with fallback
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql://aimusicstore:password@localhost:5432/aimusicstore'
)

# Engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
    echo=False  # Set to True for SQL query logging
)

# Session factory
SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False
)


@contextmanager
def get_db():
    """
    Context manager for database sessions.
    
    Guarantees that sessions are properly committed or rolled back
    and closed after use.
    
    Yields:
        Session: SQLAlchemy session instance
    
    Example:
        with get_db() as db:
            songs = db.query(Song).all()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Database error, transaction rolled back: {e}")
        raise
    finally:
        db.close()


def init_db(seed_data=False):
    """
    Initialize database schema and optionally seed test data.
    
    Args:
        seed_data: If True, seed test data for development
    
    Raises:
        Exception: If database schema creation fails
    """
    try:
        # Create all tables and indexes
        init_database(engine)
        
        # Optionally seed test data
        if seed_data:
            with get_db() as db:
                seed_test_data(db)
        
        logger.info("✅ Database initialization complete")
        
    except Exception as e:
        logger.error(f"❌ Database initialization failed: {e}")
        raise


def check_connection():
    """
    Test database connection.
    
    Returns:
        bool: True if connection successful, False otherwise
    """
    try:
        with get_db() as db:
            # Execute simple test query
            db.execute("SELECT 1")
        logger.info("✅ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection failed: {e}")
        return False


def get_db_info():
    """
    Get database statistics for monitoring.

    Returns:
        dict: Database stats (table counts, etc.)
    """
    from models import Agent, Song, Tool, Vote

    try:
        with get_db() as db:
            info = {
                "agents_count": db.query(Agent).count(),
                "songs_count": db.query(Song).count(),
                "tools_count": db.query(Tool).count(),
                "votes_count": db.query(Vote).count(),
                "database_url": DATABASE_URL.split('@')[1] if '@' in DATABASE_URL else DATABASE_URL
            }
        return info
    except Exception as e:
        logger.error(f"Failed to get database info: {e}")
        return {}


if __name__ == "__main__":
    # Test database connection and initialization
    logging.basicConfig(level=logging.INFO)
    
    print("Testing database connection...")
    if check_connection():
        print("✅ Connection successful")
        
        print("\nInitializing database schema...")
        init_db(seed_data=True)
        
        print("\nDatabase statistics:")
        info = get_db_info()
        for key, value in info.items():
            print(f"  {key}: {value}")
    else:
        print("❌ Connection failed")
        exit(1)
