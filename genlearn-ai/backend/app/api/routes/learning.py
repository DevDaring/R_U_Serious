"""
Learning Routes - Session management and content delivery
"""

import logging
from fastapi import APIRouter, HTTPException, status, Depends
from datetime import datetime
from typing import Optional

from app.api.dependencies import get_current_user
from app.database.csv_handler import CSVHandler
from app.database.file_handler import FileHandler
from app.models.session import (
    SessionCreate,
    LearningSession,
    SessionContent,
    SessionProgress,
    SessionEnd,
    SessionSummary,
    StorySegment
)
from app.services.content_generator import ContentGenerator
from app.utils.helpers import generate_unique_id
from app.utils.error_handler import handle_error, ErrorMessages

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/start", response_model=LearningSession, status_code=status.HTTP_201_CREATED)
async def start_learning_session(
    session_config: SessionCreate,
    current_user: dict = Depends(get_current_user)
):
    """
    Start a new learning session

    Args:
        session_config: Session configuration (topic, difficulty, etc.)
        current_user: Authenticated user

    Returns:
        Created learning session data
    """
    csv_handler = CSVHandler()
    content_generator = ContentGenerator()

    try:
        # Generate session ID
        session_id = generate_unique_id("SES")
        user_id = current_user["user_id"]

        # Calculate number of cycles based on duration
        # Rule: 5 minutes = 1 cycle, 15 minutes = 3 cycles, etc.
        total_cycles = max(1, session_config.duration_minutes // 5)

        # Create session record
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "topic": session_config.topic,
            "difficulty_level": session_config.difficulty_level,
            "duration_minutes": session_config.duration_minutes,
            "visual_style": session_config.visual_style,
            "story_style": session_config.story_style,
            "play_mode": session_config.play_mode,
            "avatar_id": session_config.avatar_id or "",
            "character_ids": ",".join(session_config.character_ids) if session_config.character_ids else "",
            "team_id": session_config.team_id or "",
            "tournament_id": session_config.tournament_id or "",
            "status": "in_progress",
            "current_cycle": 0,
            "total_cycles": total_cycles,
            "score": 0,
            "started_at": datetime.now().isoformat(),
            "completed_at": ""
        }

        # Save session to database
        csv_handler.create("sessions", session_data)

        # Return properly formatted response (convert for Pydantic model)
        response_data = {
            **session_data,
            "character_ids": session_config.character_ids or [],  # Return as list
            "completed_at": None  # Not completed yet
        }
        return response_data

    except HTTPException:
        raise
    except Exception as e:
        raise handle_error(
            e,
            "starting learning session",
            public_message=ErrorMessages.SESSION_ERROR,
            log_context={"user_id": current_user.get("user_id")}
        )


@router.get("/session/{session_id}/content", status_code=status.HTTP_200_OK)
async def get_session_content(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get learning content for a session

    Args:
        session_id: Session identifier
        current_user: Authenticated user

    Returns:
        Generated learning content with story segments and images
    """
    csv_handler = CSVHandler()
    content_generator = ContentGenerator()
    file_handler = FileHandler()

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

        # Get avatar and character info from session (stored during creation)
        avatar_description = None
        if session.get("avatar_id"):
            avatar = csv_handler.read_by_id("avatars", session["avatar_id"], "avatar_id")
            if avatar:
                avatar_description = avatar.get("name", "")

        character_descriptions = []
        if session.get("character_ids"):
            char_ids = session["character_ids"].split(",") if isinstance(session["character_ids"], str) else session["character_ids"]
            for char_id in char_ids:
                if char_id:
                    character = csv_handler.read_by_id("characters", char_id.strip(), "character_id")
                    if character:
                        char_desc = f"{character.get('name', 'Character')} - {character.get('description', '')}"
                        character_descriptions.append(char_desc)

        # Get story_style from session (default to "fun" if not set)
        story_style = session.get("story_style", "fun")

        # Generate content with story style
        content = await content_generator.generate_learning_content(
            topic=session["topic"],
            difficulty_level=session["difficulty_level"],
            visual_style=session["visual_style"],
            story_style=story_style,
            num_segments=session["total_cycles"],
            avatar_description=avatar_description,
            character_descriptions=character_descriptions if character_descriptions else None
        )

        # Save images and create URLs
        story_segments = []
        for idx, segment in enumerate(content["story_segments"]):
            # Generate image using scene_description (not image_prompt - no text in image)
            image_prompt = segment.get("scene_description") or segment.get("image_prompt", f"Scene for {session['topic']}")
            image_data = await content_generator.generate_image(
                prompt=image_prompt,
                style=session["visual_style"]
            )

            # Save image
            image_filename = f"ses_{session_id}_img_{idx + 1}.png"
            image_path = file_handler.save_image(
                image_data,
                "generated_images",
                image_filename
            )

            # Create history record
            history_data = {
                "history_id": generate_unique_id("HIS"),
                "user_id": current_user["user_id"],
                "session_id": session_id,
                "content_type": "image",
                "content_id": f"IMG{idx + 1:03d}",
                "content_path": image_path,
                "topic": session["topic"],
                "viewed_at": datetime.now().isoformat()
            }
            csv_handler.create("learning_history", history_data)

            # Create enhanced story segment with image URL, text overlay, and quiz
            seg_quiz = segment.get("quiz")
            if not seg_quiz or not seg_quiz.get("options") or any(opt.get("text", "").startswith("Option ") for opt in seg_quiz.get("options", [])):
                # AI didn't generate quiz or returned placeholders — generate from narrative
                narrative = segment.get("narrative", "")
                facts = segment.get("facts", [])
                fact_text = facts[0] if facts else f"a key concept about {session['topic']}"
                seg_quiz = {
                    "question_id": f"Q{idx + 1}",
                    "question_text": f"Based on what you just read, which of the following is true about {session['topic']}?",
                    "options": [
                        {"key": "A", "text": fact_text, "is_correct": True},
                        {"key": "B", "text": f"{session['topic']} has no known real-world applications", "is_correct": False},
                        {"key": "C", "text": f"{session['topic']} was disproved by modern research", "is_correct": False},
                        {"key": "D", "text": f"{session['topic']} only applies in theoretical scenarios", "is_correct": False}
                    ],
                    "correct_answers": ["A"],
                    "explanation": f"As described in the narrative: {fact_text}",
                    "is_multi_select": False,
                    "points": 10
                }
            else:
                seg_quiz["question_id"] = seg_quiz.get("question_id", f"Q{idx + 1}")
                seg_quiz["is_multi_select"] = seg_quiz.get("is_multi_select", False)
                seg_quiz["points"] = seg_quiz.get("points", 10)

            story_segments.append({
                "segment_number": segment.get("segment_number", idx + 1),
                "narrative": segment.get("narrative", ""),
                "scene_description": segment.get("scene_description", segment.get("image_prompt", "")),
                "scene_image_url": f"/media/{image_path}",
                "text_overlay": segment.get("text_overlay", {
                    "text": "",
                    "position": "bottom",
                    "style": "caption"
                }),
                "audio_url": None,
                "quiz": seg_quiz
            })

        # Save session content to CSV for revision/history
        import json
        for seg in story_segments:
            content_data = {
                "content_id": generate_unique_id("CON"),
                "session_id": session_id,
                "user_id": current_user["user_id"],
                "segment_number": seg["segment_number"],
                "narrative": seg["narrative"],
                "scene_description": seg.get("scene_description", ""),
                "scene_image_url": seg["scene_image_url"],
                "text_overlay": json.dumps(seg.get("text_overlay", {})),
                "quiz_question": seg["quiz"].get("question_text", "") if seg.get("quiz") else "",
                "quiz_options": json.dumps(seg["quiz"].get("options", [])) if seg.get("quiz") else "[]",
                "quiz_correct_answers": json.dumps(seg["quiz"].get("correct_answers", [])) if seg.get("quiz") else "[]",
                "quiz_explanation": seg["quiz"].get("explanation", "") if seg.get("quiz") else "",
                "created_at": datetime.now().isoformat()
            }
            csv_handler.create("session_content", content_data)

        return {
            "session_id": session_id,
            "topic": session["topic"],
            "story_style": session.get("story_style", "fun"),
            "story_segments": story_segments,
            "topic_summary": content.get("topic_summary", ""),
            "total_cycles": session["total_cycles"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise handle_error(
            e,
            "generating content",
            public_message=ErrorMessages.CONTENT_GENERATION_ERROR,
            log_context={"session_id": session_id}
        )


@router.post("/session/{session_id}/progress", status_code=status.HTTP_200_OK)
async def update_session_progress(
    session_id: str,
    progress: SessionProgress,
    current_user: dict = Depends(get_current_user)
):
    """
    Update session progress

    Args:
        session_id: Session identifier
        progress: Progress update data
        current_user: Authenticated user

    Returns:
        Success message
    """
    csv_handler = CSVHandler()

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

        # Update progress
        session["current_cycle"] = progress.current_cycle
        if progress.score is not None:
            session["score"] = progress.score

        # Save to database
        csv_handler.update("sessions", session_id, session, "session_id")

        return {"message": "Progress updated successfully", "session": session}

    except HTTPException:
        raise
    except Exception as e:
        raise handle_error(
            e,
            "updating session progress",
            public_message=ErrorMessages.SESSION_ERROR,
            log_context={"session_id": session_id}
        )


@router.post("/session/{session_id}/end", response_model=SessionSummary, status_code=status.HTTP_200_OK)
async def end_learning_session(
    session_id: str,
    session_end: SessionEnd,
    current_user: dict = Depends(get_current_user)
):
    """
    End a learning session and calculate final results

    Args:
        session_id: Session identifier
        session_end: Final session data
        current_user: Authenticated user

    Returns:
        Session summary with statistics
    """
    csv_handler = CSVHandler()

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

        # Update session
        session["status"] = "completed" if session_end.completed else "abandoned"
        session["score"] = session_end.final_score
        session["completed_at"] = datetime.now().isoformat()

        csv_handler.update("sessions", session_id, session, "session_id")

        # Get all answers for this session
        all_scores = csv_handler.read_all("scores")
        session_scores = [s for s in all_scores if s.get("session_id") == session_id]

        total_questions = len(session_scores)
        correct_answers = sum(1 for s in session_scores if s.get("is_correct") == "true")
        accuracy_rate = (correct_answers / total_questions * 100) if total_questions > 0 else 0.0

        # Calculate XP earned (base on score and difficulty)
        xp_earned = session_end.final_score * session["difficulty_level"]

        # Update user XP
        current_user["xp_points"] = int(current_user.get("xp_points", 0)) + xp_earned
        current_user["level"] = max(1, int(current_user["xp_points"]) // 500 + 1)
        csv_handler.update("users", current_user["user_id"], current_user, "user_id")

        return {
            "session_id": session_id,
            "topic": session["topic"],
            "difficulty_level": session["difficulty_level"],
            "duration_minutes": session["duration_minutes"],
            "score": session_end.final_score,
            "total_questions": total_questions,
            "correct_answers": correct_answers,
            "accuracy_rate": round(accuracy_rate, 2),
            "xp_earned": xp_earned,
            "time_spent_seconds": session_end.total_time_seconds,
            "completed_at": session["completed_at"]
        }

    except HTTPException:
        raise
    except Exception as e:
        raise handle_error(
            e,
            "ending learning session",
            public_message=ErrorMessages.SESSION_ERROR,
            log_context={"session_id": session_id}
        )


@router.get("/sessions", status_code=status.HTTP_200_OK)
async def get_sessions_list(
    limit: int = 10,
    offset: int = 0
):
    """
    Get learning sessions list (public endpoint for history loading)
    
    Returns sessions from sessions.csv for Mistake Autopsy integration.
    No auth required since frontend calls this during history loading.
    """
    try:
        csv_handler = CSVHandler()
        
        # Get all sessions (no user filter for guest mode)
        all_sessions = csv_handler.read_all("sessions")
        
        # Sort by started_at (most recent first)
        all_sessions.sort(key=lambda x: x.get("started_at", "") or "", reverse=True)
        
        # Paginate
        paginated = all_sessions[offset:offset + limit]
        
        # Format for Mistake Autopsy
        sessions = []
        for session in paginated:
            sessions.append({
                "session_id": session.get("session_id"),
                "topic": session.get("topic"),
                "subject": "General Learning",
                "difficulty_level": int(session.get("difficulty_level", 5)),
                "status": session.get("status"),
                "story_style": session.get("story_style", ""),
                "visual_style": session.get("visual_style", "cartoon"),
                "score": int(session.get("score", 0)),
                "started_at": session.get("started_at"),
                "completed_at": session.get("completed_at")
            })
        
        return {"sessions": sessions}
        
    except Exception as e:
        logger.error(f"Error loading sessions: {e}")
        return {"sessions": []}


@router.get("/history", status_code=status.HTTP_200_OK)
async def get_session_history(
    current_user: dict = Depends(get_current_user),
    limit: int = 20,
    offset: int = 0
):
    """
    Get user's learning session history for revision

    Returns list of past sessions with basic info
    """
    try:
        csv_handler = CSVHandler()
        
        # Get all sessions for user
        all_sessions = csv_handler.read_all("sessions")
        user_sessions = [s for s in all_sessions if s.get("user_id") == current_user["user_id"]]
        
        # Sort by started_at (most recent first)
        user_sessions.sort(key=lambda x: x.get("started_at", ""), reverse=True)
        
        # Paginate
        paginated = user_sessions[offset:offset + limit]
        
        # Format response
        history = []
        for session in paginated:
            history.append({
                "session_id": session["session_id"],
                "topic": session["topic"],
                "difficulty_level": int(session.get("difficulty_level", 5)),
                "duration_minutes": int(session.get("duration_minutes", 10)),
                "story_style": session.get("story_style", "fun"),
                "visual_style": session.get("visual_style", "cartoon"),
                "score": int(session.get("score", 0)),
                "status": session.get("status", "unknown"),
                "started_at": session.get("started_at", ""),
                "completed_at": session.get("completed_at", "")
            })
        
        return {
            "sessions": history,
            "total": len(user_sessions),
            "limit": limit,
            "offset": offset
        }
    
    except Exception as e:
        raise handle_error(
            e,
            "fetching session history",
            public_message="Failed to load history"
        )


@router.get("/history/{session_id}", status_code=status.HTTP_200_OK)
async def get_session_revision(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get complete session content for revision

    Returns session with all story segments and quizzes
    """
    import json
    
    try:
        csv_handler = CSVHandler()
        
        # Get session
        session = csv_handler.read_by_id("sessions", session_id, "session_id")
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Session not found"
            )
        
        # Verify ownership
        if session.get("user_id") != current_user["user_id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )
        
        # Get session content
        all_content = csv_handler.read_all("session_content")
        session_content = [c for c in all_content if c.get("session_id") == session_id]
        session_content.sort(key=lambda x: int(x.get("segment_number", 0)))
        
        # Build story segments from stored content
        story_segments = []
        for content in session_content:
            try:
                text_overlay = json.loads(content.get("text_overlay", "{}"))
            except:
                text_overlay = {"text": "", "position": "bottom", "style": "caption"}
            
            try:
                options = json.loads(content.get("quiz_options", "[]"))
            except:
                options = []
            
            try:
                correct_answers = json.loads(content.get("quiz_correct_answers", "[]"))
            except:
                correct_answers = []
            
            story_segments.append({
                "segment_number": int(content.get("segment_number", 1)),
                "narrative": content.get("narrative", ""),
                "scene_description": content.get("scene_description", ""),
                "scene_image_url": content.get("scene_image_url", ""),
                "text_overlay": text_overlay,
                "audio_url": None,
                "quiz": {
                    "question_id": f"Q{content.get('segment_number', 1)}",
                    "question_text": content.get("quiz_question", ""),
                    "options": options,
                    "correct_answers": correct_answers,
                    "explanation": content.get("quiz_explanation", ""),
                    "is_multi_select": False,
                    "points": 10
                }
            })
        
        return {
            "session_id": session_id,
            "topic": session["topic"],
            "difficulty_level": int(session.get("difficulty_level", 5)),
            "duration_minutes": int(session.get("duration_minutes", 10)),
            "story_style": session.get("story_style", "fun"),
            "visual_style": session.get("visual_style", "cartoon"),
            "score": int(session.get("score", 0)),
            "status": session.get("status", "unknown"),
            "started_at": session.get("started_at", ""),
            "completed_at": session.get("completed_at", ""),
            "story_segments": story_segments,
            "total_segments": len(story_segments)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise handle_error(
            e,
            "fetching session revision",
            public_message="Failed to load session content"
        )
