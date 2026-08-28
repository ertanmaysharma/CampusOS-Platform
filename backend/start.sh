#!/bin/sh

set -e

echo "========================================"
echo "🚀 Starting CampusOS"
echo "========================================"

echo "📦 Creating database tables..."

python -c "from app import create_app; from app.extensions import db; app=create_app(); app.app_context().push(); db.create_all()"

echo "🌱 Seeding database..."

python seed.py

echo "✅ Database initialization complete"
echo "🌐 Starting Gunicorn..."

exec gunicorn wsgi:app --bind 0.0.0.0:$PORT
