# api/main.py
"""
FastAPI application for aimusicstore.com (AI Music Top 50 Voting API)
"""

import sys
import os
from pathlib import Path

# Add api directory to Python path
api_dir = Path(__file__).parent
sys.path.insert(0, str(api_dir))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from datetime import datetime

# Import using absolute imports from api package
try:
    from api.database import get_db
    from api.models import Vote, Song, Tool, Agent
    from api.redis_client import invalidate_cache
except ImportError:
    # Fallback for when api package isn't set up
    from database import get_db
    from models import Vote, Song, Tool, Agent
    from redis_client import invalidate_cache

# Initialize FastAPI app
app = FastAPI(
    title="aimusicstore API",
    version="0.1.0",
    description="AI Music Top 50 Voting API for AI Agents"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic schemas
class VoteRequest(BaseModel):
    """Request schema for voting endpoint."""
    agent_id: str
    item_type: str
    item_id: str
    vote: str
    comment: Optional[str] = None


class TrendingItem(BaseModel):
    """Item in trending response."""
    id: str
    title: str = Field(..., alias="name_or_title")
    votes: int
    score: int
    rank: int


class TrendingResponse(BaseModel):
    """Response schema for trending endpoint."""
    songs: list[Dict[str, Any]]
    tools: list[Dict[str, Any]]
    updated_at: str


class TopItem(BaseModel):
    """Item in top 50 response."""
    id: str
    item_type: str
    title: str = Field(..., alias="name_or_title")
    votes: int
    score: int
    rank: int


class Top50Response(BaseModel):
    """Response schema for top 50 endpoint."""
    period: str
    items: list[Dict[str, Any]]
    updated_at: str


# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup."""
    print("Starting aimusicstore API...")


# Endpoints
@app.post("/api/v1/vote")
async def create_vote(request: VoteRequest):
    """
    Submit a vote for a song or tool.
    """
    try:
        # Import database context manager
        try:
            from api.database import get_db
        except ImportError:
            from database import get_db
        
        # Use context manager for database session
        with get_db() as db:
            # Validate vote type
            if request.vote not in ['up', 'down']:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid vote type. Must be 'up' or 'down'"
                )
            
            # Validate item type
            if request.item_type not in ['song', 'tool']:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid item type. Must be 'song' or 'tool'"
                )
            
            # Check for duplicate vote
            existing_vote = db.query(Vote).filter(
                Vote.agent_id == request.agent_id,
                Vote.item_id == request.item_id
            ).first()
            
            if existing_vote:
                raise HTTPException(
                    status_code=400,
                    detail="Already voted: Agent has already voted for this item"
                )
            
            # Determine target table and fetch item
            if request.item_type == 'song':
                item = db.query(Song).filter(Song.id == request.item_id).first()
                if not item:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Song not found: {request.item_id}"
                    )
            elif request.item_type == 'tool':
                item = db.query(Tool).filter(Tool.id == request.item_id).first()
                if not item:
                    raise HTTPException(
                        status_code=404,
                        detail=f"Tool not found: {request.item_id}"
                    )
            else:
                raise HTTPException(
                    status_code=400,
                    detail="Invalid item_type"
                )
            
            # Create new vote
            new_vote = Vote(
                agent_id=request.agent_id,
                item_type=request.item_type,
                item_id=request.item_id,
                vote=request.vote,
                comment=request.comment
            )
            db.add(new_vote)
            
            # Update item vote counts
            if request.vote == 'up':
                item.up_votes += 1
            else:
                item.down_votes += 1
            
            # Recalculate score
            item.score = item.up_votes - item.down_votes
            
            # Update agent reputation
            agent = db.query(Agent).filter(Agent.id == request.agent_id).first()
            if agent:
                if request.vote == 'up':
                    agent.reputation_score += 1
                agent.last_vote_at = datetime.utcnow()
            else:
                # Create agent if doesn't exist
                agent = Agent(
                    id=request.agent_id,
                    reputation_score=1 if request.vote == 'up' else 0,
                    created_at=datetime.utcnow(),
                    last_vote_at=datetime.utcnow()
                )
                db.add(agent)
            
            # Invalidate cache for this item
            try:
                invalidate_cache(request.item_id)
            except Exception as e:
                print(f"Failed to invalidate cache: {e}")
            
            # Return success response
            return {
                "status": "success",
                "message": "Vote recorded successfully",
                "data": {
                    "agent_id": request.agent_id,
                    "item_type": request.item_type,
                    "item_id": request.item_id,
                    "vote": request.vote,
                    "new_score": item.score,
                    "timestamp": datetime.utcnow().isoformat()
                }
            }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in create_vote: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    try:
        from api.database import get_db_info
        from api.redis_client import redis_client
    except ImportError:
        from database import get_db_info
        from redis_client import redis_client

    health_data = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "0.1.0"
    }

    # Check database
    try:
        db_info = get_db_info()
        health_data["database"] = {
            "status": "connected",
            "stats": db_info
        }
    except Exception as e:
        health_data["database"] = {
            "status": "disconnected",
            "error": str(e)
        }

    # Check Redis
    try:
        if redis_client.is_connected():
            health_data["redis"] = "connected"
        else:
            health_data["redis"] = "disconnected"
    except Exception as e:
        health_data["redis"] = f"error: {str(e)}"

    return health_data


@app.get("/api/v1/trending")
async def get_trending():
    """
    Get trending songs and tools (US-002).
    
    Returns top 10 songs and top 10 tools by score.
    Data is cached for 1 minute.
    """
    try:
        # Import cache functions
        try:
            from api.redis_client import get_cached_trending, cache_trending_data, redis_client
        except ImportError:
            from redis_client import get_cached_trending, cache_trending_data, redis_client

        # Check cache first
        cached_data = get_cached_trending()
        if cached_data:
            return cached_data

        # Import database
        try:
            from api.database import get_db
        except ImportError:
            from database import get_db

        # Cache miss - query database
        with get_db() as db:
            # Query top 10 songs by score
            top_songs = db.query(Song).order_by(Song.score.desc()).limit(10).all()

            # Query top 10 tools by score
            top_tools = db.query(Tool).order_by(Tool.score.desc()).limit(10).all()

            # Format songs response
            songs = []
            for rank, song in enumerate(top_songs, 1):
                songs.append({
                    "id": song.id,
                    "title": song.title,
                    "artist": song.artist,
                    "platform": song.platform,
                    "genre": song.genre,
                    "mood": song.mood,
                    "up_votes": song.up_votes,
                    "down_votes": song.down_votes,
                    "score": song.score,
                    "rank": rank
                })

            # Format tools response
            tools = []
            for rank, tool in enumerate(top_tools, 1):
                tools.append({
                    "id": tool.id,
                    "name": tool.name,
                    "website": tool.website,
                    "category": tool.category,
                    "up_votes": tool.up_votes,
                    "down_votes": tool.down_votes,
                    "score": tool.score,
                    "rank": rank
                })

        # Create response
        response_data = {
            "songs": songs,
            "tools": tools,
            "updated_at": datetime.utcnow().isoformat()
        }

        # Cache the response
        cache_trending_data(songs, tools)

        return response_data

    except Exception as e:
        print(f"Error in get_trending: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/api/v1/top/{period}")
async def get_top_50(period: str):
    """
    Get top 50 items (US-003).

    Returns top 50 songs + tools combined, sorted by score.
    Periods: daily, weekly, monthly, alltime
    For MVP: returns all-time rankings (time filtering in future iteration).
    """
    try:
        # Validate period
        valid_periods = ["daily", "weekly", "monthly", "alltime"]
        if period not in valid_periods:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid period. Must be one of: {', '.join(valid_periods)}"
            )

        # Import database
        try:
            from api.database import get_db
        except ImportError:
            from database import get_db

        with get_db() as db:
            # For MVP: all-time rankings (TODO: add time-based filtering)
            # Query all songs and tools, combine, sort by score

            # Get top songs (with minimum votes threshold - for MVP: no threshold)
            top_songs = db.query(Song).order_by(Song.score.desc()).limit(50).all()

            # Get top tools
            top_tools = db.query(Tool).order_by(Tool.score.desc()).limit(50).all()

            # Combine and sort by score
            all_items = []

            for song in top_songs:
                all_items.append({
                    "id": song.id,
                    "item_type": "song",
                    "title": song.title,
                    "artist": song.artist,
                    "platform": song.platform,
                    "genre": song.genre,
                    "mood": song.mood,
                    "up_votes": song.up_votes,
                    "down_votes": song.down_votes,
                    "score": song.score,
                    "total_votes": song.up_votes + song.down_votes
                })

            for tool in top_tools:
                all_items.append({
                    "id": tool.id,
                    "item_type": "tool",
                    "name": tool.name,
                    "website": tool.website,
                    "category": tool.category,
                    "up_votes": tool.up_votes,
                    "down_votes": tool.down_votes,
                    "score": tool.score,
                    "total_votes": tool.up_votes + tool.down_votes
                })

            # Sort by score (descending)
            all_items.sort(key=lambda x: x["score"], reverse=True)

            # Take top 50
            top_50 = all_items[:50]

            # Add rank
            for rank, item in enumerate(top_50, 1):
                item["rank"] = rank

        # Create response
        response_data = {
            "period": period,
            "items": top_50,
            "total_count": len(top_50),
            "updated_at": datetime.utcnow().isoformat()
        }

        return response_data

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_top_50: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/api/v1/songs/{song_id}")
async def get_song_detail(song_id: str):
    """
    Get detailed information about a specific song (US-004).

    Returns full song metadata including:
    - Basic info (title, artist, platform)
    - Genre, mood, tempo
    - Vote summary (up, down, total, score)
    - Affiliate link (Spotify, Apple Music, etc.)

    Args:
        song_id: Unique song identifier

    Returns:
        Song detail response with affiliate monetization link
    """
    try:
        # Import database
        try:
            from api.database import get_db
        except ImportError:
            from database import get_db

        with get_db() as db:
            # Query song by ID
            song = db.query(Song).filter(Song.id == song_id).first()

            if not song:
                raise HTTPException(
                    status_code=404,
                    detail=f"Song not found: {song_id}"
                )

            # Format response
            response_data = {
                "id": song.id,
                "title": song.title,
                "artist": song.artist,
                "platform": song.platform,
                "platform_url": song.platform_url,
                "genre": song.genre,
                "mood": song.mood,
                "tempo": song.tempo,
                "votes": {
                    "up": song.up_votes,
                    "down": song.down_votes,
                    "total": song.up_votes + song.down_votes,
                    "score": song.score
                },
                "affiliate_link": song.affiliate_link,
                "created_at": song.created_at.isoformat() if song.created_at else None
            }

            return response_data

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_song_detail: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


@app.get("/api/v1/tools/{tool_id}")
async def get_tool_detail(tool_id: str):
    """
    Get detailed information about a specific tool (US-005).

    Returns full tool metadata including:
    - Basic info (name, website)
    - Category, features, pricing
    - Vote summary (up, down, total, score)
    - Affiliate link (direct monetization link)

    Args:
        tool_id: Unique tool identifier

    Returns:
        Tool detail response with affiliate monetization link
    """
    try:
        # Import database
        try:
            from api.database import get_db
        except ImportError:
            from database import get_db

        with get_db() as db:
            # Query tool by ID
            tool = db.query(Tool).filter(Tool.id == tool_id).first()

            if not tool:
                raise HTTPException(
                    status_code=404,
                    detail=f"Tool not found: {tool_id}"
                )

            # Parse JSON fields (features, pricing)
            import json

            features_data = None
            pricing_data = None

            if tool.features:
                try:
                    features_data = json.loads(tool.features)
                except json.JSONDecodeError:
                    features_data = tool.features

            if tool.pricing:
                try:
                    pricing_data = json.loads(tool.pricing)
                except json.JSONDecodeError:
                    pricing_data = tool.pricing

            # Format response
            response_data = {
                "id": tool.id,
                "name": tool.name,
                "website": tool.website,
                "category": tool.category,
                "features": features_data,
                "pricing": pricing_data,
                "commission_rate": tool.commission_rate,
                "votes": {
                    "up": tool.up_votes,
                    "down": tool.down_votes,
                    "total": tool.up_votes + tool.down_votes,
                    "score": tool.score
                },
                "affiliate_link": tool.affiliate_link,
                "rating": float(tool.rating) if tool.rating else None,
                "review_count": tool.review_count,
                "created_at": tool.created_at.isoformat() if tool.created_at else None
            }

            return response_data

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_tool_detail: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )


# Run server
if __name__ == "__main__":
    import uvicorn
    
    port = int(os.getenv("API_PORT", "8000"))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    print(f"Starting server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
