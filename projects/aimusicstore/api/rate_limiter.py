# api/rate_limiter.py
"""
Rate Limiting for aimusicstore.com API

Prevents abuse and ensures fair access to voting endpoints.

Features:
- Per-agent rate limiting (votes per day)
- Per-IP rate limiting (votes per day)
- Redis-backed for distributed systems
- Configurable tiers (Free, Pro, Enterprise)
"""

import redis
import json
import logging
from datetime import datetime, timedelta
from typing import Optional, Tuple

try:
    from api.redis_client import redis_client
except ImportError:
    from redis_client import redis_client

logger = logging.getLogger(__name__)


class RateLimitTier:
    """Rate limit tiers for different access levels."""
    
    FREE = {
        "name": "free",
        "votes_per_day": 100,
        "votes_per_hour": 20,
        "requests_per_minute": 60
    }
    
    PRO = {
        "name": "pro",
        "votes_per_day": 1000,
        "votes_per_hour": 200,
        "requests_per_minute": 300
    }
    
    ENTERPRISE = {
        "name": "enterprise",
        "votes_per_day": None,  # Unlimited
        "votes_per_hour": None,
        "requests_per_minute": 1000
    }


class RateLimiter:
    """
    Redis-based rate limiting for API endpoints.
    
    Tracks:
    - Vote counts per agent (per day, per hour)
    - Request counts per agent/IP (per minute)
    - Blocked agents
    """
    
    # Redis key prefixes
    AGENT_VOTE_DAY_PREFIX = "rate_limit:agent:vote:day:"
    AGENT_VOTE_HOUR_PREFIX = "rate_limit:agent:vote:hour:"
    AGENT_REQUEST_PREFIX = "rate_limit:agent:request:"
    IP_REQUEST_PREFIX = "rate_limit:ip:request:"
    BLOCKED_AGENTS_PREFIX = "blocked_agents:"
    FLAGGED_AGENTS_PREFIX = "flagged_agents:"
    
    # TTLs (seconds)
    DAY_TTL = 86400  # 24 hours
    HOUR_TTL = 3600  # 1 hour
    MINUTE_TTL = 60  # 1 minute
    
    def __init__(self, redis_client=None):
        """
        Initialize rate limiter.
        
        Args:
            redis_client: Redis client instance (uses global if None)
        """
        self.redis = redis_client or redis_client
        
        if not self.redis:
            logger.warning("No Redis client available, rate limiting disabled")
    
    def get_agent_tier(self, agent_id: str) -> dict:
        """
        Get rate limit tier for an agent.
        
        For MVP, all agents are FREE tier.
        Future: Check database for agent's subscription tier.
        
        Args:
            agent_id: Agent identifier
        
        Returns:
            Tier configuration dict
        """
        # MVP: All agents are free tier
        # Future enhancement: Query database for agent's subscription
        return RateLimitTier.FREE
    
    def check_vote_limit(self, agent_id: str, ip_address: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """
        Check if agent is within vote rate limits.
        
        Args:
            agent_id: Agent identifier
            ip_address: Optional IP address for additional limiting
        
        Returns:
            (is_allowed, error_message)
        """
        try:
            if not self.redis:
                return True, None  # Rate limiting disabled
            
            tier = self.get_agent_tier(agent_id)
            
            # Check daily vote limit
            daily_limit = tier.get("votes_per_day")
            if daily_limit is not None:
                daily_key = f"{self.AGENT_VOTE_DAY_PREFIX}{agent_id}"
                daily_count = self.redis.get(daily_key)
                
                if daily_count is None:
                    # First vote today
                    daily_count = 0
                    self.redis.setex(daily_key, self.DAY_TTL, 0)
                else:
                    daily_count = int(daily_count)
                
                if daily_count >= daily_limit:
                    error = f"Daily vote limit exceeded: {daily_count}/{daily_limit}"
                    logger.warning(f"Agent {agent_id}: {error}")
                    return False, error
            
            # Check hourly vote limit
            hourly_limit = tier.get("votes_per_hour")
            if hourly_limit is not None:
                hourly_key = f"{self.AGENT_VOTE_HOUR_PREFIX}{agent_id}"
                hourly_count = self.redis.get(hourly_key)
                
                if hourly_count is None:
                    hourly_count = 0
                    self.redis.setex(hourly_key, self.HOUR_TTL, 0)
                else:
                    hourly_count = int(hourly_count)
                
                if hourly_count >= hourly_limit:
                    error = f"Hourly vote limit exceeded: {hourly_count}/{hourly_limit}"
                    logger.warning(f"Agent {agent_id}: {error}")
                    return False, error
            
            # Check IP-based limits (if IP provided)
            if ip_address:
                ip_daily_limit = 500  # Stricter limit per IP
                ip_key = f"rate_limit:ip:vote:day:{ip_address}"
                ip_count = self.redis.get(ip_key)
                
                if ip_count is None:
                    ip_count = 0
                    self.redis.setex(ip_key, self.DAY_TTL, 0)
                else:
                    ip_count = int(ip_count)
                
                if ip_count >= ip_daily_limit:
                    error = f"IP daily vote limit exceeded: {ip_count}/{ip_daily_limit}"
                    logger.warning(f"IP {ip_address}: {error}")
                    return False, error
            
            # All checks passed
            return True, None
            
        except Exception as e:
            logger.error(f"Error checking vote limits for {agent_id}: {e}")
            # Fail open: allow vote if rate limiter fails
            return True, None
    
    def record_vote(self, agent_id: str, ip_address: Optional[str] = None):
        """
        Record a vote in rate limiter counters.
        
        Args:
            agent_id: Agent identifier
            ip_address: Optional IP address
        """
        try:
            if not self.redis:
                return  # Rate limiting disabled
            
            # Increment daily vote counter
            daily_key = f"{self.AGENT_VOTE_DAY_PREFIX}{agent_id}"
            self.redis.incr(daily_key)
            
            # Increment hourly vote counter
            hourly_key = f"{self.AGENT_VOTE_HOUR_PREFIX}{agent_id}"
            self.redis.incr(hourly_key)
            
            # Increment IP vote counter
            if ip_address:
                ip_key = f"rate_limit:ip:vote:day:{ip_address}"
                self.redis.incr(ip_key)
            
            logger.debug(f"Recorded vote for agent {agent_id}")
            
        except Exception as e:
            logger.error(f"Error recording vote for {agent_id}: {e}")
    
    def check_request_limit(self, agent_id: str, ip_address: Optional[str] = None) -> Tuple[bool, Optional[str]]:
        """
        Check if agent is within general request rate limits.
        
        Args:
            agent_id: Agent identifier
            ip_address: Optional IP address
        
        Returns:
            (is_allowed, error_message)
        """
        try:
            if not self.redis:
                return True, None
            
            tier = self.get_agent_tier(agent_id)
            request_limit = tier.get("requests_per_minute")
            
            if request_limit is not None:
                # Check agent request limit
                agent_key = f"{self.AGENT_REQUEST_PREFIX}{agent_id}"
                agent_count = self.redis.get(agent_key)
                
                if agent_count is None:
                    agent_count = 0
                    self.redis.setex(agent_key, self.MINUTE_TTL, 0)
                else:
                    agent_count = int(agent_count)
                
                if agent_count >= request_limit:
                    error = f"Request rate limit exceeded: {agent_count}/{request_limit} per minute"
                    logger.warning(f"Agent {agent_id}: {error}")
                    return False, error
                
                # Check IP request limit (stricter)
                if ip_address:
                    ip_limit = 120  # 2 requests per second
                    ip_key = f"{self.IP_REQUEST_PREFIX}{ip_address}"
                    ip_count = self.redis.get(ip_key)
                    
                    if ip_count is None:
                        ip_count = 0
                        self.redis.setex(ip_key, self.MINUTE_TTL, 0)
                    else:
                        ip_count = int(ip_count)
                    
                    if ip_count >= ip_limit:
                        error = f"IP request rate limit exceeded: {ip_count}/{ip_limit} per minute"
                        logger.warning(f"IP {ip_address}: {error}")
                        return False, error
            
            return True, None
            
        except Exception as e:
            logger.error(f"Error checking request limits: {e}")
            return True, None
    
    def record_request(self, agent_id: str, ip_address: Optional[str] = None):
        """
        Record a request in rate limiter counters.
        
        Args:
            agent_id: Agent identifier
            ip_address: Optional IP address
        """
        try:
            if not self.redis:
                return
            
            # Increment request counter
            agent_key = f"{self.AGENT_REQUEST_PREFIX}{agent_id}"
            self.redis.incr(agent_key)
            
            # Increment IP request counter
            if ip_address:
                ip_key = f"{self.IP_REQUEST_PREFIX}{ip_address}"
                self.redis.incr(ip_key)
            
        except Exception as e:
            logger.error(f"Error recording request: {e}")
    
    def is_agent_blocked(self, agent_id: str) -> bool:
        """
        Check if agent is blocked.
        
        Args:
            agent_id: Agent identifier
        
        Returns:
            True if blocked, False otherwise
        """
        try:
            if not self.redis:
                return False
            
            blocked_key = f"{self.BLOCKED_AGENTS_PREFIX}{agent_id}"
            return self.redis.exists(blocked_key) > 0
            
        except Exception as e:
            logger.error(f"Error checking if agent {agent_id} is blocked: {e}")
            return False
    
    def block_agent(self, agent_id: str, reason: str, duration_hours: int = 24):
        """
        Block an agent for specified duration.
        
        Args:
            agent_id: Agent identifier
            reason: Reason for blocking
            duration_hours: Block duration in hours (default 24)
        """
        try:
            if not self.redis:
                logger.warning("Cannot block agent: Redis not available")
                return
            
            blocked_key = f"{self.BLOCKED_AGENTS_PREFIX}{agent_id}"
            
            # Store block reason and timestamp
            block_data = {
                "reason": reason,
                "blocked_at": datetime.utcnow().isoformat(),
                "duration_hours": duration_hours
            }
            
            self.redis.setex(
                blocked_key,
                duration_hours * 3600,
                json.dumps(block_data)
            )
            
            logger.warning(f"Blocked agent {agent_id}: {reason} for {duration_hours} hours")
            
        except Exception as e:
            logger.error(f"Error blocking agent {agent_id}: {e}")
    
    def unblock_agent(self, agent_id: str):
        """
        Unblock an agent.
        
        Args:
            agent_id: Agent identifier
        """
        try:
            if not self.redis:
                return
            
            blocked_key = f"{self.BLOCKED_AGENTS_PREFIX}{agent_id}"
            self.redis.delete(blocked_key)
            
            logger.info(f"Unblocked agent {agent_id}")
            
        except Exception as e:
            logger.error(f"Error unblocking agent {agent_id}: {e}")
    
    def is_agent_flagged(self, agent_id: str) -> bool:
        """
        Check if agent is flagged (warning state).
        
        Args:
            agent_id: Agent identifier
        
        Returns:
            True if flagged, False otherwise
        """
        try:
            if not self.redis:
                return False
            
            flagged_key = f"{self.FLAGGED_AGENTS_PREFIX}{agent_id}"
            return self.redis.exists(flagged_key) > 0
            
        except Exception as e:
            logger.error(f"Error checking if agent {agent_id} is flagged: {e}")
            return False
    
    def flag_agent(self, agent_id: str, reason: str, warning_count: int = 1):
        """
        Flag an agent with a warning.
        
        Args:
            agent_id: Agent identifier
            reason: Reason for flagging
            warning_count: Number of warnings (default 1)
        """
        try:
            if not self.redis:
                return
            
            flagged_key = f"{self.FLAGGED_AGENTS_PREFIX}{agent_id}"
            
            # Store flag data
            flag_data = {
                "reason": reason,
                "flagged_at": datetime.utcnow().isoformat(),
                "warning_count": warning_count
            }
            
            # Flags expire after 7 days
            self.redis.setex(
                flagged_key,
                7 * 86400,
                json.dumps(flag_data)
            )
            
            logger.warning(f"Flagged agent {agent_id}: {reason} (warning #{warning_count})")
            
        except Exception as e:
            logger.error(f"Error flagging agent {agent_id}: {e}")
    
    def get_usage_stats(self, agent_id: str) -> dict:
        """
        Get rate limit usage statistics for an agent.
        
        Args:
            agent_id: Agent identifier
        
        Returns:
            Dictionary with usage stats
        """
        try:
            if not self.redis:
                return {"error": "Redis not available"}
            
            tier = self.get_agent_tier(agent_id)
            
            # Get current counters
            daily_key = f"{self.AGENT_VOTE_DAY_PREFIX}{agent_id}"
            hourly_key = f"{self.AGENT_VOTE_HOUR_PREFIX}{agent_id}"
            
            daily_count = int(self.redis.get(daily_key) or 0)
            hourly_count = int(self.redis.get(hourly_key) or 0)
            
            daily_limit = tier.get("votes_per_day", "unlimited")
            hourly_limit = tier.get("votes_per_hour", "unlimited")
            
            return {
                "agent_id": agent_id,
                "tier": tier["name"],
                "votes_today": daily_count,
                "votes_today_limit": daily_limit,
                "votes_today_remaining": max(0, daily_limit - daily_count) if daily_limit != "unlimited" else "unlimited",
                "votes_last_hour": hourly_count,
                "votes_last_hour_limit": hourly_limit,
                "votes_last_hour_remaining": max(0, hourly_limit - hourly_count) if hourly_limit != "unlimited" else "unlimited",
            }
            
        except Exception as e:
            logger.error(f"Error getting usage stats for {agent_id}: {e}")
            return {"error": str(e)}


# Singleton instance
rate_limiter = RateLimiter()
