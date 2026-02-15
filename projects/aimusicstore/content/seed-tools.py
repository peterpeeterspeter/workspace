#!/usr/bin/env python3
"""
Seed aimusicstore.com database with AI music tools
Addresses cold start problem by adding 10+ popular tools
"""

import psycopg2
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/root/.openclaw/workspace/projects/aimusicstore/.env')

# Database connection
DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@127.0.0.1:5432/aimusicstore')

# AI Music Tools to seed
TOOLS_TO_SEED = [
    {
        "name": "Suno AI",
        "website": "https://suno.ai",
        "category": "text-to-music",
        "features": '{"free_tier": true, "commercial": true, "vocal_generation": true}',
        "pricing": '{"free": "50 songs/day", "pro": "$10/month", "premium": "$30/month"}'
    },
    {
        "name": "Udio",
        "website": "https://www.udio.com",
        "category": "text-to-music",
        "features": '{"vocal_control": true, "commercial": true, "high_quality": true}',
        "pricing": '{"free": "10 tracks/month", "premium": "$12/month"}'
    },
    {
        "name": "Mubert",
        "website": "https://www.mubert.com",
        "category": "text-to-music",
        "features": '{"copyright_free": true, "api_access": true, "real_time": true}',
        "pricing": '{"free": "personal use", "creator": "$14/month", "business": "$39/month"}'
    },
    {
        "name": "Soundraw",
        "website": "https://soundraw.com",
        "category": "text-to-music",
        "features": '{"customization": true, "video_sync": true, "unlimited_licenses": true}',
        "pricing": '{"free": "limited", "personal": "$16.99/month", "commercial": "$29.99/month"}'
    },
    {
        "name": "Boomy",
        "website": "https://boomy.com",
        "category": "text-to-music",
        "features": '{"free_tier": true, "social_sharing": true, "easy_to_use": true}',
        "pricing": '{"free": "25 songs/month", "pro": "$9.99/month"}'
    },
    {
        "name": "Amper Music",
        "website": "https://www.ampermusic.com",
        "category": "music-generation",
        "features": '{"video_audio_sync": true, "api_access": true, "commercial_license": true}',
        "pricing": '{"custom": "contact sales", "enterprise": "contact sales"}'
    },
    {
        "name": "AIVA",
        "website": "https://www.aiva.ai",
        "category": "music-generation",
        "features": '{"classical_focus": true, "midi_export": true, "commercial_license": true}',
        "pricing": '{"free": "personal use", "standard": "\u20ac11/month", "pro": "\u20ac33/month"}'
    },
    {
        "name": "Ecrett Music",
        "website": "https://ecrettmusic.com",
        "category": "music-generation",
        "features": '{"soundtrack_creation": true, "mood_selection": true, "unlimited_downloads": true}',
        "pricing": '{"free": "trial", "individual": "$8/month", "business": "$25/month"}'
    },
    {
        "name": "Soundful",
        "website": "https://soundful.io",
        "category": "music-library",
        "features": '{"royalty_free": true, "ai_generated": true, "high_quality": true}',
        "pricing": '{"starter": "$9.99/month", "creator": "$19.99/month"}'
    },
    {
        "name": "Beatoven",
        "website": "https://beatoven.ai",
        "category": "music-generation",
        "features": '{"beat_creation": true, "mood_based": true, "video_soundtrack": true}',
        "pricing": '{"free": "limited", "monthly": "$10/month", "yearly": "$96/year"}'
    },
    {
        "name": "BandLab SongStarter",
        "website": "https://www.bandlab.com",
        "category": "text-to-music",
        "features": '{"free_tier": true, "social_features": true, "collaboration": true}',
        "pricing": '{"free": "forever"}'
    }
]

def seed_tools():
    """Insert tools into database"""
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()

    print(f"[{datetime.utcnow()}] Seeding {len(TOOLS_TO_SEED)} tools...")

    inserted = 0
    for idx, tool in enumerate(TOOLS_TO_SEED, 1):
        tool_id = f"tool-{idx:02d}"
        try:
            cursor.execute(
                """
                INSERT INTO tools (id, name, website, category, features, pricing, created_at, up_votes, down_votes, score, weighted_score)
                VALUES (%s, %s, %s, %s, %s, %s, NOW(), 0, 0, 0, 0)
                """,
                (tool_id, tool['name'], tool['website'], tool['category'], tool['features'], tool['pricing'])
            )
            inserted += 1
            print(f"✅ Inserted: {tool['name']} ({tool['category']}) - ID: {tool_id}")
        except Exception as e:
            print(f"❌ Error inserting {tool['name']}: {e}")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"\n[{datetime.utcnow()}] Seeding complete: {inserted}/{len(TOOLS_TO_SEED)} tools inserted")

if __name__ == "__main__":
    seed_tools()
