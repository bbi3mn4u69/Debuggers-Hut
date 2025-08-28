"""
Receipt formatting and printing for the Hotel Booking System (Part 2).
"""

import logging
from typing import Optional

from .config import HOTEL_NAME, CURRENCY

logger = logging.getLogger(__name__)
LINE = "=" * 57


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
    supp_items: list[tuple[str, int, float]] | None = None,  # (id, qty, price)
    supp_subtotal: float | None = None,
) -> None:
    """
    Print a formatted booking receipt with optional supplementary items section.
    """
    try:
        print(LINE)
        print(f"               {HOTEL_NAME} - Booking Receipt")
        print(LINE)

        print(f"\nGuest Name:  {guest_name}")
        print(f"Number of guests: {num_guests}")
        print(f"Apartment name:  {apartment_id}")
        print(f"Apartment rate:  ${apartment_rate:.2f} ({CURRENCY})")
        print(f"Check-in date:  {checkin}")
        print(f"Check-out date:  {checkout}")
        print(f"Length of stay: {length_of_stay} (nights)")
        print(f"Booking date:  {booking_date}")
        print("-" * 80)

        # Supplementary items (only if present)
        if supp_items:
            print("Supplementary items")
            for iid, qty, price in supp_items:
                cost = price * qty
                print(f"Item id:  {iid}")
                print(f"Quantity:  {qty}")
                print(f"Price:   ${price:.2f}")
                print(f"Cost:   ${cost:.2f}\n")
            if supp_subtotal is not None:
                print(f"Sub-total:  ${supp_subtotal:.2f}")
            print("-" * 80)

        if discount_amount > 0:
            print(f"Subtotal:           ${total_cost + discount_amount:.2f} ({CURRENCY})")
            print(f"Discount:           -${discount_amount:.2f} ({CURRENCY})")

        print(f"Total cost:          ${total_cost:.2f} ({CURRENCY})")
        print(f"Earned rewards:        {reward_points} (points)\n")
        print("Thank you for your booking! We hope you will have an enjoyable stay.")
        print(LINE)

        logger.info("Receipt printed for %s - Total: $%.2f", guest_name, total_cost)

    except Exception as e:
        logger.error("Error printing receipt: %s", e)
        print("Error: Could not print receipt properly.")


def format_currency(amount: float) -> str:
    return f"${amount:.2f} ({CURRENCY})"
