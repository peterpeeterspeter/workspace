"""
Agent registration router for aimusicstore.com
Enables autonomous agents to self-register
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel, Field
from typing import Optional, Dict
import uuid
import secrets
import hashlib
from datetime import datetime
import sys
from pathlib import Path

# Add api directory to Python path
api_dir = Path(__file__).parent.parent.parent / "api"
sys.path.insert(0, str(api_dir))

try:
    from api.database import get_db
    from api.models import Agent, APIKey
except ImportError:
    # Fallback for direct execution
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "api"))
    from database import get_db
    from models import Agent, APIKey

router = APIRouter(prefix="/api/v1/agents", tags=["agents"])


class AgentRegistrationRequest(BaseModel):
    """Request schema for agent registration"""
    name: str = Field(..., description="Agent name/handle")
    type: str = Field(..., description="Agent type: 'autonomous' or 'human'")
    preferences: Optional[Dict] = Field(default=None, description="Genre/mood preferences")
    description: Optional[str] = Field(default=None, description="Agent description/bio")


class AgentRegistrationResponse(BaseModel):
    """Response schema for agent registration"""
    agent_id: str
    api_key: str
    reputation: int
    tier: str
    status: str
    created_at: str
    message: str


@router.post("/register", response_model=AgentRegistrationResponse)
async def register_agent(request: AgentRegistrationRequest):
    """
    Register a new autonomous or human agent
    
    - Validates request
    - Checks for duplicates
    - Creates agent with unique ID
    - Generates and stores API key
    - Returns credentials (API key shown only once!)
    
    **Note:** Copy the API key immediately - it won't be shown again!
    """
    
    # Generate unique agent ID
    agent_id = f"agent-{uuid.uuid4().hex[:8]}"
    
    # Generate API key (shown only once!)
    raw_api_key = f"sk_live_{secrets.token_urlsafe(32)}"
    
    # Hash the API key for storage (SHA-256)
    api_key_hash = hashlib.sha256(raw_api_key.encode()).hexdigest()
    
    # Generate key_id (public identifier)
    key_id = f"key_{uuid.uuid4().hex[:12]}"
    
    # Validate agent type
    if request.type not in ["autonomous", "human"]:
        raise HTTPException(
            status_code=400,
            detail="Invalid agent type. Must be 'autonomous' or 'human'"
        )
    
    # Validate preferences JSON
    if request.preferences and not isinstance(request.preferences, dict):
        raise HTTPException(
            status_code=400,
            detail="Preferences must be a JSON object"
        )
    
    try:
        with get_db() as db:
            # Check if agent name already exists (optional uniqueness check)
            existing_agent = db.query(Agent).filter(Agent.id == agent_id).first()
            if existing_agent:
                raise HTTPException(
                    status_code=400,
                    detail=f"Agent ID already exists: {agent_id}"
                )
            
            # Determine tier based on type
            tier = "starter" if request.type == "autonomous" else "verified"
            
            # Create agent (Agent model only has: id, reputation_score, created_at, last_vote_at)
            new_agent = Agent(
                id=agent_id,
                reputation_score=0
            )
            db.add(new_agent)
            db.flush()  # Get the agent ID
            
            # Create API key entry
            new_api_key = APIKey(
                key_id=key_id,
                name=f"{request.name} - {request.type} agent",
                key_hash=api_key_hash,
                tier=tier,
                agent_id=agent_id,
                is_active=True
            )
            db.add(new_api_key)
            
            db.commit()
            
            return {
                "agent_id": agent_id,
                "api_key": raw_api_key,  # Only shown once!
                "reputation": 0,
                "tier": tier,
                "status": "registered",
                "created_at": datetime.utcnow().isoformat(),
                "message": "⚠️ Copy this API key now - it won't be shown again!"
            }
            
    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Registration failed: {str(e)}"
        )


@router.get("/me")
async def get_current_agent(agent_id: str = Query(..., description="Agent ID")):
    """
    Get current agent information by ID
    
    Returns:
    - Agent ID
    - Reputation score
    - Creation date
    - Last vote timestamp
    - Associated API keys (count only)
    """
    try:
        with get_db() as db:
            # Query agent
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            
            if not agent:
                raise HTTPException(
                    status_code=404,
                    detail=f"Agent not found: {agent_id}"
                )
            
            # Count API keys for this agent
            api_key_count = db.query(APIKey).filter(
                APIKey.agent_id == agent_id,
                APIKey.is_active == True
            ).count()
            
            return {
                "agent_id": agent.id,
                "reputation_score": agent.reputation_score,
                "created_at": agent.created_at.isoformat() if agent.created_at else None,
                "last_vote_at": agent.last_vote_at.isoformat() if agent.last_vote_at else None,
                "api_keys": {
                    "active_count": api_key_count
                }
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to retrieve agent: {str(e)}"
        )


@router.get("/list")
async def list_agents(limit: int = Query(50, description="Maximum agents to return")):
    """
    List all registered agents (Admin endpoint)
    
    Returns paginated list of agents with their reputation scores.
    """
    try:
        with get_db() as db:
            agents = db.query(Agent).order_by(
                Agent.reputation_score.desc()
            ).limit(limit).all()
            
            result = []
            for agent in agents:
                # Count active API keys
                api_key_count = db.query(APIKey).filter(
                    APIKey.agent_id == agent.id,
                    APIKey.is_active == True
                ).count()
                
                result.append({
                    "agent_id": agent.id,
                    "reputation_score": agent.reputation_score,
                    "created_at": agent.created_at.isoformat() if agent.created_at else None,
                    "last_vote_at": agent.last_vote_at.isoformat() if agent.last_vote_at else None,
                    "api_keys_count": api_key_count
                })
            
            return {
                "count": len(result),
                "agents": result
            }
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list agents: {str(e)}"
        )
