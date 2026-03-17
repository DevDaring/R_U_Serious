"""
Video Routes - Video generation and status
"""

from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional

from app.api.dependencies import get_current_user, verify_api_key
from app.database.csv_handler import CSVHandler
from app.services.video_generator import VideoGenerator

router = APIRouter()


class VideoStatus(BaseModel):
    """Video generation status model"""
    session_id: str
    cycle_number: int
    status: str  # 'generating', 'ready', 'failed', 'not_started'
    video_url: Optional[str] = None
    progress_percent: Optional[int] = None
    error_message: Optional[str] = None


@router.get("/session/{session_id}/cycle/{cycle_number}", response_model=VideoStatus, status_code=status.HTTP_200_OK)
async def get_video(
    session_id: str,
    cycle_number: int,
    current_user: dict = Depends(get_current_user),
    api_key_valid: bool = Depends(verify_api_key)
):
    """
    Get video for a specific cycle (triggers generation if not exists)
    """
    csv_handler = CSVHandler()
    video_generator = VideoGenerator()

    try:
        # Get session
        session = csv_handler.read_by_id("sessions", session_id, "session_id")
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        # Verify user owns this session
        if session.get("user_id") != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this session"
            )

        # Check if video already exists
        all_history = csv_handler.read_all("learning_history")
        session_history = [
            h for h in all_history
            if h.get("session_id") == session_id and h.get("content_type") == "video"
        ]

        video_record = None
        for h in session_history:
            if f"cycle_{cycle_number}" in h.get("content_path", ""):
                video_record = h
                break

        if video_record:
            return {
                "session_id": session_id,
                "cycle_number": cycle_number,
                "status": "ready",
                "video_url": f"/media/{video_record['content_path']}",
                "progress_percent": 100
            }
        else:
            try:
                video_url = await video_generator.generate_cycle_video(
                    session_id=session_id,
                    cycle_number=cycle_number,
                    user_id=current_user["user_id"]
                )

                return {
                    "session_id": session_id,
                    "cycle_number": cycle_number,
                    "status": "ready",
                    "video_url": video_url,
                    "progress_percent": 100
                }
            except Exception as gen_error:
                return {
                    "session_id": session_id,
                    "cycle_number": cycle_number,
                    "status": "failed",
                    "progress_percent": 0,
                    "error_message": str(gen_error)
                }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching video: {str(e)}"
        )


@router.get("/session/{session_id}/cycle/{cycle_number}/status", response_model=VideoStatus, status_code=status.HTTP_200_OK)
async def get_video_status(
    session_id: str,
    cycle_number: int,
    current_user: dict = Depends(get_current_user),
    api_key_valid: bool = Depends(verify_api_key)
):
    """
    Check video generation status without triggering generation
    """
    csv_handler = CSVHandler()

    try:
        session = csv_handler.read_by_id("sessions", session_id, "session_id")
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )

        if session.get("user_id") != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied to this session"
            )

        all_history = csv_handler.read_all("learning_history")
        session_history = [
            h for h in all_history
            if h.get("session_id") == session_id and h.get("content_type") == "video"
        ]

        video_record = None
        for h in session_history:
            if f"cycle_{cycle_number}" in h.get("content_path", ""):
                video_record = h
                break

        if video_record:
            return {
                "session_id": session_id,
                "cycle_number": cycle_number,
                "status": "ready",
                "video_url": f"/media/{video_record['content_path']}",
                "progress_percent": 100
            }
        else:
            return {
                "session_id": session_id,
                "cycle_number": cycle_number,
                "status": "not_started",
                "progress_percent": 0
            }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error checking video status: {str(e)}"
        )
