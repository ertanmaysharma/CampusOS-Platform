#!/bin/sh

set -e

echo "========================================"
echo "🚀 Starting CampusOS"
echo "========================================"

echo "📦 Running database migrations..."
flask db upgrade

echo "🌱 Seeding database..."
python seed.py

echo "✅ Database initialization complete"
echo "🌐 Starting Gunicorn..."

exec gunicorn wsgi:app --bind 0.0.0.0:$PORT
