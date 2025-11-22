#!/bin/bash

# Start Backend
echo "Starting Backend..."
cd backend
pip install -r requirements.txt
python main.py dev &
BACKEND_PID=$!

# Start Frontend
echo "Starting Frontend..."
cd ../frontend
npm install
npm run dev &
FRONTEND_PID=$!

echo "App is running. Backend PID: $BACKEND_PID, Frontend PID: $FRONTEND_PID"
wait