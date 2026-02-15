"""
Discovery router for aimusicstore.com
Enables agents to discover tracks and tools needing votes
"""

from fastapi import APIRouter, HTTPException, Query, Depends
from pydantic import BaseModel
from typing import Optional, Dict, List
import json
import random
import sys
from pathlib import Path

# Add api directory to Python path
api_dir = Path(__file__).parent.parent.parent / "api"
sys.path.insert(0, str(api_dir))

try:
    from api.database import get_db
    from api.models import Song, Tool, Agent, Vote
except ImportError:
    # Fallback for direct execution
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "api"))
    from database import get_db
    from models import Song, Tool, Agent, Vote

router = APIRouter(prefix="/api/v1/discovery", tags=["discovery"])


class DiscoveryResponse(BaseModel):
    """Response schema for discovery endpoint"""
    agent_id: str
    queue_type: str  # "songs", "tools", or "mixed"
    items: List[Dict]
    count: int
    preferences_matched: int


@router.get("/discover")
async def discover_items(
    agent_id: str = Query(..., description="Agent ID to fetch preferences for"),
    item_type: Optional[str] = Query(None, description="Filter: 'song', 'tool', or None for mixed"),
    limit: int = Query(10, ge=1, le=50, description="Number of items to return (1-50)"),
    genre: Optional[str] = Query(None, description="Filter by genre (songs only)"),
    mood: Optional[str] = Query(None, description="Filter by mood (songs only)"),
    category: Optional[str] = Query(None, description="Filter by category (tools only)")
):
    """
    Discover items (songs/tools) needing votes based on agent preferences
    
    Priority system:
    1. Items matching agent's preferred genres/moods/categories
    2. Items with fewer votes (cold start prevention)
    3. Randomized to prevent bias
    
    Returns:
        - Queue of items needing votes
        - Matched preference count
        - Agent preferences used for filtering
    """
    
    try:
        with get_db() as db:
            # Get agent preferences
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            
            if not agent:
                raise HTTPException(
                    status_code=404,
                    detail=f"Agent not found: {agent_id}"
                )
            
            # Get agent's votes to avoid items already voted on
            voted_item_ids = db.query(Vote.item_id).filter(
                Vote.agent_id == agent_id
            ).all()
            voted_ids_set = {vote[0] for vote in voted_item_ids}
            
            # Parse agent preferences (stored as JSON string in Agent model)
            # Note: Current Agent model doesn't have preferences field, so we'll use empty defaults
            agent_preferences = {
                "genres": [],
                "moods": [],
                "categories": []
            }
            
            # Build query based on item_type
            items = []
            preferences_matched = 0
            
            if item_type == "song" or item_type is None:
                # Query songs needing votes
                songs_query = db.query(Song).filter(
                    ~Song.id.in_(voted_ids_set)  # Exclude already voted
                )
                
                # Apply filters if provided
                if genre:
                    songs_query = songs_query.filter(Song.genre == genre)
                elif agent_preferences["genres"]:
                    # Use agent's preferred genres
                    songs_query = songs_query.filter(Song.genre.in_(agent_preferences["genres"]))
                
                if mood:
                    songs_query = songs_query.filter(Song.mood == mood)
                elif agent_preferences["moods"]:
                    # Use agent's preferred moods
                    songs_query = songs_query.filter(Song.mood.in_(agent_preferences["moods"]))
                
                # Order by vote count (asc) to prioritize cold start items, then randomize
                songs = songs_query.order_by(
                    (Song.up_votes + Song.down_votes).asc()
                ).limit(limit * 2).all()  # Get extra, then randomize
                
                # Randomize and limit
                random.shuffle(songs)
                songs = songs[:limit]
                
                # Count preference matches
                for song in songs:
                    if agent_preferences["genres"] and song.genre in agent_preferences["genres"]:
                        preferences_matched += 1
                    elif agent_preferences["moods"] and song.mood in agent_preferences["moods"]:
                        preferences_matched += 1
                
                # Format songs
                for song in songs:
                    items.append({
                        "id": song.id,
                        "type": "song",
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
                        "weighted_score": song.weighted_score,
                        "affiliate_link": song.affiliate_link
                    })
            
            if item_type == "tool" or item_type is None:
                # Query tools needing votes
                tools_query = db.query(Tool).filter(
                    ~Tool.id.in_(voted_ids_set)  # Exclude already voted
                )
                
                # Apply filters if provided
                if category:
                    tools_query = tools_query.filter(Tool.category == category)
                elif agent_preferences["categories"]:
                    # Use agent's preferred categories
                    tools_query = tools_query.filter(Tool.category.in_(agent_preferences["categories"]))
                
                # Order by vote count (asc) to prioritize cold start items, then randomize
                tools = tools_query.order_by(
                    (Tool.up_votes + Tool.down_votes).asc()
                ).limit(limit * 2).all()  # Get extra, then randomize
                
                # Randomize and limit
                random.shuffle(tools)
                tools = tools[:limit]
                
                # Count preference matches
                for tool in tools:
                    if agent_preferences["categories"] and tool.category in agent_preferences["categories"]:
                        preferences_matched += 1
                
                # Format tools
                for tool in tools:
                    # Parse JSON fields
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
                    
                    items.append({
                        "id": tool.id,
                        "type": "tool",
                        "name": tool.name,
                        "website": tool.website,
                        "category": tool.category,
                        "features": features_data,
                        "pricing": pricing_data,
                        "votes": {
                            "up": tool.up_votes,
                            "down": tool.down_votes,
                            "total": tool.up_votes + tool.down_votes,
                            "score": tool.score
                        },
                        "weighted_score": tool.weighted_score,
                        "affiliate_link": tool.affiliate_link,
                        "commission_rate": tool.commission_rate,
                        "rating": float(tool.rating) if tool.rating else None,
                        "review_count": tool.review_count
                    })
            
            # If mixed query, randomize the combined list
            if item_type is None:
                random.shuffle(items)
                items = items[:limit]
            
            return DiscoveryResponse(
                agent_id=agent_id,
                queue_type=item_type or "mixed",
                items=items,
                count=len(items),
                preferences_matched=preferences_matched
            )
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Discovery failed: {str(e)}"
        )


@router.get("/stats")
async def get_discovery_stats(
    agent_id: str = Query(..., description="Agent ID to get stats for")
):
    """
    Get discovery statistics for an agent
    
    Returns:
        - Total items in database
        - Items remaining to vote on
        - Agent's voting history count
        - Coverage by genre/mood/category
    """
    
    try:
        with get_db() as db:
            # Verify agent exists
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            
            if not agent:
                raise HTTPException(
                    status_code=404,
                    detail=f"Agent not found: {agent_id}"
                )
            
            # Get counts
            total_songs = db.query(Song).count()
            total_tools = db.query(Tool).count()
            total_items = total_songs + total_tools
            
            # Get agent's voted items
            voted_count = db.query(Vote).filter(Vote.agent_id == agent_id).count()
            
            # Get unique items voted on
            unique_voted = db.query(Vote.item_id).filter(
                Vote.agent_id == agent_id
            ).distinct().count()
            
            # Get genre distribution for songs
            from sqlalchemy import func
            genre_dist = db.query(
                Song.genre,
                func.count(Song.id).label('count')
            ).group_by(Song.genre).all()
            
            genres = {g[0]: g[1] for g in genre_dist}
            
            # Get category distribution for tools
            category_dist = db.query(
                Tool.category,
                func.count(Tool.id).label('count')
            ).group_by(Tool.category).all()
            
            categories = {c[0]: c[1] for c in category_dist}
            
            return {
                "agent_id": agent_id,
                "database": {
                    "total_items": total_items,
                    "total_songs": total_songs,
                    "total_tools": total_tools,
                    "genres": genres,
                    "categories": categories
                },
                "agent_progress": {
                    "votes_cast": voted_count,
                    "unique_items_voted": unique_voted,
                    "items_remaining": total_items - unique_voted,
                    "coverage_percent": round((unique_voted / total_items * 100), 2) if total_items > 0 else 0
                }
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get discovery stats: {str(e)}"
        )
