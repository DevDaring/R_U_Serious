"""
Enhanced Features Routes - All 8 new AI-powered features
"""

import logging
import base64
import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form
from pydantic import BaseModel
from typing import Optional, List

from app.api.dependencies import get_current_user
from app.database.csv_handler import CSVHandler
from app.services.feature_chat import feature_chat_service
from app.services.content_generator import ContentGenerator
from app.services.provider_factory import ProviderFactory
from app.services.image_providers.base import ImageGenerationRequest
from app.utils.helpers import generate_unique_id

logger = logging.getLogger(__name__)
router = APIRouter()
csv_handler = CSVHandler()
content_generator = ContentGenerator()


# ============================================================
# Pydantic Models
# ============================================================

class LessonRequest(BaseModel):
    image_description: str
    subject: str
    topic: str
    grade_level: int = 10
    user_message: str
    language: str = "en"

class ReverseClassroomRequest(BaseModel):
    topic: str
    persona: str = "curious_beginner"
    user_message: str
    session_id: Optional[str] = None
    language: str = "en"

class TimeTravelRequest(BaseModel):
    character_name: str
    user_message: str
    session_id: Optional[str] = None
    language: str = "en"

class ConceptCollisionRequest(BaseModel):
    topics: List[dict]
    language: str = "en"

class MistakeAutopsyRequest(BaseModel):
    question: str
    correct_answer: str
    student_answer: str
    subject: str
    topic: str
    language: str = "en"

class YouTubeRequest(BaseModel):
    video_url: str = None
    transcript: str = None
    title: str = None
    channel: str = None
    duration: str = None
    language: str = "en"

class DebateRequest(BaseModel):
    topic: str
    student_position: str
    user_message: str
    difficulty: str = "casual"
    round_number: int = 1
    session_id: Optional[str] = None
    language: str = "en"

class DreamProjectRequest(BaseModel):
    dream: str
    grade_level: int = 10
    hours_per_week: int = 5
    user_message: Optional[str] = None
    session_id: Optional[str] = None
    language: str = "en"


# ============================================================
# Feature 2: Learn from Anything 📸
# ============================================================

@router.post("/learn-from-image/analyze", status_code=status.HTTP_200_OK)
async def analyze_image(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """Analyze uploaded image and suggest learning opportunities"""
    try:
        # Read and encode image
        contents = await file.read()
        image_base64 = base64.b64encode(contents).decode('utf-8')
        
        # Get AI analysis
        response = await feature_chat_service.get_response(
            feature_type="learn_from_anything_analyze",
            user_message="Analyze this image for educational opportunities",
            context={},
            image_base64=image_base64,
            language="en"  # Image analysis stays in English
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Image analysis error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/learn-from-image/lesson", status_code=status.HTTP_200_OK)
async def get_image_lesson(
    request: LessonRequest,
    current_user: dict = Depends(get_current_user)
):
    """Get a lesson based on the selected topic from image"""
    try:
        response = await feature_chat_service.get_response(
            feature_type="learn_from_anything_lesson",
            user_message=request.user_message,
            context={
                "image_description": request.image_description,
                "subject": request.subject,
                "topic": request.topic,
                "grade_level": request.grade_level
            },
            language=request.language
        )
        
        # Generate image if requested
        if response.get("generate_image") and response.get("image_prompt"):
            try:
                image_data = await content_generator.generate_image(
                    prompt=response["image_prompt"],
                    style=response.get("image_style", "cartoon")
                )
                # Return as base64 inline (Cloud Run ephemeral storage)
                import base64 as b64
                response["image_url"] = f"data:image/png;base64,{b64.b64encode(image_data).decode('utf-8')}"
            except Exception as img_err:
                logger.warning(f"Image generation failed: {img_err}")
        
        return response
        
    except Exception as e:
        logger.error(f"Lesson error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# Feature 3: Reverse Classroom 🎓
# ============================================================

@router.post("/reverse-classroom/chat", status_code=status.HTTP_200_OK)
async def reverse_classroom_chat(
    request: ReverseClassroomRequest,
    current_user: dict = Depends(get_current_user)
):
    """AI student responds to user's teaching"""
    try:
        session_id = request.session_id or generate_unique_id("RCS")
        
        response = await feature_chat_service.get_response(
            feature_type="reverse_classroom",
            user_message=request.user_message,
            context={
                "topic": request.topic,
                "persona": request.persona
            },
            language=request.language
        )
        
        # Update user's teaching score
        score_update = response.get("teaching_score_update", 0)
        if score_update > 0:
            current_user["xp_points"] = int(current_user.get("xp_points", 0)) + score_update
            csv_handler.update("users", current_user["user_id"], current_user, "user_id")
        
        response["session_id"] = session_id
        return response
        
    except Exception as e:
        logger.error(f"Reverse classroom error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# Feature 4: Time Travel Interview ⏰
# ============================================================

HISTORICAL_FIGURES = {
    "gandhi": {
        "character_name": "Mahatma Gandhi",
        "birth_year": "1869",
        "death_year": "1948",
        "key_events": "Salt March, Quit India Movement, Non-cooperation movement, Champaran Satyagraha"
    },
    "nehru": {
        "character_name": "Jawaharlal Nehru",
        "birth_year": "1889",
        "death_year": "1964",
        "key_events": "First PM of India, Discovery of India author, Non-Aligned Movement founder"
    },
    "bhagat_singh": {
        "character_name": "Bhagat Singh",
        "birth_year": "1907",
        "death_year": "1931",
        "key_events": "Central Assembly bombing, Lahore Conspiracy Case, hunger strike in jail"
    },
    "einstein": {
        "character_name": "Albert Einstein",
        "birth_year": "1879",
        "death_year": "1955",
        "key_events": "Theory of Relativity, Nobel Prize 1921, Letter to Roosevelt on atomic bomb"
    },
    "kalam": {
        "character_name": "APJ Abdul Kalam",
        "birth_year": "1931",
        "death_year": "2015",
        "key_events": "Missile Man of India, ISRO, President of India, Wings of Fire"
    },
    "curie": {
        "character_name": "Marie Curie",
        "birth_year": "1867",
        "death_year": "1934",
        "key_events": "Discovery of Polonium and Radium, Two Nobel Prizes, First woman professor at Sorbonne"
    }
}


@router.get("/interview/figures", status_code=status.HTTP_200_OK)
async def get_historical_figures(
    current_user: dict = Depends(get_current_user)
):
    """Get list of available historical figures"""
    return {
        "figures": [
            {"id": k, **v} for k, v in HISTORICAL_FIGURES.items()
        ]
    }


@router.post("/interview/chat", status_code=status.HTTP_200_OK)
async def time_travel_chat(
    request: TimeTravelRequest,
    current_user: dict = Depends(get_current_user)
):
    """Chat with a historical figure"""
    try:
        # Get figure details - search by character_name since frontend sends full name
        figure = None
        request_name_lower = request.character_name.lower()
        for fig_id, fig_data in HISTORICAL_FIGURES.items():
            if fig_data["character_name"].lower() == request_name_lower or fig_id == request_name_lower:
                figure = fig_data
                break
        if not figure:
            figure = HISTORICAL_FIGURES.get("gandhi")  # Fallback
        
        session_id = request.session_id or generate_unique_id("TTI")
        
        response = await feature_chat_service.get_response(
            feature_type="time_travel",
            user_message=request.user_message,
            context=figure,
            language=request.language
        )
        
        response["session_id"] = session_id
        return response
        
    except Exception as e:
        logger.error(f"Time travel error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# Feature 5: Concept Collision 🔗
# ============================================================

@router.post("/concepts/find-connections", status_code=status.HTTP_200_OK)
async def find_concept_connections(
    request: ConceptCollisionRequest,
    current_user: dict = Depends(get_current_user)
):
    """Find connections between learned topics"""
    try:
        topics_str = json.dumps(request.topics)
        
        response = await feature_chat_service.get_response(
            feature_type="concept_collision",
            user_message="Find surprising connections between these topics",
            context={"topics": topics_str},
            language=request.language
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Concept collision error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# Feature 6: Mistake Autopsy 🔬
# ============================================================

@router.post("/mistake/analyze", status_code=status.HTTP_200_OK)
async def analyze_mistake(
    request: MistakeAutopsyRequest,
    current_user: dict = Depends(get_current_user)
):
    """Analyze why a mistake was made"""
    try:
        response = await feature_chat_service.get_response(
            feature_type="mistake_autopsy",
            user_message="Analyze this mistake",
            context={
                "question": request.question,
                "correct_answer": request.correct_answer,
                "student_answer": request.student_answer,
                "subject": request.subject
            },
            language=request.language
        )
        
        # Save mistake pattern for future reference
        try:
            mistake_data = {
                "id": generate_unique_id("MST"),
                "user_id": current_user["user_id"],
                "subject": request.subject,
                "topic": request.topic,
                "error_category": response.get("diagnosis", {}).get("error_category", "unknown"),
                "created_at": datetime.now().isoformat()
            }
            csv_handler.create("mistake_patterns", mistake_data)
        except Exception as save_err:
            logger.warning(f"Failed to save mistake pattern: {save_err}")
        
        return response
        
    except Exception as e:
        logger.error(f"Mistake autopsy error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# Feature 6b: Misconception Cascade Tracing (MCT) 🧠
# ============================================================

class MCTRequest(BaseModel):
    """Request model for MCT chat"""
    question: str
    correct_answer: str
    student_answer: str
    subject: str
    topic: str
    user_message: str
    session_id: Optional[str] = None
    conversation_history: List[dict] = []
    phase: str = "surface_capture"
    cascade_tracking: dict = {}
    turn_number: int = 1  # Track conversation turn for spaced image generation
    language: str = "en"


@router.post("/mct/start", status_code=status.HTTP_200_OK)
async def start_mct_session(
    request: MistakeAutopsyRequest,
    current_user: dict = Depends(get_current_user)
):
    """Start a new MCT diagnostic session"""
    try:
        session_id = generate_unique_id("MCT")
        
        # Initialize cascade tracking
        cascade_tracking = {
            "surface_error": request.student_answer,
            "tested_prerequisites": [],
            "broken_link_found": False,
            "root_misconception": None,
            "repair_progress": []
        }
        
        # Get initial AI response with hypotheses
        response = await feature_chat_service.get_response(
            feature_type="mct_diagnostic",
            user_message="Begin the MCT session. Analyze this wrong answer and ask the first diagnostic question.",
            context={
                "question": request.question,
                "correct_answer": request.correct_answer,
                "student_answer": request.student_answer,
                "subject": request.subject,
                "topic": request.topic,
                "conversation_history": "[]",
                "phase": "surface_capture",
                "cascade_tracking": json.dumps(cascade_tracking)
            },
            language=request.language
        )
        
        # Add session metadata
        response["session_id"] = session_id
        if "cascade_tracking" not in response:
            response["cascade_tracking"] = cascade_tracking
        
        # Store session in CSV
        try:
            mct_data = {
                "id": session_id,
                "user_id": current_user["user_id"],
                "subject": request.subject,
                "topic": request.topic,
                "original_question": request.question,
                "student_answer": request.student_answer,
                "correct_answer": request.correct_answer,
                "phase": response.get("phase", "surface_capture"),
                "root_found": False,
                "created_at": datetime.now().isoformat()
            }
            csv_handler.create("mct_sessions", mct_data)
        except Exception as save_err:
            logger.warning(f"Failed to save MCT session: {save_err}")
        
        return response
        
    except Exception as e:
        logger.error(f"MCT start error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/mct/sessions/user/{user_id}")
async def get_user_mct_sessions(
    user_id: str,
    limit: int = 10,
    current_user: dict = Depends(get_current_user)
):
    """Get MCT sessions history for a user"""
    try:
        sessions = csv_handler.read_all("mct_sessions")
        
        # Return ALL sessions for now (no user filtering - single user app)
        user_sessions = sessions if sessions else []
        
        # Sort by created_at descending
        user_sessions.sort(key=lambda x: x.get('created_at', ''), reverse=True)
        
        # Apply limit
        user_sessions = user_sessions[:limit]
        
        return {"user_id": user_id, "sessions": user_sessions}
    except Exception as e:
        logger.error(f"Failed to get MCT sessions: {e}")
        return {"user_id": user_id, "sessions": []}


@router.get("/mct/conversation/{session_id}")
async def get_mct_conversation(
    session_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get conversation history for an MCT session"""
    try:
        conversations = csv_handler.read_all("mct_conversations")
        
        # Filter by session_id
        session_messages = [c for c in conversations if c.get('session_id') == session_id]
        
        # Sort by created_at (handle None values safely)
        session_messages.sort(key=lambda x: x.get('created_at') or x.get('image_path') or '')
        
        return {"session_id": session_id, "messages": session_messages}
    except Exception as e:
        logger.error(f"Failed to get MCT conversation: {e}")
        return {"session_id": session_id, "messages": []}


@router.post("/mct/chat", status_code=status.HTTP_200_OK)
async def mct_chat(
    request: MCTRequest,
    current_user: dict = Depends(get_current_user)
):
    """Continue MCT diagnostic conversation"""
    try:
        session_id = request.session_id or generate_unique_id("MCT")
        
        # Build conversation history string
        history_str = json.dumps(request.conversation_history[-10:])  # Last 10 messages
        
        # Get AI response
        response = await feature_chat_service.get_response(
            feature_type="mct_diagnostic",
            user_message=request.user_message,
            context={
                "question": request.question,
                "correct_answer": request.correct_answer,
                "student_answer": request.student_answer,
                "subject": request.subject,
                "topic": request.topic,
                "conversation_history": history_str,
                "phase": request.phase,
                "cascade_tracking": json.dumps(request.cascade_tracking)
            },
            language=request.language
        )
        
        response["session_id"] = session_id
        
        # Spaced Image Generation: Generate at turns 1, 2, 4, 7, 11, 16, 22...
        # Pattern: 1, +1=2, +2=4, +3=7, +4=11, +5=16, +6=22...
        image_turns = [1, 2, 4, 7, 11, 16, 22, 29, 37, 46]  # Pre-calculated spaced turns
        
        if request.turn_number in image_turns:
            try:
                image_provider = ProviderFactory.get_image_provider()
                
                # Create educational image prompts based on topic and phase
                image_prompts = [
                    f"Educational diagram showing {request.topic} concept, clean and simple, colorful cartoon style for students, no text labels",
                    f"Visual metaphor explaining {request.topic} using everyday objects, friendly cartoon illustration, educational",
                    f"Step-by-step visual showing how {request.topic} works, cartoon style, easy to understand, for learners",
                    f"Comparison diagram showing correct vs incorrect understanding of {request.topic}, cartoon style, educational",
                    f"Fun illustrated example of {request.topic} in real life, cartoon style, engaging for students",
                ]
                
                # Select prompt based on turn index
                turn_index = image_turns.index(request.turn_number) % len(image_prompts)
                prompt = image_prompts[turn_index]
                
                image_request = ImageGenerationRequest(
                    prompt=prompt,
                    style="cartoon",
                    width=512,
                    height=512
                )
                
                image_bytes = await image_provider.generate_image(image_request)
                
                # Convert to base64 for frontend display
                image_base64 = base64.b64encode(image_bytes).decode('utf-8')
                response["image"] = f"data:image/png;base64,{image_base64}"
                
                # Save image to disk for history loading
                import os
                image_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'mct_images')
                os.makedirs(image_dir, exist_ok=True)
                image_filename = f"{session_id}_turn{request.turn_number}.png"
                image_path = os.path.join(image_dir, image_filename)
                with open(image_path, 'wb') as f:
                    f.write(image_bytes)
                response["image_path"] = f"/data/mct_images/{image_filename}"
                
                logger.info(f"Generated and saved spaced image for MCT turn {request.turn_number}")
            except Exception as img_err:
                logger.warning(f"Failed to generate MCT image: {img_err}")
                # Don't fail the whole response if image fails
        
        # Save conversation to history
        try:
            # Save user message
            csv_handler.create("mct_conversations", {
                "id": generate_unique_id("MSG"),
                "session_id": session_id,
                "role": "user",
                "message": request.user_message,
                "phase": request.phase,
                "image_path": "",
                "created_at": datetime.utcnow().isoformat()
            })
            
            # Save assistant message (with image path if generated)
            csv_handler.create("mct_conversations", {
                "id": generate_unique_id("MSG"),
                "session_id": session_id,
                "role": "assistant",
                "message": response.get("message", ""),
                "phase": response.get("phase", request.phase),
                "image_path": response.get("image_path", ""),
                "created_at": datetime.utcnow().isoformat()
            })
        except Exception as save_err:
            logger.warning(f"Failed to save MCT conversation: {save_err}")
        
        # Update session if root found or phase changes
        new_phase = response.get("phase", request.phase)
        root_found = response.get("cascade_tracking", {}).get("broken_link_found", False)
        
        if new_phase != request.phase or root_found:
            try:
                csv_handler.update(
                    "mct_sessions",
                    session_id,
                    {
                        "phase": new_phase,
                        "root_found": root_found,
                        "root_misconception": response.get("cascade_tracking", {}).get("root_misconception", "")
                    },
                    "id"
                )
            except Exception as update_err:
                logger.warning(f"Failed to update MCT session: {update_err}")
        
        return response
        
    except Exception as e:
        logger.error(f"MCT chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# Feature 7: YouTube to Course 📺
# ============================================================

@router.post("/youtube/process", status_code=status.HTTP_200_OK)
async def process_youtube(
    request: YouTubeRequest,
    current_user: dict = Depends(get_current_user)
):
    """Generate course from YouTube video"""
    try:
        # For now, use provided transcript (YouTube API integration can be added later)
        transcript = request.transcript or "No transcript provided"
        
        response = await feature_chat_service.get_response(
            feature_type="youtube_course",
            user_message="Create a comprehensive course from this video",
            context={
                "title": request.title or "Unknown Video",
                "channel": request.channel or "Unknown Channel",
                "duration": request.duration or "Unknown",
                "transcript": transcript[:8000]  # Limit transcript length
            },
            language=request.language
        )
        
        return response
        
    except Exception as e:
        logger.error(f"YouTube processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# Feature 8: Debate Arena ⚔️
# ============================================================

DEBATE_TOPICS = [
    {"topic": "Should homework be abolished?", "category": "Education"},
    {"topic": "Should AI replace teachers?", "category": "Education"},
    {"topic": "Is social media harmful for teenagers?", "category": "Technology"},
    {"topic": "Should video games be considered a sport?", "category": "Technology"},
    {"topic": "Should voting age be lowered to 16?", "category": "Society"},
    {"topic": "Is climate change the biggest threat to humanity?", "category": "Society"},
    {"topic": "Should gene editing on humans be allowed?", "category": "Science"},
    {"topic": "Should we colonize Mars before fixing Earth?", "category": "Science"},
]


@router.get("/debate/topics", status_code=status.HTTP_200_OK)
async def get_debate_topics(
    current_user: dict = Depends(get_current_user)
):
    """Get available debate topics"""
    return {"topics": DEBATE_TOPICS}


@router.post("/debate/round", status_code=status.HTTP_200_OK)
async def debate_round(
    request: DebateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Process a debate round"""
    try:
        session_id = request.session_id or generate_unique_id("DEB")
        opposite = "NO" if request.student_position.upper() == "YES" else "YES"
        
        response = await feature_chat_service.get_response(
            feature_type="debate_arena",
            user_message=request.user_message,
            context={
                "topic": request.topic,
                "student_position": request.student_position,
                "opposite_position": opposite,
                "difficulty": request.difficulty,
                "round": request.round_number
            },
            language=request.language
        )
        
        response["session_id"] = session_id
        response["round_number"] = request.round_number
        
        # Save debate history on final round
        if request.round_number >= 5:
            try:
                debate_data = {
                    "id": session_id,
                    "user_id": current_user["user_id"],
                    "topic": request.topic,
                    "student_position": request.student_position,
                    "rounds_completed": 5,
                    "created_at": datetime.now().isoformat()
                }
                csv_handler.create("debate_history", debate_data)
            except Exception as save_err:
                logger.warning(f"Failed to save debate history: {save_err}")
        
        return response
        
    except Exception as e:
        logger.error(f"Debate error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# Feature 9: Dream Project Path 🎯
# ============================================================

@router.post("/dream/analyze", status_code=status.HTTP_200_OK)
async def analyze_dream_project(
    request: DreamProjectRequest,
    current_user: dict = Depends(get_current_user)
):
    """Analyze dream project and create learning path"""
    try:
        session_id = generate_unique_id("DRM")
        
        response = await feature_chat_service.get_response(
            feature_type="dream_project",
            user_message=request.user_message or "Create a learning path for my dream",
            context={
                "dream": request.dream,
                "grade_level": request.grade_level,
                "hours_per_week": request.hours_per_week
            },
            language=request.language
        )
        
        # Save dream project
        try:
            dream_data = {
                "id": session_id,
                "user_id": current_user["user_id"],
                "dream_title": response.get("dream_analysis", {}).get("dream_title", request.dream),
                "dream_description": request.dream,
                "current_phase": 1,
                "progress_percent": 0,
                "created_at": datetime.now().isoformat()
            }
            csv_handler.create("dream_projects", dream_data)
        except Exception as save_err:
            logger.warning(f"Failed to save dream project: {save_err}")
        
        response["session_id"] = session_id
        return response
        
    except Exception as e:
        logger.error(f"Dream project error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/dream/mentor", status_code=status.HTTP_200_OK)
async def dream_mentor_chat(
    request: DreamProjectRequest,
    current_user: dict = Depends(get_current_user)
):
    """Chat with dream project mentor"""
    try:
        response = await feature_chat_service.get_response(
            feature_type="dream_project",
            user_message=request.user_message or "Help me with my learning path",
            context={
                "dream": request.dream,
                "grade_level": request.grade_level,
                "hours_per_week": request.hours_per_week
            },
            language=request.language
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Dream mentor error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
