# 🎓 FunLearn — Feynman AI for Every Student

<div align="center">

**🏆 Built for DigitalOcean Gradient™ AI Hackathon**

*Learn by Teaching. Powered by DigitalOcean Gradient™ AI.*

[![DigitalOcean](https://img.shields.io/badge/Powered%20by-DigitalOcean%20Gradient%20AI-0080FF?style=for-the-badge&logo=digitalocean&logoColor=white)](https://www.digitalocean.com/products/ai/)
[![Live Demo](https://img.shields.io/badge/Live%20Demo-165.22.218.159-00C853?style=for-the-badge&logo=googlechrome&logoColor=white)](http://165.22.218.159)
[![React](https://img.shields.io/badge/React-18.3-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://react.dev/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)](LICENSE)

</div>

---

## 🔗 Live Demo & Testing

| | |
|---|---|
| **Live App** | **http://165.22.218.159** |
| **API Docs** | **http://165.22.218.159:8000/docs** |
| **Username** | `DebK` |
| **Password** | `password123` |

> Deployed on a DigitalOcean Droplet (Ubuntu 22.04) with Nginx reverse proxy + FastAPI backend. Infrastructure provisioned via Terraform (see [`infra/`](infra/)).

---

## 🎯 The Problem & Solution

**1.5 million students fail board exams in India every year.** Not because they're not smart enough — because passive learning doesn't work. Reading textbooks, watching videos, memorizing answers — it's broken.

**FunLearn** flips the script. Instead of AI teaching students, **students teach the AI**. This activates the **Feynman Technique** at scale — the proven method where explaining a concept in your own words reveals what you truly understand and where your gaps are.

### Why This Matters (Potential Impact)

- **Target**: 250M+ students in India alone, 1.5B+ globally
- **Problem**: 93% of learning apps are passive (watch/read/memorize)
- **Solution**: Active learning through teaching — proven 2.5x more effective than passive methods
- **Languages**: 11 languages supported (English, Hindi, Bengali, Spanish, Portuguese, Mandarin, Japanese, Arabic, Russian, Punjabi, Vietnamese)
- **Accessibility**: Works on any device with a browser — no app install needed

---

## 🧠 How DigitalOcean Gradient™ AI Powers FunLearn

FunLearn is built entirely on **DigitalOcean's full-stack AI platform**. Here's exactly how we use it:

### 1. Gradient AI Inference API — The Brain

All AI interactions use **Meta Llama 3.3 70B Instruct** via DigitalOcean's Gradient AI inference endpoint:

```
Endpoint: https://inference.do-ai.run/v1
Model:    meta-llama/Meta-Llama-3.3-70B-Instruct
```

This powers:
- **Feynman Engine** (5-layer Socratic AI dialogue)
- **Story-Based Learning** (AI-generated educational stories)
- **Misconception Cascade Tracing** (5-phase diagnostic probing)
- **Content generation** (questions, evaluations, feedback)
- **AI illustration data** (structured visual cards)
- **Multi-language responses** (11 languages)

### 2. Gradient AI Agent — Ritty's Persona

We provision a **custom Gradient AI Agent** via Terraform that gives Ritty (the AI tutor character) a persistent persona with NCERT knowledge base context. This agent is created using the DigitalOcean GenAI Agent API.

```hcl
# From infra/gradient_ai.tf
resource "digitalocean_gen_ai_agent" "ritty_agent" {
  name        = "ritty-feynman-tutor"
  model       = { uuid = "..." }
  instruction = "You are Ritty, a curious 8-year-old..."
}
```

### 3. DigitalOcean Droplet — Hosting

The full application runs on a **DigitalOcean Droplet** provisioned via Terraform:
- Ubuntu 22.04 LTS
- Nginx (serves React frontend + reverse proxies to FastAPI)
- systemd service for the Python backend
- Persistent volume for data storage

### 4. DigitalOcean Volume — Data Persistence

A **5GB Block Storage Volume** attached to the Droplet stores all CSV data files and generated media (images, audio).

### 5. Provider Factory — Plug & Play Architecture

All AI/Image/Voice providers are abstracted behind a **Provider Factory** pattern. Switching providers requires only changing an environment variable:

```env
AI_PROVIDER=digitalocean    # ← Uses Gradient AI inference
IMAGE_PROVIDER=bria         # Bria.ai FIBO v2 for image generation
```

This design demonstrates deep integration with DigitalOcean while maintaining extensibility.

---

## ✨ Core Features

### Feature 1: The Feynman Engine (5 Progressive Layers)

> *"If you can't explain it simply, you don't understand it well enough."* — Richard Feynman

Students explain topics to **Ritty** — an AI-powered curious 8-year-old. The AI probes understanding through 5 progressive layers:

| Layer | Name | What Happens |
|-------|------|-------------|
| 1 | **Curious Child** 🧒 | Student explains concept in plain language. Ritty asks "why?" questions. |
| 2 | **Compression Challenge** 📝 | Student compresses explanation into fewer words. Reveals shallow understanding. |
| 3 | **Why Spiral** 🌀 | Recursive "but why?" questioning — drills to the foundation of knowledge. |
| 4 | **Analogy Bridge** 🌉 | Student creates analogies. AI generates images to visualize them. |
| 5 | **Lecture Hall** 🎓 | Student teaches a skeptical audience. Highest difficulty. |

Each layer response includes:
- AI text feedback with gap detection
- **AI-generated educational image** (via Bria.ai FIBO v2)
- Structured illustration cards
- Confusion/curiosity level tracking
- Knowledge gap logging

### Feature 2: Story-Based Learning 📖

1. Enter any concept (e.g., "Gravity", "Democracy")
2. AI generates a 150-250 word engaging story with relatable characters
3. Each story comes with an **AI-generated image**
4. Follow-up questions test understanding via Socratic dialogue
5. Every discussion response includes a new contextual image

### Feature 3: Misconception Cascade Tracing (MCT) 🔬

The most advanced diagnostic tool — a 5-phase Socratic dialogue that traces a misunderstanding back to its root:

```
Phase 1: Surface Capture    → Record the wrong answer
Phase 2: Diagnostic Probing → Probe prerequisite knowledge
Phase 3: Root Found         → Identify the broken knowledge link
Phase 4: Remediation        → Fix from root up to surface
Phase 5: Verification       → Confirm understanding is restored
```

Every MCT response includes an **AI-generated educational image** for visual reinforcement.

### Feature 4: AI Image Generation with Every Response 🎨

Every AI response across all features generates a contextual educational image using **Bria.ai FIBO v2**:
1. **Prompt → VLM Bridge** — Bria's hosted Gemini 2.5 Flash VLM converts prompts into structured JSON
2. **JSON → FIBO Model** — 8B-parameter DiT model generates high-fidelity images
3. **Fallback** — Google Imagen 4.0 serves as automatic fallback

### Feature 5: Multi-Language Support 🌍

11 languages with language compliance enforced at the prompt level — every AI request includes a critical instruction ensuring responses match the selected language.

### Feature 6: Immersive Visual Experience 🎪

- 7 ambient particle themes (snow, rain, sunny, sparkle, bubbles, neural, fireflies)
- Motion-based page transitions (fade, slide, scale)
- AI illustration cards with gradient rendering
- Deep blue/purple ambient backgrounds

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
│  Styling: Tailwind CSS   Animations: motion + tsparticles        │
└───────────────────────────┬──────────────────────────────────────┘
                            │ REST API (JSON)
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│                     BACKEND  (FastAPI + Python 3.11+)            │
│                                                                  │
│  Routers: auth · users · learning · quiz · features ·            │
│           feynman · sessions · story · admin                      │
│                                                                  │
│  Services: FeynmanAIService · StoryService · ContentGenerator ·  │
│            QuestionGenerator · AnswerEvaluator · ScoringService   │
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
                            │
                            ▼
┌──────────────────────────────────────────────────────────────────┐
│              DIGITALOCEAN INFRASTRUCTURE (Terraform)             │
│                                                                  │
│  Droplet: Ubuntu 22.04 + Nginx + systemd                        │
│  Volume:  5GB persistent block storage                           │
│  Agent:   Gradient AI Agent (Ritty persona)                      │
│  Firewall: HTTP/HTTPS/SSH                                        │
└──────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| AI Model | **DigitalOcean Gradient AI** | Llama 3.3 70B Instruct — all AI interactions |
| AI Agent | **DigitalOcean GenAI Agent** | Ritty's persistent persona |
| Hosting | **DigitalOcean Droplet** | Ubuntu 22.04 server |
| Storage | **DigitalOcean Volume** | 5GB block storage for data |
| IaC | **Terraform** | DigitalOcean provider for all infrastructure |
| Frontend | React 18 + TypeScript + Vite | Modern SPA |
| Styling | Tailwind CSS | Utility-first CSS |
| State | Zustand | Lightweight state management |
| Backend | FastAPI + Python 3.11+ | Async REST API |
| Data | pandas (CSV) | Lightweight data persistence |
| Auth | JWT + bcrypt | Secure authentication |
| Images | Bria.ai FIBO v2 | AI image generation |
| Image Fallback | Google Imagen 4.0 | Automatic failover |

---

## 🚀 Quick Start (Local Development)

### Prerequisites

- Python 3.11+
- Node.js 18+
- DigitalOcean Gradient API Key ([get one here](https://cloud.digitalocean.com/))

### Backend

```bash
cd genlearn-ai/backend
python -m venv venv
source venv/bin/activate          # macOS/Linux
# venv\Scripts\activate           # Windows
pip install -r requirements.txt
cp .env.example .env              # Edit .env — add GRADIENT_API_KEY
python run.py
```

Backend: **http://localhost:8000** | API docs: **http://localhost:8000/docs**

### Frontend

```bash
cd genlearn-ai/frontend
npm install
npm run dev
```

Frontend: **http://localhost:5173**

---

## 🏗️ Project Structure

```
R_U_Serious/
├── LICENSE                          # MIT License (OSI-approved)
├── README.md                        # ← You are here
│
├── genlearn-ai/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── main.py             # FastAPI app entry point
│   │   │   ├── config.py           # Environment config
│   │   │   ├── api/routes/         # All REST endpoints
│   │   │   ├── services/           # Business logic + AI providers
│   │   │   ├── models/             # Pydantic models
│   │   │   ├── database/           # CSV handler + file I/O
│   │   │   └── utils/              # Helpers, validators, rate limiter
│   │   ├── data/csv/               # CSV database files
│   │   └── requirements.txt
│   │
│   └── frontend/
│       └── src/
│           ├── pages/              # React page components
│           ├── components/         # Reusable UI components
│           ├── services/api.ts     # API client
│           ├── store/              # Zustand state
│           └── contexts/           # Language context
│
└── infra/                           # Terraform IaC
    ├── main.tf                      # Provider config
    ├── droplet.tf                   # DO Droplet
    ├── volume.tf                    # DO Volume
    ├── gradient_ai.tf               # DO Gradient AI Agent
    ├── variables.tf                 # Variable definitions
    └── outputs.tf                   # Terraform outputs
```

---

## 🔑 Environment Variables

```env
# ── DigitalOcean Gradient AI (REQUIRED) ───────────────────────
AI_PROVIDER=digitalocean
GRADIENT_API_KEY=your_gradient_api_key_here
GRADIENT_BASE_URL=https://inference.do-ai.run/v1
GRADIENT_MODEL=meta-llama/Meta-Llama-3.3-70B-Instruct

# ── Image Generation ──────────────────────────────────────────
IMAGE_PROVIDER=bria
BRIA_API_KEY=your_bria_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here    # Fallback

# ── Application ───────────────────────────────────────────────
SECRET_KEY=your_secret_key_here
BACKEND_PORT=8000
```

---

## 📡 API Endpoints

| Method | Endpoint | Feature |
|--------|----------|---------|
| POST | `/api/auth/login` | Authentication |
| POST | `/api/feynman/session/start` | Start Feynman session |
| POST | `/api/feynman/teach` | Layer 1: Teach Ritty |
| POST | `/api/feynman/compress` | Layer 2: Compression |
| POST | `/api/feynman/why-spiral` | Layer 3: Why Spiral |
| POST | `/api/feynman/analogy` | Layer 4: Analogy Bridge |
| POST | `/api/feynman/lecture-hall` | Layer 5: Lecture Hall |
| GET | `/api/feynman/session/{id}/summary` | Session summary |
| POST | `/api/story/generate` | Generate learning story |
| POST | `/api/story/discuss` | Socratic discussion |
| POST | `/api/features/mct/start` | Start MCT session |
| POST | `/api/features/mct/chat` | MCT conversation |
| GET | `/api/features/mct/sessions/user/{id}` | MCT history |

Full interactive docs: **http://165.22.218.159:8000/docs**

---

## 🏆 Hackathon Prize Category Fit

| Prize | Why FunLearn Qualifies |
|-------|----------------------|
| **1st/2nd/3rd Place** | Full-stack app using Gradient AI for all AI interactions, deployed on DO infrastructure |
| **Best AI Agent Persona** | **Ritty** — a curious 8-year-old with distinct personality, emoji reactions, confusion levels, and 5 engagement modes. Provisioned via DO GenAI Agent API. |
| **The Great Whale Prize** | Targets 1.5B+ students globally with 11-language support. Transforms passive learning into active teaching at scale. |
| **Best Program for the People** | MIT-licensed, open source. Education technology accessible to any student with a browser. No app install required. |

---

<div align="center">

**Made for DigitalOcean Gradient™ AI Hackathon**

*FunLearn — Where understanding happens by teaching, not by being taught.*

*Powered by DigitalOcean Gradient™ AI — Feynman Technique for Every Student*

</div>
