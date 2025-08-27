"""
Data storage and management for the Hotel Booking System.
"""

import logging
from typing import Dict, Any
from .config import APARTMENTS, GUESTS_POINTS

logger = logging.getLogger(__name__)

# In-memory storage (in production, this would be a database)
# These are now managed by the StorageManager class
_guests_points: Dict[str, int] = GUESTS_POINTS.copy()
_apartments: Dict[str, float] = APARTMENTS.copy()

# Reference to storage manager for synchronization
_storage_manager = None


def get_rate(apartment_id: str) -> float:
    """
    Return nightly rate for a known apartment.
    
    Note:
        - Apartment ID is case-insensitive
        - Apartment ID is stored in lowercase in the storage manager
        - Apartment ID is stored in lowercase in the local storage
        - Apartment ID is stored in lowercase in the _apartments dictionary
        - Apartment ID is stored in lowercase in the _guests_points dictionary
        - Apartment ID is stored in lowercase in the _storage_manager dictionary
    Args:
        apartment_id: The apartment identifier
        
    Returns:
        float: Nightly rate in AUD, 0.0 if apartment not found
    """
    # Try to get from storage manager first, then fall back to local storage
    try:
        from .storage_manager import get_storage_manager
        storage_manager = get_storage_manager()
        apartments = storage_manager.view_apartments()
        
        apartment_id_lower = apartment_id.lower()
        storage_apartments_lower = {k.lower(): v for k, v in apartments.items()}
        
        rate = storage_apartments_lower.get(apartment_id_lower, 0.0)
    except ImportError:
        # Fallback to local storage if storage manager is not available
        apartment_id_lower = apartment_id.lower()
        storage_apartments_lower = {k.lower(): v for k, v in _apartments.items()}
        rate = storage_apartments_lower.get(apartment_id_lower, 0.0)
    
    if rate == 0.0:
        logger.warning(f"Unknown apartment ID: {apartment_id}")
    return rate


def add_points(guest_name: str, earned: int) -> int:
    """
    Create or update a guest's reward points.
    
    Args:
        guest_name: Name of the guest
        earned: Points to add to the guest's account
        
    Returns:
        int: New total points for the guest
    """
    if not guest_name.strip():
        raise ValueError("Guest name cannot be empty")
    
    if earned < 0:
        raise ValueError("Earned points cannot be negative")
    
    # Try to use storage manager first, then fall back to local storage
    try:
        from .storage_manager import get_storage_manager
        storage_manager = get_storage_manager()
        current_points = storage_manager.view_guests().get(guest_name, 0)
        new_total = current_points + earned
        storage_manager.update_guest_points(guest_name, new_total)
    except ImportError:
        # Fallback to local storage if storage manager is not available
        current_points = _guests_points.get(guest_name, 0)
        new_total = current_points + earned
        _guests_points[guest_name] = new_total
    
    logger.info(f"Added {earned} points to {guest_name}. New total: {new_total}")
    return new_total


def get_guest_points(guest_name: str) -> int:
    """
    Get current points for a guest.
    
    Args:
        guest_name: Name of the guest
        
    Returns:
        int: Current points balance
    """
    # Try to get from storage manager first, then fall back to local storage
    try:
        from .storage_manager import get_storage_manager
        storage_manager = get_storage_manager()
        guests = storage_manager.view_guests()
        return guests.get(guest_name, 0)
    except ImportError:
        # Fallback to local storage if storage manager is not available
        return _guests_points.get(guest_name, 0)


def get_all_apartments() -> Dict[str, float]:
    """
    Get all available apartments and their rates.
    
    Returns:
        Dict[str, float]: Dictionary of apartment IDs and their rates
    """
    # Try to get from storage manager first, then fall back to local storage
    try:
        from .storage_manager import get_storage_manager
        storage_manager = get_storage_manager()
        return storage_manager.view_apartments()
    except (ImportError, Exception) as e:
        # Fallback to local storage if storage manager is not available
        logger.warning(f"Storage manager not available, using local storage: {e}")
        return _apartments.copy()


def get_all_guests() -> Dict[str, int]:
    """
    Get all guests and their current points.
    
    Returns:
        Dict[str, int]: Dictionary of guest names and their points
    """
    # Try to get from storage manager first, then fall back to local storage
    try:
        from .storage_manager import get_storage_manager
        storage_manager = get_storage_manager()
        return storage_manager.view_guests()
    except (ImportError, Exception) as e:
        # Fallback to local storage if storage manager is not available
        logger.warning(f"Storage manager not available, using local storage: {e}")
        return _guests_points.copy()
