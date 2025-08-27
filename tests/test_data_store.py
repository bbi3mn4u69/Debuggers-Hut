"""
Unit tests for the data_store module.
"""

import pytest
from hotel_booking.data_store import (
    get_rate,
    add_points,
    get_guest_points,
    get_all_apartments,
    get_all_guests
)


class TestGetRate:
    """Test cases for get_rate function."""
    
    def test_existing_apartment(self):
        """Test getting rate for existing apartment."""
        result = get_rate("U12swan")
        assert result == 95.0
    
    def test_another_existing_apartment(self):
        """Test getting rate for another existing apartment."""
        result = get_rate("U209duck")
        assert result == 106.7
    
    def test_nonexistent_apartment(self):
        """Test getting rate for non-existent apartment."""
        result = get_rate("nonexistent")
        assert result == 0.0
    
    def test_empty_string(self):
        """Test getting rate with empty string."""
        result = get_rate("")
        assert result == 0.0


class TestAddPoints:
    """Test cases for add_points function."""
    
    def test_add_points_to_existing_guest(self):
        """Test adding points to existing guest."""
        # Reset to known state
        initial_points = get_guest_points("Alyssa")
        result = add_points("Alyssa", 10)
        assert result == initial_points + 10
    
    def test_add_points_to_new_guest(self):
        """Test adding points to new guest."""
        result = add_points("NewGuest", 25)
        assert result == 25
    
    def test_add_zero_points(self):
        """Test adding zero points."""
        result = add_points("TestGuest", 0)
        assert result == 0
    
    def test_empty_guest_name(self):
        """Test that empty guest name raises ValueError."""
        with pytest.raises(ValueError, match="Guest name cannot be empty"):
            add_points("", 10)
    
    def test_whitespace_guest_name(self):
        """Test that whitespace-only guest name raises ValueError."""
        with pytest.raises(ValueError, match="Guest name cannot be empty"):
            add_points("   ", 10)
    
    def test_negative_points(self):
        """Test that negative points raises ValueError."""
        with pytest.raises(ValueError, match="Earned points cannot be negative"):
            add_points("TestGuest", -5)


class TestGetGuestPoints:
    """Test cases for get_guest_points function."""
    
    def test_existing_guest(self):
        """Test getting points for existing guest."""
        points = get_guest_points("Alyssa")
        assert isinstance(points, int)
        assert points >= 0
    
    def test_nonexistent_guest(self):
        """Test getting points for non-existent guest."""
        result = get_guest_points("NonexistentGuest")
        assert result == 0
    
    def test_empty_string(self):
        """Test getting points with empty string."""
        result = get_guest_points("")
        assert result == 0


class TestGetAllApartments:
    """Test cases for get_all_apartments function."""
    
    def test_returns_copy(self):
        """Test that function returns a copy, not the original."""
        apartments = get_all_apartments()
        assert isinstance(apartments, dict)
        assert len(apartments) > 0
        
        # Modify the returned dict and ensure it doesn't affect the original
        apartments["test"] = 999.0
        apartments_again = get_all_apartments()
        assert "test" not in apartments_again
    
    def test_contains_expected_apartments(self):
        """Test that returned dict contains expected apartments."""
        apartments = get_all_apartments()
        assert "U12swan" in apartments
        assert "U209duck" in apartments
        assert "U49goose" in apartments


class TestGetAllGuests:
    """Test cases for get_all_guests function."""
    
    def test_returns_copy(self):
        """Test that function returns a copy, not the original."""
        guests = get_all_guests()
        assert isinstance(guests, dict)
        assert len(guests) > 0
        
        # Modify the returned dict and ensure it doesn't affect the original
        guests["test"] = 999
        guests_again = get_all_guests()
        assert "test" not in guests_again
    
    def test_contains_expected_guests(self):
        """Test that returned dict contains expected guests."""
        guests = get_all_guests()
        assert "Alyssa" in guests
        assert "Luigi" in guests
