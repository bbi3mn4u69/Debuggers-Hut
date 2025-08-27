"""
Main application entry point for the Hotel Booking System.

This module orchestrates the booking flow: collect inputs → calculate costs → 
award points → print receipt → update guest points.
"""

import logging
import sys
from typing import Optional

from .data_store import get_rate, add_points
from .calculations import compute_total_cost, points_round_half_up
from .receipt import print_receipt
from .io_prompts import (
    prompt_guest_name, prompt_num_guests, prompt_apartment_id,
    prompt_checkin, prompt_checkout, prompt_length_of_stay, prompt_booking_date
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('hotel_booking.log')
    ]
)

logger = logging.getLogger(__name__)


def run_once() -> bool:
    """
    Execute one complete booking flow.
    
    Returns:
        bool: True if booking was successful, False otherwise
    """
    try:
        logger.info("Starting new booking process")
        
        # Collect inputs
        guest_name = prompt_guest_name()
        num_guests = prompt_num_guests()
        apartment_id = prompt_apartment_id()
        checkin = prompt_checkin()
        checkout = prompt_checkout()
        length_of_stay = prompt_length_of_stay()
        booking_date = prompt_booking_date()

        # Compute totals
        rate = get_rate(apartment_id)
        if rate == 0.0:
            logger.warning(f"Unknown apartment ID: {apartment_id}")
            print(f"\nWarning: Apartment '{apartment_id}' not found. Rate set to $0.00")
        
        total = compute_total_cost(rate, length_of_stay)
        earned = points_round_half_up(total)

        # Print receipt
        print_receipt(
            guest_name=guest_name,
            num_guests=num_guests,
            apartment_id=apartment_id,
            apartment_rate=rate,
            checkin=checkin,
            checkout=checkout,
            length_of_stay=length_of_stay,
            booking_date=booking_date,
            total_cost=total,
            reward_points=earned,
        )

        # Update guest points
        new_total = add_points(guest_name, earned)
        print(f"\n[Info] Guest '{guest_name}' now has {new_total} reward points.")
        
        logger.info(f"Booking completed successfully for {guest_name}")
        return True
        
    except KeyboardInterrupt:
        print("\n\nBooking cancelled by user.")
        logger.info("Booking cancelled by user")
        return False
    except Exception as e:
        logger.error(f"Error during booking process: {e}")
        print(f"\nError: {e}")
        print("Booking could not be completed. Please try again.")
        return False


def run_interactive() -> None:
    """
    Run the application in interactive mode, allowing multiple bookings.
    """
    print("Welcome to the Hotel Booking System!")
    print("=" * 50)
    
    while True:
        try:
            success = run_once()
            
            if not success:
                continue
            
            # Ask if user wants to make another booking
            while True:
                response = input("\nWould you like to make another booking? (y/n): ").strip().lower()
                if response in ['y', 'yes']:
                    print("\n" + "=" * 50)
                    break
                elif response in ['n', 'no']:
                    print("\nThank you for using the Hotel Booking System!")
                    logger.info("Application terminated by user")
                    return
                else:
                    print("Please enter 'y' or 'n'.")
                    
        except KeyboardInterrupt:
            print("\n\nThank you for using the Hotel Booking System!")
            logger.info("Application terminated by user")
            return


def main() -> None:
    """
    Main entry point for the application.
    """
    try:
        run_interactive()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
