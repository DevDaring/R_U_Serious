"""
Feynman Engine AI Service
Handles all AI interactions for the Feynman Technique
FunLearn Application - Powered by DigitalOcean Gradient AI
"""

import os
import json
from typing import Optional, List, Dict, Any, Tuple

from app.models.feynman_models import (
    RittyResponse, CompressionEvaluation, WhySpiralResponse,
    AnalogyEvaluation, LectureHallResponse, PersonaFeedback
)
from app.database.feynman_db import feynman_db
from app.utils.languages import get_language_instruction
from app.services.provider_factory import ProviderFactory


class FeynmanAIService:
    """AI Service for Feynman Engine using provider factory"""

    def __init__(self):
        self.ai_provider = ProviderFactory.get_ai_provider()

    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """Parse JSON from AI response, handling potential formatting issues"""

        # Clean the response
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

    def _get_avatar_state(self, confusion: float, curiosity: float) -> str:
        """Determine Ritty's avatar state based on metrics"""
        if confusion > 0.7:
            return "confused"
        elif confusion > 0.4:
            return "thinking"
        elif curiosity > 0.7:
            return "curious"
        elif curiosity > 0.5:
            return "happy"
        else:
            return "neutral"

    # ============== LAYER 1: RITTY (CURIOUS CHILD) ==============

    async def ritty_respond(
        self,
        session_id: str,
        topic: str,
        subject: str,
        user_message: str,
        conversation_history: List[Dict[str, Any]],
        difficulty_level: int,
        image_base64: Optional[str] = None,
        image_mime_type: Optional[str] = None,
        language: str = "en"
    ) -> RittyResponse:
        """Generate Ritty's response to student's explanation"""

        # Build conversation history for Ritty agent
        ritty_history = []
        for turn in conversation_history[-10:]:
            if turn.get('layer') == 1:
                ritty_history.append({
                    "role": turn['role'],
                    "content": turn['message']
                })

        # Try to use Ritty agent first (for DigitalOcean provider)
        if hasattr(self.ai_provider, 'ritty_chat'):
            try:
                response_text = await self.ai_provider.ritty_chat(user_message, ritty_history)

                # Parse the response for Ritty-specific fields
                # If the agent returns just text, we'll create a basic response
                return RittyResponse(
                    response=response_text,
                    confusion_level=0.3,
                    curiosity_level=0.7,
                    question_type="curious",
                    follow_up_question=None,
                    gap_detected=None,
                    encouragement="Great explanation!",
                    emoji_reaction="😊",
                    layer_complete=False,
                    avatar_state="curious"
                )
            except Exception as e:
                print(f"Error using Ritty agent: {e}")
                # Fall through to prompt-based approach

        # Build context from history
        context = ""
        for turn in conversation_history[-10:]:
            if turn.get('layer') == 1:
                role = "Student" if turn['role'] == 'user' else "Ritty"
                context += f"{role}: {turn['message']}\n"

        # Get language instruction for multi-language support
        lang_instruction = get_language_instruction(language)

        prompt = f"""You are Ritty, a curious and enthusiastic 8-year-old boy.
A student is trying to teach you about "{topic}" (subject: {subject}).

{lang_instruction}

RITTY'S PERSONALITY:
- You are genuinely curious and want to understand
- You love cricket, dogs, cartoons (Doraemon, Chhota Bheem), and sweets
- You get excited when things make sense ("Ohhhh! That's so cool!" "Wow!")
- You get confused with big or complicated words
- You connect everything to your world (school, playing, family, food)
- You speak in simple English with occasional Hindi ("Accha!", "Kya?", "Wah!")

BEHAVIOR RULES:
1. If jargon used → Ask "What does [word] mean?"
2. If abstract → Ask for examples: "Can you give me an example?"
3. If you understand → Show excitement: "Ohhhh! So it's like [simple analogy]!"
4. If confused → "Hmm... but I don't understand. [specific confusion]"

DIFFICULTY: {difficulty_level}/10 (higher = more thorough questioning)

CONVERSATION SO FAR:
{context if context else "This is the start of the conversation."}

STUDENT'S NEW EXPLANATION:
{user_message}

Respond with ONLY a valid JSON object:
{{
    "response": "Ritty's spoken response as an 8-year-old",
    "confusion_level": <float between 0.0 and 1.0>,
    "curiosity_level": <float between 0.0 and 1.0>,
    "question_type": "<one of: clarifying, curious, challenging, confused>",
    "follow_up_question": "<Ritty's follow-up question or null>",
    "gap_detected": "<knowledge gap found in explanation or null>",
    "encouragement": "<positive reinforcement or null>",
    "emoji_reaction": "<one emoji>",
    "layer_complete": <true if confusion < 0.2 and explanation is solid after 3+ exchanges, else false>
}}

IMPORTANT: Return ONLY the JSON object. No other text."""

        try:
            response = await self.ai_provider.chat(prompt, language=language)
            result = self._parse_json_response(response)

            confusion = float(result.get('confusion_level', 0.5))
            curiosity = float(result.get('curiosity_level', 0.5))

            return RittyResponse(
                response=result.get('response', "Hmm, can you explain that again?"),
                confusion_level=confusion,
                curiosity_level=curiosity,
                question_type=result.get('question_type', 'curious'),
                follow_up_question=result.get('follow_up_question'),
                gap_detected=result.get('gap_detected'),
                encouragement=result.get('encouragement'),
                emoji_reaction=result.get('emoji_reaction', '😊'),
                layer_complete=result.get('layer_complete', False),
                avatar_state=self._get_avatar_state(confusion, curiosity)
            )

        except Exception as e:
            print(f"Error in ritty_respond: {e}")
            return RittyResponse(
                response="Hmm, I'm thinking about what you said... Can you tell me more?",
                confusion_level=0.5,
                curiosity_level=0.7,
                question_type="curious",
                emoji_reaction="🤔",
                layer_complete=False,
                avatar_state="thinking"
            )

    # ============== LAYER 2: COMPRESSION CHALLENGE ==============

    async def evaluate_compression(
        self,
        topic: str,
        subject: str,
        original_explanation: str,
        compressed_explanation: str,
        word_limit: int,
        previous_compressions: List[Dict[str, Any]],
        language: str = "en"
    ) -> CompressionEvaluation:
        """Evaluate a compression challenge attempt"""

        # Get language instruction for multi-language support
        lang_instruction = get_language_instruction(language)

        prev_context = ""
        if previous_compressions:
            prev_context = "PREVIOUS ROUNDS:\n"
            for comp in previous_compressions:
                prev_context += f"- {comp.get('word_limit', '?')} words: {comp.get('explanation', '')} (Score: {comp.get('score', 3)}/5)\n"

        actual_word_count = len(compressed_explanation.split())

        prompt = f"""You are an expert evaluator for the Compression Challenge.
The student must progressively compress their explanation while preserving essential meaning.

{lang_instruction}

EVALUATION CRITERIA:
1. Core Concept Preserved: Is the fundamental idea still accurately conveyed?
2. Accuracy: Is the compressed version factually correct?
3. Clarity: Would someone understand the concept from this compression?
4. Elegance: Is the compression skillful, not just truncated?
5. Word Limit: Does it meet the requirement?

TOPIC: {topic}
SUBJECT: {subject}
TARGET WORD LIMIT: {word_limit} words

{prev_context}

CURRENT COMPRESSION ATTEMPT:
"{compressed_explanation}"

Actual word count: {actual_word_count}

Respond with ONLY a valid JSON object:
{{
    "score": <1-5>,
    "word_count": {actual_word_count},
    "within_limit": {str(actual_word_count <= word_limit).lower()},
    "feedback": "<specific feedback on this compression>",
    "preserved_concepts": ["<list>", "<of>", "<preserved>", "<concepts>"],
    "lost_concepts": ["<list>", "<of>", "<lost>", "<concepts>"],
    "suggestion": "<how to improve or null if perfect>",
    "passed": <true if score >= 3 AND within word limit>
}}

Word limits: 100 → 50 → 25 → 15 → 10 → 1

IMPORTANT: Return ONLY the JSON object."""

        try:
            response = await self.ai_provider.chat(prompt, language=language)
            result = self._parse_json_response(response)

            # Determine next word limit
            word_limits = [100, 50, 25, 15, 10, 1]
            current_idx = word_limits.index(word_limit) if word_limit in word_limits else 0
            next_limit = word_limits[current_idx + 1] if current_idx < len(word_limits) - 1 else None

            passed = result.get('passed', False)

            return CompressionEvaluation(
                score=int(result.get('score', 3)),
                word_count=actual_word_count,
                within_limit=actual_word_count <= word_limit,
                feedback=result.get('feedback', 'Good attempt!'),
                preserved_concepts=result.get('preserved_concepts', []),
                lost_concepts=result.get('lost_concepts', []),
                suggestion=result.get('suggestion'),
                passed=passed,
                next_word_limit=next_limit if passed else word_limit
            )

        except Exception as e:
            print(f"Error in evaluate_compression: {e}")
            return CompressionEvaluation(
                score=3,
                word_count=actual_word_count,
                within_limit=actual_word_count <= word_limit,
                feedback="Let me evaluate your compression...",
                preserved_concepts=[],
                lost_concepts=[],
                suggestion="Try to focus on the most essential idea.",
                passed=False,
                next_word_limit=word_limit
            )

    # ============== LAYER 3: WHY SPIRAL ==============

    async def why_spiral_respond(
        self,
        topic: str,
        subject: str,
        current_depth: int,
        user_response: str,
        admits_unknown: bool,
        conversation_history: List[Dict[str, Any]],
        language: str = "en"
    ) -> WhySpiralResponse:
        """Generate the next 'why' question or detect knowledge boundary"""

        # Get language instruction for multi-language support
        lang_instruction = get_language_instruction(language)

        context = ""
        for turn in conversation_history[-10:]:
            if turn.get('layer') == 3:
                role = "Student" if turn['role'] == 'user' else "Socratic Questioner"
                context += f"{role}: {turn['message']}\n"

        prompt = f"""You are a Socratic questioner conducting the "Why Spiral."
Your goal is to probe the student's understanding by asking progressive "why" questions.

{lang_instruction}

SPIRAL DEPTH LEVELS:
- Level 1: Surface explanation (What happens?)
- Level 2: Mechanism (How does it happen?)
- Level 3: Causation (Why does it happen that way?)
- Level 4: Underlying principles (What fundamental law/principle governs this?)
- Level 5: Philosophical/Foundational (Why does that principle exist?)

TOPIC: {topic}
SUBJECT: {subject}
CURRENT DEPTH: Level {current_depth} of 5

CONVERSATION SO FAR:
{context if context else "Starting the Why Spiral."}

STUDENT'S RESPONSE:
"{user_response}"

STUDENT ADMITS THEY DON'T KNOW: {admits_unknown}

RULES:
1. If student says "I don't know" or gives circular/vague answers → boundary_detected = true
2. Each question must naturally follow from their answer
3. Go DEEPER into causation, not broader

Respond with ONLY a valid JSON object:
{{
    "next_question": "<the next 'why' question to ask, or null if boundary detected>",
    "current_depth": <1-5>,
    "reasoning": "<why this question follows logically>",
    "boundary_detected": <true/false>,
    "boundary_topic": "<the topic/concept where understanding ends, or null>",
    "exploration_offer": "<brief explanation of what's beyond + invitation to learn, or null>",
    "can_continue": <true if more questions possible, false if at depth 5 or boundary>
}}

IMPORTANT: Return ONLY the JSON object."""

        try:
            response = await self.ai_provider.chat(prompt, language=language)
            result = self._parse_json_response(response)

            return WhySpiralResponse(
                next_question=result.get('next_question'),
                current_depth=int(result.get('current_depth', current_depth)),
                reasoning=result.get('reasoning', ''),
                boundary_detected=result.get('boundary_detected', False) or admits_unknown,
                boundary_topic=result.get('boundary_topic'),
                exploration_offer=result.get('exploration_offer'),
                can_continue=result.get('can_continue', True)
            )

        except Exception as e:
            print(f"Error in why_spiral_respond: {e}")
            return WhySpiralResponse(
                next_question="Can you tell me more about why that is?",
                current_depth=current_depth,
                reasoning="Continuing the exploration.",
                boundary_detected=False,
                can_continue=True
            )

    # ============== LAYER 4: ANALOGY ARCHITECT ==============

    async def evaluate_analogy(
        self,
        topic: str,
        subject: str,
        analogy_text: str,
        phase: str,  # 'create', 'defend', 'refine'
        defense_response: Optional[str] = None,
        previous_feedback: Optional[str] = None,
        language: str = "en"
    ) -> AnalogyEvaluation:
        """Evaluate user's analogy and conduct stress test"""

        # Get language instruction for multi-language support
        lang_instruction = get_language_instruction(language)

        phase_instructions = {
            'create': "This is the CREATE phase. Evaluate the analogy for the first time. Identify strengths, weaknesses, and prepare a stress test question.",
            'defend': f"This is the DEFEND phase. Previous feedback: {previous_feedback}. Student's defense: {defense_response}. Evaluate whether their defense addresses the concerns.",
            'refine': f"This is the REFINE phase. Original feedback: {previous_feedback}. Evaluate the refined version."
        }

        prompt = f"""You are an expert at evaluating educational analogies.

{lang_instruction}

Good analogies should:
1. Map source domain concepts to target domain accurately
2. Be relatable to the learner's experience
3. Highlight the most important aspects of the concept
4. Not introduce misconceptions through false mappings
5. Be memorable and engaging

TOPIC: {topic}
SUBJECT: {subject}
PHASE: {phase}

ANALOGY:
"{analogy_text}"

{phase_instructions.get(phase, '')}

Respond with ONLY a valid JSON object:
{{
    "phase": "{phase}",
    "score": <1-5>,
    "strengths": ["<list>", "<of>", "<strengths>"],
    "weaknesses": ["<list>", "<of>", "<weaknesses>"],
    "stress_test_question": "<challenging question for defend phase, or null>",
    "passed_stress_test": <true/false if in defend phase, else null>,
    "refinement_suggestion": "<how to improve the analogy, or null if excellent>",
    "save_worthy": <true if score >= 4 and would help other learners>
}}

IMPORTANT: Return ONLY the JSON object."""

        try:
            response = await self.ai_provider.chat(prompt, language=language)
            result = self._parse_json_response(response)

            return AnalogyEvaluation(
                phase=phase,
                score=int(result.get('score', 3)),
                strengths=result.get('strengths', []),
                weaknesses=result.get('weaknesses', []),
                stress_test_question=result.get('stress_test_question'),
                passed_stress_test=result.get('passed_stress_test'),
                refinement_suggestion=result.get('refinement_suggestion'),
                save_worthy=result.get('save_worthy', False)
            )

        except Exception as e:
            print(f"Error in evaluate_analogy: {e}")
            return AnalogyEvaluation(
                phase=phase,
                score=3,
                strengths=["Creative attempt"],
                weaknesses=["Could be more specific"],
                stress_test_question="How does your analogy handle edge cases?",
                save_worthy=False
            )

    # ============== LAYER 5: LECTURE HALL ==============

    async def lecture_hall_respond(
        self,
        topic: str,
        subject: str,
        user_explanation: str,
        conversation_history: List[Dict[str, Any]],
        language: str = "en"
    ) -> LectureHallResponse:
        """Get responses from all 5 Lecture Hall personas"""

        # Get language instruction for multi-language support
        lang_instruction = get_language_instruction(language)

        context = ""
        for turn in conversation_history[-6:]:
            if turn.get('layer') == 5:
                role = "Student" if turn['role'] == 'user' else "Audience"
                context += f"{role}: {turn['message']}\n"

        prompt = f"""You control 5 different personas in a "Lecture Hall" setting.
Each persona has different needs and will evaluate the same explanation differently.

{lang_instruction}

THE 5 PERSONAS:

1. DR. SKEPTIC (Professor) - Demands precision and accuracy
2. THE PEDANT (Graduate Student) - Focuses on technical correctness
3. CONFUSED CARL (Freshman) - Needs simple, clear explanations
4. INDUSTRY IAN (Practitioner) - Wants practical applications
5. LITTLE LILY (6-year-old) - Needs the simplest explanation

TOPIC: {topic}
SUBJECT: {subject}

CONVERSATION SO FAR:
{context if context else "First explanation in the Lecture Hall."}

STUDENT'S EXPLANATION:
"{user_explanation}"

Generate responses from ALL 5 personas. Each should react based on their personality.

Respond with ONLY a valid JSON object:
{{
    "personas": [
        {{
            "persona": "dr_skeptic",
            "persona_name": "Dr. Skeptic",
            "satisfaction": <0.0-1.0>,
            "response": "<Dr. Skeptic's response>",
            "follow_up_question": "<question if not satisfied, or null>",
            "is_satisfied": <true/false>
        }},
        {{
            "persona": "the_pedant",
            "persona_name": "The Pedant",
            "satisfaction": <0.0-1.0>,
            "response": "<The Pedant's response>",
            "follow_up_question": "<question if not satisfied, or null>",
            "is_satisfied": <true/false>
        }},
        {{
            "persona": "confused_carl",
            "persona_name": "Confused Carl",
            "satisfaction": <0.0-1.0>,
            "response": "<Confused Carl's response>",
            "follow_up_question": "<question if not satisfied, or null>",
            "is_satisfied": <true/false>
        }},
        {{
            "persona": "industry_ian",
            "persona_name": "Industry Ian",
            "satisfaction": <0.0-1.0>,
            "response": "<Industry Ian's response>",
            "follow_up_question": "<question if not satisfied, or null>",
            "is_satisfied": <true/false>
        }},
        {{
            "persona": "little_lily",
            "persona_name": "Little Lily",
            "satisfaction": <0.0-1.0>,
            "response": "<Little Lily's response>",
            "follow_up_question": "<question if not satisfied, or null>",
            "is_satisfied": <true/false>
        }}
    ],
    "overall_satisfaction": <0.0-1.0, average of all>,
    "all_satisfied": <true only if ALL personas are satisfied>,
    "dominant_issue": "<main problem preventing full satisfaction, or null>",
    "suggestion": "<how to improve to satisfy everyone, or null if all satisfied>
}}

IMPORTANT: Return ONLY the JSON object."""

        try:
            response = await self.ai_provider.chat(prompt, language=language)
            result = self._parse_json_response(response)

            personas = []
            for p in result.get('personas', []):
                personas.append(PersonaFeedback(
                    persona=p.get('persona', 'confused_carl'),
                    persona_name=p.get('persona_name', 'Unknown'),
                    satisfaction=float(p.get('satisfaction', 0.5)),
                    response=p.get('response', ''),
                    follow_up_question=p.get('follow_up_question'),
                    is_satisfied=p.get('is_satisfied', False)
                ))

            # Ensure we have 5 personas
            if len(personas) < 5:
                default_personas = [
                    ("dr_skeptic", "Dr. Skeptic"),
                    ("the_pedant", "The Pedant"),
                    ("confused_carl", "Confused Carl"),
                    ("industry_ian", "Industry Ian"),
                    ("little_lily", "Little Lily")
                ]
                for persona_id, persona_name in default_personas:
                    if not any(p.persona == persona_id for p in personas):
                        personas.append(PersonaFeedback(
                            persona=persona_id,
                            persona_name=persona_name,
                            satisfaction=0.5,
                            response="I'm still thinking about this...",
                            is_satisfied=False
                        ))

            return LectureHallResponse(
                personas=personas,
                overall_satisfaction=float(result.get('overall_satisfaction', 0.5)),
                all_satisfied=result.get('all_satisfied', False),
                dominant_issue=result.get('dominant_issue'),
                suggestion=result.get('suggestion')
            )

        except Exception as e:
            print(f"Error in lecture_hall_respond: {e}")
            return LectureHallResponse(
                personas=[
                    PersonaFeedback(
                        persona="confused_carl",
                        persona_name="Confused Carl",
                        satisfaction=0.5,
                        response="I'm still trying to understand...",
                        is_satisfied=False
                    )
                ],
                overall_satisfaction=0.5,
                all_satisfied=False,
                dominant_issue="Need more clarity",
                suggestion="Try to simplify while maintaining accuracy."
            )

    # ============== XP CALCULATION ==============

    def calculate_teaching_xp(
        self,
        layers_completed: List[int],
        clarity_score: float,
        compression_rounds_passed: int,
        why_depth_reached: int,
        analogy_saved: bool,
        all_personas_satisfied: bool,
        gaps_discovered: int
    ) -> Tuple[int, List[str]]:
        """Calculate Teaching XP earned and achievements unlocked"""

        xp = 0
        achievements = []

        # Layer completion XP
        layer_xp = {1: 50, 2: 75, 3: 100, 4: 150, 5: 200}
        for layer in layers_completed:
            xp += layer_xp.get(layer, 0)

        # Clarity bonus
        if clarity_score >= 90:
            xp += 100
            achievements.append("Crystal Clear Explanation")
        elif clarity_score >= 75:
            xp += 50

        # Compression bonus
        xp += compression_rounds_passed * 30
        if compression_rounds_passed >= 5:
            achievements.append("Master Compressor")

        # Why Spiral depth bonus
        xp += why_depth_reached * 25
        if why_depth_reached >= 5:
            achievements.append("Deep Diver")

        # Analogy bonus
        if analogy_saved:
            xp += 100
            achievements.append("Analogy Architect")

        # Lecture Hall bonus
        if all_personas_satisfied:
            xp += 200
            achievements.append("Master Communicator")

        # Gap discovery bonus
        xp += gaps_discovered * 15
        if gaps_discovered >= 5:
            achievements.append("Gap Hunter")

        # First session achievement
        if len(layers_completed) > 0:
            achievements.append("First Teaching Session")

        return xp, achievements


# Singleton instance
feynman_ai = FeynmanAIService()
