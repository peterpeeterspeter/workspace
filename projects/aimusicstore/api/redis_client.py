# api/redis_client.py
"""
Redis caching layer for aimusicstore.com

Provides:
- Redis connection management
- Vote count caching (5-minute TTL)
- Trending data caching (1-minute TTL)
- Cache invalidation helpers
"""

import redis
import json
import logging
import os
from typing import Optional, Any, Dict
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

logger = logging.getLogger(__name__)

# Redis connection settings
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_DB = int(os.getenv('REDIS_DB', 0))
REDIS_URL = os.getenv('REDIS_URL', f'redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}')

# TTL settings (in seconds)
VOTE_COUNT_TTL = 300  # 5 minutes
TRENDING_DATA_TTL = 60  # 1 minute
ITEM_DETAILS_TTL = 600  # 10 minutes


class RedisClient:
    """
    Redis client wrapper with error handling and fallback.
    
    If Redis is unavailable, operations fail gracefully and
    return None (cache miss behavior).
    """
    
    def __init__(self, redis_url: str = REDIS_URL):
        """
        Initialize Redis client.
        
        Args:
            redis_url: Redis connection URL
        """
        self.redis_url = redis_url
        self._client = None
        self._connected = False
        
        try:
            self._connect()
        except Exception as e:
            logger.warning(f"Redis connection failed: {e}. Cache operations will be skipped.")
    
    def _connect(self):
        """
        Establish Redis connection.
        
        Raises:
            Exception: If connection fails
        """
        try:
            self._client = redis.from_url(
                self.redis_url,
                decode_responses=True,
                socket_connect_timeout=5,
                socket_timeout=5
            )
            # Test connection
            self._client.ping()
            self._connected = True
            logger.info(f"✅ Redis connected: {self.redis_url}")
        except Exception as e:
            self._connected = False
            raise Exception(f"Redis connection failed: {e}")
    
    def is_connected(self) -> bool:
        """
        Check if Redis client is connected.
        
        Returns:
            bool: True if connected, False otherwise
        """
        if not self._client:
            return False
        
        try:
            self._client.ping()
            return True
        except Exception:
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from Redis.
        
        Args:
            key: Cache key
        
        Returns:
            Value if exists, None if not found or error
        """
        if not self.is_connected():
            return None
        
        try:
            value = self._client.get(key)
            return value
        except Exception as e:
            logger.error(f"Redis GET error for key '{key}': {e}")
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set value in Redis with optional TTL.
        
        Args:
            key: Cache key
            value: Value to store (will be JSON-serialized if not string)
            ttl: Time-to-live in seconds
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_connected():
            return False
        
        try:
            # Serialize to JSON if not string
            if not isinstance(value, str):
                value = json.dumps(value)
            
            # Set with or without TTL
            if ttl:
                self._client.setex(key, ttl, value)
            else:
                self._client.set(key, value)
            
            return True
        except Exception as e:
            logger.error(f"Redis SET error for key '{key}': {e}")
            return False
    
    def delete(self, *keys: str) -> bool:
        """
        Delete keys from Redis.
        
        Args:
            *keys: One or more keys to delete
        
        Returns:
            bool: True if successful, False otherwise
        """
        if not self.is_connected():
            return False
        
        try:
            if keys:
                self._client.delete(*keys)
            return True
        except Exception as e:
            logger.error(f"Redis DELETE error for keys {keys}: {e}")
            return False
    
    def exists(self, key: str) -> bool:
        """
        Check if key exists in Redis.
        
        Args:
            key: Cache key
        
        Returns:
            bool: True if exists, False otherwise
        """
        if not self.is_connected():
            return False
        
        try:
            return self._client.exists(key) > 0
        except Exception as e:
            logger.error(f"Redis EXISTS error for key '{key}': {e}")
            return False


# Global Redis client instance
redis_client = RedisClient()


def invalidate_cache(item_id: str):
    """
    Invalidate cache for specific item and global trending.
    
    Args:
        item_id: ID of song or tool that was voted on
    
    This invalidates:
    - Vote count cache for the item
    - Trending data cache
    - Item details cache (if exists)
    """
    try:
        # Delete vote count cache
        redis_client.delete(f"votes:{item_id}")
        
        # Delete item details cache
        redis_client.delete(f"item:{item_id}")
        
        # Delete trending data cache
        redis_client.delete("trending_data")
        redis_client.delete("trending_songs")
        redis_client.delete("trending_tools")
        
        logger.debug(f"Cache invalidated for item: {item_id}")
        
    except Exception as e:
        logger.error(f"Failed to invalidate cache: {e}")


def cache_vote_count(item_id: str, vote_count: int) -> bool:
    """
    Cache vote count for an item.
    
    Args:
        item_id: ID of song or tool
        vote_count: Current vote count
    
    Returns:
        bool: True if cached successfully, False otherwise
    """
    key = f"votes:{item_id}"
    return redis_client.set(key, vote_count, ttl=VOTE_COUNT_TTL)


def get_cached_vote_count(item_id: str) -> Optional[int]:
    """
    Get cached vote count for an item.
    
    Args:
        item_id: ID of song or tool
    
    Returns:
        int: Vote count if cached, None if not found
    """
    key = f"votes:{item_id}"
    value = redis_client.get(key)
    
    if value:
        try:
            return int(value)
        except ValueError:
            pass
    
    return None


def cache_trending_data(songs: list, tools: list) -> bool:
    """
    Cache trending data.
    
    Args:
        songs: List of trending songs
        tools: List of trending tools
    
    Returns:
        bool: True if cached successfully, False otherwise
    """
    data = {
        "songs": songs,
        "tools": tools,
        "updated_at": __import__('datetime').datetime.utcnow().isoformat()
    }
    
    # Cache combined data
    success = redis_client.set("trending_data", data, ttl=TRENDING_DATA_TTL)
    
    # Also cache separate lists for specific queries
    redis_client.set("trending_songs", songs, ttl=TRENDING_DATA_TTL)
    redis_client.set("trending_tools", tools, ttl=TRENDING_DATA_TTL)
    
    return success


def get_cached_trending() -> Optional[Dict]:
    """
    Get cached trending data.
    
    Returns:
        dict: Trending data with songs, tools, updated_at
        None: If not cached
    """
    return redis_client.get("trending_data")


def cache_item_details(item_type: str, item_id: str, details: Dict) -> bool:
    """
    Cache song or tool details.
    
    Args:
        item_type: 'song' or 'tool'
        item_id: ID of item
        details: Item details dictionary
    
    Returns:
        bool: True if cached successfully, False otherwise
    """
    key = f"item:{item_id}"
    return redis_client.set(key, details, ttl=ITEM_DETAILS_TTL)


def get_cached_item_details(item_id: str) -> Optional[Dict]:
    """
    Get cached item details.
    
    Args:
        item_id: ID of song or tool
    
    Returns:
        dict: Item details if cached, None if not found
    """
    key = f"item:{item_id}"
    return redis_client.get(key)


if __name__ == "__main__":
    # Test Redis connection
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("Testing Redis connection...")
    
    if redis_client.is_connected():
        print("✅ Redis connection successful")
        
        # Test cache operations
        print("\nTesting cache operations...")
        redis_client.set("test_key", "test_value", ttl=60)
        print(f"Set: test_key = test_value")
        
        value = redis_client.get("test_key")
        print(f"Get: test_key = {value}")
        
        # Test JSON serialization
        data = {"test": "data", "number": 123}
        redis_client.set("test_json", data, ttl=60)
        print(f"Set: test_json = {data}")
        
        json_value = redis_client.get("test_json")
        print(f"Get: test_json = {json_value}")
        
        # Clean up
        redis_client.delete("test_key", "test_json")
        print("✅ Cache operations successful")
        
    else:
        print("❌ Redis connection failed")
