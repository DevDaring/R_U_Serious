"""
FastAPI Router for Feynman Engine endpoints
Fun Learn Application
"""

import json
import logging
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, HTTPException

from app.models.feynman_models import (
    StartSessionRequest, TeachMessageRequest, TeachWithImageRequest,
    CompressionSubmitRequest, WhySpiralResponseRequest, AnalogySubmitRequest,
    LectureHallMessageRequest, ChangeLayerRequest,
    RittyResponse, CompressionEvaluation, WhySpiralResponse,
    AnalogyEvaluation, LectureHallResponse, SessionResponse,
    SessionSummary, GapResponse
)
from app.services.feynman_service import feynman_ai
from app.database.feynman_db import feynman_db
from app.services.content_generator import ContentGenerator
from app.database.file_handler import FileHandler
from app.utils.helpers import generate_unique_id

logger = logging.getLogger(__name__)
content_generator = ContentGenerator()
file_handler = FileHandler()


router = APIRouter(prefix="/feynman", tags=["Feynman Engine"])


# ============== SESSION ENDPOINTS ==============

@router.post("/session/start", response_model=SessionResponse)
async def start_session(request: StartSessionRequest):
    """Start a new Feynman Engine session"""
    
    try:
        session = feynman_db.create_session(
            user_id=request.user_id,
            topic=request.topic,
            subject=request.subject,
            difficulty_level=request.difficulty_level,
            starting_layer=request.starting_layer
        )
        
        return SessionResponse(
            session_id=session['id'],
            user_id=session['user_id'],
            topic=session['topic'],
            subject=session['subject'],
            difficulty_level=session['difficulty_level'],
            current_layer=session['current_layer'],
            status='active',
            clarity_score=0.0,
            teaching_xp_earned=0,
            started_at=session['started_at'],
            completed_at=None
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/session/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    """Get session details"""
    
    session = feynman_db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return SessionResponse(
        session_id=session['id'],
        user_id=session['user_id'],
        topic=session['topic'],
        subject=session['subject'],
        difficulty_level=int(session.get('difficulty_level', 5)),
        current_layer=int(session.get('current_layer', 1)),
        status=session.get('status', 'active'),
        clarity_score=float(session.get('clarity_score', 0) or 0),
        teaching_xp_earned=int(session.get('teaching_xp_earned', 0) or 0),
        started_at=session['started_at'],
        completed_at=session.get('completed_at') if session.get('completed_at') else None
    )


@router.get("/session/{session_id}/history")
async def get_session_history(session_id: str, layer: Optional[int] = None):
    """Get conversation history for a session"""
    
    history = feynman_db.get_conversation_history(session_id, layer)
    return {"session_id": session_id, "history": history}


@router.post("/session/change-layer")
async def change_layer(request: ChangeLayerRequest):
    """Change to a different layer (layers are optional)"""
    
    session = feynman_db.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    feynman_db.update_session(request.session_id, {'current_layer': request.target_layer})
    
    return {"success": True, "new_layer": request.target_layer}


@router.post("/session/{session_id}/complete", response_model=SessionSummary)
async def complete_session(session_id: str):
    """Complete a session and get summary"""
    
    session = feynman_db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get gaps for this session
    session_gaps = feynman_db.get_session_gaps(session_id)
    
    # Calculate compression rounds from history
    compression_history = feynman_db.get_conversation_history(session_id, layer=2)
    compression_rounds = len([h for h in compression_history if h['role'] == 'user'])
    
    # Check if all personas satisfied in lecture hall
    lecture_history = feynman_db.get_conversation_history(session_id, layer=5)
    all_satisfied = len(lecture_history) > 0  # Simplified check
    
    # Calculate which layers were completed (any with conversation history)
    layers_completed = []
    for layer in range(1, 6):
        layer_history = feynman_db.get_conversation_history(session_id, layer=layer)
        if len([h for h in layer_history if h['role'] == 'user']) > 0:
            layers_completed.append(layer)
    
    # Calculate final XP
    xp, achievements = feynman_ai.calculate_teaching_xp(
        layers_completed=layers_completed,
        clarity_score=float(session.get('clarity_score', 0) or 0),
        compression_rounds_passed=compression_rounds,
        why_depth_reached=int(session.get('why_depth_reached', 0) or 0),
        analogy_saved=float(session.get('analogy_score', 0) or 0) >= 4,
        all_personas_satisfied=all_satisfied,
        gaps_discovered=len(session_gaps)
    )
    
    # Update session
    feynman_db.update_session(session_id, {
        'status': 'completed',
        'completed_at': datetime.utcnow().isoformat(),
        'teaching_xp_earned': xp
    })
    
    # Update user XP (graceful - works without users.csv)
    feynman_db.update_user_xp(session['user_id'], xp)
    
    # Calculate total time
    try:
        started = datetime.fromisoformat(session['started_at'])
        total_minutes = (datetime.utcnow() - started).total_seconds() / 60
    except:
        total_minutes = 0
    
    # Build gap responses
    gap_responses = [
        GapResponse(
            gap_id=g['id'],
            topic=g['gap_topic'],
            description=g['gap_description'],
            layer_discovered=int(g['layer_discovered']),
            why_depth=int(g['why_depth']) if g.get('why_depth') else None,
            resolved=bool(g.get('resolved', False))
        )
        for g in session_gaps
    ]
    
    return SessionSummary(
        session_id=session_id,
        topic=session['topic'],
        total_time_minutes=round(total_minutes, 1),
        layers_completed=layers_completed,
        final_clarity_score=float(session.get('clarity_score', 0) or 0),
        compression_score=float(session.get('compression_score')) if session.get('compression_score') else None,
        analogy_score=float(session.get('analogy_score')) if session.get('analogy_score') else None,
        why_depth_reached=int(session.get('why_depth_reached', 0) or 0),
        gaps_discovered=gap_responses,
        teaching_xp_earned=xp,
        achievements_unlocked=achievements
    )


@router.get("/sessions/user/{user_id}")
async def get_user_sessions(
    user_id: str, 
    status: Optional[str] = None,
    limit: int = 20
):
    """Get all sessions for a user"""
    
    sessions = feynman_db.get_user_sessions(user_id, status, limit)
    return {"user_id": user_id, "sessions": sessions}


@router.get("/session/{session_id}/full")
async def get_session_with_conversations(session_id: str):
    """Get a session with all its conversation history from all layers.
    Used by Mistake Autopsy to load full chat history for analysis."""
    
    session = feynman_db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Get conversation history for all layers
    conversations = {}
    all_messages = []
    
    for layer in range(1, 6):
        history = feynman_db.get_conversation_history(session_id, layer)
        if history:
            conversations[f"layer_{layer}"] = history
            # Add layer info to each message and collect all
            for msg in history:
                all_messages.append({
                    **msg,
                    "layer": layer
                })
    
    # Sort all messages by created_at if available
    try:
        all_messages.sort(key=lambda x: x.get('created_at', ''))
    except:
        pass
    
    return {
        "session": session,
        "conversations_by_layer": conversations,
        "all_messages": all_messages
    }


# ============== LAYER 1: RITTY (CURIOUS CHILD) ==============

@router.post("/layer1/teach", response_model=RittyResponse)
async def teach_ritty(request: TeachMessageRequest):
    """Send a teaching message to Ritty"""
    
    session = feynman_db.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save user message
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=1,
        role="user",
        message=request.message
    )
    
    # Get conversation history
    history = feynman_db.get_conversation_history(request.session_id, layer=1)
    
    # Get AI response
    response = await feynman_ai.ritty_respond(
        session_id=request.session_id,
        topic=session['topic'],
        subject=session['subject'],
        user_message=request.message,
        conversation_history=history,
        difficulty_level=int(session.get('difficulty_level', 5))
    )
    
    # Save AI response
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=1,
        role="assistant",
        message=response.response,
        confusion_level=response.confusion_level,
        curiosity_level=response.curiosity_level,
        question_type=response.question_type,
        gap_detected=response.gap_detected
    )
    
    # If gap detected, save it
    if response.gap_detected:
        feynman_db.add_gap(
            session_id=request.session_id,
            user_id=session['user_id'],
            gap_topic=response.gap_detected,
            gap_description=f"Gap detected while explaining {session['topic']}",
            layer_discovered=1
        )
    
    # Update clarity score (inverse of confusion)
    clarity = (1 - response.confusion_level) * 100
    feynman_db.update_session(request.session_id, {'clarity_score': clarity})
    
    return response


@router.post("/layer1/start")
async def start_ritty_session(session_id: str):
    """Get Ritty's opening message"""
    
    session = feynman_db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Check if there's already conversation
    history = feynman_db.get_conversation_history(session_id, layer=1)
    if history:
        return {"message": "Session already started", "history": history}
    
    opening = f"Hi! 👋 I'm Ritty! I heard you know about {session['topic']}. Can you teach me? I really want to learn! What is {session['topic']}? 🤔"
    
    # Save opening message
    feynman_db.add_conversation_turn(
        session_id=session_id,
        layer=1,
        role="assistant",
        message=opening,
        confusion_level=0.5,
        curiosity_level=0.9
    )
    
    return {
        "message": opening,
        "avatar_state": "curious"
    }


# ============== LAYER 2: COMPRESSION CHALLENGE ==============

@router.post("/layer2/start")
async def start_compression(session_id: str):
    """Start the compression challenge"""
    
    session = feynman_db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {
        "message": f"🎯 **Compression Challenge**\n\nNow let's see if you truly understand {session['topic']}!\n\nExplain it in **100 words or less**.\n\nThe better you understand something, the more simply you can explain it.",
        "current_word_limit": 100,
        "progression": [100, 50, 25, 15, 10, 1]
    }


@router.post("/layer2/compress", response_model=CompressionEvaluation)
async def submit_compression(request: CompressionSubmitRequest):
    """Submit a compression challenge attempt"""
    
    session = feynman_db.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save user attempt
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=2,
        role="user",
        message=f"[{request.word_limit} words]: {request.explanation}"
    )
    
    # Get previous compressions
    history = feynman_db.get_conversation_history(request.session_id, layer=2)
    previous = []
    for h in history:
        if h['role'] == 'user' and ']: ' in h['message']:
            try:
                limit_part = h['message'].split(']')[0].replace('[', '').split()[0]
                explanation = h['message'].split(']: ')[1]
                previous.append({
                    'word_limit': int(limit_part),
                    'explanation': explanation,
                    'score': 3
                })
            except:
                pass
    
    # Get evaluation
    evaluation = await feynman_ai.evaluate_compression(
        topic=session['topic'],
        subject=session['subject'],
        original_explanation="",
        compressed_explanation=request.explanation,
        word_limit=request.word_limit,
        previous_compressions=previous
    )
    
    # Save evaluation
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=2,
        role="assistant",
        message=f"Score: {evaluation.score}/5 - {evaluation.feedback}"
    )
    
    # Update compression score
    feynman_db.update_session(request.session_id, {
        'compression_score': evaluation.score * 20  # Convert to 0-100
    })
    
    return evaluation


# ============== LAYER 3: WHY SPIRAL ==============

@router.post("/layer3/start")
async def start_why_spiral(session_id: str):
    """Start the Why Spiral with the first question"""
    
    session = feynman_db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Check if there's already conversation history
    history = feynman_db.get_conversation_history(session_id, layer=3)
    if history:
        # Calculate current depth from history
        user_turns = len([h for h in history if h['role'] == 'user'])
        return {
            "question": history[-1]['message'] if history[-1]['role'] == 'assistant' else "Continue your exploration...",
            "current_depth": min(user_turns + 1, 5),
            "max_depth": 5,
            "history": history
        }
    
    # Generate first question
    response = await feynman_ai.why_spiral_respond(
        topic=session['topic'],
        subject=session['subject'],
        current_depth=1,
        user_response="",
        admits_unknown=False,
        conversation_history=[]
    )
    
    first_question = response.next_question or f"Let's explore why {session['topic']} works the way it does. Can you explain the basic principle behind it?"
    
    # Save the first question
    feynman_db.add_conversation_turn(
        session_id=session_id,
        layer=3,
        role="assistant",
        message=first_question
    )
    
    return {
        "question": first_question,
        "current_depth": 1,
        "max_depth": 5
    }


@router.post("/layer3/respond", response_model=WhySpiralResponse)
async def respond_why_spiral(request: WhySpiralResponseRequest):
    """Respond to a Why Spiral question"""
    
    session = feynman_db.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save user response
    message = f"[I don't know] {request.response}" if request.admits_unknown else request.response
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=3,
        role="user",
        message=message
    )
    
    # Get history
    history = feynman_db.get_conversation_history(request.session_id, layer=3)
    current_depth = len([h for h in history if h['role'] == 'assistant'])
    
    # Get next question or detect boundary
    response = await feynman_ai.why_spiral_respond(
        topic=session['topic'],
        subject=session['subject'],
        current_depth=current_depth,
        user_response=request.response,
        admits_unknown=request.admits_unknown,
        conversation_history=history
    )
    
    # Save AI response
    if response.next_question:
        feynman_db.add_conversation_turn(
            session_id=request.session_id,
            layer=3,
            role="assistant",
            message=response.next_question
        )
    elif response.boundary_detected and response.boundary_topic:
        boundary_message = f"🎯 Knowledge boundary found: {response.boundary_topic}\n\n{response.exploration_offer or ''}"
        feynman_db.add_conversation_turn(
            session_id=request.session_id,
            layer=3,
            role="assistant",
            message=boundary_message
        )
        
        # Save the gap
        feynman_db.add_gap(
            session_id=request.session_id,
            user_id=session['user_id'],
            gap_topic=response.boundary_topic,
            gap_description=response.exploration_offer or "",
            layer_discovered=3,
            why_depth=response.current_depth
        )
    
    # Update why depth
    feynman_db.update_session(request.session_id, {
        'why_depth_reached': response.current_depth
    })
    
    return response


# ============== LAYER 4: ANALOGY ARCHITECT ==============

@router.post("/layer4/start")
async def start_analogy(session_id: str):
    """Start the Analogy Architect challenge"""
    
    session = feynman_db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Check if there's already conversation history
    history = feynman_db.get_conversation_history(session_id, layer=4)
    if history:
        # Determine current phase from history
        user_turns = len([h for h in history if h['role'] == 'user'])
        phase = 'create' if user_turns == 0 else ('defend' if user_turns == 1 else 'refine')
        return {
            "message": "Continue with your analogy",
            "phase": phase,
            "phases": ["create", "defend", "refine"],
            "history": history
        }
    
    return {
        "message": f"🎨 **Analogy Architect**\n\nCreate an original analogy to explain {session['topic']}.\n\nA great analogy:\n- Maps concepts accurately\n- Is relatable and memorable\n- Doesn't create misconceptions\n\nWhat's your analogy?",
        "phase": "create",
        "phases": ["create", "defend", "refine"]
    }


@router.post("/layer4/submit", response_model=AnalogyEvaluation)
async def submit_analogy(request: AnalogySubmitRequest):
    """Submit or refine an analogy with spaced visual image generation"""
    
    session = feynman_db.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save user submission
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=4,
        role="user",
        message=f"[{request.phase}]: {request.analogy_text}"
    )
    
    # Get previous feedback if any
    history = feynman_db.get_conversation_history(request.session_id, layer=4)
    previous_feedback = None
    for h in reversed(history):
        if h['role'] == 'assistant':
            previous_feedback = h['message']
            break
    
    # Evaluate
    evaluation = await feynman_ai.evaluate_analogy(
        topic=session['topic'],
        subject=session['subject'],
        analogy_text=request.analogy_text,
        phase=request.phase,
        defense_response=request.defense_response,
        previous_feedback=previous_feedback
    )
    
    # ========== SPACED VISUAL ANALOGY GENERATION ==========
    # Intervals: 0, 1, 2, 3... (generate after N more interactions since last image)
    analogy_image_url = None
    
    # Get current tracking values from session
    analogy_image_count = int(session.get('analogy_image_count', 0))
    interactions_since_image = int(session.get('interactions_since_image', 0))
    
    # Calculate next trigger interval (increases by 1 each time)
    next_trigger_interval = analogy_image_count  # 0, 1, 2, 3...
    
    # Check if we should generate an image
    should_generate_image = (interactions_since_image >= next_trigger_interval)
    
    if should_generate_image:
        try:
            # Create a visual prompt from the analogy
            visual_prompt = f"""Educational illustration showing the analogy:
"{request.analogy_text}"

Create a split-scene image:
- Left side: The concept being explained ({session['topic']})
- Right side: The familiar analogy object/concept  
- Visual arrows or connections showing how they relate

Style: Clean, colorful educational illustration, labeled diagram style, 
easy to understand, professional educational material quality.
No text in image, just visual elements."""

            # Generate the image
            image_bytes = await content_generator.generate_image(
                prompt=visual_prompt,
                style="cartoon"
            )
            
            # Return base64 inline for immediate display (Cloud Run ephemeral storage)
            import base64
            analogy_image_base64 = f"data:image/png;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
            analogy_image_url = analogy_image_base64
            
            # Also try to save to disk for history
            image_filename = f"analogy_{generate_unique_id('AIM')}.png"
            success, image_path = file_handler.save_file(image_bytes, image_filename, "generated_images")
            if not success:
                logger.warning("Failed to save analogy image to disk")
            
            # Update tracking - reset counter and increment image count
            feynman_db.update_session(request.session_id, {
                'analogy_image_count': analogy_image_count + 1,
                'interactions_since_image': 0
            })
            
            logger.info(f"Generated analogy image #{analogy_image_count + 1} for session {request.session_id}")
            
        except Exception as img_err:
            logger.warning(f"Analogy image generation failed: {img_err}")
            # Still increment interaction counter even if image fails
            feynman_db.update_session(request.session_id, {
                'interactions_since_image': interactions_since_image + 1
            })
    else:
        # Increment interaction counter
        feynman_db.update_session(request.session_id, {
            'interactions_since_image': interactions_since_image + 1
        })
    
    # Save evaluation
    feedback_msg = f"Score: {evaluation.score}/5\n"
    feedback_msg += f"Strengths: {', '.join(evaluation.strengths)}\n"
    feedback_msg += f"Weaknesses: {', '.join(evaluation.weaknesses)}\n"
    if evaluation.stress_test_question:
        feedback_msg += f"\n🔥 Stress Test: {evaluation.stress_test_question}"
    if analogy_image_url:
        feedback_msg += f"\n🖼️ Analogy visualization generated!"
    
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=4,
        role="assistant",
        message=feedback_msg,
        image_url=analogy_image_url  # Store image URL in history for persistence
    )
    
    # Update analogy score
    feynman_db.update_session(request.session_id, {
        'analogy_score': evaluation.score * 20  # Convert to 0-100
    })
    
    # If save-worthy, save to analogies library
    if evaluation.save_worthy:
        feynman_db.save_analogy(
            user_id=session['user_id'],
            topic=session['topic'],
            subject=session['subject'],
            analogy_text=request.analogy_text,
            stress_test_passed=evaluation.passed_stress_test or False
        )
    
    # Return evaluation with image URL
    return AnalogyEvaluation(
        phase=evaluation.phase,
        score=evaluation.score,
        strengths=evaluation.strengths,
        weaknesses=evaluation.weaknesses,
        stress_test_question=evaluation.stress_test_question,
        passed_stress_test=evaluation.passed_stress_test,
        refinement_suggestion=evaluation.refinement_suggestion,
        save_worthy=evaluation.save_worthy,
        analogy_image_url=analogy_image_url
    )


# ============== LAYER 5: LECTURE HALL ==============

@router.post("/layer5/start")
async def start_lecture_hall(session_id: str):
    """Start the Lecture Hall challenge"""
    
    session = feynman_db.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Check if there's already conversation history
    history = feynman_db.get_conversation_history(session_id, layer=5)
    if history:
        return {
            "message": "Continue your lecture",
            "personas": [
                {"id": "dr_skeptic", "name": "Dr. Skeptic", "emoji": "👨‍🔬"},
                {"id": "the_pedant", "name": "The Pedant", "emoji": "📚"},
                {"id": "confused_carl", "name": "Confused Carl", "emoji": "😕"},
                {"id": "industry_ian", "name": "Industry Ian", "emoji": "🏭"},
                {"id": "little_lily", "name": "Little Lily", "emoji": "👧"}
            ],
            "history": history
        }
    
    return {
        "message": f"🎓 **Welcome to the Lecture Hall**\n\nYou're about to explain {session['topic']} to 5 different people:\n\n👨‍🔬 **Dr. Skeptic** - Demands precision\n📚 **The Pedant** - Wants technical accuracy\n😕 **Confused Carl** - Needs simplicity\n🏭 **Industry Ian** - Wants practical examples\n👧 **Little Lily** - Needs the simplest explanation\n\nCan you satisfy them ALL?",
        "personas": [
            {"id": "dr_skeptic", "name": "Dr. Skeptic", "emoji": "👨‍🔬"},
            {"id": "the_pedant", "name": "The Pedant", "emoji": "📚"},
            {"id": "confused_carl", "name": "Confused Carl", "emoji": "😕"},
            {"id": "industry_ian", "name": "Industry Ian", "emoji": "🏭"},
            {"id": "little_lily", "name": "Little Lily", "emoji": "👧"}
        ]
    }


@router.post("/layer5/explain", response_model=LectureHallResponse)
async def explain_to_lecture_hall(request: LectureHallMessageRequest):
    """Send explanation to Lecture Hall"""
    
    session = feynman_db.get_session(request.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Save user message
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=5,
        role="user",
        message=request.message
    )
    
    # Get history
    history = feynman_db.get_conversation_history(request.session_id, layer=5)
    
    # Get responses from all personas
    response = await feynman_ai.lecture_hall_respond(
        topic=session['topic'],
        subject=session['subject'],
        user_explanation=request.message,
        conversation_history=history
    )
    
    # Save combined response
    combined_responses = []
    for p in response.personas:
        combined_responses.append(f"{p.persona_name}: {p.response}")
    
    feynman_db.add_conversation_turn(
        session_id=request.session_id,
        layer=5,
        role="assistant",
        message="\n\n".join(combined_responses)
    )
    
    return response


# ============== GAP MANAGEMENT ==============

@router.get("/gaps/user/{user_id}")
async def get_user_gaps(user_id: str, resolved: Optional[bool] = None):
    """Get all gaps for a user"""
    
    gaps = feynman_db.get_user_gaps(user_id, resolved)
    return {"user_id": user_id, "gaps": gaps}


@router.post("/gaps/{gap_id}/resolve")
async def resolve_gap(gap_id: str, linked_session_id: Optional[str] = None):
    """Mark a gap as resolved"""
    
    success = feynman_db.resolve_gap(gap_id, linked_session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Gap not found")
    
    return {"success": True}


# ============== ANALOGIES LIBRARY ==============

@router.get("/analogies")
async def get_analogies(
    topic: Optional[str] = None,
    subject: Optional[str] = None,
    featured_only: bool = False,
    limit: int = 20
):
    """Get analogies from the community library"""
    
    analogies = feynman_db.get_analogies(topic, subject, featured_only, limit)
    return {"analogies": analogies}


@router.post("/analogies/{analogy_id}/vote")
async def vote_analogy(analogy_id: str, vote_type: str):
    """Upvote or downvote an analogy"""
    
    if vote_type not in ['upvote', 'downvote']:
        raise HTTPException(status_code=400, detail="vote_type must be 'upvote' or 'downvote'")
    
    success = feynman_db.vote_analogy(analogy_id, vote_type)
    if not success:
        raise HTTPException(status_code=404, detail="Analogy not found")
    
    return {"success": True}
