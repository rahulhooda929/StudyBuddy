#!/usr/bin/env bash
# Start backend and frontend concurrently (POSIX shell / WSL / macOS / Linux)
set -e

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "Starting backend..."
cd "$ROOT_DIR/backend"
if [ -f .venv/bin/activate ]; then
  source .venv/bin/activate
fi
uvicorn main:app --host 127.0.0.1 --port 8000 &
BACKEND_PID=$!

echo "Starting frontend..."
cd "$ROOT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"

wait $BACKEND_PID $FRONTEND_PID
