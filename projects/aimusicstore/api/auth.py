# api/auth.py
"""
API Authentication for aimusicstore.com

Provides:
- API key authentication
- Tier-based access control (Free, Pro, Enterprise)
- Token-based authentication (JWT optional)
- API key management endpoints
"""

import os
import secrets
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, List, ClassVar
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(env_path)

logger = logging.getLogger(__name__)

# Try to import database models
try:
    from api.database import get_db
    from api.models import APIKey, Agent
except ImportError:
    from database import get_db
    from models import APIKey, Agent


class AccessTier(BaseModel):
    """Access tier for API keys."""
    
    FREE: str = "free"
    PRO: str = "pro"
    ENTERPRISE: str = "enterprise"
    
    # Rate limits per tier (ClassVar - not a field)
    LIMITS: ClassVar[Dict[str, Dict]] = {
        "free": {
            "votes_per_day": 100,
            "votes_per_hour": 20,
            "requests_per_minute": 60,
            "features": ["basic_voting", "trending", "top_50"]
        },
        "pro": {
            "votes_per_day": 1000,
            "votes_per_hour": 200,
            "requests_per_minute": 300,
            "features": ["basic_voting", "trending", "top_50", "item_details", "affiliate_links"]
        },
        "enterprise": {
            "votes_per_day": None,  # Unlimited
            "votes_per_hour": None,
            "requests_per_minute": 1000,
            "features": ["all"]  # All features available
        }
    }


class APIKeyCreate(BaseModel):
    """Schema for creating API key."""
    name: str = Field(..., description="Name/label for the API key")
    tier: str = Field(default="free", description="Access tier: free, pro, enterprise")
    agent_id: Optional[str] = Field(None, description="Associated agent ID (if applicable)")


class APIKeyResponse(BaseModel):
    """Schema for API key response."""
    key_id: str
    name: str
    tier: str
    agent_id: Optional[str]
    is_active: bool
    created_at: str
    last_used: Optional[str]
    expires_at: Optional[str]
    rate_limits: Dict[str, Optional[int]]


class APIKeyAuthenticator:
    """
    API key authentication and validation.
    
    Features:
    - API key generation (secure random tokens)
    - Tier-based access control
    - Key validation and expiration
    - Usage tracking
    """
    
    def __init__(self):
        """Initialize API key authenticator."""
        self.secret_key = os.getenv('API_SECRET_KEY', secrets.token_hex(32))
        self.algorithm = "HS256"
        self.default_expiry_days = int(os.getenv('API_KEY_DEFAULT_EXPIRY_DAYS', '365'))
    
    def generate_api_key(self, name: str, tier: str = "free", agent_id: Optional[str] = None) -> tuple[str, str]:
        """
        Generate a new API key.
        
        Args:
            name: Name/label for the key
            tier: Access tier (free, pro, enterprise)
            agent_id: Associated agent ID (optional)
        
        Returns:
            tuple: (key_id, api_key)
        """
        # Generate unique key ID
        key_id = secrets.token_urlsafe(16)
        
        # Generate secure API key
        api_key_prefix = "aimusic_"
        api_key_suffix = secrets.token_urlsafe(32)
        api_key = f"{api_key_prefix}{api_key_suffix}"
        
        # Hash the key for storage (don't store raw key)
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        # Calculate expiration
        created_at = datetime.now()
        expires_at = created_at + timedelta(days=self.default_expiry_days) if self.default_expiry_days > 0 else None
        
        # Store in database
        try:
            with get_db() as db:
            
                new_key = APIKey(
                    key_id=key_id,
                    name=name,
                    key_hash=key_hash,
                    tier=tier,
                    agent_id=agent_id,
                    is_active=True,
                    created_at=created_at,
                    expires_at=expires_at
                )
                
                db.add(new_key)
                db.commit()
                db.refresh(new_key)
                
                logger.info(f"✅ API key created: {key_id} ({tier})")
                return key_id, api_key
                
        except Exception as e:
            logger.error(f"❌ Failed to create API key: {e}")
            raise
    
    def validate_api_key(self, api_key: str) -> Optional[Dict]:
        """
        Validate API key and return key details.
        
        Args:
            api_key: API key to validate
        
        Returns:
            dict: Key details if valid, None otherwise
        """
        if not api_key:
            return None
        
        # Hash the provided key
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        try:
            with get_db() as db:
                # Query for active, non-expired key
                key_record = db.query(APIKey).filter(
                    APIKey.key_hash == key_hash,
                    APIKey.is_active == True
                ).first()
                
                if not key_record:
                    logger.warning(f"Invalid API key attempted")
                    return None
                
                # Check expiration
                if key_record.expires_at and key_record.expires_at < datetime.now():
                    logger.warning(f"Expired API key attempted: {key_record.key_id}")
                    return None
                
                # Update last used timestamp
                key_record.last_used = datetime.now()
                db.commit()
                
                # Get tier limits
                tier_limits = AccessTier.LIMITS.get(key_record.tier, AccessTier.LIMITS["free"])
                
                return {
                    "key_id": key_record.key_id,
                    "name": key_record.name,
                    "tier": key_record.tier,
                    "agent_id": key_record.agent_id,
                    "rate_limits": {
                        "votes_per_day": tier_limits.get("votes_per_day"),
                        "votes_per_hour": tier_limits.get("votes_per_hour"),
                        "requests_per_minute": tier_limits.get("requests_per_minute")
                    },
                    "features": tier_limits.get("features", [])
                }
                
        except Exception as e:
            logger.error(f"❌ API key validation error: {e}")
            return None
    
    def list_api_keys(self, agent_id: Optional[str] = None) -> List[APIKeyResponse]:
        """
        List API keys, optionally filtered by agent.
        
        Args:
            agent_id: Filter by agent ID (optional)
        
        Returns:
            List of API key responses
        """
        try:
            with get_db() as db:
                query = db.query(APIKey)
                if agent_id:
                    query = query.filter(APIKey.agent_id == agent_id)
                
                keys = query.order_by(APIKey.created_at.desc()).all()
                
                result = []
                for key in keys:
                    tier_limits = AccessTier.LIMITS.get(key.tier, AccessTier.LIMITS["free"])
                    
                    result.append(APIKeyResponse(
                        key_id=key.key_id,
                        name=key.name,
                        tier=key.tier,
                        agent_id=key.agent_id,
                        is_active=key.is_active,
                        created_at=key.created_at.isoformat(),
                        last_used=key.last_used.isoformat() if key.last_used else None,
                        expires_at=key.expires_at.isoformat() if key.expires_at else None,
                        rate_limits={
                            "votes_per_day": tier_limits.get("votes_per_day"),
                            "votes_per_hour": tier_limits.get("votes_per_hour"),
                            "requests_per_minute": tier_limits.get("requests_per_minute")
                        }
                    ))
                
                return result
            
        except Exception as e:
            logger.error(f"❌ Failed to list API keys: {e}")
            return []
    
    def revoke_api_key(self, key_id: str) -> bool:
        """
        Revoke (deactivate) an API key.
        
        Args:
            key_id: Key ID to revoke
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with get_db() as db:
                key = db.query(APIKey).filter(APIKey.key_id == key_id).first()
                
                if not key:
                    logger.warning(f"API key not found: {key_id}")
                    return False
                
                key.is_active = False
                key.revoked_at = datetime.now()
                db.commit()
                
                logger.info(f"✅ API key revoked: {key_id}")
                return True
            
        except Exception as e:
            logger.error(f"❌ Failed to revoke API key: {e}")
            return False
    
    def update_api_key_tier(self, key_id: str, new_tier: str) -> bool:
        """
        Update API key tier.
        
        Args:
            key_id: Key ID to update
            new_tier: New tier (free, pro, enterprise)
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with get_db() as db:
                key = db.query(APIKey).filter(APIKey.key_id == key_id).first()
                
                if not key:
                    logger.warning(f"API key not found: {key_id}")
                    return False
                
                key.tier = new_tier
                db.commit()
                
                logger.info(f"✅ API key tier updated: {key_id} -> {new_tier}")
                return True
            
        except Exception as e:
            logger.error(f"❌ Failed to update API key tier: {e}")
            return False


# Global authenticator instance
authenticator = APIKeyAuthenticator()


def require_api_key(api_key: str) -> Optional[Dict]:
    """
    Validate and return API key details.
    
    Convenience function for use in endpoints.
    
    Args:
        api_key: API key from request header
    
    Returns:
        dict: Key details if valid, None otherwise
    """
    return authenticator.validate_api_key(api_key)


def check_feature_access(api_key_details: Dict, feature: str) -> bool:
    """
    Check if API key has access to specific feature.
    
    Args:
        api_key_details: Details from validate_api_key()
        feature: Feature to check (e.g., "basic_voting", "affiliate_links")
    
    Returns:
        bool: True if has access, False otherwise
    """
    if not api_key_details:
        return False
    
    features = api_key_details.get("features", [])
    
    # Enterprise has access to all features
    if "all" in features:
        return True
    
    return feature in features


if __name__ == "__main__":
    # Test API key generation
    import logging
    logging.basicConfig(level=logging.INFO)
    
    print("Testing API key generation...")
    
    try:
        # Generate test key
        key_id, api_key = authenticator.generate_api_key(
            name="Test Key",
            tier="pro",
            agent_id=None  # No agent for test key
        )
        
        print(f"✅ API Key Generated:")
        print(f"   Key ID: {key_id}")
        print(f"   API Key: {api_key}")
        
        # Validate the key
        details = authenticator.validate_api_key(api_key)
        print(f"\n✅ Key Validation:")
        print(f"   Name: {details.get('name')}")
        print(f"   Tier: {details.get('tier')}")
        print(f"   Features: {details.get('features')}")
        print(f"   Rate Limits: {details.get('rate_limits')}")
        
        # Test feature access
        print(f"\n✅ Feature Access:")
        print(f"   Basic Voting: {check_feature_access(details, 'basic_voting')}")
        print(f"   Affiliate Links: {check_feature_access(details, 'affiliate_links')}")
        
        # Test invalid key
        invalid_details = authenticator.validate_api_key("invalid_key_123")
        print(f"\n✅ Invalid Key Test: {invalid_details is None}")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
