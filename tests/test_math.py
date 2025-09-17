"""
Tests for basic math operations.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def test_addition():
    """Test basic addition operations."""
    assert 2 + 3 == 5
    assert 10 + 15 == 25
    assert -5 + 3 == -2
    assert 0 + 0 == 0


def test_subtraction():
    """Test basic subtraction operations."""
    assert 5 - 3 == 2
    assert 10 - 15 == -5
    assert -5 - 3 == -8
    assert 0 - 0 == 0


def test_multiplication():
    """Test basic multiplication operations."""
    assert 2 * 3 == 6
    assert 4 * 5 == 20
    assert -3 * 4 == -12
    assert 0 * 10 == 0


def test_division():
    """Test basic division operations."""
    assert 6 / 2 == 3
    assert 15 / 3 == 5
    assert -12 / 4 == -3
    assert 10 / 2 == 5.0
