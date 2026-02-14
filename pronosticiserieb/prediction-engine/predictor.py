#!/usr/bin/env python3
"""
Serie B Prediction Engine
Rule-based model with ML upgrade path
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum


class Outcome(Enum):
    HOME = "home"
    DRAW = "draw"
    AWAY = "away"


@dataclass
class Team:
    name: str
    league_position: int
    form: List[str]  # Last 5: ['W', 'D', 'L', 'W', 'W']
    home_goals_for: int
    home_goals_against: int
    away_goals_for: int
    away_goals_against: int
    points: int


@dataclass
class Match:
    home_team: Team
    away_team: Team
    match_date: datetime
    head_to_head: List[Dict]  # Last 5 H2H results


@dataclass
class Prediction:
    home_win_prob: float
    draw_prob: float
    away_win_prob: float
    confidence: int  # 0-100
    recommended_outcome: Outcome
    value_bet: bool
    reasoning: str


class SerieBPredictor:
    """
    Rule-based Serie B prediction engine.

    Factors:
    - League position (25%)
    - Recent form (30%)
    - Home/away performance (20%)
    - Head-to-head record (15%)
    - Goal difference (10%)
    """

    def __init__(self):
        self.home_advantage = 0.08  # 8% edge for home team
        self.draw_base = 0.28  # Base draw probability

    def calculate_form_score(self, form: List[str]) -> float:
        """Calculate form score from last 5 games."""
        points = {'W': 3, 'D': 1, 'L': 0}
        total = sum(points.get(result, 0) for result in form)
        max_points = len(form) * 3
        return total / max_points if max_points > 0 else 0

    def calculate_home_strength(self, team: Team) -> float:
        """Home strength based on goals scored/conceded at home."""
        if team.home_goals_for + team.home_goals_against == 0:
            return 0.5
        return team.home_goals_for / (team.home_goals_for + team.home_goals_against)

    def calculate_away_strength(self, team: Team) -> float:
        """Away strength based on goals scored/conceded away."""
        if team.away_goals_for + team.away_goals_against == 0:
            return 0.5
        return team.away_goals_for / (team.away_goals_for + team.away_goals_against)

    def calculate_h2h_advantage(self, h2h: List[Dict], team_name: str) -> float:
        """Calculate head-to-head advantage."""
        if not h2h:
            return 0.5

        wins = 0
        for match in h2h:
            if match.get('winner') == team_name:
                wins += 1

        return wins / len(h2h)

    def calculate_position_advantage(self, home_pos: int, away_pos: int) -> float:
        """Position advantage (lower is better)."""
        if home_pos == away_pos:
            return 0.5
        diff = abs(home_pos - away_pos)
        # Logarithmic scale: 1 position = 2% edge, caps at 20%
        edge = min(0.02 * diff, 0.20)
        if home_pos < away_pos:
            return 0.5 + edge
        return 0.5 - edge

    def predict(self, match: Match) -> Prediction:
        """Generate prediction for a match."""

        # 1. Form scores (30% weight)
        home_form = self.calculate_form_score(match.home_team.form)
        away_form = self.calculate_form_score(match.away_team.form)
        form_diff = home_form - away_form

        # 2. Home/Away strength (20% weight)
        home_strength = self.calculate_home_strength(match.home_team)
        away_strength = self.calculate_away_strength(match.away_team)
        venue_strength = (home_strength + (1 - away_strength)) / 2

        # 3. H2H (15% weight)
        home_h2h = self.calculate_h2h_advantage(match.head_to_head, match.home_team.name)
        h2h_advantage = home_h2h - 0.5

        # 4. Position (25% weight)
        position_advantage = self.calculate_position_advantage(
            match.home_team.league_position,
            match.away_team.league_position
        )
        position_diff = position_advantage - 0.5

        # 5. Goal difference (10% weight)
        home_gd = match.home_team.home_goals_for - match.home_team.home_goals_against
        away_gd = match.away_team.away_goals_for - match.away_team.away_goals_against
        gd_advantage = min(max(home_gd - away_gd, -10), 10) / 40  # Normalize -10 to +10 -> -0.25 to +0.25

        # Combine all factors
        home_raw = (
            0.50 +  # Base
            self.home_advantage +  # Home edge
            (form_diff * 0.30) +  # Form
            (venue_strength - 0.50) * 0.40 +  # Home/away strength
            (h2h_advantage * 0.30) +  # H2H
            position_diff * 0.50 +  # Position
            gd_advantage * 0.20  # Goal diff
        )

        # Normalize to 0-1
        home_prob = max(0.05, min(0.85, home_raw))

        # Calculate draw and away
        draw_prob = self.draw_base * (1 - abs(home_prob - 0.50))
        remaining = 1 - draw_prob
        away_prob = 1 - home_prob - draw_prob

        # Normalize all three (ensure non-negative)
        home_prob = max(0.01, home_prob)
        draw_prob = max(0.01, draw_prob)
        away_prob = max(0.01, away_prob)

        total = home_prob + draw_prob + away_prob
        home_prob /= total
        draw_prob /= total
        away_prob /= total

        # Determine recommended outcome
        probs = {
            Outcome.HOME: home_prob,
            Outcome.DRAW: draw_prob,
            Outcome.AWAY: away_prob
        }
        recommended = max(probs, key=probs.get)

        # Calculate confidence (0-100)
        max_prob = max(probs.values())
        confidence = int((max_prob - 0.33) / 0.67 * 100)

        # Value bet: recommended outcome has >40% probability
        value_bet = max_prob > 0.40

        # Generate reasoning
        reasoning = self._generate_reasoning(match, probs, recommended)

        return Prediction(
            home_win_prob=round(home_prob, 3),
            draw_prob=round(draw_prob, 3),
            away_win_prob=round(away_prob, 3),
            confidence=confidence,
            recommended_outcome=recommended,
            value_bet=value_bet,
            reasoning=reasoning
        )

    def _generate_reasoning(
        self,
        match: Match,
        probs: Dict[Outcome, float],
        recommended: Outcome
    ) -> str:
        """Generate human-readable reasoning."""

        parts = []

        # Form
        home_form_points = sum(3 if x == 'W' else 1 if x == 'D' else 0 for x in match.home_team.form[-5:])
        away_form_points = sum(3 if x == 'W' else 1 if x == 'D' else 0 for x in match.away_team.form[-5:])
        if home_form_points > away_form_points + 3:
            parts.append(f"{match.home_team.name} in better form")
        elif away_form_points > home_form_points + 3:
            parts.append(f"{match.away_team.name} in better form")

        # Position
        pos_diff = match.away_team.league_position - match.home_team.league_position
        if abs(pos_diff) >= 5:
            better_team = match.home_team.name if pos_diff > 0 else match.away_team.name
            parts.append(f"{better_team} significantly higher in table")

        # H2H
        if match.head_to_head:
            home_wins = sum(1 for m in match.head_to_head if m.get('winner') == match.home_team.name)
            if home_wins >= 4:
                parts.append(f"Strong H2H record for {match.home_team.name}")

        # Home advantage
        if recommended == Outcome.HOME and match.home_team.league_position <= match.away_team.league_position:
            parts.append("Home advantage expected to be key")

        return "; ".join(parts) if parts else "Balanced match expected"

    def predict_batch(self, matches: List[Match]) -> List[Prediction]:
        """Predict multiple matches."""
        return [self.predict(match) for match in matches]


def example_usage():
    """Example prediction."""

    # Example teams (Serie B 2024-25)
    brescia = Team(
        name="Brescia",
        league_position=5,
        form=['W', 'W', 'D', 'L', 'W'],
        home_goals_for=25,
        home_goals_against=12,
        away_goals_for=18,
        away_goals_against=15,
        points=45
    )

    palermo = Team(
        name="Palermo",
        league_position=8,
        form=['L', 'D', 'W', 'L', 'D'],
        home_goals_for=20,
        home_goals_against=18,
        away_goals_for=15,
        away_goals_against=22,
        points=38
    )

    # Head-to-head (last 5)
    h2h = [
        {'date': '2024-03-10', 'home': 'Brescia', 'away': 'Palermo', 'winner': 'Brescia', 'score': '2-1'},
        {'date': '2023-10-25', 'home': 'Palermo', 'away': 'Brescia', 'winner': 'Palermo', 'score': '1-0'},
        {'date': '2023-02-14', 'home': 'Brescia', 'away': 'Palermo', 'winner': 'Brescia', 'score': '3-2'},
        {'date': '2022-09-18', 'home': 'Palermo', 'away': 'Brescia', 'winner': 'Draw', 'score': '1-1'},
        {'date': '2022-02-27', 'home': 'Brescia', 'away': 'Palermo', 'winner': 'Brescia', 'score': '2-0'},
    ]

    match = Match(
        home_team=brescia,
        away_team=palermo,
        match_date=datetime.now() + timedelta(days=3),
        head_to_head=h2h
    )

    predictor = SerieBPredictor()
    prediction = predictor.predict(match)

    print(f"\n{'='*60}")
    print(f"Match: {match.home_team.name} vs {match.away_team.name}")
    print(f"Date: {match.match_date.strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")

    print(f"Probabilities:")
    print(f"  Home Win: {prediction.home_win_prob:.1%}")
    print(f"  Draw:     {prediction.draw_prob:.1%}")
    print(f"  Away Win: {prediction.away_win_prob:.1%}")
    print(f"\nRecommended: {prediction.recommended_outcome.value.upper()}")
    print(f"Confidence: {prediction.confidence}%")
    print(f"Value Bet: {'✅ Yes' if prediction.value_bet else '❌ No'}")
    print(f"\nReasoning: {prediction.reasoning}")
    print(f"{'='*60}\n")

    return prediction


if __name__ == "__main__":
    example_usage()
