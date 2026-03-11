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
