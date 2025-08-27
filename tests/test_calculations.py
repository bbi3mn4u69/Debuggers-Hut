"""
Unit tests for the calculations module.
"""

import pytest
from hotel_booking.calculations import (
    compute_total_cost, 
    points_round_half_up,
    calculate_discount,
    calculate_final_cost
)


class TestComputeTotalCost:
    """Test cases for compute_total_cost function."""
    
    def test_normal_calculation(self):
        """Test normal cost calculation."""
        result = compute_total_cost(100.0, 3)
        assert result == 300.0
    
    def test_zero_rate(self):
        """Test calculation with zero rate."""
        result = compute_total_cost(0.0, 5)
        assert result == 0.0
    
    def test_zero_nights(self):
        """Test calculation with zero nights."""
        result = compute_total_cost(100.0, 0)
        assert result == 0.0
    
    def test_negative_rate(self):
        """Test that negative rate raises ValueError."""
        with pytest.raises(ValueError, match="Rate cannot be negative"):
            compute_total_cost(-50.0, 2)
    
    def test_negative_nights(self):
        """Test that negative nights raises ValueError."""
        with pytest.raises(ValueError, match="Number of nights cannot be negative"):
            compute_total_cost(100.0, -1)


class TestPointsRoundHalfUp:
    """Test cases for points_round_half_up function."""
    
    def test_exact_half(self):
        """Test rounding up at exactly 0.5."""
        result = points_round_half_up(599.5)
        assert result == 600
    
    def test_less_than_half(self):
        """Test rounding down when less than 0.5."""
        result = points_round_half_up(350.4)
        assert result == 350
    
    def test_more_than_half(self):
        """Test rounding up when more than 0.5."""
        result = points_round_half_up(350.6)
        assert result == 351
    
    def test_whole_number(self):
        """Test with whole number."""
        result = points_round_half_up(100.0)
        assert result == 100
    
    def test_zero(self):
        """Test with zero."""
        result = points_round_half_up(0.0)
        assert result == 0
    
    def test_negative_amount(self):
        """Test that negative amount raises ValueError."""
        with pytest.raises(ValueError, match="Amount cannot be negative"):
            points_round_half_up(-50.0)


class TestCalculateDiscount:
    """Test cases for calculate_discount function."""
    
    def test_normal_discount(self):
        """Test normal discount calculation."""
        result = calculate_discount(100.0, 10.0)
        assert result == 10.0
    
    def test_zero_discount(self):
        """Test zero discount."""
        result = calculate_discount(100.0, 0.0)
        assert result == 0.0
    
    def test_full_discount(self):
        """Test 100% discount."""
        result = calculate_discount(100.0, 100.0)
        assert result == 100.0
    
    def test_negative_original_cost(self):
        """Test that negative original cost raises ValueError."""
        with pytest.raises(ValueError, match="Original cost cannot be negative"):
            calculate_discount(-50.0, 10.0)
    
    def test_invalid_discount_percentage(self):
        """Test that invalid discount percentage raises ValueError."""
        with pytest.raises(ValueError, match="Discount percentage must be between 0 and 100"):
            calculate_discount(100.0, 150.0)
        
        with pytest.raises(ValueError, match="Discount percentage must be between 0 and 100"):
            calculate_discount(100.0, -10.0)


class TestCalculateFinalCost:
    """Test cases for calculate_final_cost function."""
    
    def test_normal_final_cost(self):
        """Test normal final cost calculation."""
        result = calculate_final_cost(100.0, 10.0)
        assert result == 90.0
    
    def test_no_discount(self):
        """Test final cost with no discount."""
        result = calculate_final_cost(100.0)
        assert result == 100.0
    
    def test_discount_greater_than_cost(self):
        """Test that final cost doesn't go below zero."""
        result = calculate_final_cost(50.0, 100.0)
        assert result == 0.0
    
    def test_negative_original_cost(self):
        """Test that negative original cost raises ValueError."""
        with pytest.raises(ValueError, match="Original cost cannot be negative"):
            calculate_final_cost(-50.0, 10.0)
    
    def test_negative_discount(self):
        """Test that negative discount raises ValueError."""
        with pytest.raises(ValueError, match="Discount amount cannot be negative"):
            calculate_final_cost(100.0, -10.0)
