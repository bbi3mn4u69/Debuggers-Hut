"""
User input handling and validation for the Hotel Booking System.
"""

import logging
from typing import Optional
from datetime import datetime
from .config import DATE_FORMAT

logger = logging.getLogger(__name__)

DATE_FORMAT = 'd/m/yyyy'
_DATETIME_FORMAT = '%d/%m/%Y' 

def prompt_guest_name() -> str:
    """
    Prompt for guest name with validation.
    
    Returns:
        str: Validated guest name
    """
    while True:
        try:
            name = input("Enter the guest's name: ").strip()
            if not name:
                print("Error: Guest name cannot be empty. Please try again.")
                continue
            
            if len(name) > 100:
                print("Error: Guest name is too long. Please use a shorter name.")
                continue
            
            logger.debug(f"Guest name entered: {name}")
            return name
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise
        except Exception as e:
            logger.error(f"Error getting guest name: {e}")
            print("An error occurred. Please try again.")


def prompt_num_guests() -> int:
    """
    Prompt for number of guests with validation.
    
    Returns:
        int: Validated number of guests
    """
    while True:
        try:
            num_str = input("Enter number of guests: ").strip()
            num_guests = int(num_str)
            
            if num_guests <= 0:
                print("Error: Number of guests must be positive. Please try again.")
                continue
            
            if num_guests > 20:
                print("Error: Maximum 20 guests allowed. Please try again.")
                continue
            
            logger.debug(f"Number of guests entered: {num_guests}")
            return num_guests
            
        except ValueError:
            print("Error: Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise
        except Exception as e:
            logger.error(f"Error getting number of guests: {e}")
            print("An error occurred. Please try again.")


def prompt_apartment_id() -> str:
    """
    Prompt for apartment ID with validation.
    
    Returns:
        str: Validated apartment ID
    """
    while True:
        try:
            apartment_id = input("Enter apartment ID (e.g., U12swan): ").strip()
            if not apartment_id:
                print("Error: Apartment ID cannot be empty. Please try again.")
                continue
            
            if len(apartment_id) > 20:
                print("Error: Apartment ID is too long. Please try again.")
                continue
            
            logger.debug(f"Apartment ID entered: {apartment_id}")
            return apartment_id
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise
        except Exception as e:
            logger.error(f"Error getting apartment ID: {e}")
            print("An error occurred. Please try again.")


def _validate_date(date_str: str) -> bool:
    """
    Validate date string format.
    
    Args:
        date_str: Date string to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        datetime.strptime(date_str, _DATETIME_FORMAT)
        return True
    except ValueError:
        return False


def prompt_checkin() -> str:
    """
    Prompt for check-in date.
    
    Returns:
        str: Check-in date in d/m/yyyy format
    """
    while True:
        try:
            checkin = input(f"Enter check-in date ({DATE_FORMAT}): ").strip()
            if not checkin:
                print("Error: Check-in date cannot be empty. Please try again.")
                continue
            if not _validate_date(checkin):
                print(f"Error: Invalid date format. Please use {DATE_FORMAT} and try again.")
                continue
            logger.debug(f"Check-in date entered: {checkin}")
            return checkin
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise
        except Exception as e:
            logger.error(f"Error getting check-in date: {e}")
            print("An error occurred. Please try again.")


def prompt_checkout() -> str:
    """
    Prompt for check-out date.
    
    Returns:
        str: Check-out date in d/m/yyyy format
    """
    while True:
        try:
            checkout = input(f"Enter check-out date ({DATE_FORMAT}): ").strip()
            if not checkout:
                print("Error: Check-out date cannot be empty. Please try again.")
                continue
            if not _validate_date(checkout):
                print(f"Error: Invalid date format. Please use {DATE_FORMAT} and try again.")
                continue
            
            logger.debug(f"Check-out date entered: {checkout}")
            return checkout
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise
        except Exception as e:
            logger.error(f"Error getting check-out date: {e}")
            print("An error occurred. Please try again.")


def prompt_length_of_stay() -> int:
    """
    Prompt for length of stay with validation.
    
    Returns:
        int: Validated length of stay in nights
    """
    while True:
        try:
            nights_str = input("Enter length of stay (nights): ").strip()
            nights = int(nights_str)
            
            if nights <= 0:
                print("Error: Length of stay must be positive. Please try again.")
                continue
            
            if nights > 365:
                print("Error: Maximum stay is 365 nights. Please try again.")
                continue
            
            logger.debug(f"Length of stay entered: {nights} nights")
            return nights
            
        except ValueError:
            print("Error: Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise
        except Exception as e:
            logger.error(f"Error getting length of stay: {e}")
            print("An error occurred. Please try again.")


def prompt_booking_date() -> str:
    """
    Prompt for booking date.
    
    Returns:
        str: Booking date in d/m/yyyy format
    """
    while True:
        try:
            booking_date = input(f"Enter booking date ({DATE_FORMAT}): ").strip()
            if not booking_date:
                print("Error: Booking date cannot be empty. Please try again.")
                continue
            
            logger.debug(f"Booking date entered: {booking_date}")
            return booking_date
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise
        except Exception as e:
            logger.error(f"Error getting booking date: {e}")
            print("An error occurred. Please try again.")
