# Project_Changes.md
# Code Changes Required for FunLearn — DigitalOcean Hackathon Version

## OBJECTIVE
You are an AI coding assistant. The existing project was built for Google Gemini Hackathon.
Your task is to modify it for the DigitalOcean Gradient™ AI Hackathon.
The app must ONLY use DigitalOcean services — no Google/GCP dependencies.
Focus: Feynman Technique + Story-Based Learning. Remove all other features.

---

## STEP 0: READ THIS FIRST

### Features to KEEP (Rename/Redesign as needed)
1. **Feynman Engine** — "Teach Ritty" (all 5 layers) — THIS IS THE HERO FEATURE
2. **Story-Based Learning** — NEW feature replacing "Time Travel Interview" (see details below)
3. **Misconception Cascade Tracing (MCT)** — Keep, it reinforces Feynman learning
4. **Multi-language support** — Keep all 9 languages (critical for "people" prize)
5. **Basic Gamification** — Keep only XP + Daily Streaks (remove tournaments)

### Features to DELETE ENTIRELY
- Debate Arena
- YouTube to Course
- Concept Collision
- Dream Project Path
- Avatar Creator & Custom Characters
- Tournaments & Leaderboards & Teams
- Image generation (Imagen 3 / any image AI)
- "Learn from Anything" (image upload feature)
- Reverse Classroom (redundant with Feynman Engine)

### Core AI Provider Change
- DELETE: All Gemini API calls (`google.generativeai`, Gemini SDK)
- DELETE: All GCP TTS/STT calls
- DELETE: Imagen 3 calls
- ADD: DigitalOcean Gradient Serverless LLM API (OpenAI-compatible)
- ADD: DigitalOcean Gradient AI Agent for Ritty (via Agent UUID)

---

## STEP 1: CLEAN UP BRANDING

### 1.1 README.md — Rewrite completely
- Remove all mentions of: Google, Gemini, GCP, Google Cloud, Imagen, Google Gemini 3 Hackathon
- New title: "FunLearn — Feynman AI for Every Student"
- New tagline: "Learn by Teaching. Powered by DigitalOcean Gradient™ AI."
- Add badge: DigitalOcean Gradient AI
- Remove the Demo Script section
- Add new Demo Script focused only on Feynman Engine and Story Learning

### 1.2 Frontend — Remove Google badges from UI
- Find all files containing "Gemini", "Google", "GCP", "Powered by Google"
- Replace with "Powered by DigitalOcean Gradient™ AI"
- Update favicon if it has Google branding

---

## STEP 2: BACKEND — REPLACE AI PROVIDER

### 2.1 Create new file: backend/app/services/providers/digitalocean_provider.py

```python
import httpx
import os
from typing import AsyncGenerator

GRADIENT_BASE_URL = os.getenv("GRADIENT_BASE_URL", "https://inference.do-ai.run/v1")
GRADIENT_API_KEY = os.getenv("GRADIENT_API_KEY", "")
GRADIENT_MODEL = os.getenv("GRADIENT_MODEL", "meta-llama/Meta-Llama-3.3-70B-Instruct")
RITTY_AGENT_UUID = os.getenv("RITTY_AGENT_UUID", "")


async def chat_completion(messages: list[dict], stream: bool = False) -> str:
    """Call DO Gradient Serverless LLM — OpenAI-compatible endpoint."""
    headers = {
        "Authorization": f"Bearer {GRADIENT_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": GRADIENT_MODEL,
        "messages": messages,
        "stream": stream,
        "max_tokens": 1024,
        "temperature": 0.7
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"{GRADIENT_BASE_URL}/chat/completions",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        return data["choices"][0]["message"]["content"]


async def ritty_agent_chat(user_message: str, conversation_history: list[dict]) -> str:
    """
    Call the Ritty Gradient AI Agent by UUID.
    Uses the DO Gradient Agent API — not the raw LLM endpoint.
    The agent has Ritty's persona and NCERT Knowledge Base pre-attached.
    """
    headers = {
        "Authorization": f"Bearer {GRADIENT_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "message": user_message,
        "conversation_history": conversation_history
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.post(
            f"https://api.digitalocean.com/v2/gen-ai/agents/{RITTY_AGENT_UUID}/chat",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        data = response.json()
        return data["message"]["content"]
```

### 2.2 Update backend/app/services/providers/__init__.py (Provider Factory)

```python
import os

AI_PROVIDER = os.getenv("AI_PROVIDER", "digitalocean")

def get_ai_provider():
    if AI_PROVIDER == "digitalocean":
        from .digitalocean_provider import chat_completion
        return chat_completion
    raise ValueError(f"Unsupported AI_PROVIDER: {AI_PROVIDER}")

def get_ritty_provider():
    """Always use DO Gradient Agent for Ritty."""
    from .digitalocean_provider import ritty_agent_chat
    return ritty_agent_chat
```

### 2.3 Update backend/app/services/feynman_service.py

- Find every call to `gemini_client.generate_content(...)` or `model.generate_content(...)`
- Replace with: `await chat_completion(messages=[{"role": "user", "content": prompt}])`
- For Ritty-specific calls: use `await ritty_agent_chat(user_message, history)` instead

### 2.4 Update backend/app/services/mct_service.py

- Same as 2.3: replace all Gemini SDK calls with `await chat_completion(...)`
- MCT diagnostic prompts remain unchanged — only the API call changes

### 2.5 Delete these files entirely
```
backend/app/services/providers/gemini_provider.py
backend/app/services/providers/imagen_provider.py
backend/app/services/providers/gcp_tts_provider.py
backend/app/services/providers/gcp_stt_provider.py
```
(Delete whichever of these exist in the project)

### 2.6 Update backend/requirements.txt
- REMOVE: `google-generativeai`, `google-cloud-texttospeech`, `google-cloud-speech`
- ADD: `httpx>=0.27.0` (likely already present)

---

## STEP 3: BACKEND — UPDATE ENVIRONMENT VARIABLES

### 3.1 Update backend/.env.example
Replace the entire file with:

```env
# DigitalOcean Gradient AI
AI_PROVIDER=digitalocean
GRADIENT_API_KEY=your_gradient_api_key_here
GRADIENT_BASE_URL=https://inference.do-ai.run/v1
GRADIENT_MODEL=meta-llama/Meta-Llama-3.3-70B-Instruct
RITTY_AGENT_UUID=your_ritty_agent_uuid_from_terraform_output

# Storage — CSV files on DO Volume
DATA_DIR=/mnt/funlearn-data/csv

# Disabled providers
IMAGE_PROVIDER=none
VOICE_TTS_PROVIDER=none
VOICE_STT_PROVIDER=none

# Auth
JWT_SECRET=replace_with_random_secret_string
```

### 3.2 Update backend/app/database/ CSV path handling
- Find where CSV file paths are defined (likely a config.py or constants.py)
- Change hardcoded paths like `./data/csv/` to read from env var `DATA_DIR`

```python
import os
DATA_DIR = os.getenv("DATA_DIR", "./data/csv")
USERS_CSV = os.path.join(DATA_DIR, "users.csv")
SESSIONS_CSV = os.path.join(DATA_DIR, "sessions.csv")
FEYNMAN_CSV = os.path.join(DATA_DIR, "feynman_sessions.csv")
MCT_CSV = os.path.join(DATA_DIR, "mct_sessions.csv")
```

---

## STEP 4: BACKEND — REMOVE DELETED FEATURE ROUTES

### 4.1 Delete these route files from backend/app/api/routes/
```
debate_arena.py       (or similar name)
youtube_course.py
concept_collision.py
dream_project.py
avatar.py
characters.py
tournament.py
team.py
leaderboard.py
image_upload.py       (Learn from Anything)
reverse_classroom.py  (redundant with feynman)
```

### 4.2 In backend/app/main.py or app/api/__init__.py
- Find all `app.include_router(...)` lines
- Remove routers for the deleted features above
- Keep only: feynman, mct, story_learning, auth, language

---

## STEP 5: ADD NEW FEATURE — STORY-BASED LEARNING

### 5.1 Create backend/app/services/story_service.py

```python
from app.services.providers import get_ai_provider

chat_completion = get_ai_provider()

STORY_SYSTEM_PROMPT = """
You are a master storyteller and educator.
Your job is to explain any concept the student provides through an engaging short story.
Rules:
- The story must be 150-250 words maximum
- The concept must be embedded naturally in the story plot
- Use relatable characters (school kids, village settings, everyday Indian life)
- End with one reflection question: "What did [character] learn?"
- Respond in the language the student selects
- Never use textbook language. Make it feel like a campfire story.
"""

async def generate_concept_story(concept: str, language: str = "English") -> dict:
    messages = [
        {"role": "system", "content": STORY_SYSTEM_PROMPT},
        {"role": "user", "content": f"Tell me a story that teaches: {concept}. Language: {language}"}
    ]
    story = await chat_completion(messages=messages)

    follow_up_messages = [
        {"role": "system", "content": "You are a Socratic teacher. Ask ONE probing question about the story to check if the student understood the concept. Be concise. Under 30 words."},
        {"role": "user", "content": f"The story was about: {concept}. Story: {story}"}
    ]
    follow_up = await chat_completion(messages=follow_up_messages)

    return {"story": story, "follow_up_question": follow_up, "concept": concept}


async def continue_story_discussion(concept: str, story: str, student_answer: str, language: str = "English") -> str:
    messages = [
        {"role": "system", "content": "You are a kind Socratic teacher. The student just answered a question about a story. Affirm what they got right, gently correct what they got wrong, and ask one more follow-up question to go deeper. Under 60 words. Respond in the student's language."},
        {"role": "user", "content": f"Concept: {concept}\nStory: {story}\nStudent Answer: {student_answer}\nLanguage: {language}"}
    ]
    return await chat_completion(messages=messages)
```

### 5.2 Create backend/app/api/routes/story_learning.py

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.story_service import generate_concept_story, continue_story_discussion

router = APIRouter(prefix="/api/story", tags=["story-learning"])

class StoryRequest(BaseModel):
    concept: str
    language: str = "English"

class StoryDiscussionRequest(BaseModel):
    concept: str
    story: str
    student_answer: str
    language: str = "English"

@router.post("/generate")
async def get_story(request: StoryRequest):
    try:
        return await generate_concept_story(request.concept, request.language)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/discuss")
async def discuss_story(request: StoryDiscussionRequest):
    try:
        response = await continue_story_discussion(
            request.concept, request.story, request.student_answer, request.language
        )
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 5.3 Register the new route in backend/app/main.py
Add this line alongside other router registrations:
```python
from app.api.routes.story_learning import router as story_router
app.include_router(story_router)
```

---

## STEP 6: FRONTEND — REMOVE DELETED FEATURE PAGES

### 6.1 Delete these page/component files from frontend/src/pages/ (or similar folder)
```
DebateArena.tsx
YouTubeCourse.tsx
ConceptCollision.tsx
DreamProject.tsx
AvatarCreator.tsx
CharacterBuilder.tsx
Tournaments.tsx
Leaderboard.tsx
Teams.tsx
ImageLearn.tsx         (Learn from Anything)
ReverseClassroom.tsx
TimeTravel.tsx         (replaced by Story Learning)
```

### 6.2 Update frontend navigation (sidebar/navbar)
- Find the navigation config file (likely in `src/components/Sidebar.tsx` or `src/App.tsx`)
- Remove all nav items for deleted features
- Keep nav items: Feynman Engine, Story Learning, MCT Diagnose, Profile

### 6.3 Update frontend/src/App.tsx routing
- Remove all `<Route>` entries for deleted pages
- Add new route: `<Route path="/story" element={<StoryLearning />} />`

---

## STEP 7: FRONTEND — ADD STORY LEARNING PAGE

### 7.1 Create frontend/src/pages/StoryLearning.tsx

```tsx
import React, { useState } from "react";
import { useLanguage } from "../contexts/LanguageContext";

const StoryLearning: React.FC = () => {
  const { language } = useLanguage();
  const [concept, setConcept] = useState("");
  const [story, setStory] = useState("");
  const [followUp, setFollowUp] = useState("");
  const [studentAnswer, setStudentAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(false);

  const generateStory = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/story/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ concept, language })
      });
      const data = await res.json();
      setStory(data.story);
      setFollowUp(data.follow_up_question);
      setFeedback("");
      setStudentAnswer("");
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const submitAnswer = async () => {
    setLoading(true);
    try {
      const res = await fetch("/api/story/discuss", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ concept, story, student_answer: studentAnswer, language })
      });
      const data = await res.json();
      setFeedback(data.response);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <h1 className="text-3xl font-bold mb-2">📖 Story Learning</h1>
      <p className="text-gray-500 mb-6">Any concept. One story. Deep understanding.</p>

      {!story && (
        <div>
          <input
            className="w-full border rounded-lg p-3 text-lg mb-4"
            placeholder="What concept should the story teach? (e.g. Photosynthesis)"
            value={concept}
            onChange={e => setConcept(e.target.value)}
          />
          <button
            onClick={generateStory}
            disabled={loading || !concept.trim()}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Crafting story..." : "Tell Me a Story"}
          </button>
        </div>
      )}

      {story && (
        <div className="space-y-6">
          <div className="bg-amber-50 border-l-4 border-amber-400 p-5 rounded-lg">
            <p className="text-gray-800 leading-relaxed whitespace-pre-wrap">{story}</p>
          </div>

          <div className="bg-blue-50 border border-blue-200 p-4 rounded-lg">
            <p className="font-semibold text-blue-800">🤔 {followUp}</p>
          </div>

          {!feedback && (
            <div>
              <textarea
                className="w-full border rounded-lg p-3 mb-3"
                rows={3}
                placeholder="Your answer..."
                value={studentAnswer}
                onChange={e => setStudentAnswer(e.target.value)}
              />
              <button
                onClick={submitAnswer}
                disabled={loading || !studentAnswer.trim()}
                className="bg-green-600 text-white px-6 py-2 rounded-lg font-semibold hover:bg-green-700 disabled:opacity-50"
              >
                {loading ? "Thinking..." : "Submit Answer"}
              </button>
            </div>
          )}

          {feedback && (
            <div className="bg-green-50 border border-green-200 p-4 rounded-lg">
              <p className="text-gray-800 whitespace-pre-wrap">{feedback}</p>
            </div>
          )}

          <button
            onClick={() => { setStory(""); setFollowUp(""); setFeedback(""); setConcept(""); }}
            className="text-gray-500 underline text-sm"
          >
            Try another concept
          </button>
        </div>
      )}
    </div>
  );
};

export default StoryLearning;
```

---

## STEP 8: SIMPLIFY GAMIFICATION

### 8.1 In frontend and backend, find all tournament/team/leaderboard references
- Remove all tournament-related UI components and API calls
- Remove all team creation/joining UI and API calls
- Keep: XP points display, daily streak counter, level badge on profile

### 8.2 Find the gamification service/utility in backend
- Remove: `calculate_tournament_score`, `update_team_rank`, `global_leaderboard` functions
- Keep: `add_xp(user_id, points)`, `update_streak(user_id)`, `get_user_level(xp)`

---

## STEP 9: FINAL VERIFICATION CHECKLIST

Before submitting, confirm ALL of these are true:

- [ ] `grep -r "gemini" backend/` returns zero results
- [ ] `grep -r "google" backend/` returns zero results (except in comments/docs)
- [ ] `grep -r "GCP" backend/` returns zero results
- [ ] `grep -r "imagen" backend/` returns zero results
- [ ] `pip list | grep google` shows nothing installed in requirements.txt
- [ ] App starts successfully with `AI_PROVIDER=digitalocean` in .env
- [ ] Feynman Engine (all 5 layers) works end-to-end via Ritty Agent
- [ ] Story Learning page is live and generates stories
- [ ] MCT diagnostic flow completes successfully
- [ ] Language switcher changes AI response language correctly
- [ ] No broken nav links to deleted features
- [ ] README has zero mentions of Google/Gemini

---

## HACKATHON SUBMISSION CHECKLIST

1. Push all code to a **public GitHub repo** with MIT License
2. Record a **3-minute demo video** — structure it as:
   - 0:00–0:20 → Problem: 1.5M Indian students fail board exams
   - 0:20–1:00 → Demo Feynman Engine: teach Ritty photosynthesis in Bengali
   - 1:00–1:40 → Demo Story Learning: "explain gravity through a story"
   - 1:40–2:10 → Demo MCT: enter a wrong answer, watch root cause diagnosis
   - 2:10–2:40 → Show DigitalOcean Gradient Agent + Knowledge Base in DO Console
   - 2:40–3:00 → Close: "Education for every student, in every language"
3. In Devpost description, explicitly list every DO feature used:
   - DigitalOcean Gradient™ Serverless LLM Inference
   - DigitalOcean Gradient™ AI Agent Builder (Ritty persona)
   - DigitalOcean Gradient™ Knowledge Base (NCERT RAG)
   - DigitalOcean Droplet (Ubuntu 22.04, s-2vcpu-4gb)
   - DigitalOcean Volume (5GB persistent storage)
