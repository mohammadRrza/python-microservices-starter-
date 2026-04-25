#!/bin/sh

echo "Running migrations..."
python3 -m alembic upgrade head

echo "Starting app..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8003