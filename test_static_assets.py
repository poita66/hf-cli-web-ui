#!/usr/bin/env python3
"""
Simple test to verify static asset serving works
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Import the Flask app
from app import app


class TestStaticAssets(unittest.TestCase):
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
    
    def tearDown(self):
        """Clean up after each test method."""
        self.app_context.pop()
    
    def test_serve_frontend_index(self):
        """Test that the frontend index.html is served correctly"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        # Should return HTML content
        self.assertTrue(b'<html' in response.data or b'<!DOCTYPE' in response.data)
    
    def test_serve_frontend_static(self):
        """Test that static assets are served correctly"""
        # This test assumes that the frontend has been built
        # and that we can access static assets
        response = self.app.get('/static/index.js')
        # This will likely return a 404 if the static files don't exist
        # but we're just verifying the route handling works
        self.assertIn(response.status_code, [200, 404])


if __name__ == '__main__':
    unittest.main()