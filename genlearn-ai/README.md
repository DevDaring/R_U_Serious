# 🎓 R U Serious? — FunLearn: AI-Powered Adaptive Learning Platform

<div align="center">

**🏆 Built for the [DigitalOcean GenAI Hackathon](https://digitalocean.devpost.com/)**

*Learn by Teaching. Powered by DigitalOcean Gradient™ AI.*

[![DigitalOcean](https://img.shields.io/badge/Powered%20by-DigitalOcean%20Gradient%20AI-0080FF?style=for-the-badge&logo=digitalocean&logoColor=white)](https://www.digitalocean.com/products/ai/)
[![React](https://img.shields.io/badge/React-18.3-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)

**[Live Demo](http://165.22.218.159)** · **Login:** `DebK` / `password123`

</div>

---

## Table of Contents

1. [The Problem & Solution](#-the-problem--solution)
2. [Hackathon Qualification](#-hackathon-qualification--digitalocean-services-used)
3. [Key Features](#-key-features)
4. [Quick Start](#-quick-start)
5. [Core Feature: The Feynman Engine](#-core-feature-the-feynman-engine)
6. [Story-Based Learning](#-story-based-learning)
7. [Misconception Cascade Tracing](#-misconception-cascade-tracing)
8. [Multi-Language Support](#-multi-language-support)
9. [Technical Architecture](#-technical-architecture)
10. [Project Structure](#-project-structure)
11. [Environment Variables](#-environment-variables)
12. [Deployment](#-deployment)

---

## 🎯 The Problem & Solution

**1.5 million students fail board exams in India every year.** Not because they're not smart enough — because passive learning doesn't work. Reading textbooks, watching videos, memorizing answers — it's broken.

**FunLearn** flips the script. Instead of AI teaching students, **students teach the AI**. This activates the Feynman Technique at scale, powered by DigitalOcean's Gradient™ AI.

---

## 🏆 Hackathon Qualification — DigitalOcean Services Used

FunLearn is purpose-built for the **DigitalOcean GenAI Hackathon** and deeply leverages **5 DigitalOcean services** across compute, storage, and the full Gradient™ AI stack.

### 1. Gradient™ AI Agent Builder — *Ritty, the Feynman Agent*

FunLearn deploys **Ritty** as a fully managed DigitalOcean Gradient™ AI Agent with a defined persona (curious 8-year-old), system instructions, and safe Guardrails to ensure age-appropriate, non-toxic responses. Ritty is not a raw LLM prompt — she is a named, versioned agent deployed on the Gradient platform with persistent configuration, provisioned via Terraform.

### 2. Gradient™ AI Knowledge Base (RAG)

A **Gradient™ Knowledge Base** is attached to Ritty's agent, ingesting NCERT and CBSE curriculum content via the web crawler data source. This grounds every Feynman Engine and Story Learning session in actual Indian curriculum — not generic world knowledge — making AI responses educationally accurate and curriculum-aligned.

### 3. Gradient™ Serverless LLM Inference

All AI features — Story Learning, Misconception Cascade Tracing, and Feynman Engine scoring — call the **DigitalOcean Gradient Serverless Inference API** using the `meta-llama/Meta-Llama-3.3-70B-Instruct` model via the OpenAI-compatible endpoint at `https://inference.do-ai.run/v1`. This is a pay-per-token, zero-infrastructure managed inference layer. The same inference API also powers the **IllustrationService** for AI-generated educational illustration cards.

### 4. DigitalOcean Droplet (Compute)

The entire application — FastAPI backend + React frontend served via Nginx — is hosted on a **Ubuntu 22.04 Droplet** (`s-2vcpu-4gb`). The app runs as a `systemd` service for auto-restart on failure, with a firewall allowing only ports 22, 80, and 443.

### 5. DigitalOcean Volume (Persistent Storage)

A **5GB Block Storage Volume** is attached to the Droplet and mounted at `/mnt/funlearn-data/csv`. All user data — accounts, learning sessions, Feynman conversations, MCT diagnostic history, and XP/streak records — is persisted on this volume, surviving Droplet reboots and redeployments.

### How We Meet Judging Criteria

| Criterion | How FunLearn Addresses It |
|---|---|
| **Thoroughly leverage the required tool** | 3 distinct Gradient™ AI services: Agent Builder, Knowledge Base, Serverless Inference |
| **Quality software development** | Provider Factory pattern for clean DO integration; full Terraform IaC for all infrastructure |
| **Potential Impact** | Targets 1.5M Indian students who fail board exams yearly; 11 languages including Hindi and Bengali |
| **Creative & unique idea** | Feynman Engine (teach the AI to learn), Story-Based Learning, MCT root-cause diagnosis — novel pedagogy approaches |
| **Design** | React + Tailwind UI with multilingual support, AI-generated illustration cards, ambient particle effects (7 themes), motion-based transitions |

### Prize Categories Targeted

- **Best Program for the People** — Grassroots education impact across India
- **Best AI Agent Persona** — Ritty is a fully deployed, character-rich Gradient AI Agent with Guardrails
- **The Great Whale Prize** — Deep platform usage across 5 DigitalOcean services

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Feynman Engine** | 5-layer progressive teaching system — students teach the AI to learn |
| **Story-Based Learning** | AI generates engaging stories around any concept with follow-up Socratic dialogue |
| **Misconception Cascade Tracing (MCT)** | 5-phase diagnostic that finds the root cause of misunderstandings |
| **AI-Generated Images** | Every AI response includes a contextual educational image (Bria FIBO v2 + Imagen 4.0 fallback) |
| **AI Illustration Cards** | Structured visual cards with title, visual type, key elements, and insights |
| **11-Language Support** | English, Hindi, Bengali, Spanish, Portuguese, Chinese, Japanese, Arabic, Russian, Punjabi, Vietnamese |
| **Custom Avatars** | Draw, upload, or pick from gallery to personalize the learning experience |
| **Story Characters** | Create and add custom characters to appear in AI-generated stories |
| **Ambient Visual Effects** | 7 particle themes (snow, rain, sparkle, bubbles, neural, fireflies, sunny) |
| **Gamification** | XP, streaks, leveling system, and score tracking |
| **Admin Panel** | Manage users, upload questions via CSV, and configure the platform |
| **Terraform IaC** | Full infrastructure-as-code for one-command deployment to DigitalOcean |

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
| `illustration` | AI-generated educational illustration card (see below) |
| `image_url` | AI-generated educational image (base64 data URL) |

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

### AI-Generated Educational Illustrations

Every learning interaction generates **visual illustration cards** alongside text responses. The system uses the AI provider to create structured illustration data — not bitmap images — rendered as beautiful gradient cards with:

- **Title & emoji icon** — Quick visual anchor for the concept
- **Visual type badge** — `diagram`, `process`, `comparison`, `concept`, `timeline`, or `formula`
- **Element list** — Key components with contextual icons
- **Key insight** — One-line takeaway

**Adaptive frequency**: The first 5 turns always include an illustration. After that, illustrations appear every 2 turns — keeping engagement high without overwhelming.

This approach works without any external image API, using zero additional infrastructure.

### AI-Generated Images (Bria.ai FIBO v2)

FunLearn generates **real AI images with every AI response** across all learning features using the **Bria.ai FIBO v2** pipeline:

1. **Prompt → VLM Bridge** — Bria's hosted Gemini 2.5 Flash VLM converts text prompts into structured JSON (~1000 words of scene description)
2. **JSON → FIBO Model** — The 8B-parameter FIBO DiT model generates deterministic, high-fidelity images from the structured JSON
3. **Fallback** — If Bria is unavailable, **Google Imagen 4.0** serves as an automatic fallback

**Every AI response includes a contextual educational image** — whether it's a Feynman Engine interaction (all 5 layers), a Story Learning session, or an MCT diagnostic conversation. This ensures students always receive both textual and visual reinforcement of concepts.

Set `IMAGE_PROVIDER=bria` (or `gemini`, `pollinations`) in `.env` to enable.

---

## 🎨 Visual Effects & Animations

FunLearn uses ambient particle effects and page transitions to create an immersive learning environment:

### Ambient Particles (7 themes)

| Theme | Effect | Used On |
|-------|--------|---------|
| `snow` | Gentle falling snowflakes | — |
| `rain` | Blue streaking raindrops | — |
| `sunny` | Warm golden floating orbs | Main content background |
| `sparkle` | Purple/pink twinkling stars | Home page hero |
| `bubbles` | Rising cyan bubbles | — |
| `neural` | Connected network nodes | — |
| `fireflies` | Pulsing multicolor dots | Login page |

### Page Transitions

All pages use motion-based animations:
- **PageTransition** — Fade + slide-up on route change
- **FadeIn** — Staggered opacity reveal (configurable delay)
- **ScaleIn** — Scale-up entrance for cards and stats
- **FloatingElement** — Gentle infinite bounce for mascot images
- **PulseGlow** — Subtle scale pulse for active elements

### CSS Gradient Animations

Background gradient shifts, shimmer effects, and floating keyframes add life to the UI — all GPU-accelerated and lightweight.

---

## 📖 Story-Based Learning

Our newest feature replaces "Time Travel Interview" with a more focused learning approach.

**How it works:**
1. Enter any concept (e.g., "Gravity", "Democracy", "Photosynthesis")
2. AI generates a 150-250 word engaging story with relatable characters
3. An AI-generated educational image accompanies each story and discussion response
4. A follow-up question checks understanding
5. Socratic dialogue continues to deepen knowledge, each response paired with a new image

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
│  Effects: AmbientParticles (tsparticles) ·                       │
│           PageTransition / FadeIn / ScaleIn (motion) ·           │
│           AIIllustration cards · CSS gradient animations          │
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
│            StoryService · IllustrationService ·                  │
│            ScoringService                                        │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           PROVIDER FACTORY  (Plug & Play)                │   │
│  │                                                          │   │
│  │  AI:     DigitalOcean Gradient ✓ · OpenAI · Anthropic   │   │
│  │  Image:  Bria.ai FIBO v2 ✓ · Gemini Imagen 4.0 ✓ ·     │   │
│  │          Pollinations · Stability · None                 │   │
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
| Animations | motion (framer-motion) | 12.x |
| Particles | @tsparticles/react + slim | 3.x |
| Backend framework | FastAPI | 0.109 |
| Backend language | Python | 3.11+ |
| Data validation | Pydantic v2 | 2.5 |
| ASGI server | Uvicorn | 0.27 |
| Data storage | pandas (CSV) | 2.2 |
| Authentication | JWT + bcrypt | — |
| AI model | DigitalOcean Gradient | Llama 3.3 70B |
| Image generation | Bria.ai FIBO v2 | JSON-native DiT |
| Image fallback | Google Imagen 4.0 | via Generative Language API |

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
│       │   ├── illustration_service.py # AI-generated visual illustration cards
│       │   ├── content_generator.py
│       │   ├── question_generator.py
│       │   ├── answer_evaluator.py
│       │   ├── scoring_service.py
│       │   ├── ai_providers/        # digitalocean · openai · anthropic
│       │   └── image_providers/     # bria · gemini · pollinations · fibo · stability · none
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
│       ├── components/
│       │   ├── common/
│       │   │   └── AIIllustration.tsx # Educational illustration cards
│       │   ├── effects/
│       │   │   ├── AmbientParticles.tsx # 7-theme particle backgrounds
│       │   │   └── PageTransition.tsx   # Motion-based animation wrappers
│       │   ├── auth/
│       │   │   └── LoginForm.tsx
│       │   └── layout/
│       │       └── MainContent.tsx
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
IMAGE_PROVIDER=bria          # bria, gemini, pollinations, fibo, stability, none
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

# ── Image Generation ──────────────────────────────────────────
BRIA_API_KEY=your_bria_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here

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

**Built for the [DigitalOcean GenAI Hackathon](https://digitalocean.devpost.com/)**

*FunLearn — Where understanding happens by teaching, not by being taught.*

*Powered by DigitalOcean Gradient™ AI · Llama 3.3 70B Instruct · Bria FIBO v2*

</div>
