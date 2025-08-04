#!/bin/bash

# Script to run both backend and frontend servers using uv

# Exit on any error
set -e

# Function to cleanup on exit
cleanup() {
    echo "Shutting down servers..."
    kill $BACKEND_PID 2>/dev/null || true
    exit 0
}

# Trap SIGINT (Ctrl+C) to cleanup
trap cleanup SIGINT

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Change to frontend directory first to build the frontend
cd /var/home/peter/Repos/Personal/hf-cli-web-ui/frontend

echo "Building frontend..."
npm run build

# Change to backend directory
cd /var/home/peter/Repos/Personal/hf-cli-web-ui/backend

# Create virtual environment with uv if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with uv..."
    uv venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies with uv if needed
if ! uv pip list | grep -q "flask"; then
    echo "Installing dependencies with uv..."
    uv pip install -e .
fi

# Start backend server
echo "Starting backend server..."
python app.py &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

echo "Backend server is running on http://localhost:5000"
echo "Frontend will be served through the backend"
echo "Press Ctrl+C to stop"

# Keep the script running to maintain the backend process
wait $BACKEND_PID
