#!/usr/bin/env python3
"""
Unit tests for the backend endpoints
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from main import app


class TestBackendEndpoints(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Clean up after each test method."""
        self.app_context.pop()
    
    @patch('app.cache_dir')
    def test_get_cache_stats(self, mock_cache_dir):
        """Test the /api/cache/stats endpoint"""
        # Mock the cache_dir object
        mock_cache_dir.size_on_disk = 1024
        mock_cache_dir.repos = []
        
        # Make the request
        response = self.app.get('/api/cache/stats')
        
        # Assert the response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('size', data)
        self.assertIn('size_formatted', data)
        self.assertIn('folders', data)
        self.assertIn('files', data)
        self.assertIn('last_updated', data)
    
    @patch('app.cache_dir')
    def test_get_cache_files(self, mock_cache_dir):
        """Test the /api/cache/files endpoint"""
        # Mock the cache_dir object
        mock_repo = MagicMock()
        mock_repo.repo_path = "/mock/repo/path"
        mock_repo.size_on_disk = 1024
        mock_repo.last_accessed = 1234567890
        
        # Mock revisions
        mock_revision = MagicMock()
        mock_revision.files = []
        
        # Mock a file in the revision
        mock_file = MagicMock()
        mock_file.file_path = "/mock/file/path"
        mock_file.size_on_disk = 512
        mock_file.blob_last_accessed = 1234567890
        
        # Set up the mock hierarchy
        mock_revision.files = [mock_file]
        mock_repo.revisions = [mock_revision]
        
        mock_cache_dir.repos = [mock_repo]
        
        # Make the request
        response = self.app.get('/api/cache/files')
        
        # Assert the response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('files', data)
        self.assertIn('total_count', data)
        # We expect 1 file to be returned
        self.assertEqual(len(data['files']), 1)
        
        # Check that the response contains expected fields
        file_data = data['files'][0]
        self.assertIn('path', file_data)
        self.assertIn('size', file_data)
        self.assertIn('size_formatted', file_data)
        self.assertIn('last_accessed', file_data)
        self.assertIn('folder', file_data)


if __name__ == '__main__':
    unittest.main()