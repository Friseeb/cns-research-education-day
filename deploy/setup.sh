#!/bin/bash
set -e

# Run as root on a fresh Ubuntu 24.04 Droplet.
# Usage: bash setup.sh

APP_USER="cns"
APP_DIR="/home/$APP_USER/app"
REPO="https://github.com/Friseeb/cns-research-education-day.git"
PYTHON="python3.11"

echo "=== CNS Research Day — Droplet Setup ==="
echo ""
read -p "Droplet IP address: " SERVER_IP
read -p "PostgreSQL password for app DB: " DB_PASSWORD
read -p "Django SECRET_KEY (press enter to auto-generate): " SECRET_KEY
if [ -z "$SECRET_KEY" ]; then
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")
    echo "Generated: $SECRET_KEY"
fi
echo ""

# ── System packages ──────────────────────────────────────────────
echo "--- Installing system packages..."
apt-get update -q
apt-get install -y -q python3.11 python3.11-venv python3-pip postgresql nginx git

# ── PostgreSQL ───────────────────────────────────────────────────
echo "--- Setting up PostgreSQL..."
sudo -u postgres psql -c "CREATE USER cns_user WITH PASSWORD '$DB_PASSWORD';" 2>/dev/null || echo "User already exists."
sudo -u postgres psql -c "CREATE DATABASE cns_db OWNER cns_user;" 2>/dev/null || echo "Database already exists."

DATABASE_URL="postgres://cns_user:$DB_PASSWORD@localhost:5432/cns_db"

# ── App user ─────────────────────────────────────────────────────
echo "--- Creating app user..."
id -u $APP_USER &>/dev/null || useradd -m -s /bin/bash $APP_USER

# ── Clone repo ───────────────────────────────────────────────────
echo "--- Cloning repo..."
if [ -d "$APP_DIR" ]; then
    cd $APP_DIR && git pull
else
    git clone $REPO $APP_DIR
fi
chown -R $APP_USER:$APP_USER $APP_DIR

# ── Python virtualenv + dependencies ─────────────────────────────
echo "--- Installing Python dependencies..."
sudo -u $APP_USER $PYTHON -m venv $APP_DIR/.venv
sudo -u $APP_USER $APP_DIR/.venv/bin/pip install -q --upgrade pip
sudo -u $APP_USER $APP_DIR/.venv/bin/pip install -q -r $APP_DIR/requirements.txt

# ── Environment file ─────────────────────────────────────────────
echo "--- Writing .env..."
cat > $APP_DIR/.env <<EOF
SECRET_KEY=$SECRET_KEY
DEBUG=False
ALLOWED_HOSTS=$SERVER_IP
CSRF_TRUSTED_ORIGINS=http://$SERVER_IP
DATABASE_URL=$DATABASE_URL
EOF
chown $APP_USER:$APP_USER $APP_DIR/.env
chmod 600 $APP_DIR/.env

# ── Django setup ─────────────────────────────────────────────────
echo "--- Running migrations and collectstatic..."
cd $APP_DIR
sudo -u $APP_USER bash -c "
    set -a && source .env && set +a
    .venv/bin/python manage.py migrate --noinput
    .venv/bin/python manage.py collectstatic --noinput
"

# ── Gunicorn systemd service ──────────────────────────────────────
echo "--- Setting up gunicorn service..."
cat > /etc/systemd/system/cns.service <<EOF
[Unit]
Description=CNS Research Day gunicorn
After=network.target

[Service]
User=$APP_USER
Group=$APP_USER
WorkingDirectory=$APP_DIR
EnvironmentFile=$APP_DIR/.env
ExecStart=$APP_DIR/.venv/bin/gunicorn researchday.wsgi:application \
    --workers 2 \
    --bind 127.0.0.1:8000 \
    --access-logfile - \
    --error-logfile -
Restart=on-failure

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable cns
systemctl restart cns

# ── Nginx ────────────────────────────────────────────────────────
echo "--- Configuring nginx..."
cat > /etc/nginx/sites-available/cns <<EOF
server {
    listen 80;
    server_name $SERVER_IP;

    client_max_body_size 20M;

    location /static/ {
        alias $APP_DIR/staticfiles/;
    }

    location /media/ {
        alias $APP_DIR/media/;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

ln -sf /etc/nginx/sites-available/cns /etc/nginx/sites-enabled/cns
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl restart nginx

echo ""
echo "=== Done! ==="
echo ""
echo "App running at: http://$SERVER_IP"
echo "Admin:          http://$SERVER_IP/admin"
echo ""
echo "Create a superuser:"
echo "  sudo -u $APP_USER bash -c 'set -a && source $APP_DIR/.env && set +a && $APP_DIR/.venv/bin/python $APP_DIR/manage.py createsuperuser'"
echo ""
echo "Load demo data:"
echo "  sudo -u $APP_USER bash -c 'set -a && source $APP_DIR/.env && set +a && $APP_DIR/.venv/bin/python $APP_DIR/manage.py seed_demo_event'"
