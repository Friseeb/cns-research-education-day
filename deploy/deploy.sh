#!/bin/bash
set -e

# Run on the Droplet to pull latest code and restart the app.
# Usage: bash deploy/deploy.sh

APP_DIR="/home/cns/app"

echo "--- Pulling latest code..."
cd $APP_DIR
sudo -u cns git pull

echo "--- Installing dependencies..."
sudo -u cns .venv/bin/pip install -q -r requirements.txt

echo "--- Running migrations..."
sudo -u cns bash -c "set -a && source .env && set +a && .venv/bin/python manage.py migrate --noinput"

echo "--- Collecting static files..."
sudo -u cns bash -c "set -a && source .env && set +a && .venv/bin/python manage.py collectstatic --noinput"

echo "--- Restarting gunicorn..."
systemctl restart cns

echo "Done."
