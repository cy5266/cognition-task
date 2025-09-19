"""
Tests for the main application.
"""
import sys
import os
import subprocess

def test_app_file_exists():
    """Test that app.py file exists."""
    app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app.py')
    assert os.path.exists(app_path)

def test_requirements_has_pytest():
    """Test that requirements.txt includes pytest."""
    req_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'requirements.txt')
    with open(req_path, 'r') as f:
        content = f.read()
    assert 'pytest' in content

def test_streamlit_syntax_check():
    """Test that app.py has valid Python syntax."""
    app_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'app.py')
    result = subprocess.run([sys.executable, '-m', 'py_compile', app_path], 
                          capture_output=True, text=True)
    assert result.returncode == 0, f"Syntax error in app.py: {result.stderr}"
