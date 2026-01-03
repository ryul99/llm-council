#!/bin/bash

# LLM Council - Start script

echo "Starting LLM Council..."
echo ""

# Start backend
echo "Starting backend on http://localhost:8001..."
uv run python -m backend.main &
BACKEND_PID=$!

# Wait a bit for backend to start
sleep 2

# Start frontend
echo "Starting frontend on http://localhost:5173..."
cd frontend
if [ ! -x "node_modules/.bin/vite" ]; then
  echo "Frontend dependencies not found (missing node_modules/.bin/vite). Installing locally..."
  if [ -f "package-lock.json" ]; then
    npm ci --include=dev || {
      echo "npm ci --include=dev failed; retrying with npm ci..."
      npm ci || { echo "Failed to install frontend dependencies via npm ci"; exit 1; }
    }
  else
    npm install --include=dev || {
      echo "npm install --include=dev failed; retrying with npm install..."
      npm install || { echo "Failed to install frontend dependencies via npm install"; exit 1; }
    }
  fi
  if [ ! -x "node_modules/.bin/vite" ]; then
    echo "vite is still missing after install. If you have NODE_ENV=production set, unset it and retry."
    exit 1
  fi
fi
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✓ LLM Council is running!"
echo "  Backend:  http://localhost:8001"
echo "  Frontend: http://localhost:5173"
echo ""
echo "Press Ctrl+C to stop both servers"

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" SIGINT SIGTERM
wait
