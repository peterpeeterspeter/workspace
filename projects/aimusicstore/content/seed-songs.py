#!/usr/bin/env python3
"""
Seed aimusicstore.com database with sample songs
Addresses cold start problem by adding diverse content
Uses actual database schema
"""

import psycopg2
import os
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/root/.openclaw/workspace/projects/aimusicstore/.env')

# Database connection
DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@127.0.0.1:5432/aimusicstore')

# Sample songs (using correct schema)
SONGS_TO_SEED = [
    # Electronic
    {
        "title": "Neon Dreams",
        "artist": "Suno AI",
        "platform": "Suno",
        "platform_url": "https://suno.com",
        "genre": "electronic",
        "mood": "energetic",
        "tempo": 128
    },
    {
        "title": "Cyber Pulse",
        "artist": "Suno AI",
        "platform": "Suno",
        "platform_url": "https://suno.com",
        "genre": "electronic",
        "mood": "upbeat",
        "tempo": 140
    },
    # Ambient
    {
        "title": "Midnight Lullaby",
        "artist": "Udio",
        "platform": "Udio",
        "platform_url": "https://udio.com",
        "genre": "ambient",
        "mood": "chill",
        "tempo": 80
    },
    {
        "title": "Ocean Whispers",
        "artist": "Udio",
        "platform": "Udio",
        "platform_url": "https://udio.com",
        "genre": "ambient",
        "mood": "calm",
        "tempo": 75
    },
    # Hip-Hop
    {
        "title": "Urban Flow",
        "artist": "Suno AI",
        "platform": "Suno",
        "platform_url": "https://suno.com",
        "genre": "hip-hop",
        "mood": "energetic",
        "tempo": 95
    },
    {
        "title": "Street Chronicles",
        "artist": "Suno AI",
        "platform": "Suno",
        "platform_url": "https://suno.com",
        "genre": "hip-hop",
        "mood": "upbeat",
        "tempo": 100
    },
    # Lo-Fi
    {
        "title": "Starlight Lullaby",
        "artist": "Suno AI",
        "platform": "Suno",
        "platform_url": "https://suno.com",
        "genre": "lo-fi",
        "mood": "chill",
        "tempo": 85
    },
    # Chill
    {
        "title": "Coffee Shop Vibes",
        "artist": "Suno AI",
        "platform": "Suno",
        "platform_url": "https://suno.com",
        "genre": "lo-fi",
        "mood": "calm",
        "tempo": 90
    }
]

def seed_songs():
    """Insert songs into database using correct schema"""
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()

    print(f"[{datetime.now()}] Seeding {len(SONGS_TO_SEED)} songs...")

    inserted = 0
    for song in SONGS_TO_SEED:
        try:
            # Generate unique ID
            song_id = f"song-{uuid.uuid4().hex[:4]}"
            
            cursor.execute(
                """
                INSERT INTO songs (id, title, artist, platform, platform_url, genre, mood, tempo, up_votes, down_votes, score, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
                """,
                (
                    song_id,
                    song['title'],
                    song['artist'],
                    song['platform'],
                    song['platform_url'],
                    song['genre'],
                    song['mood'],
                    song['tempo'],
                    0,  # up_votes
                    0,  # down_votes
                    0   # score
                )
            )
            inserted += 1
            print(f"✅ Inserted: {song['title']} ({song['genre']})")
        except Exception as e:
            print(f"❌ Error inserting {song['title']}: {e}")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"\n[{datetime.now()}] Seeding complete: {inserted}/{len(SONGS_TO_SEED)} songs inserted")
    print(f"Database now has {2 + inserted} songs total")

if __name__ == "__main__":
    from datetime import datetime
    seed_songs()
