"""
Story Learning API Routes

Provides endpoints for generating educational stories
and conducting Socratic discussions.
FunLearn Application - Powered by DigitalOcean Gradient AI
"""

import base64
import logging
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import Optional

from app.services.story_service import story_service
from app.services.illustration_service import illustration_service
from app.services.content_generator import ContentGenerator
from app.database.file_handler import FileHandler
from app.utils.helpers import generate_unique_id
from app.api.dependencies import get_current_user

logger = logging.getLogger(__name__)
content_generator = ContentGenerator()
file_handler = FileHandler()


async def _generate_story_image(concept: str, context: str, style: str = "cartoon") -> Optional[str]:
    """Generate an educational image for a story response. Returns base64 data URL or None."""
    try:
        prompt = f"""Educational illustration about {concept}.
Context: {context[:300]}

Create a clear, colorful educational diagram or illustration that visually explains this concept.
Style: Clean, vibrant, child-friendly educational illustration. No text in image."""
        image_bytes = await content_generator.generate_image(prompt=prompt, style=style)
        image_filename = f"story_{generate_unique_id('SIM')}.png"
        file_handler.save_file(image_bytes, image_filename, "generated_images")
        return f"data:image/png;base64,{base64.b64encode(image_bytes).decode('utf-8')}"
    except Exception as e:
        logger.warning(f"Story image generation failed for concept '{concept}': {e}")
        return None


router = APIRouter(prefix="/api/story", tags=["story-learning"])


# ============================================================
# Request/Response Models
# ============================================================

class StoryRequest(BaseModel):
    concept: str = Field(..., description="The concept to teach through story")
    language: str = Field(default="English", description="Language for the story")
    difficulty_level: int = Field(default=5, ge=1, le=10, description="Difficulty level (1-10)")


class StoryDiscussionRequest(BaseModel):
    concept: str = Field(..., description="The concept being taught")
    story: str = Field(..., description="The story that was told")
    student_answer: str = Field(..., description="Student's response to the question")
    language: str = Field(default="English", description="Language for the response")


class StoryQuizRequest(BaseModel):
    concept: str = Field(..., description="The concept being taught")
    story: str = Field(..., description="The story to base quiz on")
    language: str = Field(default="English", description="Language for the quiz")


# ============================================================
# Endpoints
# ============================================================

@router.post("/generate")
async def generate_story(request: StoryRequest):
    """
    Generate an educational story for a given concept.

    The story will:
    - Be 150-250 words
    - Use relatable characters
    - Embed the concept naturally
    - Include a follow-up question
    """
    try:
        result = await story_service.generate_concept_story(
            concept=request.concept,
            language=request.language,
            difficulty_level=request.difficulty_level
        )
        
        # Generate illustration for the story concept
        try:
            illustration = await illustration_service.generate_illustration(
                topic=request.concept,
                subject="General",
                context=result.get("story", request.concept),
                turn_number=1  # First turn always gets illustration
            )
            if illustration:
                result["illustration"] = illustration
        except Exception:
            pass
        
        # Generate actual image for the story
        image_url = await _generate_story_image(
            concept=request.concept,
            context=result.get("story", request.concept)
        )
        if image_url:
            result["image_url"] = image_url
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate story: {str(e)}"
        )


@router.post("/discuss")
async def discuss_story(request: StoryDiscussionRequest):
    """
    Continue a story discussion with Socratic feedback.

    Provides affirmation, correction, and a follow-up question
    to deepen understanding.
    """
    try:
        response = await story_service.continue_story_discussion(
            concept=request.concept,
            story=request.story,
            student_answer=request.student_answer,
            language=request.language
        )
        
        # Generate image for the discussion response
        image_url = await _generate_story_image(
            concept=request.concept,
            context=f"{request.student_answer} - {response[:200] if isinstance(response, str) else str(response)[:200]}"
        )
        
        result = {"response": response}
        if image_url:
            result["image_url"] = image_url
        
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to continue discussion: {str(e)}"
        )


@router.post("/quiz")
async def generate_story_quiz(request: StoryQuizRequest):
    """
    Generate a quiz question based on the story.

    Creates a multiple choice question to test understanding
    of the concept taught in the story.
    """
    try:
        result = await story_service.generate_quiz_from_story(
            concept=request.concept,
            story=request.story,
            language=request.language
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate quiz: {str(e)}"
        )


@router.get("/health")
async def health_check():
    """Health check endpoint for story learning service"""
    return {"status": "healthy", "service": "story-learning"}
