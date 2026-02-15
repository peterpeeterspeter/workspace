# api/reputation.py
"""
Weighted score calculation for reputation-weighted rankings (US-007).

Instead of counting votes equally, weight them by agent reputation.
High-reputation agents have more influence on rankings.
"""

from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func
import logging

try:
    from api.models import Vote, Agent, Song, Tool
except ImportError:
    from models import Vote, Agent, Song, Tool

logger = logging.getLogger(__name__)


def calculate_weighted_score(db: Session, item_type: str, item_id: str) -> int:
    """
    Calculate weighted score for a song or tool.
    
    Weighted score = sum(up_vote_weights) - sum(down_vote_weights)
    
    IMPORTANT: Uses weight_applied snapshot from votes table, NOT live agent reputation!
    This prevents retroactive manipulation when agent reputation changes.
    
    Args:
        db: Database session
        item_type: 'song' or 'tool'
        item_id: Item ID
    
    Returns:
        Weighted score (integer)
    
    Example:
        Vote 1: weight_applied=90, vote='up' → +90
        Vote 2: weight_applied=30, vote='up' → +30
        Vote 3: weight_applied=10, vote='down' → -10
        Weighted score = 90 + 30 - 10 = 110
    """
    try:
        # Get all votes for this item with their weight_applied snapshots
        votes = db.query(Vote).filter(
            Vote.item_type == item_type,
            Vote.item_id == item_id
        ).all()
        
        if not votes:
            return 0
        
        # Calculate weighted score using weight_applied snapshot
        weighted_score = 0
        for vote in votes:
            weight = vote.weight_applied if vote.weight_applied else 0
            
            if vote.vote == 'up' or vote.vote == 1:
                weighted_score += weight
            elif vote.vote == 'down' or vote.vote == -1:
                weighted_score -= weight
            # vote=0 is abstain, no effect
        
        return weighted_score
        
    except Exception as e:
        logger.error(f"Error calculating weighted score for {item_type}:{item_id}: {e}")
        return 0


def update_item_weighted_score(db: Session, item_type: str, item_id: str) -> int:
    """
    Update weighted_score for an item (song or tool) in database.
    
    Args:
        db: Database session
        item_type: 'song' or 'tool'
        item_id: Item ID
    
    Returns:
        New weighted score
    """
    try:
        # Calculate weighted score
        weighted_score = calculate_weighted_score(db, item_type, item_id)
        
        # Update item in database
        if item_type == 'song':
            item = db.query(Song).filter(Song.id == item_id).first()
            if item:
                item.weighted_score = weighted_score
        elif item_type == 'tool':
            item = db.query(Tool).filter(Tool.id == item_id).first()
            if item:
                item.weighted_score = weighted_score
        else:
            logger.warning(f"Invalid item_type: {item_type}")
            return 0
        
        db.commit()
        logger.debug(f"Updated weighted_score for {item_type}:{item_id}: {weighted_score}")
        
        return weighted_score
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update weighted_score for {item_type}:{item_id}: {e}")
        return 0


def backfill_all_weighted_scores(db: Session) -> Dict[str, int]:
    """
    Backfill weighted scores for all existing items (migration 005).
    
    Args:
        db: Database session
    
    Returns:
        Dictionary with counts of updated items
    """
    try:
        results = {"songs_updated": 0, "tools_updated": 0, "errors": 0}
        
        # Backfill all songs
        songs = db.query(Song).all()
        for song in songs:
            try:
                weighted_score = calculate_weighted_score(db, 'song', song.id)
                song.weighted_score = weighted_score
                results["songs_updated"] += 1
            except Exception as e:
                logger.error(f"Error backfilling song {song.id}: {e}")
                results["errors"] += 1
        
        # Backfill all tools
        tools = db.query(Tool).all()
        for tool in tools:
            try:
                weighted_score = calculate_weighted_score(db, 'tool', tool.id)
                tool.weighted_score = weighted_score
                results["tools_updated"] += 1
            except Exception as e:
                logger.error(f"Error backfilling tool {tool.id}: {e}")
                results["errors"] += 1
        
        db.commit()
        
        logger.info(f"Backfill complete: {results}")
        return results
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to backfill weighted scores: {e}")
        return {"songs_updated": 0, "tools_updated": 0, "errors": 1}
