#!/bin/bash
set -euxo pipefail

# Log everything
exec > >(tee /var/log/user-data.log | logger -t user-data) 2>&1

echo "===== EC2 Bootstrap Started ====="

############################################
# Update OS
############################################

apt-get update
apt-get upgrade -y

############################################
# Install Packages
############################################

apt-get install -y \
curl \
wget \
git \
python3 \
python3-pip \
python3-venv \
nginx \
ufw \
htop \
net-tools \
unattended-upgrades

############################################
# Install CloudWatch Agent
############################################

wget -q https://s3.amazonaws.com/amazoncloudwatch-agent/ubuntu/amd64/latest/amazon-cloudwatch-agent.deb

dpkg -i -E amazon-cloudwatch-agent.deb

rm -f amazon-cloudwatch-agent.deb

############################################
# Install AWS CLI
############################################

apt-get install -y awscli

############################################
# Create Flask App
############################################

mkdir -p /opt/webapp

cd /opt/webapp

python3 -m venv venv

/opt/webapp/venv/bin/pip install --upgrade pip

/opt/webapp/venv/bin/pip install Flask==2.3.3 Werkzeug==2.3.7

cat >/opt/webapp/app.py <<'EOF'
from flask import Flask, render_template_string
import socket
from datetime import datetime

app = Flask(__name__)

HTML="""
<!DOCTYPE html>
<html>
<head>
<title>EC2 Server</title>
<style>
body{font-family:Arial;background:#eef2ff;padding:40px;}
.container{
background:white;
padding:30px;
border-radius:10px;
max-width:800px;
margin:auto;
}
</style>
</head>
<body>
<div class="container">
<h1>🚀 EC2 Linux Server Running</h1>
<p><b>Hostname:</b> {{hostname}}</p>
<p><b>Private IP:</b> {{ip}}</p>
<p><b>Time:</b> {{time}}</p>
</div>
</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(
        HTML,
        hostname=socket.gethostname(),
        ip=socket.gethostbyname(socket.gethostname()),
        time=datetime.utcnow()
    )

@app.route("/health")
def health():
    return {"status":"healthy"}

app.run(host="0.0.0.0",port=8080)
EOF

############################################
# Systemd Service
############################################

cat >/etc/systemd/system/webapp.service <<EOF
[Unit]
Description=Flask Web Application
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/webapp
ExecStart=/opt/webapp/venv/bin/python /opt/webapp/app.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

chown -R www-data:www-data /opt/webapp

############################################
# Configure Nginx
############################################

cat >/etc/nginx/sites-available/webapp <<EOF
server {

    listen 80;

    server_name _;

    location / {

        proxy_pass http://127.0.0.1:8080;

        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;

    }

    location /health {

        proxy_pass http://127.0.0.1:8080/health;

    }

}
EOF

ln -sf /etc/nginx/sites-available/webapp /etc/nginx/sites-enabled/webapp

rm -f /etc/nginx/sites-enabled/default

############################################
# Start Flask
############################################

systemctl daemon-reload

systemctl enable webapp

systemctl start webapp

############################################
# Start Nginx
############################################

nginx -t

systemctl enable nginx

systemctl restart nginx

############################################
# Configure CloudWatch Agent
############################################

/opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
-a fetch-config \
-m ec2 \
-c ssm:/cloudwatch/linux/config \
-s

############################################
# Firewall
############################################

ufw --force enable

ufw allow OpenSSH

ufw allow 80/tcp

ufw allow 443/tcp

############################################
# Automatic Updates
############################################

systemctl enable unattended-upgrades

systemctl start unattended-upgrades

echo "===== Bootstrap Completed Successfully ====="