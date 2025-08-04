#!/usr/bin/env python3
"""Test script to verify the modular structure works correctly"""

import sys
import os

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

def test_imports():
    """Test that all modules can be imported correctly"""
    try:
        # Test importing the main module
        import main
        print("✓ main module imported successfully")
        
        # Test importing the API modules
        from api import cache
        from api import downloads
        print("✓ API modules imported successfully")
        
        # Test importing the utils
        from utils import formatting
        print("✓ Formatting module imported successfully")
        
        print("\nAll modules imported successfully!")
        return True
    except Exception as e:
        print(f"✗ Error importing modules: {e}")
        return False

if __name__ == "__main__":
    test_imports()