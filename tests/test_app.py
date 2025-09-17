"""
Tests for the main application.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app

def test_app_exists():
    """Test that Flask app exists."""
    assert app is not None

def test_app_is_flask_instance():
    """Test that app is a Flask instance."""
    from flask import Flask
    assert isinstance(app, Flask)
