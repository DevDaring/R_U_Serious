# 🎓 FunLearn — Feynman AI for Every Student

<div align="center">

**🏆 Built for DigitalOcean Gradient™ AI Hackathon**

*Learn by Teaching. Powered by DigitalOcean Gradient™ AI.*

[![DigitalOcean](https://img.shields.io/badge/Powered%20by-DigitalOcean%20Gradient%20AI-0080FF?style=for-the-badge&logo=digitalocean&logoColor=white)](https://www.digitalocean.com/products/ai/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

</div>

---

## Table of Contents

1. [The Problem & Solution](#-the-problem--solution)
2. [Quick Start](#-quick-start)
3. [Core Feature: The Feynman Engine](#-core-feature-the-feynman-engine)
4. [Story-Based Learning](#-story-based-learning)
5. [Misconception Cascade Tracing](#-misconception-cascade-tracing)
6. [Multi-Language Support](#-multi-language-support)
7. [Technical Architecture](#-technical-architecture)
8. [Project Structure](#-project-structure)
9. [Environment Variables](#-environment-variables)
10. [Deployment](#-deployment)

---

## 🎯 The Problem & Solution

**1.5 million students fail board exams in India every year.** Not because they're not smart enough — because passive learning doesn't work. Reading textbooks, watching videos, memorizing answers — it's broken.

**FunLearn** flips the script. Instead of AI teaching students, **students teach the AI**. This activates the Feynman Technique at scale, powered by DigitalOcean's Gradient™ AI.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- DigitalOcean Gradient API Key

### Backend

```powershell
cd genlearn-ai/backend

# Create and activate virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env — add GRADIENT_API_KEY at minimum

# Start the server
python run.py
```

Backend runs at **http://localhost:8000**
Interactive API docs at **http://localhost:8000/docs**

### Frontend

```powershell
cd genlearn-ai/frontend

npm install
npm run dev
```

Frontend runs at **http://localhost:5173**

### Default Login

| Username | Password     |
|----------|--------------|
| `DebK`   | `password123`|

---

## ✨ Core Feature: The Feynman Engine

> *"If you can't explain it simply, you don't understand it well enough."* — Richard Feynman

The Feynman Engine is the heart of FunLearn. Students explain topics to **Ritty** — an AI-powered curious 8-year-old — progressing through 5 progressive layers of depth.

### Starting a Session

- Choose any topic (e.g., "Photosynthesis", "Newton's Laws", "The Cold War")
- Set a subject, difficulty level (1–10), and starting layer
- Sessions are persisted to CSV and can be resumed

### Layer 1 — Curious Child (Teach Ritty) 🧒

The student explains the concept in plain language. Ritty responds with:

| Response Field | Description |
|----------------|-------------|
| `response` | Ritty's reaction to the explanation |
| `confusion_level` (0–10) | How confused Ritty is — reveals gaps |
| `curiosity_level` (0–10) | Engagement level |
| `follow_up_question` | Probing "why?" or "what?" question |
| `gap_detected` | Knowledge gap Ritty spotted |
| `emoji_reaction` | Expressive emoji feedback |
| `avatar_state` | Ritty's visual state (`thinking`, `confused`, `excited`, etc.) |
| `layer_complete` | True when the explanation satisfies Ritty |

**API endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/feynman/session/start` | Start a session |
| GET | `/api/feynman/session/{id}` | Get session state |
| POST | `/api/feynman/teach` | Message Ritty (Layer 1) |
| POST | `/api/feynman/teach-with-image` | Teach using image |
| POST | `/api/feynman/compress` | Compression submit (Layer 2) |
| POST | `/api/feynman/why-spiral` | Why Spiral response (Layer 3) |
| POST | `/api/feynman/analogy` | Analogy submit (Layer 4) |
| POST | `/api/feynman/lecture-hall` | Lecture Hall (Layer 5) |
| POST | `/api/feynman/session/{id}/change-layer` | Jump to a layer |
| GET | `/api/feynman/session/{id}/summary` | Session summary + gaps |
| GET | `/api/feynman/gaps/{user_id}` | All detected gaps |

---

## 📖 Story-Based Learning

Our newest feature replaces "Time Travel Interview" with a more focused learning approach.

**How it works:**
1. Enter any concept (e.g., "Gravity", "Democracy", "Photosynthesis")
2. AI generates a 150-250 word engaging story with relatable characters
3. A follow-up question checks understanding
4. Socratic dialogue continues to deepen knowledge

**API endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/story/generate` | Concept → story with follow-up |
| POST | `/api/story/discuss` | Continue Socratic discussion |
| POST | `/api/story/quiz` | Generate quiz from story |

---

## 🔬 Misconception Cascade Tracing (MCT)

The most advanced diagnostic tool. MCT runs a **5-phase Socratic dialogue** to find the *root* of a misunderstanding:

```
Phase 1: Surface Capture    → Record the wrong answer
Phase 2: Diagnostic Probing → Probe prerequisite knowledge
Phase 3: Root Found         → Identify the broken knowledge link
Phase 4: Remediation        → Fix from root up to surface
Phase 5: Verification       → Confirm understanding is restored
```

**API endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/features/mct/start` | Begin MCT session |
| POST | `/api/features/mct/chat` | Continue diagnostic conversation |
| GET | `/api/features/mct/sessions/user/{id}` | User's MCT history |
| GET | `/api/features/mct/conversation/{id}` | MCT chat log |

---

## 🌍 Multi-Language Support

FunLearn supports **11 languages** across all AI features:

| Code | Language | Script |
|------|----------|--------|
| `en` | English | English |
| `hi` | Hindi | हिन्दी |
| `bn` | Bengali | বাংলা |
| `es` | Spanish | Español |
| `pt` | Portuguese | Português |
| `zh` | Mandarin Chinese | 中文 |
| `ja` | Japanese | 日本語 |
| `ar` | Arabic | العربية |
| `ru` | Russian | Русский |
| `pa` | Punjabi | ਪੰਜਾਬੀ |
| `vi` | Vietnamese | Tiếng Việt |

Language compliance is enforced at the **prompt level** — a critical instruction is injected into every AI request ensuring responses are in the selected language.

---

## 🛠️ Technical Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     FRONTEND  (React 18 + TypeScript + Vite)     │
│                                                                  │
│  Pages: Dashboard · Feynman · MCT · Story Learning ·            │
│         History · Profile · Settings                             │
│                                                                  │
│  State: Zustand   Routing: React Router v6   HTTP: Axios         │
│  Styling: Tailwind CSS                                            │
└───────────────────────────┬──────────────────────────────────────┘
                            │ REST API (JSON)
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                     BACKEND  (FastAPI + Python 3.11+)            │
│                                                                  │
│  Routers: auth · users · learning · quiz · features ·            │
│           feynman · sessions · story · admin                      │
│                                                                  │
│  Services: ContentGenerator · QuestionGenerator ·               │
│            AnswerEvaluator · FeynmanAIService ·                 │
│            StoryService · ScoringService                         │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           PROVIDER FACTORY  (Plug & Play)                │   │
│  │                                                          │   │
│  │  AI:     DigitalOcean Gradient ✓ · OpenAI · Anthropic   │   │
│  │  Image:  None (disabled for hackathon)                   │   │
│  │  Voice:  None (disabled for hackathon)                   │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Data: CSV files (pandas)   Auth: JWT + bcrypt                   │
└──────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Version |
|-------|-----------|---------|
| Frontend framework | React | 18.3 |
| Frontend language | TypeScript | 5.2 |
| Frontend build | Vite | 5.x |
| Styling | Tailwind CSS | 3.x |
| State management | Zustand | 4.4 |
| Routing | React Router | 6.20 |
| HTTP client | Axios | 1.6 |
| Backend framework | FastAPI | 0.109 |
| Backend language | Python | 3.11+ |
| Data validation | Pydantic v2 | 2.5 |
| ASGI server | Uvicorn | 0.27 |
| Data storage | pandas (CSV) | 2.2 |
| Authentication | JWT + bcrypt | — |
| AI model | DigitalOcean Gradient | Llama 3.3 70B |

---

## 🏗️ Project Structure

```
genlearn-ai/
│
├── backend/
│   ├── run.py                      # Dev server runner
│   ├── requirements.txt
│   ├── .env                        # Copy from .env.example
│   │
│   └── app/
│       ├── main.py                 # FastAPI app, CORS, router registration
│       ├── config.py               # pydantic-settings config from env vars
│       │
│       ├── api/
│       │   ├── dependencies.py     # JWT auth, API key verification
│       │   └── routes/
│       │       ├── auth.py         # Login
│       │       ├── users.py        # User CRUD
│       │       ├── learning.py     # Learning session management
│       │       ├── quiz.py         # MCQ + descriptive
│       │       ├── features.py     # MCT + other features
│       │       ├── feynman.py      # Feynman Engine (5 layers)
│       │       ├── story_learning.py # Story Learning
│       │       ├── sessions.py     # Session history
│       │       └── admin.py        # Admin panel
│       │
│       ├── services/
│       │   ├── provider_factory.py  # Single config point for all providers
│       │   ├── feynman_service.py   # Feynman Engine AI logic
│       │   ├── story_service.py     # Story Learning AI logic
│       │   ├── content_generator.py
│       │   ├── question_generator.py
│       │   ├── answer_evaluator.py
│       │   ├── scoring_service.py
│       │   └── ai_providers/        # digitalocean · gemini · openai · anthropic
│       │
│       ├── models/                  # Pydantic models
│       │   ├── user.py
│       │   ├── session.py
│       │   ├── quiz.py
│       │   └── feynman_models.py    # Feynman layer models + enums
│       │
│       ├── database/
│       │   ├── csv_handler.py       # Generic CRUD on CSV files
│       │   ├── feynman_db.py        # Feynman session/conversation persistence
│       │   └── file_handler.py      # Media file I/O
│       │
│       └── utils/
│           ├── languages.py         # 11-language constants + prompt injection
│           ├── rate_limiter.py      # Rate limiting
│           └── error_handler.py
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   │
│   └── src/
│       ├── App.tsx                  # Routes + layout
│       ├── pages/
│       │   ├── DashboardPage.tsx
│       │   ├── LearningPage.tsx
│       │   ├── FeynmanEnginePage.tsx
│       │   ├── StoryLearningPage.tsx
│       │   ├── MistakeAutopsyPage.tsx
│       │   └── ...
│       │
│       ├── services/
│       │   └── api.ts               # Axios instance + all API functions
│       ├── contexts/
│       │   └── LanguageContext.tsx   # Global language selector
│       ├── store/
│       │   └── authStore.ts          # Zustand auth state
│       └── types/
│           └── index.ts              # All TypeScript interfaces
│
└── data/
    ├── csv/                          # All CSV database files
    └── media/                        # Generated images, audio
```

---

## 🔑 Environment Variables

Full `backend/.env` reference:

```env
# ── Application ───────────────────────────────────────────────
APP_NAME=FunLearn
APP_ENV=development
DEBUG=true
SECRET_KEY=your_secret_key_here

# ── Server ────────────────────────────────────────────────────
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
FRONTEND_URL=http://localhost:5173

# ── Provider Selection ────────────────────────────────────────
AI_PROVIDER=digitalocean
IMAGE_PROVIDER=none
VOICE_TTS_PROVIDER=none
VOICE_STT_PROVIDER=none

# ── DigitalOcean Gradient AI ──────────────────────────────────
GRADIENT_API_KEY=your_gradient_api_key_here
GRADIENT_BASE_URL=https://inference.do-ai.run/v1
GRADIENT_MODEL=meta-llama/Meta-Llama-3.3-70B-Instruct
RITTY_AGENT_UUID=your_ritty_agent_uuid_from_terraform

# ── Data Storage ───────────────────────────────────────────────
DATA_DIR=./data
CSV_DIR=./data/csv
MEDIA_DIR=./data/media

# ── Security ──────────────────────────────────────────────────
APP_API_KEY=kd_dreaming007
JWT_EXPIRATION_HOURS=24
```

---

## 🚀 Deployment

### Terraform Infrastructure

We provide Terraform configurations for deploying to DigitalOcean:

```bash
cd infra/

# Fill in terraform.tfvars with your credentials
terraform init
terraform plan
terraform apply
```

Resources created:
- **Droplet**: Ubuntu 22.04 with FastAPI + Nginx
- **Volume**: 5GB persistent storage for CSV data
- **Gradient AI Agent**: Ritty persona with NCERT knowledge base
- **Firewall**: Configured for HTTP/HTTPS/SSH access

See `infra/` directory for complete infrastructure setup.

---

<div align="center">

**Made for DigitalOcean Gradient™ AI Hackathon**

*FunLearn — Where understanding happens by teaching, not by being taught.*

*Powered by DigitalOcean Gradient™ AI — Feynman Technique for Every Student*

</div>
