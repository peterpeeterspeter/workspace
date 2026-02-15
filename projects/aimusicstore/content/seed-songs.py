#!/usr/bin/env python3
"""
Seed aimusicstore.com database with diverse sample songs
Addresses cold start problem by adding 50+ diverse tracks

Key features:
- Platform diversity: Suno, Udio, Mubert, Soundraw
- Genre diversity: Electronic, Pop, Ambient, Hip-hop, Rock, Lo-fi, Experimental
- BPM range: 70-160
- Mood diversity
- Randomized creation timestamps (last 30 days)
"""

import psycopg2
import os
import uuid
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/root/.openclaw/workspace/projects/aimusicstore/.env')

# Database connection
DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@127.0.0.1:5432/aimusicstore')

# Platform distributions
PLATFORMS = ["Suno", "Udio", "Mubert", "Soundraw"]
PLATFORM_URLS = {
    "Suno": "https://suno.com",
    "Udio": "https://udio.com",
    "Mubert": "https://mubert.com",
    "Soundraw": "https://soundraw.com"
}

# Genre distributions with mood/tempo ranges
GENRE_CONFIG = {
    "electronic": {
        "moods": ["energetic", "upbeat", "dark", "melodic"],
        "bpm_range": (120, 140),
        "count": 12
    },
    "pop": {
        "moods": ["upbeat", "happy", "melodic", "energetic"],
        "bpm_range": (100, 130),
        "count": 10
    },
    "ambient": {
        "moods": ["calm", "chill", "relaxed", "peaceful"],
        "bpm_range": (70, 90),
        "count": 8
    },
    "hip-hop": {
        "moods": ["energetic", "upbeat", "dark", "chill"],
        "bpm_range": (85, 110),
        "count": 8
    },
    "rock": {
        "moods": ["energetic", "upbeat", "dark", "melodic"],
        "bpm_range": (110, 140),
        "count": 7
    },
    "lo-fi": {
        "moods": ["chill", "calm", "relaxed", "melodic"],
        "bpm_range": (75, 95),
        "count": 7
    },
    "experimental": {
        "moods": ["dark", "melodic", "energetic", "calm"],
        "bpm_range": (80, 150),
        "count": 6
    }
}

# Artist names per platform
PLATFORM_ARTISTS = {
    "Suno": ["Suno AI", "Suno Music", "Suno Beats", "Suno Flow"],
    "Udio": ["Udio AI", "Udio Music", "Udio Sound", "Udio Wave"],
    "Mubert": ["Mubert AI", "Mubert Music", "Mubert Flow", "Mubert Beats"],
    "Soundraw": ["Soundraw AI", "Soundraw Music", "Soundraw Studio", "Soundraw Pro"]
}

# Title templates per genre/mood combination
TITLE_TEMPLATES = {
    "electronic": {
        "energetic": ["Neon {word}", "Cyber {word}", "Digital {word}", "Pulse {word}"],
        "upbeat": ["Electric {word}", "Vibrant {word}", "Solar {word}", "Radiant {word}"],
        "dark": ["Shadow {word}", "Dark {word}", "Midnight {word}", "Abyss {word}"],
        "melodic": ["Crystal {word}", "Ethereal {word}", "Floating {word}", "Dream {word}"]
    },
    "pop": {
        "upbeat": ["Summer {word}", "Bright {word}", "Sunny {word}", "Golden {word}"],
        "happy": ["Joyful {word}", "Happy {word}", "Cheerful {word}", "Smile {word}"],
        "melodic": ["Sweet {word}", "Lovely {word}", "Beautiful {word}", "Gentle {word}"],
        "energetic": ["Dynamic {word}", "Power {word}", "Strong {word}", "Bold {word}"]
    },
    "ambient": {
        "calm": ["Tranquil {word}", "Peaceful {word}", "Quiet {word}", "Gentle {word}"],
        "chill": ["Chill {word}", "Easy {word}", "Soft {word}", "Mellow {word}"],
        "relaxed": ["Relaxing {word}", "Calm {word}", "Serene {word}", "Zen {word}"],
        "peaceful": ["Harmony {word}", "Balance {word}", "Stillness {word}", "Silence {word}"]
    },
    "hip-hop": {
        "energetic": ["Street {word}", "Urban {word}", "City {word}", "Block {word}"],
        "upbeat": ["Groove {word}", "Bounce {word}", "Rhythm {word}", "Flow {word}"],
        "dark": ["Underground {word}", "Shadow {word}", "Night {word}", "Grime {word}"],
        "chill": ["Laid Back {word}", "Smooth {word}", "Easy {word}", "Cool {word}"]
    },
    "rock": {
        "energetic": ["Thunder {word}", "Power {word}", "Force {word}", "Storm {word}"],
        "upbeat": ["Rising {word}", "Alive {word}", "Wild {word}", "Free {word}"],
        "dark": ["Dark {word}", "Heavy {word}", "Grit {word}", "Edge {word}"],
        "melodic": ["Echo {word}", "Horizon {word}", "Journey {word}", "Waves {word}"]
    },
    "lo-fi": {
        "chill": ["Lo-Fi {word}", "Chill {word}", "Cozy {word}", "Warm {word}"],
        "calm": ["Peaceful {word}", "Quiet {word}", "Soft {word}", "Mellow {word}"],
        "relaxed": ["Relax {word}", "Unwind {word}", "Rest {word}", "Ease {word}"],
        "melodic": ["Nostalgic {word}", "Memory {word}", "Dreamy {word}", "Wistful {word}"]
    },
    "experimental": {
        "dark": ["Void {word}", "Chaos {word}", "Glitch {word}", "Static {word}"],
        "melodic": ["Abstract {word}", "Beyond {word}", "Transcend {word}", "Ascend {word}"],
        "energetic": ["Fragment {word}", "Disrupt {word}", "Break {word}", "Shatter {word}"],
        "calm": ["Drift {word}", "Float {word}", "Suspend {word}", "Hover {word}"]
    }
}

TITLE_WORDS = [
    "Dreams", "Waves", "Horizon", "Echo", "Pulse", "Flow", "Drift", "Rise",
    "Shadows", "Light", "Night", "Day", "Stars", "Moon", "Sun", "Sky",
    "Fire", "Water", "Earth", "Air", "Spirit", "Soul", "Mind", "Heart",
    "Voyage", "Quest", "Path", "Way", "Gate", "Door", "Key", "Lock"
]

def generate_song_title(genre, mood):
    """Generate a unique song title based on genre and mood"""
    templates = TITLE_TEMPLATES.get(genre, {}).get(mood, ["{word} Dreams"])
    template = random.choice(templates)
    word = random.choice(TITLE_WORDS)
    return template.format(word=word)

def generate_random_timestamp():
    """Generate a random timestamp within the last 30 days"""
    days_ago = random.randint(0, 30)
    hours_ago = random.randint(0, 23)
    minutes_ago = random.randint(0, 59)

    return datetime.utcnow() - timedelta(
        days=days_ago,
        hours=hours_ago,
        minutes=minutes_ago
    )

def generate_songs():
    """Generate diverse song list based on genre configuration"""
    songs = []

    for genre, config in GENRE_CONFIG.items():
        count = config['count']
        moods = config['moods']
        bpm_range = config['bpm_range']

        for i in range(count):
            mood = random.choice(moods)
            platform = random.choice(PLATFORMS)
            artist = random.choice(PLATFORM_ARTISTS[platform])

            song = {
                "title": generate_song_title(genre, mood),
                "artist": artist,
                "platform": platform,
                "platform_url": PLATFORM_URLS[platform],
                "genre": genre,
                "mood": mood,
                "tempo": random.randint(bpm_range[0], bpm_range[1]),
                "created_at": generate_random_timestamp()
            }
            songs.append(song)

    return songs

def seed_songs():
    """Insert songs into database"""
    songs_to_seed = generate_songs()

    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()

    print(f"[{datetime.utcnow()}] Seeding {len(songs_to_seed)} songs...")
    print(f"Distribution:")
    for genre, config in GENRE_CONFIG.items():
        print(f"  - {genre}: {config['count']} songs")

    inserted = 0
    for song in songs_to_seed:
        try:
            # Generate unique ID
            song_id = f"song-{uuid.uuid4().hex[:4]}"

            # Format timestamp for PostgreSQL
            created_at = song['created_at'].strftime('%Y-%m-%d %H:%M:%S')

            cursor.execute(
                """
                INSERT INTO songs (id, title, artist, platform, platform_url, genre, mood, tempo, up_votes, down_votes, score, weighted_score, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
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
                    0,  # score
                    0,  # weighted_score
                    created_at
                )
            )
            inserted += 1

            if inserted % 10 == 0:
                print(f"  Progress: {inserted}/{len(songs_to_seed)} songs inserted...")

        except Exception as e:
            print(f"❌ Error inserting {song['title']}: {e}")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"\n[{datetime.utcnow()}] Seeding complete!")
    print(f"  Inserted: {inserted}/{len(songs_to_seed)} songs")
    print(f"  Database total: {inserted + 10} songs (including existing 10)")
    print(f"\nGenre distribution:")
    from collections import Counter
    genre_counts = Counter(song['genre'] for song in songs_to_seed)
    for genre, count in sorted(genre_counts.items()):
        print(f"  - {genre}: {count}")
    print(f"\nPlatform distribution:")
    platform_counts = Counter(song['platform'] for song in songs_to_seed)
    for platform, count in sorted(platform_counts.items()):
        print(f"  - {platform}: {count}")
    print(f"\nBPM range: {min(song['tempo'] for song in songs_to_seed)}-{max(song['tempo'] for song in songs_to_seed)}")
    print(f"Date range: Last 30 days (randomized)")

if __name__ == "__main__":
    seed_songs()
