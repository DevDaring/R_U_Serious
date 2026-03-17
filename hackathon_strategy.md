Here is a clean writeup of every DigitalOcean feature FunLearn uses, mapped directly to the hackathon's judging criteria . You can copy this directly into your Devpost project description.

***

## DigitalOcean Features Used in FunLearn

### 🤖 1. Gradient™ AI Agent Builder — *Ritty, the Feynman Agent*

FunLearn deploys **Ritty** as a fully managed DigitalOcean Gradient™ AI Agent with a defined persona, system instruction, and persistent configuration. Ritty is not a raw LLM prompt — she is a named, versioned agent deployed on the Gradient platform with a specific teaching persona (curious 8-year-old) and safe Guardrails to ensure age-appropriate, non-toxic responses for student interactions .

***

### 📚 2. Gradient™ AI Knowledge Base (RAG)

A **Gradient™ Knowledge Base** is attached to Ritty's agent, ingesting NCERT and CBSE curriculum content via the web crawler data source. This grounds every Feynman Engine and Story Learning session in actual Indian curriculum — not generic world knowledge — making the AI responses educationally accurate and curriculum-aligned .

***

### ⚡ 3. Gradient™ Serverless LLM Inference

All AI features in FunLearn — Story Learning, Misconception Cascade Tracing (MCT), and Feynman Engine scoring — call the **DO Gradient Serverless Inference API** using the `meta-llama/Meta-Llama-3.3-70B-Instruct` model via the OpenAI-compatible endpoint at `https://inference.do-ai.run/v1`. This is a pay-per-token, zero-infrastructure managed inference layer .

***

### 🖥️ 4. DigitalOcean Droplet (Compute)

The entire FunLearn application — FastAPI backend + React frontend served via Nginx — is hosted on a **plain Ubuntu 22.04 Droplet** (`s-2vcpu-4gb`). The app runs as a `systemd` service for auto-restart on failure, with a firewall allowing only ports 22, 80, and 443 .

***

### 💾 5. DigitalOcean Volume (Persistent Storage)

A **5GB Block Storage Volume** is attached to the Droplet and mounted at `/mnt/funlearn-data/csv`. All user data — accounts, learning sessions, Feynman conversations, MCT diagnostic history, and XP/streak records — is persisted on this volume. This ensures data survives Droplet reboots and redeployments .

***

## How These Features Map to Judging Criteria

| Judging Criterion | How FunLearn Satisfies It |
|---|---|
| **Thoroughly leverage the required tool**  | 3 distinct Gradient™ AI services used: Agent Builder, Knowledge Base, Serverless Inference |
| **Quality software development**  | Provider Factory pattern allows clean DO integration; Terraform IaC for all infra |
| **Potential Impact**  | Targets 1.5M Indian students who fail board exams yearly; 9 languages including Hindi and Bengali |
| **Creative & unique idea**  | Feynman Engine (teach the AI to learn), Story-Based Learning, MCT root-cause diagnosis — all novel pedagogy |
| **Design**  | React + Tailwind UI with full multilingual support and accessible voice-free UX |

***

## Prize Categories Targeted

- 🥇 **Best Program for the People** — Primary target; grassroots education impact across India 
- 🎭 **Best AI Agent Persona** — Ritty is a fully deployed, character-rich Gradient AI Agent with Guardrails 
- 🐋 **The Great Whale Prize** — Deep platform usage across 5 DO services including Gradient AI stack