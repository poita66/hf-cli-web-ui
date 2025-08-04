#!/usr/bin/env python3
"""
Comprehensive tests for the backend endpoints
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
    
    @patch('api.cache.cache_dir')
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
    
    @patch('api.cache.cache_dir')
    def test_get_cache_files_empty(self, mock_cache_dir):
        """Test the /api/cache/files endpoint with no files"""
        # Mock the cache_dir object with no repos
        mock_cache_dir.repos = []
        
        # Make the request
        response = self.app.get('/api/cache/files')
        
        # Assert the response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('files', data)
        self.assertIn('total_count', data)
        self.assertEqual(len(data['files']), 0)
        self.assertEqual(data['total_count'], 0)
    
    @patch('api.cache.cache_dir')
    def test_get_cache_files_with_files(self, mock_cache_dir):
        """Test the /api/cache/files endpoint with files present"""
        # Mock a repo with revisions and files
        mock_repo = MagicMock()
        mock_repo.repo_path = "/mock/repo/path"
        
        # Mock a revision with files
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
        
        # Mock the cache_dir object
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
        self.assertEqual(data['total_count'], 1)
        
        # Check that the response contains expected fields
        file_data = data['files'][0]
        self.assertIn('path', file_data)
        self.assertIn('size', file_data)
        self.assertIn('size_formatted', file_data)
        self.assertIn('last_accessed', file_data)
        self.assertIn('folder', file_data)
        
        # Check specific values
        self.assertEqual(file_data['path'], "/mock/file/path")
        self.assertEqual(file_data['size'], 512)
        self.assertEqual(file_data['folder'], "/mock/repo/path")
    
    @patch('api.cache.cache_dir')
    def test_get_cache_files_multiple_files(self, mock_cache_dir):
        """Test the /api/cache/files endpoint with multiple files"""
        # Mock a repo with revisions and files
        mock_repo = MagicMock()
        mock_repo.repo_path = "/mock/repo/path"
        
        # Mock a revision with files
        mock_revision = MagicMock()
        mock_revision.files = []
        
        # Mock multiple files in the revision
        mock_file1 = MagicMock()
        mock_file1.file_path = "/mock/file1/path"
        mock_file1.size_on_disk = 512
        mock_file1.blob_last_accessed = 1234567890
        
        mock_file2 = MagicMock()
        mock_file2.file_path = "/mock/file2/path"
        mock_file2.size_on_disk = 1024
        mock_file2.blob_last_accessed = 1234567891
        
        # Set up the mock hierarchy
        mock_revision.files = [mock_file1, mock_file2]
        mock_repo.revisions = [mock_revision]
        
        # Mock the cache_dir object
        mock_cache_dir.repos = [mock_repo]
        
        # Make the request
        response = self.app.get('/api/cache/files')
        
        # Assert the response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('files', data)
        self.assertIn('total_count', data)
        # We expect 2 files to be returned
        self.assertEqual(len(data['files']), 2)
        self.assertEqual(data['total_count'], 2)
        
        # Check that the response contains expected fields for both files
        file_data1 = data['files'][0]
        file_data2 = data['files'][1]
        self.assertIn('path', file_data1)
        self.assertIn('size', file_data1)
        self.assertIn('size_formatted', file_data1)
        self.assertIn('last_accessed', file_data1)
        self.assertIn('folder', file_data1)
        
        self.assertIn('path', file_data2)
        self.assertIn('size', file_data2)
        self.assertIn('size_formatted', file_data2)
        self.assertIn('last_accessed', file_data2)
        self.assertIn('folder', file_data2)
        
        # Check specific values
        self.assertEqual(file_data1['path'], "/mock/file1/path")
        self.assertEqual(file_data1['size'], 512)
        self.assertEqual(file_data1['folder'], "/mock/repo/path")
        
        self.assertEqual(file_data2['path'], "/mock/file2/path")
        self.assertEqual(file_data2['size'], 1024)
        self.assertEqual(file_data2['folder'], "/mock/repo/path")


if __name__ == '__main__':
    unittest.main()