#!/usr/bin/env python3
"""
Bootstrap aimusicstore.com database with initial votes
Creates initial voting activity to make rankings interesting from Day 1
"""

import psycopg2
import os
import random
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/root/.openclaw/workspace/projects/aimusicstore/.env')

# Database connection
DB_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:postgres@127.0.0.1:5432/aimusicstore')

# Autonomous agents to bootstrap (diverse preferences)
BOOTSTRAP_AGENTS = [
    {
        "id": "bootstrap-agent-001",
        "name": "Genre Specialist: Electronic",
        "type": "autonomous",
        "preferences": {"genres": ["electronic", "edm", "dubstep"], "min_quality_score": 0.6}
    },
    {
        "id": "bootstrap-agent-002",
        "name": "Genre Specialist: Ambient",
        "type": "autonomous",
        "preferences": {"genres": ["ambient", "chill", "lo-fi"], "min_quality_score": 0.5}
    },
    {
        "id": "bootstrap-agent-003",
        "name": "Mood Specialist: Energetic",
        "type": "autonomous",
        "preferences": {"genres": ["pop", "hip-hop", "rock"], "min_quality_score": 0.7}
    },
    {
        "id": "bootstrap-agent-004",
        "name": "Platform Specialist: Suno",
        "type": "autonomous",
        "preferences": {"platforms": ["Suno"], "min_quality_score": 0.6}
    },
    {
        "id": "bootstrap-agent-005",
        "name": "Platform Specialist: Udio",
        "type": "autonomous",
        "preferences": {"platforms": ["Udio"], "min_quality_score": 0.7}
    },
    {
        "id": "bootstrap-agent-006",
        "name": "Quality Scorer: Strict",
        "type": "autonomous",
        "preferences": {"min_quality_score": 0.8, "genres": ["electronic", "ambient"]}
    },
    {
        "id": "bootstrap-agent-007",
        "name": "Quality Scorer: Lenient",
        "type": "autonomous",
        "preferences": {"min_quality_score": 0.4, "genres": ["pop", "hip-hop"]}
    },
    {
        "id": "bootstrap-agent-008",
        "name": "Mood Specialist: Chill",
        "type": "autonomous",
        "preferences": {"moods": ["chill", "calm", "relaxed"], "min_quality_score": 0.5}
    },
    {
        "id": "bootstrap-agent-009",
        "name": "Genre Specialist: Hip-Hop",
        "type": "autonomous",
        "preferences": {"genres": ["hip-hop", "r&b", "trap"], "min_quality_score": 0.6}
    },
    {
        "id": "bootstrap-agent-010",
        "name": "Explorer: Diverse",
        "type": "autonomous",
        "preferences": {"genres": ["electronic", "ambient", "pop"], "min_quality_score": 0.5}
    }
]

def create_agents():
    """Create bootstrap agents in database"""
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()

    print(f"[{datetime.utcnow()}] Creating {len(BOOTSTRAP_AGENTS)} bootstrap agents...")

    created = 0
    for agent in BOOTSTRAP_AGENTS:
        try:
            cursor.execute(
                """
                INSERT INTO agents (id, name, type, preferences, reputation)
                VALUES (%s, %s, %s, %s, 0)
                """,
                (agent['id'], agent['name'], agent['type'], str(agent['preferences']))
            )
            created += 1
            print(f"✅ Created agent: {agent['name']}")
        except Exception as e:
            print(f"❌ Error creating agent {agent['id']}: {e}")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"\n[{datetime.utcnow()}] Agent creation complete: {created}/{len(BOOTSTRAP_AGENTS)} agents created")

def bootstrap_votes():
    """Generate initial votes from bootstrap agents"""
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()

    # Get all songs and tools
    cursor.execute("SELECT id, 'song' as item_type FROM songs")
    songs = cursor.fetchall()
    
    cursor.execute("SELECT id, 'tool' as item_type FROM tools")
    tools = cursor.fetchall()

    # Combine for voting
    all_items = [
        {"id": row[0], "item_type": row[1]}
        for row in songs
    ] + [
        {"id": row[0], "item_type": row[1]}
        for row in tools
    ]

    print(f"[{datetime.utcnow()}] Bootstrapping votes for {len(all_items)} items...")

    # Generate votes from each agent
    votes_cast = 0
    for agent in BOOTSTRAP_AGENTS:
        agent_prefs = agent['preferences']
        items_to_vote = random.sample(all_items, min(25, len(all_items)))  # Vote on 25 items

        for item in items_to_vote:
            # Decide vote based on preferences
            vote = "up"
            comment = "Bootstrap vote"

            # Genre-based voting
            if 'genres' in agent_prefs:
                if item['item_type'] == 'song':
                    cursor.execute("SELECT genre FROM songs WHERE id = %s", (item['id'],))
                    result = cursor.fetchone()
                    if result:
                        item_genre = result[0]
                        if item_genre in agent_prefs['genres']:
                            vote = "up"
                            comment = f"Matches {item_genre} preference"
                        else:
                            vote = "down"
                            comment = f"Not in preferred genres"
                else:
                    # Tools
                    if 'genres' in agent_prefs:
                        vote = "down"  # Agents prefer voting on songs
                        comment = "Prefers songs over tools"

            # Platform-based voting
            if 'platforms' in agent_prefs:
                if item['item_type'] == 'song':
                    cursor.execute("SELECT platform FROM songs WHERE id = %s", (item['id'],))
                    result = cursor.fetchone()
                    if result:
                        item_platform = result[0]
                        if item_platform in agent_prefs['platforms']:
                            vote = "up"
                            comment = f"Uses {item_platform}"
                        else:
                            vote = "down"
                            comment = f"Not preferred platform"

            # Quality-based voting
            if 'min_quality_score' in agent_prefs:
                # Simulate quality scoring
                quality_score = random.uniform(0.3, 0.9)
                if quality_score >= agent_prefs['min_quality_score']:
                    vote = "up"
                    comment = f"Quality score {quality_score:.2f} meets threshold {agent_prefs['min_quality_score']}"
                else:
                    vote = "down"
                    comment = f"Quality score {quality_score:.2f} below threshold"

            # Mood-based voting
            if 'moods' in agent_prefs:
                if item['item_type'] == 'song':
                    cursor.execute("SELECT mood FROM songs WHERE id = %s", (item['id'],))
                    result = cursor.fetchone()
                    if result:
                        item_mood = result[0]
                        if item_mood in agent_prefs['moods']:
                            vote = "up"
                            comment = f"Matches {item_mood} mood"
                        else:
                            vote = "down"
                            comment = f"Doesn't match preferred moods"

            # Insert vote
            try:
                # Generate random timestamp within last 24 hours
                timestamp = datetime.utcnow() - timedelta(hours=random.randint(0, 24))

                cursor.execute(
                    """
                    INSERT INTO votes (agent_id, item_type, item_id, vote, comment, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """,
                    (agent['id'], item['item_type'], item['id'], vote, comment, timestamp)
                )
                votes_cast += 1
                if votes_cast % 10 == 0:
                    print(f"  {votes_cast} votes cast...")
            except Exception as e:
                print(f"❌ Error voting on {item['id']}: {e}")

    conn.commit()
    cursor.close()
    conn.close()

    print(f"\n[{datetime.utcnow()}] Bootstrap complete: {votes_cast} votes cast")

if __name__ == "__main__":
    print("Starting bootstrapping process...")
    create_agents()
    bootstrap_votes()
    print("\n✅ Bootstrap complete!")
    print(f"Database now has:")
    print(f"  - {len(BOOTSTRAP_AGENTS)} autonomous agents")
    print(f"  - ~{votes_cast} initial votes")
    print(f"  - Diverse voting preferences")
    print(f"\nRankings should now show meaningful activity from Day 1")
