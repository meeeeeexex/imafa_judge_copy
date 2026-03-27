#!/bin/sh
set -e

# Run migrations
alembic upgrade head

# Seed data (idempotent — skips if already seeded)
python -c "from app.db.seed import seed; seed()"

# Start server
exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
