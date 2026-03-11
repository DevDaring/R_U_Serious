
terraform_md = '''# Terraform_Creation.md
# DigitalOcean Infrastructure for FunLearn — Feynman AI App

## OBJECTIVE
You are an AI coding assistant. Your task is to create a complete, working Terraform configuration
for the FunLearn application infrastructure on DigitalOcean. Follow every instruction below exactly.
Do not skip any step. Do not add extra services not listed here.

---

## PREREQUISITES (Human must do these manually before running Terraform)

1. Create a DigitalOcean account at https://digitalocean.com
2. Generate a Personal Access Token (PAT) from DO Console → API → Tokens → Generate New Token (Read + Write)
3. Upload an SSH public key to DO Console → Settings → Security → Add SSH Key. Note the SSH Key ID (numeric).
4. Install Terraform CLI: https://developer.hashicorp.com/terraform/install
5. Install DigitalOcean CLI (doctl): https://docs.digitalocean.com/reference/doctl/how-to/install/

---

## FILE STRUCTURE TO CREATE

Create the following files in a folder called `infra/`:

```
infra/
├── main.tf
├── variables.tf
├── outputs.tf
├── gradient_ai.tf
├── droplet.tf
├── volume.tf
└── terraform.tfvars       ← human fills this in
```

---

## FILE 1: infra/variables.tf

```hcl
variable "do_token" {
  description = "DigitalOcean Personal Access Token"
  type        = string
  sensitive   = true
}

variable "ssh_key_id" {
  description = "Numeric ID of the SSH key uploaded to DigitalOcean"
  type        = string
}

variable "gradient_api_key" {
  description = "DigitalOcean Gradient AI API Key"
  type        = string
  sensitive   = true
}

variable "region" {
  description = "DigitalOcean region"
  type        = string
  default     = "blr1"
}

variable "droplet_size" {
  description = "Droplet size slug"
  type        = string
  default     = "s-2vcpu-4gb"
}
```

---

## FILE 2: infra/terraform.tfvars
## INSTRUCTION: Create this file but leave placeholder values. Human fills in real values.

```hcl
do_token         = "YOUR_DIGITALOCEAN_PAT_HERE"
ssh_key_id       = "YOUR_SSH_KEY_NUMERIC_ID_HERE"
gradient_api_key = "YOUR_GRADIENT_AI_API_KEY_HERE"
region           = "blr1"
droplet_size     = "s-2vcpu-4gb"
```

---

## FILE 3: infra/main.tf

```hcl
terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.78.0"
    }
  }
  required_version = ">= 1.5.0"
}

provider "digitalocean" {
  token = var.do_token
}
```

---

## FILE 4: infra/volume.tf
## PURPOSE: Persistent 5GB volume attached to the Droplet to store all CSV data files.
## CRITICAL: CSV files must be stored on this volume, NOT on the Droplet root disk.
## The volume will be mounted at /mnt/funlearn-data on the Droplet.

```hcl
resource "digitalocean_volume" "funlearn_data" {
  region                   = var.region
  name                     = "funlearn-data"
  size                     = 5
  initial_filesystem_type  = "ext4"
  description              = "Persistent CSV storage for FunLearn app"
}

resource "digitalocean_volume_attachment" "funlearn_data_attach" {
  droplet_id = digitalocean_droplet.funlearn_app.id
  volume_id  = digitalocean_volume.funlearn_data.id
}
```

---

## FILE 5: infra/droplet.tf
## PURPOSE: A plain Ubuntu 22.04 Droplet that hosts FastAPI backend + React frontend via Nginx.
## user_data script below installs all dependencies on first boot automatically.
## IMPORTANT: The user_data script mounts the volume, sets up Python venv, and starts the app.

```hcl
resource "digitalocean_droplet" "funlearn_app" {
  name     = "funlearn-app"
  size     = var.droplet_size
  image    = "ubuntu-22-04-x64"
  region   = var.region
  ssh_keys = [var.ssh_key_id]

  user_data = <<-EOF
    #!/bin/bash
    set -e

    # Mount the volume for persistent CSV storage
    mkdir -p /mnt/funlearn-data
    mount -o discard,defaults /dev/disk/by-id/scsi-0DO_Volume_funlearn-data /mnt/funlearn-data
    echo "/dev/disk/by-id/scsi-0DO_Volume_funlearn-data /mnt/funlearn-data ext4 defaults,nofail,discard 0 2" >> /etc/fstab

    # Create CSV data directory on volume
    mkdir -p /mnt/funlearn-data/csv
    chmod 777 /mnt/funlearn-data/csv

    # System updates and install dependencies
    apt-get update -y
    apt-get install -y python3.11 python3.11-venv python3-pip nodejs npm nginx git

    # Clone the application repo (human must update this URL)
    git clone https://github.com/YOUR_GITHUB_USERNAME/funlearn.git /opt/funlearn

    # Backend setup
    cd /opt/funlearn/backend
    python3.11 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt

    # Write environment variables
    cat > /opt/funlearn/backend/.env <<ENVEOF
    AI_PROVIDER=digitalocean
    GRADIENT_API_KEY=${var.gradient_api_key}
    GRADIENT_BASE_URL=https://inference.do-ai.run/v1
    GRADIENT_MODEL=meta-llama/Meta-Llama-3.3-70B-Instruct
    DATA_DIR=/mnt/funlearn-data/csv
    IMAGE_PROVIDER=none
    VOICE_TTS_PROVIDER=none
    VOICE_STT_PROVIDER=none
    ENVEOF

    # Create systemd service for FastAPI backend
    cat > /etc/systemd/system/funlearn-backend.service <<SVCEOF
    [Unit]
    Description=FunLearn FastAPI Backend
    After=network.target

    [Service]
    User=root
    WorkingDirectory=/opt/funlearn/backend
    ExecStart=/opt/funlearn/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
    Restart=always

    [Install]
    WantedBy=multi-user.target
    SVCEOF

    # Frontend build
    cd /opt/funlearn/frontend
    npm install
    npm run build

    # Nginx config to serve frontend and proxy backend
    cat > /etc/nginx/sites-available/funlearn <<NGINXEOF
    server {
        listen 80;
        server_name _;

        root /opt/funlearn/frontend/dist;
        index index.html;

        location / {
            try_files \\$uri \\$uri/ /index.html;
        }

        location /api/ {
            proxy_pass http://localhost:8000/;
            proxy_set_header Host \\$host;
            proxy_set_header X-Real-IP \\$remote_addr;
        }
    }
    NGINXEOF

    ln -sf /etc/nginx/sites-available/funlearn /etc/nginx/sites-enabled/
    rm -f /etc/nginx/sites-enabled/default
    systemctl restart nginx

    # Start backend
    systemctl daemon-reload
    systemctl enable funlearn-backend
    systemctl start funlearn-backend
  EOF

  tags = ["funlearn", "hackathon"]
}

resource "digitalocean_firewall" "funlearn_fw" {
  name = "funlearn-firewall"

  droplet_ids = [digitalocean_droplet.funlearn_app.id]

  inbound_rule {
    protocol         = "tcp"
    port_range       = "22"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "80"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  inbound_rule {
    protocol         = "tcp"
    port_range       = "443"
    source_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "tcp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }

  outbound_rule {
    protocol              = "udp"
    port_range            = "1-65535"
    destination_addresses = ["0.0.0.0/0", "::/0"]
  }
}
```

---

## FILE 6: infra/gradient_ai.tf
## PURPOSE: Creates the Ritty AI Agent and NCERT Knowledge Base on DO Gradient AI.
## IMPORTANT: Knowledge Base is created first. Agent depends on it.
## The agent UUID output is needed in the application .env as RITTY_AGENT_UUID.

```hcl
resource "digitalocean_gradientai_knowledge_base" "ncert_kb" {
  name        = "ncert-curriculum-kb"
  description = "NCERT and CBSE curriculum content for Feynman Engine and Story Learning"
  region      = "tor1"

  web_crawler_data_source = {
    base_url        = "https://ncert.nic.in/textbook.php"
    crawling_option = "SCOPED"
    embed_media     = false
  }
}

resource "digitalocean_gradientai_agent" "ritty" {
  name        = "Ritty-Feynman-Agent"
  model       = "meta-llama/Meta-Llama-3.3-70B-Instruct"
  description = "Ritty is a curious 8-year-old AI child who helps students learn through the Feynman Technique"

  instruction = <<-PROMPT
    You are Ritty, a curious and enthusiastic 8-year-old child who LOVES learning new things.
    Your job is NOT to teach — your job is to be taught by the student.
    Ask one simple "Why?" or "How?" question at a time.
    If the student's explanation is confusing, say "I don't get it, can you say it simpler?"
    If the explanation is clear, say "Oh! So it's like..." and make a childlike analogy.
    Never give the answer. Always ask questions.
    Keep responses under 3 sentences.
    Respond in whatever language the student is using.
    You are safe, kind, and never use adult language.
  PROMPT

  knowledge_base_ids = [digitalocean_gradientai_knowledge_base.ncert_kb.uuid]

  depends_on = [digitalocean_gradientai_knowledge_base.ncert_kb]
}
```

---

## FILE 7: infra/outputs.tf

```hcl
output "droplet_ip" {
  description = "Public IP of the FunLearn Droplet — use this to access the app"
  value       = digitalocean_droplet.funlearn_app.ipv4_address
}

output "ritty_agent_uuid" {
  description = "UUID of the Ritty Gradient AI Agent — add this to backend .env as RITTY_AGENT_UUID"
  value       = digitalocean_gradientai_agent.ritty.uuid
}

output "ncert_kb_uuid" {
  description = "UUID of the NCERT Knowledge Base"
  value       = digitalocean_gradientai_knowledge_base.ncert_kb.uuid
}

output "volume_id" {
  description = "ID of the persistent CSV data volume"
  value       = digitalocean_volume.funlearn_data.id
}
```

---

## HOW TO RUN (In order)

```bash
# Step 1: Go into the infra folder
cd infra/

# Step 2: Fill in terraform.tfvars with real values (DO NOT commit this file to git)

# Step 3: Initialize Terraform
terraform init

# Step 4: Preview what will be created
terraform plan

# Step 5: Create all infrastructure
terraform apply

# Step 6: Note the outputs — especially droplet_ip and ritty_agent_uuid
terraform output

# Step 7: SSH into the Droplet to verify everything is running
ssh root@<droplet_ip>
systemctl status funlearn-backend
```

---

## HOW TO DESTROY (After hackathon to avoid charges)

```bash
terraform destroy
```

---

## COST ESTIMATE

| Resource | Size | Monthly Cost |
|---|---|---|
| Droplet | s-2vcpu-4gb | ~$24/mo |
| Volume | 5 GB | ~$0.50/mo |
| Gradient AI Agent | Managed | Free tier / usage |
| Gradient Serverless Inference | Per token | ~$0–5/mo for demo |
| **Total** | | **~$25–30/mo** |

Destroy after the hackathon demo to stop all charges.
'''

project_md = '''# Project_Changes.md
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
    The agent has Ritty\'s persona and NCERT Knowledge Base pre-attached.
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
        {"role": "system", "content": "You are a kind Socratic teacher. The student just answered a question about a story. Affirm what they got right, gently correct what they got wrong, and ask one more follow-up question to go deeper. Under 60 words. Respond in the student\'s language."},
        {"role": "user", "content": f"Concept: {concept}\\nStory: {story}\\nStudent Answer: {student_answer}\\nLanguage: {language}"}
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
'''

with open("Terraform_Creation.md", "w") as f:
    f.write(terraform_md)

with open("Project_Changes.md", "w") as f:
    f.write(project_md)

print("Both files written successfully.")
print(f"Terraform_Creation.md: {len(terraform_md)} chars")
print(f"Project_Changes.md: {len(project_md)} chars")
