"""
AI Illustration Service
Generates structured visual illustration data using the LLM.
Since IMAGE_PROVIDER=none, we use the AI to create rich illustrated card data
that the frontend renders as beautiful educational visuals.
"""

import json
import logging
from typing import Optional, Dict, Any

from app.services.provider_factory import ProviderFactory

logger = logging.getLogger(__name__)


class IllustrationService:
    """Generate educational illustration data using the LLM"""

    def __init__(self):
        self.ai_provider = ProviderFactory.get_ai_provider()

    def should_generate_illustration(self, turn_number: int) -> bool:
        """
        Determine if an illustration should be generated for this turn.
        Rule: First 5 turns ALWAYS get illustrations, then 1 every 2 turns.
        """
        if turn_number <= 5:
            return True
        return (turn_number - 5) % 2 == 0

    async def generate_illustration(
        self,
        topic: str,
        subject: str,
        context: str,
        turn_number: int,
        style: str = "educational"
    ) -> Optional[Dict[str, Any]]:
        """
        Generate structured illustration data for the frontend to render.
        
        Returns a dict with:
        - title: Short title for the illustration
        - description: What the visual shows
        - visual_type: diagram|concept_map|comparison|process|analogy|example
        - elements: List of visual elements with labels/icons
        - colors: Suggested gradient colors
        - emoji_icon: Main representative emoji
        """
        if not self.should_generate_illustration(turn_number):
            return None

        prompt = f"""Generate a structured visual illustration description for an educational concept.

TOPIC: {topic}
SUBJECT: {subject}
CONTEXT (what's being discussed): {context[:500]}

Create an educational visual that helps explain this concept. Return ONLY a JSON object:
{{
    "title": "Short title (3-6 words)",
    "description": "One-sentence description of what this visual shows",
    "visual_type": "<one of: diagram, concept_map, comparison, process, analogy, formula, example, timeline>",
    "emoji_icon": "<single emoji representing the concept>",
    "elements": [
        {{"label": "Element 1", "detail": "Brief explanation", "icon": "<emoji>"}},
        {{"label": "Element 2", "detail": "Brief explanation", "icon": "<emoji>"}},
        {{"label": "Element 3", "detail": "Brief explanation", "icon": "<emoji>"}}
    ],
    "key_insight": "The main takeaway from this visual",
    "gradient": ["#color1", "#color2"]
}}

RULES:
- Use 3-5 elements maximum
- Each element should have a relevant emoji icon
- gradient colors should be soft, educational, pleasing
- key_insight should be memorable and concise
- Make it visually descriptive so it can be rendered as a card

Return ONLY the JSON object."""

        try:
            response = await self.ai_provider.chat(prompt)
            result = self._parse_json(response)
            
            if result and "title" in result:
                result["turn_number"] = turn_number
                return result
            
            # Fallback if parsing fails - create a simple illustration
            return self._create_fallback_illustration(topic, context, turn_number)
            
        except Exception as e:
            logger.warning(f"Illustration generation failed: {e}")
            return self._create_fallback_illustration(topic, context, turn_number)

    def _create_fallback_illustration(
        self, topic: str, context: str, turn_number: int
    ) -> Dict[str, Any]:
        """Create a fallback illustration when LLM fails"""
        return {
            "title": f"Understanding {topic[:30]}",
            "description": f"Key concept visualization for {topic}",
            "visual_type": "concept_map",
            "emoji_icon": "💡",
            "elements": [
                {"label": "Core Concept", "detail": topic[:50], "icon": "🎯"},
                {"label": "Key Point", "detail": "Think about how this connects", "icon": "🔗"},
                {"label": "Application", "detail": "Where this applies in practice", "icon": "⚡"}
            ],
            "key_insight": f"Understanding {topic} builds on connecting its core ideas",
            "gradient": ["#667eea", "#764ba2"],
            "turn_number": turn_number
        }

    def _parse_json(self, response: str) -> Optional[Dict[str, Any]]:
        """Parse JSON from AI response"""
        text = response.strip()
        
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
            start = text.find('{')
            end = text.rfind('}') + 1
            if start != -1 and end > start:
                try:
                    return json.loads(text[start:end])
                except json.JSONDecodeError:
                    pass
        return None


# Singleton instance
illustration_service = IllustrationService()
