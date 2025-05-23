#!/bin/bash

echo "🔄 Pulling latest changes from git..."
git pull origin main

echo "🛠 Running Django migrations..."
poetry run python Hume/manage.py migrate

echo "🚀 Restarting Supervisor app..."
sudo supervisorctl restart hume

echo "✅ Deployment complete."