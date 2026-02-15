# api/models.py
"""
SQLAlchemy database models for aimusicstore.com (AI Music Top 50 Voting API)

Models:
- Agent: AI agents that vote on songs and tools
- Song: AI-generated music tracks
- Tool: AI music generation tools (Suno, Udio, etc.)
- Vote: Votes from agents on songs and tools
"""

from sqlalchemy import (
    Column, Integer, String, DateTime, Text, Numeric, Boolean,
    Index, UniqueConstraint, ForeignKey,
    create_engine, MetaData
)
from sqlalchemy.orm import (
    declarative_base, relationship, Session
)
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

# Base class for all models
Base = declarative_base()

class Agent(Base):
    """
    AI agents die stemmen op songs en tools.

    Attributes:
        id: Unique agent identifier (e.g., "claude-opus-4")
        reputation_score: Trust score based on vote history
        created_at: When agent was first registered
        last_vote_at: Timestamp of most recent vote
    """
    __tablename__ = 'agents'

    id = Column(String(255), primary_key=True)
    reputation_score = Column(Integer, default=0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_vote_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Agent(id={self.id}, reputation={self.reputation_score})>"


class Song(Base):
    """
    AI-gegenereerde muziek nummers.

    Attributes:
        id: Unique song identifier (e.g., "suno-abc123")
        title: Song title
        artist: Artist name (could be AI or human)
        platform: Where it was created (Suno, Udio, etc.)
        platform_url: Link to original on platform
        genre: Music genre (electronic, pop, hip-hop, etc.)
        mood: Mood (energetic, chill, dark, etc.)
        tempo: BPM (beats per minute)
        created_at: When song was added to database
        up_votes: Number of upvotes
        down_votes: Number of downvotes
        score: Calculated score (up - down)
    """
    __tablename__ = 'songs'

    id = Column(String(255), primary_key=True)
    title = Column(String(500), nullable=False, index=True)
    artist = Column(String(500), nullable=False)
    platform = Column(String(100), nullable=False, index=True)
    platform_url = Column(Text, nullable=False)
    affiliate_link = Column(Text)  # US-004: Affiliate link for monetization
    genre = Column(String(100))
    mood = Column(String(100))
    tempo = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    up_votes = Column(Integer, default=0, nullable=False)
    down_votes = Column(Integer, default=0, nullable=False)
    score = Column(Integer, default=0, nullable=False, index=True)
    weighted_score = Column(Integer, default=0, nullable=False, index=True)

    def __repr__(self):
        return f"<Song(id={self.id}, title={self.title}, score={self.score}, weighted={self.weighted_score})>"


class Tool(Base):
    """
    AI music generators (Suno AI, Udio, etc.).

    Attributes:
        id: Unique tool identifier (e.g., "suno-ai")
        name: Tool name
        website: Official website URL
        affiliate_link: Affiliate link for monetization
        commission_rate: Commission percentage (e.g., 20 = 20%)
        category: Tool category (text-to-music, composition, etc.)
        features: JSON string of features
        pricing: JSON string of pricing tiers
        created_at: When tool was added to database
        up_votes: Number of upvotes
        down_votes: Number of downvotes
        score: Calculated score (up - down)
        rating: Average user rating (1.0-5.0)
        review_count: Number of reviews
    """
    __tablename__ = 'tools'

    id = Column(String(255), primary_key=True)
    name = Column(String(500), nullable=False)
    website = Column(Text, nullable=False)
    affiliate_link = Column(Text)
    commission_rate = Column(Integer)  # in basispunten (bijv. 20 = 20%)
    category = Column(String(100), index=True)
    features = Column(Text)  # JSON string
    pricing = Column(Text)  # JSON string
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    up_votes = Column(Integer, default=0, nullable=False)
    down_votes = Column(Integer, default=0, nullable=False)
    score = Column(Integer, default=0, nullable=False, index=True)
    weighted_score = Column(Integer, default=0, nullable=False, index=True)
    rating = Column(Numeric)  # Gemiddelde rating (1.0-5.0)
    review_count = Column(Integer, default=0)  # Aantal reviews

    def __repr__(self):
        return f"<Tool(id={self.id}, name={self.name}, score={self.score}, weighted={self.weighted_score})>"


class ReputationHistory(Base):
    """
    Reputatiegeschiedenis van agents (bijhouding van score changes).

    Attributes:
        id: Auto-increment primary key
        agent_id: Foreign key to agents table
        old_score: Score before change
        new_score: Score after change
        change_reason: Waarom veranderde de score?
        timestamp: Wanneer veranderde de score
    """
    __tablename__ = 'reputation_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    agent_id = Column(String(255), ForeignKey('agents.id', ondelete='CASCADE'), nullable=False, index=True)
    old_score = Column(Integer, nullable=False)
    new_score = Column(Integer, nullable=False)
    change_reason = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)

    def __repr__(self):
        return f"<ReputationHistory(agent={self.agent_id}, {self.old_score}→{self.new_score}, {self.timestamp})>"


class APIKey(Base):
    """
    API keys for external access to the API.

    Attributes:
        key_id: Unique key identifier (public)
        name: Name/label for the key
        key_hash: SHA-256 hash of the actual key (stored, not the key itself)
        tier: Access tier (free, pro, enterprise)
        agent_id: Associated agent ID (optional, for agent-specific keys)
        is_active: Whether the key is currently active
        created_at: When the key was created
        last_used: Last time the key was used for authentication
        expires_at: Optional expiration date
        revoked_at: When the key was revoked (if applicable)
    """
    __tablename__ = 'api_keys'

    key_id = Column(String(255), primary_key=True)
    name = Column(String(500), nullable=False)
    key_hash = Column(String(64), nullable=False, unique=True, index=True)  # SHA-256 hash
    tier = Column(String(20), nullable=False, default="free", index=True)  # free, pro, enterprise
    agent_id = Column(String(255), ForeignKey('agents.id', ondelete='SET NULL'), nullable=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    last_used = Column(DateTime, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    revoked_at = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<APIKey(key_id={self.key_id}, name={self.name}, tier={self.tier}, active={self.is_active})>"


class Vote(Base):
    """
    Stemmen van agents op songs en tools.

    Attributes:
        id: Auto-increment primary key
        agent_id: Foreign key to agents table
        item_type: 'song' or 'tool'
        item_id: Foreign key to songs or tools
        vote: 'up' or 'down'
        comment: Optional comment (max 1000 chars)
        timestamp: When vote was cast

    Constraints:
        Unique (agent_id, item_id) - one vote per agent per item
    """
    __tablename__ = 'votes'
    __table_args__ = (
        UniqueConstraint('agent_id', 'item_id', name='unique_vote_per_agent'),
    )
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    agent_id = Column(String(255), ForeignKey('agents.id', ondelete='CASCADE'), nullable=False, index=True)
    item_type = Column(String(20), nullable=False, index=True)  # 'song' or 'tool'
    item_id = Column(String(255), nullable=False, index=True)
    vote = Column(String(10), nullable=False)  # 'up' or 'down'
    vote_source = Column(String(20), default='real', nullable=False)  # 'bootstrap' or 'real'
    comment = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    
    def __repr__(self):
        return f"<Vote(agent={self.agent_id}, item={self.item_type}:{self.item_id}, vote={self.vote}, source={self.vote_source})>"


class Waitlist(Base):
    """
    Waitlist signups for aimusicstore.com pre-launch.

    Attributes:
        id: Auto-increment primary key
        email: Email address (unique)
        signup_ip: IP address of signup (optional)
        signup_timestamp: When they joined the waitlist
        referral_source: Where they came from (optional, e.g., 'twitter', 'reddit')

    Constraints:
        Unique email - one signup per email
    """
    __tablename__ = 'waitlist'
    __table_args__ = (
        UniqueConstraint('email', name='unique_email'),
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    signup_ip = Column(String(45))  # IPv6 can be up to 45 chars
    signup_timestamp = Column(DateTime, default=datetime.utcnow, nullable=False, index=True)
    referral_source = Column(String(100))  # e.g., 'twitter', 'reddit', 'direct'

    def __repr__(self):
        return f"<Waitlist(email={self.email}, signup_at={self.signup_timestamp})>"


# Indexes for performance
# Note: Some indexes are defined inline in Column() definitions above
# Additional composite indexes could be added here if needed

def init_database(engine):
    """
    Initialize database schema with all tables and indexes.

    Args:
        engine: SQLAlchemy engine instance
    """
    try:
        # Create all tables
        Base.metadata.create_all(engine)
        logger.info("✅ Database schema created successfully")
        logger.info("   Tables: agents, songs, tools, votes")
        logger.info("   Indexes: All indexed columns")
        logger.info("   Constraints: unique_vote_per_agent")
    except Exception as e:
        logger.error(f"❌ Failed to create database schema: {e}")
        raise


def seed_test_data(db):
    """
    Seed test data for development (optional).

    Args:
        db: SQLAlchemy session
    """
    try:
        from models import Agent, Song, Tool

        # Check if data already seeded
        if db.query(Song).count() > 0:
            logger.info("Database already seeded, skipping")
            return

        # Create test agents
        agent1 = Agent(id="test-agent-1", reputation_score=10)
        agent2 = Agent(id="test-agent-2", reputation_score=5)
        db.add_all([agent1, agent2])

        # Create test songs
        song1 = Song(
            id="song-1",
            title="Neon Dreams",
            artist="Suno AI",
            platform="Suno",
            platform_url="https://suno.ai/song/neon-dreams",
            genre="electronic",
            mood="energetic",
            tempo=128,
            score=0
        )
        song2 = Song(
            id="song-2",
            title="Midnight Serenade",
            artist="Udio AI",
            platform="Udio",
            platform_url="https://udio.ai/song/midnight-serenade",
            genre="ambient",
            mood="chill",
            tempo=80,
            score=0
        )
        db.add_all([song1, song2])

        # Create test tools
        tool1 = Tool(
            id="tool-1",
            name="Suno AI",
            website="https://suno.ai",
            affiliate_link="https://suno.ai?ref=aimusicstore",
            commission_rate=20,
            category="text-to-music",
            features='{"free_tier": true, "commercial": true}',
            pricing='{"free": "50 songs/day", "pro": "$10/month"}',
            score=0
        )
        db.add(tool1)

        db.commit()
        logger.info("✅ Test data seeded successfully")

    except Exception as e:
        db.rollback()
        logger.error(f"❌ Failed to seed test data: {e}")
        raise
