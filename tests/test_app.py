"""
Tests for the main application.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import main

def test_main_runs():
    """Test that main function runs without error."""
    main()

def test_main_function_exists():
    """Test that main function is callable."""
    assert callable(main)
