"""
Sessions Routes - General session listing for history integration
"""

import logging
from fastapi import APIRouter, status
from app.database.csv_handler import CSVHandler

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", status_code=status.HTTP_200_OK)
async def get_all_sessions(limit: int = 10, offset: int = 0):
    """
    Get all learning sessions for history loading
    
    Returns sessions from sessions.csv for Mistake Autopsy integration.
    Public endpoint - no auth required for guest mode.
    """
    try:
        csv_handler = CSVHandler()
        
        # Get all sessions
        all_sessions = csv_handler.read_all("sessions")
        
        # Sort by started_at (most recent first)
        all_sessions.sort(key=lambda x: x.get("started_at", "") or "", reverse=True)
        
        # Paginate
        paginated = all_sessions[offset:offset + limit]
        
        # Format response for Mistake Autopsy
        sessions = []
        for session in paginated:
            sessions.append({
                "session_id": session.get("session_id"),
                "topic": session.get("topic"),
                "subject": "Learning Session",
                "difficulty_level": int(session.get("difficulty_level", 5) or 5),
                "status": session.get("status"),
                "story_style": session.get("story_style", ""),
                "visual_style": session.get("visual_style", "cartoon"),
                "score": int(session.get("score", 0) or 0),
                "started_at": session.get("started_at"),
                "completed_at": session.get("completed_at")
            })
        
        return {"sessions": sessions}
        
    except Exception as e:
        logger.error(f"Error loading sessions: {e}")
        return {"sessions": []}
