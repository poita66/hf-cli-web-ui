#!/usr/bin/env python3

import os
import json
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

# Global dictionary to store download progress
downloads = {}

# Cache directory setup
cache_dir = scan_cache_dir()
print(f"Cache directory: {cache_dir}")  # Debug print

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

@app.route('/api/cache/stats', methods=['GET'])
def get_cache_stats():
    """Get cache statistics"""
    try:
        # The cache_dir object has size_on_disk directly
        stats = {
            'size': cache_dir.size_on_disk,
            'size_formatted': format_size(cache_dir.size_on_disk),
            'folders': len(cache_dir.repos),
            'files': sum(repo.nb_files for repo in cache_dir.repos),
            'last_updated': datetime.now().isoformat()
        }
        return jsonify(stats)
    except Exception as e:
        logger.error(f"Error getting cache stats: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cache/files', methods=['GET'])
def get_cache_files():
    """Get list of cached files"""
    try:
        files = []
        # Iterate through repos (not folders as in the original code)
        for repo in cache_dir.repos:
            files.append({
                'path': str(repo.repo_path),
                'size': repo.size_on_disk,
                'size_formatted': format_size(repo.size_on_disk),
                'last_accessed': datetime.fromtimestamp(repo.last_accessed).isoformat() if repo.last_accessed and not isinstance(repo.last_accessed, (int, float)) else repo.last_accessed,
                'folder': str(repo.repo_path)
            })
        
        return jsonify({
            'files': files,
            'total_count': len(files)
        })
    except Exception as e:
        logger.error(f"Error getting cache files: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cache/download', methods=['POST'])
def start_download():
    """Start downloading a model and return download ID"""
    try:
        data = request.get_json()
        repo_id = data.get('repo_id')
        filename = data.get('filename')
        
        if not repo_id or not filename:
            return jsonify({'error': 'repo_id and filename are required'}), 400
            
        # Generate unique download ID
        import uuid
        download_id = str(uuid.uuid4())
        
        # Store download info
        downloads[download_id] = {
            'status': 'downloading',
            'progress': 0,
            'repo_id': repo_id,
            'filename': filename,
            'start_time': datetime.now().isoformat(),
            'error': None
        }
        
        # Start download in background thread
        thread = threading.Thread(target=download_model, args=(download_id,))
        thread.daemon = True
        thread.start()
        
        return jsonify({
            'download_id': download_id,
            'message': 'Download started'
        })
    except Exception as e:
        logger.error(f"Error starting download: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cache/download/<download_id>/progress', methods=['GET'])
def get_download_progress(download_id):
    """Get download progress"""
    if download_id not in downloads:
        return jsonify({'error': 'Download not found'}), 404
    
    return jsonify(downloads[download_id])

@app.route('/api/cache/download/<download_id>', methods=['DELETE'])
def cancel_download(download_id):
    """Cancel a download"""
    if download_id in downloads:
        downloads[download_id]['status'] = 'cancelled'
        return jsonify({'message': 'Download cancelled'})
    else:
        return jsonify({'error': 'Download not found'}), 404

def format_size(size_in_bytes):
    """Format size in bytes to human readable format"""
    if size_in_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    i = 0
    while size_in_bytes >= 1024.0 and i < len(size_names) - 1:
        size_in_bytes /= 1024.0
        i += 1
    
    return f"{size_in_bytes:.1f} {size_names[i]}"

def download_model(download_id):
    """Download model with progress tracking"""
    try:
        # Import here to avoid circular imports
        from huggingface_hub import hf_hub_download
        
        download_info = downloads[download_id]
        repo_id = download_info['repo_id']
        filename = download_info['filename']
        
        # Download the file
        file_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            repo_type="model",
            etag_timeout=30,
            token=None  # Will use default credentials if available
        )
        
        # Update download status
        downloads[download_id]['status'] = 'completed'
        downloads[download_id]['end_time'] = datetime.now().isoformat()
        downloads[download_id]['file_path'] = file_path
        
        logger.info(f"Download completed: {repo_id}/{filename}")
    except Exception as e:
        logger.error(f"Download failed for {repo_id}/{filename}: {str(e)}")
        downloads[download_id]['status'] = 'failed'
        downloads[download_id]['error'] = str(e)
        downloads[download_id]['end_time'] = datetime.now().isoformat()

@app.route('/api/cache/clear', methods=['POST'])
def clear_cache():
    """Clear the entire cache"""
    try:
        # Clear the cache directory
        cache_dir.clear()
        return jsonify({'message': 'Cache cleared successfully'})
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/cache/remove/<repo_path>', methods=['DELETE'])
def remove_repository(repo_name):
    """Remove a specific repository from cache"""
    try:
        # Find the repository in the cache
        import shutil
        import os
        
        # Convert repo_name to a proper path
        repo_name = os.path.expanduser(repo_path)
        
        # Check if the path exists in the cache
        for repo in cache_dir.repos:
            if str(repo.repo_name) == repo_path:
                # Remove the repository directory
                shutil.rmtree(repo_name)
                return jsonify({'message': f'Repository {repo_name} removed successfully'})
        
        return jsonify({'error': 'Repository not found in cache'}), 404
    except Exception as e:
        logger.error(f"Error removing repository: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
