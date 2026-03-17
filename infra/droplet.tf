resource "digitalocean_droplet" "funlearn_app" {
  name     = "funlearn-app"
  size     = var.droplet_size
  image    = "ubuntu-22-04-x64"
  region   = var.region
  ssh_keys = [var.ssh_key_id]

  user_data = <<-EOF
    #!/bin/bash
    set -e
    exec > /var/log/user-data.log 2>&1

    # Wait for volume to be attached
    for i in $(seq 1 30); do
      [ -e /dev/disk/by-id/scsi-0DO_Volume_funlearn-data ] && break
      echo "Waiting for volume... attempt $i"
      sleep 5
    done

    # Mount the volume for persistent CSV storage
    mkdir -p /mnt/funlearn-data
    mount -o discard,defaults /dev/disk/by-id/scsi-0DO_Volume_funlearn-data /mnt/funlearn-data || true
    grep -q funlearn-data /etc/fstab || echo "/dev/disk/by-id/scsi-0DO_Volume_funlearn-data /mnt/funlearn-data ext4 defaults,nofail,discard 0 2" >> /etc/fstab

    # Create CSV data directory on volume
    mkdir -p /mnt/funlearn-data/csv
    chmod 755 /mnt/funlearn-data/csv

    # System updates and install dependencies
    apt-get update -y
    apt-get install -y python3.11 python3-pip nodejs npm nginx git

    # Clone the application repo
    git clone https://github.com/DevDaring/R_U_Serious.git /opt/funlearn-repo

    # Set app root (code is inside genlearn-ai/ subdirectory)
    APP_ROOT=/opt/funlearn-repo/genlearn-ai

    # Backend setup — install globally (no venv)
    cd $APP_ROOT/backend
    pip install --break-system-packages -r requirements.txt

    # Generate sample CSV data
    python3.11 create_csv_data.py
    # Copy generated CSVs to the persistent volume (if volume is empty)
    if [ -z "$(ls -A /mnt/funlearn-data/csv/ 2>/dev/null)" ]; then
      cp $APP_ROOT/backend/data/csv/*.csv /mnt/funlearn-data/csv/
    fi

    # Generate a stable secret key for JWT
    SECRET_KEY=$(python3.11 -c "import secrets; print(secrets.token_urlsafe(32))")

    # Write environment variables
    cat > $APP_ROOT/backend/.env <<ENVEOF
APP_ENV=production
SECRET_KEY=$SECRET_KEY
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
WorkingDirectory=$APP_ROOT/backend
ExecStart=/usr/bin/python3.11 -m uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always
EnvironmentFile=$APP_ROOT/backend/.env

[Install]
WantedBy=multi-user.target
SVCEOF

    # Frontend build
    cd $APP_ROOT/frontend
    npm install
    VITE_API_BASE_URL=/api npm run build

    # Nginx config to serve frontend and proxy backend
    cat > /etc/nginx/sites-available/funlearn <<NGINXEOF
server {
    listen 80;
    server_name _;

    root $APP_ROOT/frontend/dist;
    index index.html;

    location / {
        try_files \$uri \$uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    location /media/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
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
