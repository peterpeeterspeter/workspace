#!/usr/bin/env python3
"""
Autonomous Voting Agent for aimusicstore.com
Phase 1: Simple cron-based architecture
Discovers tracks, votes based on preferences, builds reputation over time
"""

import requests
import time
import logging
from datetime import datetime
import os
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(message)s',
    handlers=[
        logging.FileHandler('/var/log/aimusicstore-agent.log'),
        logging.StreamHandler()
    ]
)

# Load environment
load_dotenv('/root/.openclaw/workspace/projects/aimusicstore/.env')
API_BASE = os.getenv('API_BASE_URL', 'https://aimusicstore.com/api/v1')

# Agent configuration
AGENT_ID = os.getenv('AGENT_ID', 'autonomous-curator-001')
AGENT_PREFERENCES = {
    "genres": ["ambient", "electronic", "chill"],
    "min_quality_score": 0.6
}

def register_agent():
    """Register this agent with aimusicstore.com"""
    try:
        response = requests.post(
            f"{API_BASE}/agents/register",
            json={
                "name": f"Autonomous Curator {AGENT_ID.split('-')[-1]}",
                "type": "autonomous",
                "preferences": AGENT_PREFERENCES
            },
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        logging.info(f"✅ Registered as {data['agent_id']} (API key: {data['api_key'][:8]}...)")
        return data['agent_id']
    except Exception as e:
        logging.error(f"❌ Registration failed: {e}")
        # Try to use existing agent_id
        return AGENT_ID

def discover_tracks(agent_id):
    """Fetch tracks to vote on"""
    try:
        response = requests.get(
            f"{API_BASE}/discover",
            params={"agent_id": agent_id, "limit": 20},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        return data['queue']
    except Exception as e:
        logging.error(f"❌ Discovery failed: {e}")
        return []

def vote_on_track(agent_id, track, vote, comment=""):
    """Submit a vote"""
    try:
        response = requests.post(
            f"{API_BASE}/vote",
            json={
                "agent_id": agent_id,
                "item_type": track['item_type'],
                "item_id": track['id'],
                "vote": vote,
                "comment": comment
            },
            timeout=10
        )
        response.raise_for_status()
        return True
    except Exception as e:
        logging.error(f"❌ Vote failed on {track.get('title', track.get('name', 'Unknown'))}: {e}")
        return False

def main():
    """Main voting loop - runs every hour"""
    # Register agent
    agent_id = register_agent()

    logging.info(f"Autonomous Agent {agent_id} starting voting loop...")
    logging.info(f"Preferences: {AGENT_PREFERENCES}")

    cycle_count = 0

    while True:
        try:
            cycle_count += 1
            logging.info(f"\n=== Cycle {cycle_count} ===")

            # 1. Discover tracks
            logging.info("Fetching discovery queue...")
            tracks = discover_tracks(agent_id)
            
            if not tracks:
                logging.warning("No tracks discovered. Sleeping 1 hour...")
                time.sleep(3600)
                continue

            logging.info(f"Discovered {len(tracks)} tracks")

            # 2. Vote on tracks matching preferences
            votes_cast = 0
            for track in tracks:
                # Check if track matches preferences
                should_vote = False
                vote = "down"
                comment = ""

                # Genre-based decision
                if 'genres' in AGENT_PREFERENCES:
                    if track['item_type'] == 'song' and track.get('genre') in AGENT_PREFERENCES['genres']:
                        should_vote = True
                        vote = "up"
                        comment = f"Matches {track['genre']} preference"

                # Mood-based decision
                if not should_vote and 'moods' in AGENT_PREFERENCES:
                    if track['item_type'] == 'song' and track.get('mood') in AGENT_PREFERENCES.get('moods', []):
                        should_vote = True
                        vote = "up"
                        comment = f"Matches {track.get('mood', 'unknown')} mood"

                # Platform-based decision
                if not should_vote and 'platforms' in AGENT_PREFERENCES:
                    if track.get('platform') in AGENT_PREFERENCES.get('platforms', []):
                        should_vote = True
                        vote = "up"
                        comment = f"Uses {track.get('platform', 'unknown')} platform"

                # Vote if track matched preferences
                if should_vote:
                    if vote_on_track(agent_id, track, vote, comment):
                        votes_cast += 1
                        item_title = track.get('title', track.get('name', 'Unknown'))
                        logging.info(f"✅ Voted {vote} on {item_title} ({track.get('genre', 'N/A')})")
                
                # Rate limiting
                time.sleep(2)  # 2 seconds between votes

            logging.info(f"Cycle {cycle_count} complete: {votes_cast} votes cast")

            # Wait before next cycle
            logging.info("Sleeping 1 hour until next cycle...")
            time.sleep(3600)  # 1 hour

        except KeyboardInterrupt:
            logging.info("\n🛑 Agent stopped by user")
            break
        except Exception as e:
            logging.error(f"❌ Error in voting cycle: {e}")
            logging.info("Retrying in 5 minutes...")
            time.sleep(300)  # Retry in 5 minutes

if __name__ == "__main__":
    main()
