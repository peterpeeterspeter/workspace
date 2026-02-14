

@app.get("/api/v1/admin/agents/{agent_id}/reputation-history")
async def get_reputation_history(agent_id: str):
    """
    Get reputation score history for a specific agent (US-007).

    Returns list of reputation changes with timestamps and reasons.

    Args:
        agent_id: Agent ID to query

    Returns:
        Reputation history response
    """
    try:
        # Import database and models
        try:
            from api.database import get_db
            from api.models import Agent, ReputationHistory
        except ImportError:
            from database import get_db
            from models import Agent, ReputationHistory

        with get_db() as db:
            # Check if agent exists
            agent = db.query(Agent).filter(Agent.id == agent_id).first()
            if not agent:
                raise HTTPException(
                    status_code=404,
                    detail=f"Agent not found: {agent_id}"
                )

            # Query reputation history (most recent first)
            history = db.query(ReputationHistory).filter(
                ReputationHistory.agent_id == agent_id
            ).order_by(ReputationHistory.timestamp.desc()).limit(100).all()

            # Format response
            history_data = []
            for entry in history:
                history_data.append({
                    "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
                    "old_score": entry.old_score,
                    "new_score": entry.new_score,
                    "change": entry.new_score - entry.old_score,
                    "reason": entry.change_reason
                })

            response_data = {
                "agent_id": agent_id,
                "current_score": agent.reputation_score,
                "history_count": len(history_data),
                "history": history_data
            }

            return response_data

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error getting reputation history: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )
