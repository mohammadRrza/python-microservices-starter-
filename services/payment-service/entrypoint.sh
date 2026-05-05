#!/bin/sh
set -e

echo "Running payment-service migrations..."
# alembic -c /app/alembic.ini upgrade head

echo "Starting payment-service..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8006