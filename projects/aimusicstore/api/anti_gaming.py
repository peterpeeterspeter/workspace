# api/anti_gaming.py
"""
Anti-Gaming System for aimusicstore.com

Detects and prevents voting manipulation to maintain ranking integrity.

Components:
- Reputation scoring: Calculate agent trustworthiness
- Pattern detection: Identify suspicious voting behavior
- Flagging system: Mark and block malicious agents
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
from sqlalchemy import func
from sqlalchemy.orm import Session
import logging

try:
    from api.models import Vote, Agent, ReputationHistory
except ImportError:
    from models import Vote, Agent, ReputationHistory

logger = logging.getLogger(__name__)


class AntiGamingDetector:
    """
    Detects suspicious voting patterns and manipulative behavior.
    
    Detection Methods:
    1. Burst Voting: Multiple votes in short time window
    2. Unidirectional Voting: Always voting same direction
    3. Coordinated Attacks: Multiple agents with identical patterns
    4. Platform Bias: Excessive votes for same platform
    """
    
    # Detection thresholds
    BURST_THRESHOLD = 10  # votes in BURST_WINDOW seconds
    BURST_WINDOW = 60  # seconds
    UNIDIRECTIONAL_THRESHOLD = 20  # min votes before checking
    UNIDIRECTIONAL_RATIO = 1.0  # 100% same direction = suspicious
    PLATFORM_BIAS_THRESHOLD = 0.8  # 80% votes for same platform
    
    def __init__(self, db: Session):
        self.db = db
    
    def check_burst_voting(self, agent_id: str) -> Tuple[bool, Optional[str]]:
        """
        Detect burst voting (too many votes in short time).
        
        Args:
            agent_id: Agent to check
        
        Returns:
            (is_suspicious, reason)
        """
        try:
            # Get recent votes for this agent
            cutoff_time = datetime.utcnow() - timedelta(seconds=self.BURST_WINDOW)
            
            recent_votes = self.db.query(Vote).filter(
                Vote.agent_id == agent_id,
                Vote.timestamp >= cutoff_time
            ).count()
            
            if recent_votes >= self.BURST_THRESHOLD:
                reason = f"Burst voting: {recent_votes} votes in {self.BURST_WINDOW} seconds"
                logger.warning(f"Agent {agent_id}: {reason}")
                return True, reason
            
            return False, None
            
        except Exception as e:
            logger.error(f"Error checking burst voting for {agent_id}: {e}")
            return False, None
    
    def check_unidirectional_voting(self, agent_id: str) -> Tuple[bool, Optional[str]]:
        """
        Detect agents that always vote in same direction (suspicious).
        
        Args:
            agent_id: Agent to check
        
        Returns:
            (is_suspicious, reason)
        """
        try:
            # Get all votes for this agent
            votes = self.db.query(Vote).filter(Vote.agent_id == agent_id).all()
            
            # Need minimum votes before checking
            if len(votes) < self.UNIDIRECTIONAL_THRESHOLD:
                return False, None
            
            # Calculate ratio
            up_votes = sum(1 for v in votes if v.vote == 'up')
            down_votes = sum(1 for v in votes if v.vote == 'down')
            total_votes = len(votes)
            
            up_ratio = up_votes / total_votes
            down_ratio = down_votes / total_votes
            
            # Check if 100% one direction
            if up_ratio >= self.UNIDIRECTIONAL_RATIO:
                reason = f"Unidirectional: 100% upvotes ({up_votes} votes)"
                logger.warning(f"Agent {agent_id}: {reason}")
                return True, reason
            
            if down_ratio >= self.UNIDIRECTIONAL_RATIO:
                reason = f"Unidirectional: 100% downvotes ({down_votes} votes)"
                logger.warning(f"Agent {agent_id}: {reason}")
                return True, reason
            
            return False, None
            
        except Exception as e:
            logger.error(f"Error checking unidirectional voting for {agent_id}: {e}")
            return False, None
    
    def check_coordinated_attacks(self, agent_id: str, item_id: str, vote: str) -> Tuple[bool, Optional[str]]:
        """
        Detect coordinated voting (multiple agents voting identically).
        
        Args:
            agent_id: Agent casting vote
            item_id: Item being voted on
            vote: Vote direction
        
        Returns:
            (is_suspicious, reason)
        """
        try:
            # Look for recent votes on this item from other agents
            # with same vote direction within 5 minutes
            cutoff_time = datetime.utcnow() - timedelta(minutes=5)
            
            similar_votes = self.db.query(Vote).filter(
                Vote.item_id == item_id,
                Vote.vote == vote,
                Vote.timestamp >= cutoff_time,
                Vote.agent_id != agent_id
            ).all()
            
            # If 5+ agents voted same way in 5 minutes, suspicious
            if len(similar_votes) >= 5:
                other_agents = [v.agent_id for v in similar_votes]
                reason = f"Coordinated attack: {len(similar_votes)+1} agents voted {vote} on {item_id} in 5 minutes"
                logger.warning(f"Agent {agent_id}: {reason}, others: {other_agents}")
                return True, reason
            
            return False, None
            
        except Exception as e:
            logger.error(f"Error checking coordinated attacks for {agent_id}: {e}")
            return False, None
    
    def check_platform_bias(self, agent_id: str) -> Tuple[bool, Optional[str]]:
        """
        Detect agents that exclusively vote for songs from same platform.
        
        Args:
            agent_id: Agent to check
        
        Returns:
            (is_suspicious, reason)
        """
        try:
            # Get all song votes for this agent
            song_votes = self.db.query(Vote).filter(
                Vote.agent_id == agent_id,
                Vote.item_type == 'song'
            ).all()
            
            # Need minimum votes
            if len(song_votes) < 10:
                return False, None
            
            # Join with songs to get platforms
            # For MVP, we'll use a simpler approach
            # Check if agent votes on songs with similar IDs (suggesting same platform)
            song_ids = [v.item_id for v in song_votes]
            
            # Extract platform prefix (e.g., "suno" from "suno-abc123")
            platforms = []
            for sid in song_ids:
                if '-' in sid:
                    platform = sid.split('-')[0]
                    platforms.append(platform)
            
            if not platforms:
                return False, None
            
            # Calculate ratio of most common platform
            from collections import Counter
            platform_counts = Counter(platforms)
            top_platform, count = platform_counts.most_common(1)[0]
            bias_ratio = count / len(platforms)
            
            if bias_ratio >= self.PLATFORM_BIAS_THRESHOLD:
                reason = f"Platform bias: {bias_ratio:.1%} votes for '{top_platform}' platform"
                logger.warning(f"Agent {agent_id}: {reason}")
                return True, reason
            
            return False, None
            
        except Exception as e:
            logger.error(f"Error checking platform bias for {agent_id}: {e}")
            return False, None
    
    def detect_suspicious_activity(self, agent_id: str, item_id: str, vote: str) -> Tuple[bool, List[str]]:
        """
        Run all detection methods on a vote before it's recorded.
        
        Args:
            agent_id: Agent casting vote
            item_id: Item being voted on
            vote: Vote direction
        
        Returns:
            (is_suspicious, reasons)
        """
        suspicious_reasons = []
        
        # 1. Burst voting check
        is_burst, burst_reason = self.check_burst_voting(agent_id)
        if is_burst:
            suspicious_reasons.append(burst_reason)
        
        # 2. Unidirectional voting check
        is_unidirectional, unidirectional_reason = self.check_unidirectional_voting(agent_id)
        if is_unidirectional:
            suspicious_reasons.append(unidirectional_reason)
        
        # 3. Coordinated attack check
        is_coordinated, coordinated_reason = self.check_coordinated_attacks(agent_id, item_id, vote)
        if is_coordinated:
            suspicious_reasons.append(coordinated_reason)
        
        # 4. Platform bias check (less aggressive - only if other checks passed)
        if not suspicious_reasons:
            is_biased, bias_reason = self.check_platform_bias(agent_id)
            if is_biased:
                suspicious_reasons.append(bias_reason)
        
        is_suspicious = len(suspicious_reasons) > 0
        return is_suspicious, suspicious_reasons


class ReputationCalculator:
    """
    Calculate agent reputation scores based on voting behavior.
    
    Reputation Factors (Weighted):
    - Vote diversity: 30% (not all same direction)
    - Time consistency: 25% (votes spread over time, not bursts)
    - Platform diversity: 20% (votes across different platforms)
    - Account age: 15% (older accounts more trusted)
    - Total votes: 10% (more votes = more data)
    
    Final Score: 0-100
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def calculate_reputation(self, agent_id: str) -> int:
        """
        Calculate comprehensive reputation score for an agent.
        
        Args:
            agent_id: Agent to score
        
        Returns:
            Reputation score (0-100)
        """
        try:
            # Get agent data
            agent = self.db.query(Agent).filter(Agent.id == agent_id).first()
            if not agent:
                return 50  # Neutral score for new agents
            
            # Get all votes for this agent
            votes = self.db.query(Vote).filter(Vote.agent_id == agent_id).all()
            
            if not votes:
                return 50  # Neutral for agents with no votes
            
            # Calculate individual factors
            diversity_score = self._calculate_diversity_score(votes)
            consistency_score = self._calculate_time_consistency(votes)
            platform_score = self._calculate_platform_diversity(agent_id, votes)
            age_score = self._calculate_age_score(agent)
            volume_score = self._calculate_volume_score(len(votes))
            
            # Weighted average
            reputation = (
                diversity_score * 0.30 +
                consistency_score * 0.25 +
                platform_score * 0.20 +
                age_score * 0.15 +
                volume_score * 0.10
            )
            
            # Ensure 0-100 range
            reputation = max(0, min(100, int(reputation)))
            
            logger.info(f"Agent {agent_id} reputation: {reputation} "
                       f"(diversity={diversity_score}, consistency={consistency_score}, "
                       f"platform={platform_score}, age={age_score}, volume={volume_score})")
            
            return reputation
            
        except Exception as e:
            logger.error(f"Error calculating reputation for {agent_id}: {e}")
            return 50  # Default neutral score
    
    def _calculate_diversity_score(self, votes: List[Vote]) -> int:
        """
        Score based on vote direction diversity (0-100).
        
        Perfect balance (50% up, 50% down) = 100
        All one direction = 0
        """
        if not votes:
            return 50
        
        up_count = sum(1 for v in votes if v.vote == 'up')
        down_count = sum(1 for v in votes if v.vote == 'down')
        total = len(votes)
        
        up_ratio = up_count / total
        
        # Calculate deviation from perfect balance (0.5)
        deviation = abs(up_ratio - 0.5)
        
        # Convert to score: 0 deviation = 100, 0.5 deviation = 0
        score = int(100 * (1 - (deviation * 2)))
        
        return max(0, score)
    
    def _calculate_time_consistency_score(self, votes: List[Vote]) -> int:
        """
        Score based on vote timing consistency (0-100).
        
        Votes spread evenly over time = 100
        Votes clustered in bursts = 0
        """
        if not votes:
            return 100
        
        if len(votes) < 5:
            return 100  # Not enough data, give benefit of doubt
        
        # Sort votes by timestamp
        sorted_votes = sorted(votes, key=lambda v: v.timestamp)
        
        # Calculate time differences between consecutive votes
        time_diffs = []
        for i in range(1, len(sorted_votes)):
            diff = (sorted_votes[i].timestamp - sorted_votes[i-1].timestamp).total_seconds()
            time_diffs.append(diff)
        
        if not time_diffs:
            return 100
        
        # Calculate coefficient of variation (std / mean)
        import statistics
        mean_diff = statistics.mean(time_diffs)
        if mean_diff == 0:
            return 0  # All votes at same time = suspicious
        
        std_diff = statistics.stdev(time_diffs)
        cv = std_diff / mean_diff  # Coefficient of variation
        
        # Lower CV = more consistent = higher score
        # CV > 2 = very irregular = suspicious
        # CV < 0.5 = very consistent = good
        score = int(100 * max(0, 1 - (cv / 2)))
        
        return max(0, score)
    
    def _calculate_time_consistency(self, votes: List[Vote]) -> int:
        """
        Simplified version: check for burst patterns.
        """
        if not votes:
            return 100
        
        if len(votes) < 5:
            return 100
        
        # Count how many votes happened within 1 minute of another vote
        burst_count = 0
        for i, vote1 in enumerate(votes):
            for vote2 in votes[i+1:]:
                time_diff = abs((vote1.timestamp - vote2.timestamp).total_seconds())
                if time_diff <= 60:
                    burst_count += 1
                    break
        
        # If more than 50% of votes are in bursts, low score
        burst_ratio = burst_count / len(votes)
        score = int(100 * (1 - burst_ratio))
        
        return max(0, score)
    
    def _calculate_platform_diversity(self, agent_id: str, votes: List[Vote]) -> int:
        """
        Score based on platform diversity (0-100).
        
        Votes across many platforms = 100
        Votes only from one platform = 0
        """
        # Only check song votes for platform info
        song_votes = [v for v in votes if v.item_type == 'song']
        
        if not song_votes:
            return 100  # No song votes, can't determine bias
        
        # Extract platforms from song IDs
        platforms = set()
        for v in song_votes:
            if '-' in v.item_id:
                platform = v.item_id.split('-')[0]
                platforms.add(platform)
        
        if not platforms:
            return 50  # Can't determine
        
        # More platforms = higher score
        # 1 platform = 0, 5+ platforms = 100
        platform_count = len(platforms)
        score = min(100, platform_count * 25)
        
        return score
    
    def _calculate_age_score(self, agent: Agent) -> int:
        """
        Score based on account age (0-100).
        
        Older accounts = more trusted (up to a point)
        """
        age_days = (datetime.utcnow() - agent.created_at).days
        
        # 0-7 days: ramping up (0-50 points)
        # 7-30 days: established (50-75 points)
        # 30+ days: trusted (75-100 points)
        
        if age_days < 7:
            return min(50, age_days * 7)
        elif age_days < 30:
            return 50 + min(25, (age_days - 7) * 2)
        else:
            return min(100, 75 + min(25, (age_days - 30) // 7))
    
    def _calculate_volume_score(self, total_votes: int) -> int:
        """
        Score based on total vote count (0-100).
        
        More votes = more data points = more reliable
        But with diminishing returns
        """
        # 0-10 votes: ramping up
        # 10-100 votes: good data
        # 100+ votes: excellent data
        
        if total_votes < 10:
            return total_votes * 10
        elif total_votes < 100:
            return 100
        else:
            return 100  # Max score, no extra benefit


def update_agent_reputation(db: Session, agent_id: str, reason: str = "Vote recorded") -> int:
    """
    Update agent's reputation score in database (US-007: with history tracking).
    
    Args:
        db: Database session
        agent_id: Agent to update
        reason: Why the reputation changed (default: "Vote recorded")
    
    Returns:
        New reputation score
    """
    try:
        calculator = ReputationCalculator(db)
        new_score = calculator.calculate_reputation(agent_id)
        
        # Update agent in database
        agent = db.query(Agent).filter(Agent.id == agent_id).first()
        if agent:
            old_score = agent.reputation_score
            
            # Only record history if score actually changed
            if old_score != new_score:
                # Record reputation history (US-007)
                history_entry = ReputationHistory(
                    agent_id=agent_id,
                    old_score=old_score,
                    new_score=new_score,
                    change_reason=reason
                )
                db.add(history_entry)
                
                # Update agent reputation
                agent.reputation_score = new_score
                db.commit()
                
                logger.info(f"Updated reputation for agent {agent_id}: {old_score} → {new_score} ({reason})")
            else:
                logger.debug(f"Reputation unchanged for agent {agent_id}: {new_score}")
        else:
            logger.warning(f"Agent {agent_id} not found for reputation update")
        
        return new_score
        
    except Exception as e:
        db.rollback()
        logger.error(f"Failed to update reputation for {agent_id}: {e}")
        return 50  # Return neutral score on error
