"""
Pydantic models for Feynman Engine feature
R U Serious? Application
"""

from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class FeynmanLayer(int, Enum):
    """Enumeration of Feynman Engine layers"""
    CURIOUS_CHILD = 1
    COMPRESSION = 2
    WHY_SPIRAL = 3
    ANALOGY_ARCHITECT = 4
    LECTURE_HALL = 5


class SessionStatus(str, Enum):
    """Session status enumeration"""
    ACTIVE = "active"
    COMPLETED = "completed"
    ABANDONED = "abandoned"


class QuestionType(str, Enum):
    """Types of questions AI can ask"""
    CLARIFYING = "clarifying"
    CURIOUS = "curious"
    CHALLENGING = "challenging"
    CONFUSED = "confused"


class LectureHallPersona(str, Enum):
    """Personas in the Lecture Hall (Layer 5)"""
    DR_SKEPTIC = "dr_skeptic"
    THE_PEDANT = "the_pedant"
    CONFUSED_CARL = "confused_carl"
    INDUSTRY_IAN = "industry_ian"
    LITTLE_LILY = "little_lily"


# ============== REQUEST MODELS ==============

class StartSessionRequest(BaseModel):
    """Request to start a new Feynman session"""
    user_id: str = Field(default="guest", description="User ID from users.csv or 'guest'")
    topic: str = Field(..., min_length=2, max_length=200, description="Topic to explain")
    subject: str = Field(default="General", description="Subject category")
    difficulty_level: int = Field(default=5, ge=1, le=10, description="Difficulty 1-10")
    starting_layer: int = Field(default=1, ge=1, le=5, description="Layer to start from (1-5)")


class TeachMessageRequest(BaseModel):
    """Request to send a teaching message"""
    session_id: str = Field(..., description="Active session ID")
    message: str = Field(..., min_length=1, max_length=5000, description="User's explanation")
    layer: int = Field(default=1, ge=1, le=5, description="Current layer")


class TeachWithImageRequest(BaseModel):
    """Request to send a teaching message with an image"""
    session_id: str = Field(..., description="Active session ID")
    message: str = Field(..., min_length=1, max_length=5000)
    layer: int = Field(default=1, ge=1, le=5)
    image_base64: str = Field(..., description="Base64 encoded image")
    image_mime_type: str = Field(default="image/png", description="Image MIME type")


class CompressionSubmitRequest(BaseModel):
    """Request to submit a compression challenge attempt"""
    session_id: str
    word_limit: int = Field(..., description="Target word limit: 100, 50, 25, 15, 10, 1")
    explanation: str = Field(..., description="Compressed explanation")


class WhySpiralResponseRequest(BaseModel):
    """Request to respond to a Why Spiral question"""
    session_id: str
    response: str = Field(..., description="User's answer to 'why' question")
    admits_unknown: bool = Field(default=False, description="User admits they don't know")


class AnalogySubmitRequest(BaseModel):
    """Request to submit or refine an analogy"""
    session_id: str
    analogy_text: str = Field(..., min_length=10, max_length=2000)
    phase: str = Field(..., description="create, defend, or refine")
    defense_response: Optional[str] = Field(None, description="Response to stress test")


class LectureHallMessageRequest(BaseModel):
    """Request to send message in Lecture Hall"""
    session_id: str
    message: str = Field(..., description="Explanation to all personas")


class ChangeLayerRequest(BaseModel):
    """Request to change to a different layer"""
    session_id: str
    target_layer: int = Field(..., ge=1, le=5, description="Layer to switch to")


# ============== RESPONSE MODELS ==============

class RittyResponse(BaseModel):
    """Response from Ritty (Layer 1)"""
    response: str = Field(..., description="Ritty's response text")
    confusion_level: float = Field(..., ge=0, le=1, description="0=clear, 1=very confused")
    curiosity_level: float = Field(..., ge=0, le=1, description="0=bored, 1=very curious")
    question_type: str = Field(default="curious")
    follow_up_question: Optional[str] = Field(None)
    gap_detected: Optional[str] = Field(None, description="Knowledge gap if found")
    encouragement: Optional[str] = Field(None, description="Positive reinforcement")
    emoji_reaction: str = Field(default="😊")
    layer_complete: bool = Field(default=False, description="Can proceed to next layer")
    avatar_state: str = Field(default="neutral", description="curious, confused, happy, surprised, thinking")


class CompressionEvaluation(BaseModel):
    """Evaluation of compression attempt"""
    score: int = Field(..., ge=1, le=5, description="1-5 star rating")
    word_count: int
    within_limit: bool
    feedback: str
    preserved_concepts: List[str] = Field(default_factory=list)
    lost_concepts: List[str] = Field(default_factory=list)
    suggestion: Optional[str] = None
    passed: bool
    next_word_limit: Optional[int] = Field(None, description="Next round limit if passed")
    image_url: Optional[str] = Field(None, description="Generated image for the compression concept")


class WhySpiralResponse(BaseModel):
    """Response in Why Spiral (Layer 3)"""
    next_question: Optional[str] = Field(None, description="Next 'why' question")
    current_depth: int = Field(..., ge=1, le=5)
    reasoning: str = Field(default="", description="Why this question follows logically")
    boundary_detected: bool = Field(default=False)
    boundary_topic: Optional[str] = Field(None)
    exploration_offer: Optional[str] = Field(None, description="What lies beyond + invitation")
    can_continue: bool = Field(default=True)
    image_url: Optional[str] = Field(None, description="Generated image illustrating the concept")


class AnalogyEvaluation(BaseModel):
    """Evaluation of user's analogy"""
    phase: str  # create, defend, refine
    score: int = Field(..., ge=1, le=5)
    strengths: List[str] = Field(default_factory=list)
    weaknesses: List[str] = Field(default_factory=list)
    stress_test_question: Optional[str] = Field(None, description="Challenge to defend")
    passed_stress_test: Optional[bool] = Field(None)
    refinement_suggestion: Optional[str] = Field(None)
    save_worthy: bool = Field(default=False, description="Good enough to save")
    analogy_image_url: Optional[str] = Field(None, description="Generated visualization of the analogy")


class PersonaFeedback(BaseModel):
    """Feedback from a single Lecture Hall persona"""
    persona: str
    persona_name: str = Field(default="")
    satisfaction: float = Field(..., ge=0, le=1)
    response: str
    follow_up_question: Optional[str] = Field(None)
    is_satisfied: bool


class LectureHallResponse(BaseModel):
    """Response from all Lecture Hall personas"""
    personas: List[PersonaFeedback]
    overall_satisfaction: float = Field(..., ge=0, le=1)
    all_satisfied: bool
    dominant_issue: Optional[str] = Field(None, description="Main problem if not all satisfied")
    suggestion: Optional[str] = None
    image_url: Optional[str] = Field(None, description="Generated image illustrating the concept")


class SessionResponse(BaseModel):
    """Response when creating or getting a session"""
    session_id: str
    user_id: str
    topic: str
    subject: str
    difficulty_level: int
    current_layer: int
    status: str
    clarity_score: float
    teaching_xp_earned: int
    started_at: str
    completed_at: Optional[str] = None


class GapResponse(BaseModel):
    """Response for a knowledge gap"""
    gap_id: str
    topic: str
    description: str
    layer_discovered: int
    why_depth: Optional[int] = None
    resolved: bool


class SessionSummary(BaseModel):
    """Summary of completed session"""
    session_id: str
    topic: str
    total_time_minutes: float
    layers_completed: List[int]
    final_clarity_score: float
    compression_score: Optional[float] = None
    analogy_score: Optional[float] = None
    why_depth_reached: int
    gaps_discovered: List[GapResponse] = Field(default_factory=list)
    teaching_xp_earned: int
    achievements_unlocked: List[str] = Field(default_factory=list)


class ConversationTurn(BaseModel):
    """Single turn in conversation history"""
    role: str  # "user" or "assistant"
    message: str
    layer: int
    turn_number: int
    confusion_level: Optional[float] = None
    curiosity_level: Optional[float] = None
    image_url: Optional[str] = None
