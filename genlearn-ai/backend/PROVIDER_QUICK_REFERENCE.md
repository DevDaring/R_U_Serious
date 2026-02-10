# Provider System Quick Reference

## Switch Providers (Just Change .env)

```env
AI_PROVIDER=gemini          # or: openai, anthropic
IMAGE_PROVIDER=fibo         # or: stability
VOICE_TTS_PROVIDER=gcp      # or: azure
VOICE_STT_PROVIDER=gcp      # or: azure
```

## Import and Use

```python
from app.services.provider_factory import ProviderFactory

# Get providers
ai = ProviderFactory.get_ai_provider()
image = ProviderFactory.get_image_provider()
tts = ProviderFactory.get_tts_provider()
stt = ProviderFactory.get_stt_provider()
```

## AI Provider Methods

```python
from app.services.ai_providers.base import (
    ContentGenerationRequest,
    QuestionGenerationRequest,
    AnswerEvaluationRequest
)

# Generate content
content = await ai.generate_content(ContentGenerationRequest(
    topic="Photosynthesis",
    difficulty_level=5,
    visual_style="cartoon",
    num_images=3
))

# Generate MCQ questions
mcqs = await ai.generate_mcq_questions(QuestionGenerationRequest(
    topic="Photosynthesis",
    difficulty_level=5,
    content_context="Story about plants...",
    num_mcq=3
))

# Generate descriptive questions
descriptive = await ai.generate_descriptive_questions(QuestionGenerationRequest(
    topic="Photosynthesis",
    difficulty_level=5,
    content_context="Story about plants...",
    num_descriptive=3
))

# Evaluate answer
evaluation = await ai.evaluate_answer(AnswerEvaluationRequest(
    question="Explain photosynthesis",
    model_answer="Plants use sunlight...",
    user_answer="Plants make food from sun...",
    keywords=["sunlight", "chlorophyll", "oxygen"],
    max_score=10
))

# Chat
response = await ai.chat("What is photosynthesis?", language="en")
```

## Image Provider Methods

```python
from app.services.image_providers.base import ImageGenerationRequest

# Generate image
image_bytes = await image.generate_image(ImageGenerationRequest(
    prompt="A cartoon scientist in a forest",
    style="cartoon",
    width=1024,
    height=576
))

# Generate avatar
avatar_bytes = await image.generate_avatar(
    source_image=uploaded_image_bytes,
    style="cartoon"
)

# Stylize character
character_bytes = await image.stylize_character(
    source_image=drawing_bytes,
    style="realistic"
)
```

## Voice Provider Methods

```python
# Text-to-Speech
audio_bytes = await tts.synthesize_speech(
    text="Welcome to Fun Learn!",
    language="en",
    voice_type="female",
    speed=1.0
)

# Speech-to-Text
text = await stt.transcribe_audio(
    audio_data=audio_bytes,
    language="en",
    audio_format="wav"
)

# Get supported languages
languages = tts.get_supported_languages()
# Returns: ["en", "hi", "bn", "es", "fr", "de", "ja", "zh"]
```

## Health Checks

```python
# Check single provider
is_healthy = await ai.health_check()

# Check all providers
status = await ProviderFactory.check_all_providers()
# Returns:
# {
#     "ai": {"provider": "GeminiProvider", "status": "healthy"},
#     "image": {"provider": "FiboProvider", "status": "healthy"},
#     "tts": {"provider": "GCPTTSProvider", "status": "healthy"},
#     "stt": {"provider": "GCPSTTProvider", "status": "healthy"}
# }
```

## Supported Languages

All voice providers support:
- `en` - English
- `hi` - Hindi
- `bn` - Bengali
- `es` - Spanish
- `fr` - French
- `de` - German
- `ja` - Japanese
- `zh` - Chinese (Mandarin)

## Style Options

Image providers support:
- `cartoon` - Colorful, animated, child-friendly
- `realistic` - Photographic, detailed, high quality

## Voice Types

- `male` - Male voice
- `female` - Female voice

## Required Environment Variables

### Gemini (Primary AI)
```env
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-3-pro-preview
```

### OpenAI (Fallback AI)
```env
OPENAI_API_KEY=your_key
OPENAI_MODEL=gpt-4o
```

### Anthropic (Fallback AI)
```env
ANTHROPIC_API_KEY=your_key
ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
```

### FIBO (Primary Image)
```env
FIBO_API_KEY=your_key
FIBO_API_ENDPOINT=https://api.fibo.ai/v1
```

### Stability AI (Fallback Image)
```env
STABILITY_API_KEY=your_key
```

### GCP Voice (Primary)
```env
GCP_TTS_API_KEY=your_key
GCP_STT_API_KEY=your_key
GCP_TTS_ENDPOINT=https://texttospeech.googleapis.com/v1
GCP_STT_ENDPOINT=https://speech.googleapis.com/v1
```

### Azure Voice (Fallback)
```env
AZURE_SPEECH_KEY=your_key
AZURE_SPEECH_REGION=eastus
```

## Common Patterns

### Save Generated Image
```python
image_bytes = await image.generate_image(request)

# Save to file
import uuid
filename = f"{uuid.uuid4()}.png"
filepath = os.path.join(MEDIA_DIR, "generated_images", filename)
with open(filepath, "wb") as f:
    f.write(image_bytes)
```

### Save TTS Audio
```python
audio_bytes = await tts.synthesize_speech("Hello", "en", "female")

# Save to file
import uuid
filename = f"{uuid.uuid4()}.mp3"
filepath = os.path.join(MEDIA_DIR, "audio", filename)
with open(filepath, "wb") as f:
    f.write(audio_bytes)
```

### Process User Audio Upload
```python
from fastapi import UploadFile

async def process_voice_input(file: UploadFile):
    audio_data = await file.read()
    text = await stt.transcribe_audio(audio_data, "en", "wav")
    return {"transcription": text}
```

## Error Handling

```python
try:
    content = await ai.generate_content(request)
except ValueError as e:
    # API key not set or invalid configuration
    print(f"Configuration error: {e}")
except httpx.HTTPStatusError as e:
    # API returned error status
    print(f"API error: {e.response.status_code}")
except Exception as e:
    # Other errors
    print(f"Unexpected error: {e}")
```

## Testing Without API Keys

```python
# Mock provider for testing
class MockAIProvider(BaseAIProvider):
    async def generate_content(self, request):
        return {
            "story_segments": [
                {
                    "segment_number": 1,
                    "narrative": "Test narrative",
                    "facts": ["Fact 1", "Fact 2"],
                    "image_prompt": "Test prompt"
                }
            ],
            "topic_summary": "Test summary"
        }

    async def health_check(self):
        return True

    # Implement other methods...

# Use in tests
ai = MockAIProvider()
```
