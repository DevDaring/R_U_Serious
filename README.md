# 🎓 FunLearn — AI-Powered Adaptive Learning Platform

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
4. [Core Feature: The Feynman Engine](#-core-feature-the-feynman-engine)
5. [Story-Based Learning](#-story-based-learning)
6. [Misconception Cascade Tracing](#-misconception-cascade-tracing)
7. [AI-Generated Images](#-ai-generated-images)
8. [Multi-Language Support](#-multi-language-support)
9. [Technical Architecture](#-technical-architecture)
10. [Quick Start](#-quick-start)
11. [Project Structure](#-project-structure)
12. [Deployment](#-deployment)

---

## 🎯 The Problem & Solution

**1.5 million students fail board exams in India every year.** Not because they're not smart enough — because passive learning doesn't work. Reading textbooks, watching videos, memorizing answers — it's broken.

**FunLearn** flips the script. Instead of AI teaching students, **students teach the AI**. This activates the Feynman Technique at scale, powered by DigitalOcean's Gradient™ AI.

> *"If you can't explain it simply, you don't understand it well enough."* — Richard Feynman

---

## 🏆 Hackathon Qualification — DigitalOcean Services Used

FunLearn is purpose-built for the **[DigitalOcean GenAI Hackathon](https://digitalocean.devpost.com/)** and deeply leverages **5 DigitalOcean services** across compute, storage, and the full Gradient™ AI stack.

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

### How We Meet the Judging Criteria

| Criterion | How FunLearn Addresses It |
|---|---|
| **Thoroughly leverage the required tool** | 3 distinct Gradient™ AI services: Agent Builder, Knowledge Base, Serverless Inference |
| **Quality software development** | Provider Factory pattern for clean DO integration; full Terraform IaC for all infrastructure |
| **Potential Impact** | Targets 1.5M Indian students who fail board exams yearly; 11 languages including Hindi and Bengali |
| **Creative & unique idea** | Feynman Engine (teach the AI to learn), Story-Based Learning, MCT root-cause diagnosis — novel pedagogy |
| **Design** | React + Tailwind UI with multilingual support, AI illustration cards, ambient particle effects, motion transitions |

### Prize Categories Targeted

| Prize | Why FunLearn Qualifies |
|-------|----------------------|
| **Best Program for the People** | Grassroots education impact — free adaptive learning for underserved Indian students across 11 languages |
| **Best AI Agent Persona** | Ritty is a fully deployed, character-rich Gradient AI Agent with Guardrails and a curriculum-grounded Knowledge Base |
| **The Great Whale Prize** | Deep platform usage across 5 DigitalOcean services including the full Gradient AI stack |

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| **Feynman Engine** | 5-layer progressive teaching system — students teach the AI to learn |
| **Story-Based Learning** | AI generates engaging stories around any concept with Socratic follow-up dialogue |
| **Misconception Cascade Tracing** | 5-phase diagnostic that traces misunderstandings to their root cause |
| **AI-Generated Images** | Every AI response includes a contextual educational image (Bria FIBO v2 + Imagen 4.0 fallback) |
| **AI Illustration Cards** | Structured visual cards with title, visual type, key elements, and insights |
| **11-Language Support** | English, Hindi, Bengali, Spanish, Portuguese, Chinese, Japanese, Arabic, Russian, Punjabi, Vietnamese |
| **Custom Avatars** | Draw, upload, or pick from gallery to personalize the experience |
| **Story Characters** | Create custom characters that appear in AI-generated learning stories |
| **Ambient Visual Effects** | 7 particle themes — snow, rain, sparkle, bubbles, neural, fireflies, sunny |
| **Gamification** | XP, streaks, leveling system, and score tracking |
| **Admin Panel** | Manage users, upload questions via CSV, and configure the platform |
| **Terraform IaC** | Full infrastructure-as-code for one-command deployment to DigitalOcean |

---

## 🧠 Core Feature: The Feynman Engine

The Feynman Engine is the heart of FunLearn. Students explain topics to **Ritty** — an AI-powered curious 8-year-old deployed as a DigitalOcean Gradient AI Agent — progressing through **5 layers of depth**:

| Layer | Name | What Happens |
|-------|------|-------------|
| **1** | Curious Child | Student explains the concept in plain language; Ritty asks probing "why?" questions |
| **2** | Compression Challenge | Student must compress the entire concept into a single sentence |
| **3** | Why Spiral | Ritty asks progressively deeper "why?" questions — 3 to 5 levels deep |
| **4** | Analogy Builder | Student creates a real-world analogy for the concept |
| **5** | Lecture Hall | Student delivers a complete mini-lecture to a virtual classroom |

Each interaction includes:
- Real-time confusion & curiosity meters (0–10)
- Knowledge gap detection
- AI-generated educational illustration cards
- AI-generated contextual images
- Emoji reactions and avatar state changes

Sessions are persisted and can be resumed. Knowledge gaps are tracked across sessions for long-term learning.

---

## 📖 Story-Based Learning

1. Enter any concept (e.g., "Gravity", "Democracy", "Photosynthesis")
2. AI generates a 150–250 word engaging story with relatable characters
3. An AI-generated educational image accompanies each story
4. A follow-up question checks understanding
5. Socratic dialogue continues to deepen knowledge, each response paired with a new image

Students can add their own **custom characters** to stories for a personalized experience.

---

## 🔬 Misconception Cascade Tracing (MCT)

The most advanced diagnostic tool. MCT runs a **5-phase Socratic dialogue** to find the *root* of a misunderstanding — not just the symptom:

```
Phase 1: Surface Capture    → Record the wrong answer
Phase 2: Diagnostic Probing → Probe prerequisite knowledge
Phase 3: Root Found         → Identify the broken knowledge link
Phase 4: Remediation        → Fix from root up to surface
Phase 5: Verification       → Confirm understanding is restored
```

---

## 🎨 AI-Generated Images

FunLearn generates **real AI images with every AI response** across all learning features using the **Bria.ai FIBO v2** pipeline:

1. **Prompt → VLM Bridge** — Bria's hosted Gemini 2.5 Flash VLM converts text prompts into structured JSON (~1000 words of scene description)
2. **JSON → FIBO Model** — The 8B-parameter FIBO DiT model generates deterministic, high-fidelity images
3. **Fallback** — If Bria is unavailable, **Google Imagen 4.0** serves as an automatic fallback

Every AI response — in the Feynman Engine (all 5 layers), Story Learning, and MCT — includes a contextual educational image for visual reinforcement.

---

## 🌍 Multi-Language Support

FunLearn supports **11 languages** across all AI features:

| Code | Language | Code | Language |
|------|----------|------|----------|
| `en` | English | `ja` | Japanese |
| `hi` | Hindi | `ar` | Arabic |
| `bn` | Bengali | `ru` | Russian |
| `es` | Spanish | `pa` | Punjabi |
| `pt` | Portuguese | `vi` | Vietnamese |
| `zh` | Mandarin Chinese | | |

Language compliance is enforced at the **prompt level** — injected into every AI request.

---

## 🛠️ Technical Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                     FRONTEND  (React 18 + TypeScript + Vite)     │
│                                                                  │
│  Pages: Dashboard · Feynman · MCT · Story Learning ·            │
│         History · Profile · Characters · Avatar                  │
│                                                                  │
│  Effects: AmbientParticles (7 themes) · PageTransitions ·       │
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
│           feynman · sessions · story · characters · admin         │
│                                                                  │
│  Services: FeynmanAIService · StoryService · ContentGenerator · │
│            QuestionGenerator · AnswerEvaluator ·                │
│            IllustrationService · ScoringService                  │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │           PROVIDER FACTORY  (Plug & Play)                │   │
│  │                                                          │   │
│  │  AI:     DigitalOcean Gradient ✓ · OpenAI · Anthropic   │   │
│  │  Image:  Bria.ai FIBO v2 ✓ · Gemini Imagen 4.0 ✓ ·     │   │
│  │          Pollinations · Stability · None                 │   │
│  └──────────────────────────────────────────────────────────┘   │
│                                                                  │
│  Data: CSV files (pandas) on DO Volume · Auth: JWT + bcrypt      │
└──────────────────────────────────────────────────────────────────┘
```

### Technology Stack

| Layer | Technology | Details |
|-------|-----------|---------|
| Frontend | React 18.3 + TypeScript 5.2 | Vite, Tailwind CSS, Zustand, React Router v6 |
| Backend | FastAPI + Python 3.11+ | Pydantic v2, Uvicorn, pandas |
| AI Model | DigitalOcean Gradient | Llama 3.3 70B Instruct (Serverless Inference) |
| AI Agent | DigitalOcean Gradient Agent Builder | Ritty persona + NCERT Knowledge Base |
| Image Gen | Bria.ai FIBO v2 | Google Imagen 4.0 fallback |
| Compute | DigitalOcean Droplet | Ubuntu 22.04, s-2vcpu-4gb |
| Storage | DigitalOcean Volume | 5GB Block Storage for persistent data |
| IaC | Terraform | Full infrastructure-as-code |
| Auth | JWT + bcrypt | Secure token-based authentication |

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- DigitalOcean Gradient API Key

### Backend

```bash
cd genlearn-ai/backend
python -m venv venv
source venv/bin/activate        # Linux/macOS
# venv\Scripts\activate         # Windows
pip install -r requirements.txt
cp .env.example .env            # Edit .env with your API keys
python run.py
```

Backend: **http://localhost:8000** · API Docs: **http://localhost:8000/docs**

### Frontend

```bash
cd genlearn-ai/frontend
npm install
npm run dev
```

Frontend: **http://localhost:5173**

### Default Login

| Username | Password |
|----------|----------|
| `DebK` | `password123` |

---

## 🏗️ Project Structure

```
├── genlearn-ai/
│   ├── backend/
│   │   ├── app/
│   │   │   ├── main.py                  # FastAPI app + router registration
│   │   │   ├── config.py                # Environment configuration
│   │   │   ├── api/routes/              # All API route handlers
│   │   │   │   ├── auth.py              # Authentication
│   │   │   │   ├── feynman.py           # Feynman Engine (5 layers)
│   │   │   │   ├── story_learning.py    # Story-Based Learning
│   │   │   │   ├── features.py          # MCT diagnostics
│   │   │   │   ├── characters.py        # Character management
│   │   │   │   ├── learning.py          # Learning sessions
│   │   │   │   └── admin.py             # Admin panel
│   │   │   ├── services/                # Business logic
│   │   │   │   ├── provider_factory.py  # AI/Image provider switching
│   │   │   │   ├── feynman_service.py   # Feynman Engine AI logic
│   │   │   │   ├── story_service.py     # Story generation AI logic
│   │   │   │   ├── ai_providers/        # DO Gradient · OpenAI · Anthropic
│   │   │   │   └── image_providers/     # Bria · Gemini · Pollinations
│   │   │   ├── database/               # CSV handlers + file I/O
│   │   │   ├── models/                 # Pydantic data models
│   │   │   └── utils/                  # Rate limiting, validation, i18n
│   │   └── data/                       # CSV databases + media files
│   │
│   └── frontend/
│       └── src/
│           ├── pages/                   # All page components
│           ├── components/              # Reusable UI components
│           ├── services/api.ts          # API client
│           ├── store/                   # Zustand state management
│           ├── contexts/                # Language context
│           └── types/                   # TypeScript interfaces
│
└── infra/                               # Terraform IaC
    ├── main.tf                          # Provider + Droplet config
    ├── gradient_ai.tf                   # Gradient Agent + Knowledge Base
    ├── volume.tf                        # Block Storage Volume
    └── variables.tf                     # Configurable variables
```

---

## 🚀 Deployment

### Terraform (One-Command Deploy)

```bash
cd infra/
terraform init
terraform plan -var-file="terraform.tfvars"
terraform apply -var-file="terraform.tfvars"
```

This provisions:
- **Droplet** — Ubuntu 22.04 with FastAPI + Nginx + systemd
- **Volume** — 5GB persistent storage for all user data
- **Gradient AI Agent** — Ritty persona with guardrails
- **Knowledge Base** — NCERT/CBSE curriculum via web crawler
- **Firewall** — Ports 22, 80, 443 only

### Environment Variables

Key variables in `backend/.env`:

```env
AI_PROVIDER=digitalocean
GRADIENT_API_KEY=your_key_here
GRADIENT_BASE_URL=https://inference.do-ai.run/v1
GRADIENT_MODEL=meta-llama/Meta-Llama-3.3-70B-Instruct
IMAGE_PROVIDER=bria
BRIA_API_KEY=your_key_here
```

---

<div align="center">

**Built for the [DigitalOcean GenAI Hackathon](https://digitalocean.devpost.com/)**

*FunLearn — Where understanding happens by teaching, not by being taught.*

*Powered by DigitalOcean Gradient™ AI · Llama 3.3 70B Instruct · Bria FIBO v2*

</div>
