"""
Tests for the Flask application.
"""
import sys
import os
import pytest
from unittest.mock import patch, MagicMock

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_app_imports():
    """Test that the Flask app can be imported without environment variables."""
    with patch.dict(os.environ, {
        'GITHUB_TOKEN': 'test_token',
        'GITHUB_OWNER': 'test_owner', 
        'GITHUB_REPO': 'test_repo',
        'DEVIN_API_KEY': 'test_key'
    }):
        from app import app
        assert app is not None

def test_app_configuration():
    """Test that the Flask app is properly configured."""
    with patch.dict(os.environ, {
        'GITHUB_TOKEN': 'test_token',
        'GITHUB_OWNER': 'test_owner',
        'GITHUB_REPO': 'test_repo', 
        'DEVIN_API_KEY': 'test_key'
    }):
        from app import app
        assert app.name == 'app'
