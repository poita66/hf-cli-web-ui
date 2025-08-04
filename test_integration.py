#!/usr/bin/env python3
"""
Integration test for the backend files endpoint
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from main import app


class TestBackendIntegration(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Clean up after each test method."""
        self.app_context.pop()
    
    def test_get_cache_files_integration(self):
        """Integration test for the /api/cache/files endpoint"""
        # Test that the endpoint returns a valid JSON response
        response = self.app.get('/api/cache/files')
        
        # Assert the response
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('files', data)
        self.assertIn('total_count', data)
        
        # The endpoint should return a list of files and a count
        self.assertIsInstance(data['files'], list)
        self.assertIsInstance(data['total_count'], int)
        
        # Even if there are no files, it should return an empty list
        self.assertEqual(data['total_count'], len(data['files']))


if __name__ == '__main__':
    unittest.main()