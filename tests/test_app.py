"""
Tests for the Flask application.
"""
import sys
import os
import pytest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_app_imports_successfully():
    """Test that the app module can be imported with mocked environment variables."""
    with patch.dict(os.environ, {
        'GITHUB_TOKEN': 'test_token',
        'GITHUB_OWNER': 'test_owner', 
        'GITHUB_REPO': 'test_repo',
        'DEVIN_API_KEY': 'test_key'
    }):
        import app
        assert hasattr(app, 'app')
        assert app.app is not None

def test_flask_app_creation():
    """Test that Flask app is created successfully with environment variables."""
    with patch.dict(os.environ, {
        'GITHUB_TOKEN': 'test_token',
        'GITHUB_OWNER': 'test_owner',
        'GITHUB_REPO': 'test_repo', 
        'DEVIN_API_KEY': 'test_key'
    }):
        import app
        assert app.app.name == 'app'
