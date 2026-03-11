"""
Story Learning Service

Generates educational stories for any concept to help students learn
through engaging narratives.
FunLearn Application - Powered by DigitalOcean Gradient AI
"""

import json
from typing import Dict, Any
from app.services.provider_factory import ProviderFactory


class StoryLearningService:
    """Service for generating educational stories"""

    def __init__(self):
        self.ai_provider = ProviderFactory.get_ai_provider()

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from AI response, handling potential formatting issues."""
        text = response.strip()

        # Remove markdown code blocks if present
        if text.startswith('```json'):
            text = text[7:]
        if text.startswith('```'):
            text = text[3:]
        if text.endswith('```'):
            text = text[:-3]

        text = text.strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            # Try to find JSON object in the response
            start = text.find('{')
            end = text.rfind('}') + 1

            if start != -1 and end > start:
                try:
                    return json.loads(text[start:end])
                except json.JSONDecodeError:
                    pass

            print(f"Failed to parse JSON: {text[:200]}...")
            return {}

    async def generate_concept_story(
        self,
        concept: str,
        language: str = "English",
        difficulty_level: int = 5
    ) -> Dict[str, Any]:
        """
        Generate an educational story for a given concept.

        Args:
            concept: The concept to teach through story
            language: Language for the story
            difficulty_level: Difficulty (1-10)

        Returns:
            Dictionary with story and follow-up question
        """

        prompt = f"""You are a master storyteller and educator.
Your job is to explain any concept the student provides through an engaging short story.

Concept to teach: "{concept}"
Language: {language}
Difficulty Level: {difficulty_level}/10

Rules:
- The story must be 150-250 words maximum
- The concept must be embedded naturally in the story plot
- Use relatable characters (school kids, village settings, everyday Indian life)
- End with one reflection question: "What did [character] learn?"
- Respond in the language the student selects
- Never use textbook language. Make it feel like a campfire story.

Respond with ONLY a valid JSON object:
{{
    "story": "<the engaging story that teaches the concept>",
    "follow_up_question": "<one probing question to check understanding>",
    "concept": "{concept}",
    "character_names": ["<names of characters in the story>"]
}}

IMPORTANT: Return ONLY the JSON object. No other text."""

        try:
            response = await self.ai_provider.chat(prompt, language=language)
            result = self._parse_json_response(response)

            # Ensure we have the expected structure
            if "story" not in result:
                result["story"] = f"Once upon a time, there was a story about {concept}..."
            if "follow_up_question" not in result:
                result["follow_up_question"] = f"What did you learn about {concept}?"

            return result

        except Exception as e:
            print(f"Error in generate_concept_story: {e}")
            return {
                "story": f"Let me tell you a story about {concept}. Once upon a time, a curious student wanted to understand this concept...",
                "follow_up_question": f"What did you learn about {concept}?",
                "concept": concept
            }

    async def continue_story_discussion(
        self,
        concept: str,
        story: str,
        student_answer: str,
        language: str = "English"
    ) -> str:
        """
        Continue the story discussion with Socratic feedback.

        Args:
            concept: The concept being taught
            story: The story that was told
            student_answer: Student's response to the follow-up question
            language: Language for the response

        Returns:
            Feedback string
        """

        prompt = f"""You are a kind Socratic teacher.
The student just answered a question about a story.

Concept: {concept}
Story: {story}
Student's Answer: {student_answer}
Language: {language}

Your task:
1. Affirm what the student got right
2. Gently correct what they got wrong (if anything)
3. Ask one more follow-up question to go deeper

Keep your response under 60 words. Respond in the student's language ({language})."""

        try:
            return await self.ai_provider.chat(prompt, language=language)
        except Exception as e:
            print(f"Error in continue_story_discussion: {e}")
            return "Thanks for sharing your thoughts! Would you like to explore this concept further with another story?"

    async def generate_quiz_from_story(
        self,
        concept: str,
        story: str,
        language: str = "English"
    ) -> Dict[str, Any]:
        """
        Generate a quiz question based on the story.

        Args:
            concept: The concept being taught
            story: The story that was told
            language: Language for the quiz

        Returns:
            Dictionary with quiz question and options
        """

        prompt = f"""Based on this story about "{concept}":

{story}

Create ONE multiple choice question to test understanding.

Respond with ONLY a valid JSON object:
{{
    "question": "<the quiz question>",
    "options": {{
        "A": "<option A>",
        "B": "<option B>",
        "C": "<option C>",
        "D": "<option D>"
    }},
    "correct_answer": "<A, B, C, or D>",
    "explanation": "<why this is the correct answer>"
}}

IMPORTANT: Return ONLY the JSON object. No other text."""

        try:
            response = await self.ai_provider.chat(prompt, language=language)
            result = self._parse_json_response(response)

            # Ensure we have the expected structure
            if "question" not in result:
                result["question"] = f"What was the main concept in this story about {concept}?"
                result["options"] = {"A": concept, "B": "Something else", "C": "Not sure", "D": "None"}
                result["correct_answer"] = "A"
                result["explanation"] = f"The story was teaching about {concept}."

            return result

        except Exception as e:
            print(f"Error in generate_quiz_from_story: {e}")
            return {
                "question": f"What was the main concept in this story?",
                "options": {
                    "A": concept,
                    "B": "Something else",
                    "C": "Not sure",
                    "D": "None"
                },
                "correct_answer": "A",
                "explanation": f"The story was teaching about {concept}."
            }


# Singleton instance
story_service = StoryLearningService()
