"""
Misconception Cascade Tracing (MCT) Routes
Advanced diagnostic tool for identifying root causes of student misconceptions
"""

import logging
import json
import base64
import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from typing import Optional, List

from app.api.dependencies import get_current_user
from app.database.csv_handler import CSVHandler
from app.services.feature_chat import feature_chat_service
from app.services.provider_factory import ProviderFactory
from app.services.image_providers.base import ImageGenerationRequest
from app.services.illustration_service import illustration_service
from app.utils.helpers import generate_unique_id

logger = logging.getLogger(__name__)
router = APIRouter()
csv_handler = CSVHandler()


# ============================================================
# Pydantic Models
# ============================================================

class MistakeAutopsyRequest(BaseModel):
    """Request model for mistake analysis"""
    question: str
    correct_answer: str
    student_answer: str
    subject: str
    topic: str
    language: str = "en"


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


# ============================================================
# Mistake Autopsy 🔬
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
# Misconception Cascade Tracing (MCT) 🧠
# ============================================================

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

        # Generate educational illustration (first 5 always, then every 2)
        try:
            illust = await illustration_service.generate_illustration(
                topic=request.topic,
                subject=request.subject,
                context=request.user_message,
                turn_number=request.turn_number
            )
            if illust:
                response["illustration"] = illust
        except Exception as ill_err:
            logger.warning(f"MCT illustration generation skipped: {ill_err}")

        # Always generate an educational image with every MCT response
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

            # Select prompt based on turn number
            turn_index = (request.turn_number - 1) % len(image_prompts)
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
            image_dir = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'data', 'mct_images')
            os.makedirs(image_dir, exist_ok=True)
            image_filename = f"{session_id}_turn{request.turn_number}.png"
            image_path = os.path.join(image_dir, image_filename)
            with open(image_path, 'wb') as f:
                f.write(image_bytes)
            response["image_path"] = f"/data/mct_images/{image_filename}"

            logger.info(f"Generated and saved image for MCT turn {request.turn_number}")
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
