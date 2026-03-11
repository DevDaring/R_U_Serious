# Terraform_Creation.md
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
            try_files \$uri \$uri/ /index.html;
        }

        location /api/ {
            proxy_pass http://localhost:8000/;
            proxy_set_header Host \$host;
            proxy_set_header X-Real-IP \$remote_addr;
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
