"""
Tests for the main application.
"""
import os

def test_app_file_exists():
    """Test that the app.py file exists."""
    app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.py')
    assert os.path.exists(app_path), "app.py file should exist"

def test_requirements_file_exists():
    """Test that requirements.txt exists and contains expected dependencies."""
    req_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'requirements.txt')
    assert os.path.exists(req_path), "requirements.txt should exist"
    
    with open(req_path, 'r') as f:
        content = f.read()
        assert 'streamlit' in content, "requirements.txt should contain streamlit"
        assert 'requests' in content, "requirements.txt should contain requests"
        assert 'python-dotenv' in content, "requirements.txt should contain python-dotenv"

def test_app_contains_streamlit_imports():
    """Test that app.py contains expected Streamlit imports."""
    app_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'app.py')
    with open(app_path, 'r') as f:
        content = f.read()
        assert 'import streamlit' in content, "app.py should import streamlit"
        assert 'from dotenv import load_dotenv' in content, "app.py should import load_dotenv"
