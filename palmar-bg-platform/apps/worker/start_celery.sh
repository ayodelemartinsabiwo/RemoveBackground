#!/bin/bash
# Start script for Celery worker with FastAPI trigger endpoint

echo "🚀 Starting Palmar BG Worker (Celery)"

# Get concurrency from environment or default to 1 (to save memory for AI models)
CONCURRENCY="${CELERY_WORKER_CONCURRENCY:-1}"
echo "Worker concurrency: $CONCURRENCY"

# Start FastAPI trigger endpoint in background (lightweight HTTP interface)
echo "Starting FastAPI trigger endpoint..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 &
FASTAPI_PID=$!

# Wait for FastAPI to start
sleep 3

# Start Celery worker (main image processing worker)
echo "Starting Celery worker..."
celery -A celery_app worker \
    --loglevel=info \
    --concurrency=$CONCURRENCY \
    --max-tasks-per-child=10 \
    --pool=prefork \
    --task-events \
    --without-gossip \
    --without-mingle \
    --without-heartbeat

# If Celery exits, kill FastAPI
kill $FASTAPI_PID
