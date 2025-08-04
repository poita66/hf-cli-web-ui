#!/usr/bin/env python3
"""
Direct tests for the API modules to verify they work correctly with the new structure
"""

import sys
import os
import unittest
from unittest.mock import patch, MagicMock

# Add the backend directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_api_imports():
    """Test that API modules can be imported correctly"""
    try:
        # Test importing the API modules directly
        from api import cache
        from api import downloads
        print("✓ API modules imported successfully")
        
        # Test that the blueprint is correctly defined
        assert hasattr(cache, 'api_bp'), "cache module should have api_bp"
        assert hasattr(downloads, 'api_bp'), "downloads module should have api_bp"
        print("✓ API blueprints are correctly defined")
        
        return True
    except Exception as e:
        print(f"✗ Error importing API modules: {e}")
        return False

def test_utils_imports():
    """Test that utility modules can be imported correctly"""
    try:
        from utils import formatting
        print("✓ Formatting module imported successfully")
        return True
    except Exception as e:
        print(f"✗ Error importing formatting module: {e}")
        return False

if __name__ == "__main__":
    print("Testing API module imports...")
    success1 = test_api_imports()
    success2 = test_utils_imports()
    
    if success1 and success2:
        print("\n🎉 All API module tests passed!")
    else:
        print("\n💥 Some API module tests failed.")
