#!/bin/sh

echo "Starting payment-service..."

exec uvicorn app.main:app --host 0.0.0.0 --port 8006