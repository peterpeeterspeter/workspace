"""
Authentication module for aimusicstore.com API

Handles Bearer token authentication for external agents:
- Extracts Bearer token from Authorization header
- Hashes token to get key_hash
- Looks up agent_id via api_keys table
- Validates agent is active and authorized to vote

Usage:
    from api.auth import authenticate_agent
    
    # In vote endpoint:
    agent_id = await authenticate_agent(request)
"""

from fastapi import HTTPException, Request
from api.database import get_db
from api.models import APIKey, Agent
import hashlib


async def authenticate_agent(request: Request) -> str:
    """
    Authenticate agent via Bearer token (API key)
    
    Process:
    1. Parse Authorization header (Bearer <API_KEY>)
    2. Extract token
    3. Hash token (SHA-256) to get key_hash
    4. Lookup api_keys by key_hash where status='active'
    5. Load agent by agent_id
    6. Verify agent status='active'
    7. Update api_keys.last_used_at = now()
    8. Return agent_id
    
    Args:
        request: FastAPI Request object
    
    Returns:
        agent_id: str - Agent ID for authenticated agent
    
    Raises:
        HTTPException 401 if auth fails
    """
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid Authorization header. Format: 'Bearer <API_KEY>'"
        )
    
    # Extract token (remove "Bearer " prefix)
    token = auth_header[7:].strip()
    
    if not token:
        raise HTTPException(
            status_code=401,
            detail="Missing API key token"
        )
    
    # Hash token with SHA-256 to match api_keys.key_hash
    key_hash = hashlib.sha256(token.encode()).hexdigest()
    
    with get_db() as db:
        from sqlalchemy import text
        
        # Look up API key in api_keys table (using new status column)
        api_key = db.query(APIKey).filter(
            APIKey.key_hash == key_hash,
            APIKey.status == 'active'
        ).first()
        
        if not api_key:
            raise HTTPException(
                status_code=401,
                detail="Invalid or revoked API key"
            )
        
        # Get associated agent_id
        agent_id = api_key.agent_id
        
        if not agent_id:
            raise HTTPException(
                status_code=401,
                detail="API key not associated with an agent"
            )
        
        # Verify agent exists and is active (using new status column)
        agent = db.query(Agent).filter(
            Agent.id == agent_id,
            Agent.status == 'active'
        ).first()
        
        if not agent:
            raise HTTPException(
                status_code=401,
                detail="Agent not found or suspended"
            )
        
        # Update last_used timestamp
        db.execute(text("""
            UPDATE api_keys 
            SET last_used = CURRENT_TIMESTAMP 
            WHERE key_hash = :key_hash
        """), {"key_hash": key_hash})
        db.commit()
        
        return agent_id


def get_agent_from_token(token: str) -> dict:
    """
    Get agent details from API token (for internal use)
    
    Args:
        token: API key token
    
    Returns:
        Agent dict with id and details, or None if invalid
    
    Used by: vote endpoint for auth before vote processing
    """
    key_hash = hashlib.sha256(token.encode()).hexdigest()
    
    with get_db() as db:
        # Look up API key (using new status column)
        api_key = db.query(APIKey).filter(
            APIKey.key_hash == key_hash,
            APIKey.status == 'active'
        ).first()
        
        if not api_key:
            return None
        
        # Look up agent (using new status column)
        agent = db.query(Agent).filter(
            Agent.id == api_key.agent_id,
            Agent.status == 'active'
        ).first()
        
        if not agent:
            return None
        
        return {
            "id": agent.id,
            "reputation_score": agent.reputation_score,
            "status": agent.status,
            "created_at": agent.created_at.isoformat() if agent.created_at else None,
            "last_vote_at": agent.last_vote_at.isoformat() if agent.last_vote_at else None,
            "api_key_id": api_key.key_id
        }


if __name__ == "__main__":
    # Quick test
    import asyncio
    from fastapi import Request
    
    async def test_auth():
        """Test auth function"""
        class MockRequest:
            def __init__(self):
                self.headers = {"Authorization": "Bearer test_token_12345"}
        
        request = MockRequest()
        
        try:
            result = await authenticate_agent(request)
            print(f"✅ Auth passed: agent_id = {result}")
        except HTTPException as e:
            print(f"❌ Auth failed: {e.detail}")
    
    asyncio.run(test_auth())
