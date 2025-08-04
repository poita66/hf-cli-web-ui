from flask import Blueprint, jsonify, request
from datetime import datetime
import threading
import logging
from huggingface_hub import scan_cache_dir

from utils.formatting import format_size

# Create blueprint for API routes
api_bp = Blueprint('api', __name__)

# Global dictionary to store download progress
downloads = {}

# Cache directory setup
cache_dir = scan_cache_dir()

@api_bp.route('/cache/download', methods=['POST'])
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

@api_bp.route('/cache/download/<download_id>/progress', methods=['GET'])
def get_download_progress(download_id):
    """Get download progress"""
    if download_id not in downloads:
        return jsonify({'error': 'Download not found'}), 404
    
    return jsonify(downloads[download_id])

@api_bp.route('/cache/download/<download_id>', methods=['DELETE'])
def cancel_download(download_id):
    """Cancel a download"""
    if download_id in downloads:
        downloads[download_id]['status'] = 'cancelled'
        return jsonify({'message': 'Download cancelled'})
    else:
        return jsonify({'error': 'Download not found'}), 404

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