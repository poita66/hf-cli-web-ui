#!/bin/bash

# Simple installation script for the backend with uv

# Make sure we're in the right directory
cd /var/home/peter/Repos/Personal/hf-cli-web-ui/backend

# Check if uv is installed
if ! command -v uv &> /dev/null; then
    echo "uv is not installed. Installing uv..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment with uv..."
    uv venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing backend dependencies with uv..."
uv pip install -e .

echo "Backend setup complete!"
echo "To run the application:"
echo "  source .venv/bin/activate"
echo "  python app.py"