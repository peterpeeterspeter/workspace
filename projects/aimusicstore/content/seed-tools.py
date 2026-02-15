#!/usr/bin/env python3
"""
Seed aimusicstore.com database with AI music tools
Addresses cold start problem by adding 10+ popular tools
"""

import psycopg2
import os
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
        "description": "Create music with simple text prompts"
    },
    {
        "name": "Udio",
        "website": "https://www.udio.com",
        "category": "text-to-music",
        "description": "Professional AI music generation with vocal control"
    },
    {
        "name": "Mubert",
        "website": "https://www.mubert.com",
        "category": "text-to-music",
        "description": "AI-powered copyright-free music for content creators"
    },
    {
        "name": "Soundraw",
        "website": "https://soundraw.com",
        "category": "text-to-music",
        "description": "AI music composition with customization"
    },
    {
        "name": "Boomy",
        "website": "https://boomy.com",
        "category": "text-to-music",
        "description": "Free AI music generator with social sharing"
    },
    {
        "name": "Amper Music",
        "website": "https://www.ampermusic.com",
        "category": "music-generation",
        "description": "AI music for video, podcast, and games"
    },
    {
        "name": "AIVA",
        "website": "https://www.aiva.ai",
        "category": "music-generation",
        "description": "Artificial Intelligence Virtual Artist"
    },
    {
        "name": "Ecrett Music",
        "website": "https://ecrettmusic.com",
        "category": "music-generation",
        "description": "AI soundtrack and music composition"
    },
    {
        "name": "Soundful",
        "website": "https://soundful.io",
        "category": "music-library",
        "description": "Royalty-free AI music library"
    },
    {
        "name": "Beatoven",
        "website": "https://beatoven.ai",
        "category": "music-generation",
        "description": "AI-powered beat creation and music production"
    },
    {
        "name": "Soundful.io",
        "website": "https://soundful.io",
        "category": "text-to-music",
        "description": "AI music with extensive sound library"
    }
]

def seed_tools():
    """Insert tools into database"""
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()

    print(f"[{datetime.utcnow()}] Seeding {len(TOOLS_TO_SEED)} tools...")

    inserted = 0
    for tool in TOOLS_TO_SEED:
        try:
            cursor.execute(
                """
                INSERT INTO tools (name, website, category, description)
                VALUES (%s, %s, %s, %s)
                """,
                (tool['name'], tool['website'], tool['category'], tool['description'])
            )
            inserted += 1
            print(f"✅ Inserted: {tool['name']} ({tool['category']})")
        except Exception as e:
            print(f"❌ Error inserting {tool['name']}: {e}")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"\n[{datetime.utcnow()}] Seeding complete: {inserted}/{len(TOOLS_TO_SEED)} tools inserted")

if __name__ == "__main__":
    seed_tools()
