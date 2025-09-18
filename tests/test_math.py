"""
Tests for basic math operations.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_basic_arithmetic():
    """Test basic arithmetic operations."""
    assert 2 + 2 == 4
    assert 5 * 3 == 15
    assert 10 / 2 == 5
