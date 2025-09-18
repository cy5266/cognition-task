"""
Tests for basic math operations.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_basic_math():
    """Test that verifies a few basic math problems."""
    assert 2 + 3 == 5
    assert 10 + 15 == 25
    
    assert 10 - 4 == 6
    assert 20 - 8 == 12
    
    assert 3 * 4 == 12
    assert 7 * 6 == 42
    
    assert 15 / 3 == 5
    assert 24 / 6 == 4
    
    assert -5 + 8 == 3
    assert 10 * -2 == -20
