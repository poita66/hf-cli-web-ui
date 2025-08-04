#!/usr/bin/env python3

import os
import threading
import time
from pathlib import Path
from datetime import datetime
import psutil
from flask import Flask, jsonify, request, send_from_directory, send_file
from flask_cors import CORS
from huggingface_hub import scan_cache_dir
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Cache directory setup
cache_dir = scan_cache_dir()
print(f"Cache directory: {cache_dir}")  # Debug print

# Import and register API blueprints
from api import register_blueprints
register_blueprints(app)

# Serve frontend files for development mode
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_frontend(path):
    """Serve frontend static files or index.html for SPA routing"""
    if path.startswith('api/'):
        # This is an API request, let it be handled by the API routes
        return "Not Found", 404
    elif path.startswith('static/') or path.startswith('assets/'):
        # Serve static files from the frontend
        try:
            # Handle both static/ and assets/ paths
            if path.startswith('assets/'):
                return send_from_directory('../frontend/dist/assets', path[7:])
            else:
                return send_from_directory('../frontend/dist', path)
        except FileNotFoundError:
            return "File not found", 404
    else:
        # For all other routes, serve the main index.html
        try:
            return send_file('../frontend/dist/index.html')
        except FileNotFoundError:
            # If dist doesn't exist, serve a basic HTML
            return """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Hugging Face CLI Cache Manager</title>
            </head>
            <body>
                <h1>Backend server running</h1>
                <p>Frontend not built yet. Please run:</p>
                <pre>cd frontend && npm run build</pre>
            </body>
            </html>
            """

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)