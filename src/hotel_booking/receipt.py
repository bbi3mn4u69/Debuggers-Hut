"""
Receipt formatting and printing for the Hotel Booking System.
"""

import logging
from typing import Optional
from .config import HOTEL_NAME, CURRENCY

logger = logging.getLogger(__name__)


def print_receipt(
    guest_name: str,
    num_guests: int,
    apartment_id: str,
    apartment_rate: float,
    checkin: str,
    checkout: str,
    length_of_stay: int,
    booking_date: str,
    total_cost: float,
    reward_points: int,
    discount_amount: float = 0.0,
) -> None:
    """
    Print a formatted booking receipt.
    
    Args:
        guest_name: Name of the guest
        num_guests: Number of guests
        apartment_id: Apartment identifier
        apartment_rate: Nightly rate in AUD
        checkin: Check-in date
        checkout: Check-out date
        length_of_stay: Number of nights
        booking_date: Date of booking
        total_cost: Total cost in AUD
        reward_points: Points earned
        discount_amount: Discount amount (optional)
    """
    try:
        line = "=" * 57
        print(line)
        print(f"               {HOTEL_NAME} - Booking Receipt")
        print(line)
        
        print(f"\nGuest Name:  {guest_name}")
        print(f"Number of guests: {num_guests}")
        print(f"Apartment name:  {apartment_id}")
        print(f"Apartment rate:  ${apartment_rate:.2f} ({CURRENCY})")
        print(f"Check-in date:  {checkin}")
        print(f"Check-out date:  {checkout}")
        print(f"Length of stay: {length_of_stay} (nights)")
        print(f"Booking date:  {booking_date}")
        
        print("-" * 80)
        
        if discount_amount > 0:
            print(f"Subtotal:           ${total_cost + discount_amount:.2f} ({CURRENCY})")
            print(f"Discount:           -${discount_amount:.2f} ({CURRENCY})")
        
        print(f"Total cost:          ${total_cost:.2f} ({CURRENCY})")
        print(f"Earned rewards:        {reward_points} (points)\n")
        
        print("Thank you for your booking! We hope you will have an enjoyable stay.")
        print(line)
        
        logger.info(f"Receipt printed for {guest_name} - Total: ${total_cost:.2f}")
        
    except Exception as e:
        logger.error(f"Error printing receipt: {e}")
        print("Error: Could not print receipt properly.")


def format_currency(amount: float) -> str:
    """
    Format amount as currency string.
    
    Args:
        amount: Amount to format
        
    Returns:
        str: Formatted currency string
    """
    return f"${amount:.2f} ({CURRENCY})"


def create_receipt_text(
    guest_name: str,
    num_guests: int,
    apartment_id: str,
    apartment_rate: float,
    checkin: str,
    checkout: str,
    length_of_stay: int,
    booking_date: str,
    total_cost: float,
    reward_points: int,
    discount_amount: float = 0.0,
) -> str:
    """
    Create receipt text without printing (useful for testing or saving to file).
    
    Args:
        guest_name: Name of the guest
        num_guests: Number of guests
        apartment_id: Apartment identifier
        apartment_rate: Nightly rate in AUD
        checkin: Check-in date
        checkout: Check-out date
        length_of_stay: Number of nights
        booking_date: Date of booking
        total_cost: Total cost in AUD
        reward_points: Points earned
        discount_amount: Discount amount (optional)
        
    Returns:
        str: Formatted receipt text
    """
    lines = []
    line = "=" * 57
    
    lines.append(line)
    lines.append(f"               {HOTEL_NAME} - Booking Receipt")
    lines.append(line)
    lines.append("")
    lines.append(f"Guest Name:  {guest_name}")
    lines.append(f"Number of guests: {num_guests}")
    lines.append(f"Apartment name:  {apartment_id}")
    lines.append(f"Apartment rate:  {format_currency(apartment_rate)}")
    lines.append(f"Check-in date:  {checkin}")
    lines.append(f"Check-out date:  {checkout}")
    lines.append(f"Length of stay: {length_of_stay} (nights)")
    lines.append(f"Booking date:  {booking_date}")
    lines.append("-" * 80)
    
    if discount_amount > 0:
        lines.append(f"Subtotal:           {format_currency(total_cost + discount_amount)}")
        lines.append(f"Discount:           -{format_currency(discount_amount)}")
    
    lines.append(f"Total cost:          {format_currency(total_cost)}")
    lines.append(f"Earned rewards:        {reward_points} (points)")
    lines.append("")
    lines.append("Thank you for your booking! We hope you will have an enjoyable stay.")
    lines.append(line)
    
    return "\n".join(lines)
