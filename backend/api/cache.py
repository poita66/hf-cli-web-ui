from flask import Blueprint, jsonify
from huggingface_hub import scan_cache_dir
from datetime import datetime
import logging

from utils.formatting import format_size

# Create blueprint for API routes
api_bp = Blueprint('api', __name__)

# Cache directory setup
cache_dir = scan_cache_dir()

@api_bp.route('/cache/stats', methods=['GET'])
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

@api_bp.route('/cache/files', methods=['GET'])
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

@api_bp.route('/cache/clear', methods=['POST'])
def clear_cache():
    """Clear the entire cache"""
    try:
        # Clear the cache directory
        cache_dir.clear()
        return jsonify({'message': 'Cache cleared successfully'})
    except Exception as e:
        logger.error(f"Error clearing cache: {str(e)}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/cache/remove/<repo_path>', methods=['DELETE'])
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