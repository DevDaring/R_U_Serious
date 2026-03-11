"""
DigitalOcean Gradient AI Provider

Uses DigitalOcean Gradient Serverless LLM API (OpenAI-compatible endpoint)
and Gradient AI Agent for Ritty.
"""

import os
import httpx
import json
from typing import Any, Optional
from .base import (
    BaseAIProvider,
    ContentGenerationRequest,
    QuestionGenerationRequest,
    AnswerEvaluationRequest
)


GRADIENT_BASE_URL = os.getenv("GRADIENT_BASE_URL", "https://inference.do-ai.run/v1")
GRADIENT_API_KEY = os.getenv("GRADIENT_API_KEY", "")
GRADIENT_MODEL = os.getenv("GRADIENT_MODEL", "meta-llama/Meta-Llama-3.3-70B-Instruct")
RITTY_AGENT_UUID = os.getenv("RITTY_AGENT_UUID", "")


class DigitalOceanAIProvider(BaseAIProvider):
    """DigitalOcean Gradient AI provider implementation."""

    def __init__(self):
        self.api_key = GRADIENT_API_KEY
        self.base_url = GRADIENT_BASE_URL
        self.model = GRADIENT_MODEL
        self.ritty_agent_uuid = RITTY_AGENT_UUID

    async def _call_llm(self, messages: list[dict], stream: bool = False) -> str:
        """Call DO Gradient Serverless LLM — OpenAI-compatible endpoint."""
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": stream,
            "max_tokens": 2048,
            "temperature": 0.7
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def _call_ritty_agent(self, user_message: str, conversation_history: list[dict]) -> str:
        """
        Call the Ritty Gradient AI Agent by UUID.
        Uses the DO Gradient Agent API — not the raw LLM endpoint.
        The agent has Ritty's persona and NCERT Knowledge Base pre-attached.
        """
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "message": user_message,
            "conversation_history": conversation_history
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"https://api.digitalocean.com/v2/gen-ai/agents/{self.ritty_agent_uuid}/chat",
                headers=headers,
                json=payload
            )
            response.raise_for_status()
            data = response.json()
            return data["message"]["content"]

    def _parse_json_response(self, response: str) -> dict[str, Any]:
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

    async def generate_content(
        self,
        request: ContentGenerationRequest
    ) -> dict[str, Any]:
        """Generate learning content including story narratives and facts."""

        prompt = f"""Generate engaging learning content for the topic: "{request.topic}"

Difficulty Level: {request.difficulty_level}/10
Visual Style: {request.visual_style}
Story Style: {request.story_style}
Number of Segments: {request.num_images}

Generate {request.num_images} story segments. Each segment should:
1. Have an engaging narrative (150-200 words)
2. Include 3-5 key facts
3. Suggest an image description for visualization

Respond with ONLY a valid JSON object:
{{
    "story_segments": [
        {{
            "narrative": "<engaging story narrative>",
            "facts": ["<fact1>", "<fact2>", "<fact3>"],
            "image_prompt": "<description for image generation>"
        }}
    ],
    "topic_summary": "<brief summary of the topic>"
}}

IMPORTANT: Return ONLY the JSON object. No other text."""

        try:
            response = await self._call_llm([{"role": "user", "content": prompt}])
            result = self._parse_json_response(response)

            # Ensure we have the expected structure
            if "story_segments" not in result:
                result["story_segments"] = [{
                    "narrative": f"Let's learn about {request.topic}!",
                    "facts": [f"Key concept about {request.topic}"],
                    "image_prompt": f"Educational illustration about {request.topic}"
                }]
            if "topic_summary" not in result:
                result["topic_summary"] = f"Introduction to {request.topic}"

            return result
        except Exception as e:
            print(f"Error in generate_content: {e}")
            return {
                "story_segments": [{
                    "narrative": f"Welcome to learning about {request.topic}!",
                    "facts": [f"Interesting fact about {request.topic}"],
                    "image_prompt": f"Educational content about {request.topic}"
                }],
                "topic_summary": f"Overview of {request.topic}"
            }

    async def generate_mcq_questions(
        self,
        request: QuestionGenerationRequest
    ) -> list[dict[str, Any]]:
        """Generate multiple choice questions."""

        prompt = f"""Generate {request.num_mcq} multiple choice questions about: "{request.topic}"

Difficulty Level: {request.difficulty_level}/10
Context: {request.content_context}

Each question should:
1. Test understanding of the topic
2. Have 4 options (A, B, C, D)
3. Include the correct answer
4. Have a brief explanation

Respond with ONLY a valid JSON array:
[
    {{
        "question": "<question text>",
        "options": {{
            "A": "<option A>",
            "B": "<option B>",
            "C": "<option C>",
            "D": "<option D>"
        }},
        "correct_answer": "<A, B, C, or D>",
        "explanation": "<brief explanation>"
    }}
]

IMPORTANT: Return ONLY the JSON array. No other text."""

        try:
            response = await self._call_llm([{"role": "user", "content": prompt}])
            result = self._parse_json_response(response)

            if isinstance(result, list):
                return result
            elif isinstance(result, dict) and "questions" in result:
                return result["questions"]
            else:
                return []
        except Exception as e:
            print(f"Error in generate_mcq_questions: {e}")
            return []

    async def generate_descriptive_questions(
        self,
        request: QuestionGenerationRequest
    ) -> list[dict[str, Any]]:
        """Generate descriptive/open-ended questions."""

        prompt = f"""Generate {request.num_descriptive} descriptive questions about: "{request.topic}"

Difficulty Level: {request.difficulty_level}/10
Context: {request.content_context}

Each question should:
1. Require detailed explanation (not one-word answers)
2. Test deep understanding
3. Include a model answer for reference
4. List key keywords to look for

Respond with ONLY a valid JSON array:
[
    {{
        "question": "<question text>",
        "model_answer": "<detailed model answer>",
        "keywords": ["<keyword1>", "<keyword2>", "<keyword3>"],
        "max_score": 10
    }}
]

IMPORTANT: Return ONLY the JSON array. No other text."""

        try:
            response = await self._call_llm([{"role": "user", "content": prompt}])
            result = self._parse_json_response(response)

            if isinstance(result, list):
                return result
            elif isinstance(result, dict) and "questions" in result:
                return result["questions"]
            else:
                return []
        except Exception as e:
            print(f"Error in generate_descriptive_questions: {e}")
            return []

    async def evaluate_answer(
        self,
        request: AnswerEvaluationRequest
    ) -> dict[str, Any]:
        """Evaluate a descriptive answer."""

        prompt = f"""Evaluate the following student answer:

Question: {request.question}
Model Answer: {request.model_answer}
Student Answer: {request.user_answer}
Keywords to check: {", ".join(request.keywords)}
Max Score: {request.max_score}

Provide evaluation in JSON format:
{{
    "score": <score out of {request.max_score}>,
    "max_score": {request.max_score},
    "feedback": {{
        "correct_points": ["<point1>", "<point2>"],
        "improvements": ["<improvement1>", "<improvement2>"],
        "explanation": "<overall feedback>"
    }}
}}

IMPORTANT: Return ONLY the JSON object. No other text."""

        try:
            response = await self._call_llm([{"role": "user", "content": prompt}])
            result = self._parse_json_response(response)

            # Ensure we have the expected structure
            if "feedback" not in result:
                result["feedback"] = {
                    "correct_points": ["Good attempt"],
                    "improvements": ["Try to be more specific"],
                    "explanation": "Keep practicing!"
                }

            return result
        except Exception as e:
            print(f"Error in evaluate_answer: {e}")
            return {
                "score": request.max_score // 2,
                "max_score": request.max_score,
                "feedback": {
                    "correct_points": ["Thanks for your answer"],
                    "improvements": ["Try to include more details"],
                    "explanation": "Good effort!"
                }
            }

    async def chat(
        self,
        message: str,
        context: Optional[str] = None,
        language: str = "en"
    ) -> str:
        """General chat/conversation capability."""

        system_prompt = f"""You are a helpful AI learning assistant for the FunLearn app.
You help students understand concepts through engaging conversations.
Respond in {language}.
Keep your responses concise and friendly."""

        messages = [{"role": "system", "content": system_prompt}]

        if context:
            messages.append({"role": "system", "content": f"Context: {context}"})

        messages.append({"role": "user", "content": message})

        try:
            return await self._call_llm(messages)
        except Exception as e:
            print(f"Error in chat: {e}")
            return "I'm here to help you learn! What would you like to know?"

    async def ritty_chat(
        self,
        user_message: str,
        conversation_history: list[dict]
    ) -> str:
        """
        Call the Ritty Gradient AI Agent by UUID.
        This is used specifically for the Feynman Engine Layer 1.
        """
        try:
            return await self._call_ritty_agent(user_message, conversation_history)
        except Exception as e:
            print(f"Error in ritty_chat: {e}")
            # Fallback to regular LLM if agent call fails
            return await self.chat(user_message)

    async def health_check(self) -> bool:
        """Check if the provider is accessible."""
        try:
            # Simple test call to verify connectivity
            test_response = await self._call_llm([
                {"role": "user", "content": "Hello"}
            ])
            return bool(test_response)
        except Exception:
            return False
