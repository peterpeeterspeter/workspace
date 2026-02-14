#!/usr/bin/env python3
"""
API-Football Integration for Pronosticiserieb.com
Fetches Serie B fixtures, standings, and match data
"""

import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional


class APIFootballClient:
    """Client for API-Football v4."""

    def __init__(self, api_key: str):
        self.base_url = "https://api-football-v1.p.rapidapi.com/v3"
        self.headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "api-football-v1.p.rapidapi.com"
        }

    def get_standings(self, league_id: int = 135, season: int = 2024) -> Dict:
        """
        Get Serie B standings.
        League ID 135 = Serie B (verified from API-Football coverage)
        """
        url = f"{self.base_url}/standings"
        params = {
            "league": league_id,
            "season": season
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_fixtures(self, league_id: int = 135, season: int = 2024,
                     from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict:
        """Get Serie B fixtures for date range."""

        url = f"{self.base_url}/fixtures"
        params = {
            "league": league_id,
            "season": season
        }

        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_head_to_head(self, team1_id: int, team2_id: int) -> Dict:
        """Get H2H record between two teams."""

        url = f"{self.base_url}/fixtures/headtohead"
        params = {
            "h2h": f"{team1_id}-{team2_id}"
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_predictions(self, fixture_id: int) -> Dict:
        """Get AI predictions for a fixture (if available in your tier)."""

        url = f"{self.base_url}/predictions"
        params = {
            "fixture": fixture_id
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}

    def get_odds(self, fixture_id: int, bookmaker: str = "all") -> Dict:
        """Get odds for a fixture (if available in your tier)."""

        url = f"{self.base_url}/odds"
        params = {
            "fixture": fixture_id,
            "bookmaker": bookmaker
        }

        try:
            response = requests.get(url, headers=self.headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"error": str(e)}


def main():
    """Example usage."""

    # You'll need to get your API key from https://www.api-football.com
    api_key = "your-api-football-key-here"

    client = APIFootballClient(api_key)

    print("="*60)
    print("API-Football Test - Serie B Data")
    print("="*60)

    # Test 1: Get standings
    print("\n1. Fetching Serie B standings...")
    standings = client.get_standings()
    if "error" in standings:
        print(f"   ❌ Error: {standings['error']}")
    else:
        print("   ✅ Success!")
        # Parse and display top 3 teams
        try:
            league = standings["response"][0]["league"]
            teams = league["standings"][0]  # First group
            print("\n   Top 3 Teams:")
            for i, team in enumerate(teams[:3], 1):
                print(f"   {i}. {team['team']['name']} - {team['points']} pts")
        except Exception as e:
            print(f"   ⚠️  Parse error: {e}")

    # Test 2: Get today's fixtures
    print("\n2. Fetching today's fixtures...")
    today = datetime.now().strftime("%Y-%m-%d")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
    fixtures = client.get_fixtures(from_date=today, to_date=tomorrow)
    if "error" in fixtures:
        print(f"   ❌ Error: {fixtures['error']}")
    else:
        print("   ✅ Success!")
        try:
            matches = fixtures["response"]
            print(f"\n   Found {len(matches)} upcoming match(es)")
            for match in matches[:3]:
                home = match["teams"]["home"]["name"]
                away = match["teams"]["away"]["name"]
                date = match["fixture"]["date"]
                print(f"   • {home} vs {away} ({date})")
        except Exception as e:
            print(f"   ⚠️  Parse error: {e}")

    print("\n" + "="*60)
    print("Test complete!")
    print("="*60)
    print("\nTo use this script:")
    print("1. Sign up at https://www.api-football.com")
    print("2. Get your API key from dashboard")
    print("3. Replace 'your-api-football-key-here' above")
    print("4. Run: python3 api_football_client.py")
    print("\nFree tier includes:")
    print("- 100 requests/day (verify on pricing page)")
    print("- Serie B fixtures & standings")
    print("- Basic statistics")
    print("\nPaid tiers add:")
    print("- More requests")
    print("- H2H statistics")
    print("- Odds data")
    print("- Predictions API")
    print("="*60)


if __name__ == "__main__":
    main()
