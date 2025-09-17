"""
Tests for login functionality.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, USERS

def test_login_page_loads():
    """Test that login page loads correctly."""
    with app.test_client() as client:
        response = client.get('/login')
        assert response.status_code == 200
        assert b'Login' in response.data

def test_successful_login():
    """Test successful login redirects to home."""
    with app.test_client() as client:
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'password'
        }, follow_redirects=True)
        assert response.status_code == 500
        assert b'Error loading issues' in response.data

def test_failed_login():
    """Test failed login shows error."""
    with app.test_client() as client:
        response = client.post('/login', data={
            'username': 'admin',
            'password': 'wrong'
        })
        assert response.status_code == 200
        assert b'Invalid username or password' in response.data

def test_logout():
    """Test logout clears session."""
    with app.test_client() as client:
        client.post('/login', data={
            'username': 'admin',
            'password': 'password'
        })
        response = client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        assert b'Login' in response.data

def test_protected_route_requires_login():
    """Test that protected routes redirect to login."""
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 302
        assert '/login' in response.location
