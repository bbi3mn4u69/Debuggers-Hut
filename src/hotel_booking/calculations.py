"""
Business logic and calculations for the Hotel Booking System.
"""

import logging
from typing import Union

logger = logging.getLogger(__name__)


def compute_total_cost(rate: float, nights: int) -> float:
    """
    Calculate total cost for a booking.
    
    Args:
        rate: Nightly rate in AUD
        nights: Number of nights
        
    Returns:
        float: Total cost in AUD
        
    Raises:
        ValueError: If rate or nights are negative
    """
    if rate < 0:
        raise ValueError("Rate cannot be negative")
    
    if nights < 0:
        raise ValueError("Number of nights cannot be negative")
    
    total = rate * nights
    logger.debug(f"Calculated total cost: ${rate:.2f} × {nights} nights = ${total:.2f}")
    return total


def points_round_half_up(amount_aud: float) -> int:
    """
    Calculate reward points with half-up rounding.
    
    Reward points: 1 point per dollar, rounded to nearest integer with HALF-UP rule.
    Examples: 599.50 -> 600, 350.4 -> 350.
    
    Args:
        amount_aud: Amount in AUD
        
    Returns:
        int: Number of reward points earned
        
    Raises:
        ValueError: If amount is negative
    """
    if amount_aud < 0:
        raise ValueError("Amount cannot be negative")
    
    points = int(amount_aud + 0.5)
    logger.debug(f"Calculated reward points: ${amount_aud:.2f} -> {points} points")
    return points


def calculate_discount(original_cost: float, discount_percentage: float) -> float:
    """
    Calculate discount amount.
    
    Args:
        original_cost: Original cost in AUD
        discount_percentage: Discount percentage (0-100)
        
    Returns:
        float: Discount amount in AUD
    """
    if not 0 <= discount_percentage <= 100:
        raise ValueError("Discount percentage must be between 0 and 100")
    
    if original_cost < 0:
        raise ValueError("Original cost cannot be negative")
    
    discount = original_cost * (discount_percentage / 100)
    return round(discount, 2)


def calculate_final_cost(original_cost: float, discount_amount: float = 0.0) -> float:
    """
    Calculate final cost after applying discount.
    
    Args:
        original_cost: Original cost in AUD
        discount_amount: Discount amount in AUD
        
    Returns:
        float: Final cost in AUD
    """
    if original_cost < 0:
        raise ValueError("Original cost cannot be negative")
    
    if discount_amount < 0:
        raise ValueError("Discount amount cannot be negative")
    
    final_cost = original_cost - discount_amount
    return max(0, final_cost)  # Ensure cost doesn't go below zero
