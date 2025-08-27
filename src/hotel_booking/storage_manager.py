"""
Storage Management Utility for the Hotel Booking System.

This module provides tools to view, manage, and manipulate the in-memory storage
used by the application.
"""

import logging
from typing import Dict, List, Optional, Tuple
from .data_store import get_all_apartments, get_all_guests
from .config import APARTMENTS, GUESTS_POINTS

logger = logging.getLogger(__name__)


class StorageManager:
    """
    Manages the in-memory storage for apartments and guest points.
    """
    
    def __init__(self):
        """Initialize the storage manager."""
        self._apartments = APARTMENTS.copy()
        self._guests_points = GUESTS_POINTS.copy()
    
    def view_all_storage(self) -> Dict[str, Dict]:
        """
        View all current storage data.
        
        Returns:
            Dict containing both apartments and guests data
        """
        return {
            "apartments": self._apartments.copy(),
            "guests": self._guests_points.copy()
        }
    
    def view_apartments(self) -> Dict[str, float]:
        """
        View all apartments and their rates.
        
        Returns:
            Dict of apartment IDs and their nightly rates
        """
        return self._apartments.copy()
    
    def view_guests(self) -> Dict[str, int]:
        """
        View all guests and their points.
        
        Returns:
            Dict of guest names and their points
        """
        return self._guests_points.copy()
    
    def get_storage_summary(self) -> Dict[str, any]:
        """
        Get a summary of the current storage.
        
        Returns:
            Dict containing storage statistics
        """
        total_apartments = len(self._apartments)
        total_guests = len(self._guests_points)
        total_points = sum(self._guests_points.values())
        total_value = sum(self._apartments.values())
        
        return {
            "total_apartments": total_apartments,
            "total_guests": total_guests,
            "total_points": total_points,
            "total_apartment_value": total_value,
            "average_rate": total_value / total_apartments if total_apartments > 0 else 0,
            "average_points": total_points / total_guests if total_guests > 0 else 0
        }
    
    def add_apartment(self, apartment_id: str, rate: float) -> bool:
        """
        Add a new apartment to storage.
        
        Args:
            apartment_id: The apartment identifier
            rate: Nightly rate in AUD
            
        Returns:
            bool: True if added successfully, False if apartment already exists
        """
        if apartment_id in self._apartments:
            logger.warning(f"Apartment {apartment_id} already exists")
            return False
        
        if rate <= 0:
            raise ValueError("Rate must be positive")
        
        self._apartments[apartment_id] = rate
        logger.info(f"Added apartment {apartment_id} with rate ${rate:.2f}")
        return True
    
    def update_apartment_rate(self, apartment_id: str, new_rate: float) -> bool:
        """
        Update the rate of an existing apartment.
        
        Args:
            apartment_id: The apartment identifier
            new_rate: New nightly rate in AUD
            
        Returns:
            bool: True if updated successfully, False if apartment doesn't exist
        """
        if apartment_id not in self._apartments:
            logger.warning(f"Apartment {apartment_id} not found")
            return False
        
        if new_rate <= 0:
            raise ValueError("Rate must be positive")
        
        old_rate = self._apartments[apartment_id]
        self._apartments[apartment_id] = new_rate
        logger.info(f"Updated apartment {apartment_id} rate from ${old_rate:.2f} to ${new_rate:.2f}")
        return True
    
    def delete_apartment(self, apartment_id: str) -> bool:
        """
        Delete an apartment from storage.
        
        Args:
            apartment_id: The apartment identifier
            
        Returns:
            bool: True if deleted successfully, False if apartment doesn't exist
        """
        if apartment_id not in self._apartments:
            logger.warning(f"Apartment {apartment_id} not found")
            return False
        
        rate = self._apartments.pop(apartment_id)
        logger.info(f"Deleted apartment {apartment_id} with rate ${rate:.2f}")
        return True
    
    def add_guest(self, guest_name: str, initial_points: int = 0) -> bool:
        """
        Add a new guest to storage.
        
        Args:
            guest_name: The guest's name
            initial_points: Initial points balance (default: 0)
            
        Returns:
            bool: True if added successfully, False if guest already exists
        """
        if guest_name in self._guests_points:
            logger.warning(f"Guest {guest_name} already exists")
            return False
        
        if initial_points < 0:
            raise ValueError("Initial points cannot be negative")
        
        self._guests_points[guest_name] = initial_points
        logger.info(f"Added guest {guest_name} with {initial_points} points")
        return True
    
    def update_guest_points(self, guest_name: str, new_points: int) -> bool:
        """
        Update a guest's points balance.
        
        Args:
            guest_name: The guest's name
            new_points: New points balance
            
        Returns:
            bool: True if updated successfully, False if guest doesn't exist
        """
        if guest_name not in self._guests_points:
            logger.warning(f"Guest {guest_name} not found")
            return False
        
        if new_points < 0:
            raise ValueError("Points cannot be negative")
        
        old_points = self._guests_points[guest_name]
        self._guests_points[guest_name] = new_points
        logger.info(f"Updated guest {guest_name} points from {old_points} to {new_points}")
        return True
    
    def delete_guest(self, guest_name: str) -> bool:
        """
        Delete a guest from storage.
        
        Args:
            guest_name: The guest's name
            
        Returns:
            bool: True if deleted successfully, False if guest doesn't exist
        """
        if guest_name not in self._guests_points:
            logger.warning(f"Guest {guest_name} not found")
            return False
        
        points = self._guests_points.pop(guest_name)
        logger.info(f"Deleted guest {guest_name} with {points} points")
        return True
    
    def clear_all_apartments(self) -> int:
        """
        Clear all apartments from storage.
        
        Returns:
            int: Number of apartments cleared
        """
        count = len(self._apartments)
        self._apartments.clear()
        logger.info(f"Cleared all {count} apartments from storage")
        return count
    
    def clear_all_guests(self) -> int:
        """
        Clear all guests from storage.
        
        Returns:
            int: Number of guests cleared
        """
        count = len(self._guests_points)
        self._guests_points.clear()
        logger.info(f"Cleared all {count} guests from storage")
        return count
    
    def clear_all_storage(self) -> Dict[str, int]:
        """
        Clear all storage data.
        
        Returns:
            Dict containing counts of cleared items
        """
        apartments_cleared = self.clear_all_apartments()
        guests_cleared = self.clear_all_guests()
        
        return {
            "apartments_cleared": apartments_cleared,
            "guests_cleared": guests_cleared
        }
    
    def reset_to_defaults(self) -> Dict[str, int]:
        """
        Reset storage to default values from config.
        
        Returns:
            Dict containing counts of reset items
        """
        self._apartments = APARTMENTS.copy()
        self._guests_points = GUESTS_POINTS.copy()
        
        logger.info("Storage reset to default values")
        return {
            "apartments_reset": len(self._apartments),
            "guests_reset": len(self._guests_points)
        }
    
    def search_apartments(self, search_term: str) -> Dict[str, float]:
        """
        Search apartments by ID (case-insensitive).
        
        Args:
            search_term: Search term to match against apartment IDs
            
        Returns:
            Dict of matching apartments
        """
        search_term = search_term.lower()
        matches = {
            apt_id: rate for apt_id, rate in self._apartments.items()
            if search_term in apt_id.lower()
        }
        return matches
    
    def search_guests(self, search_term: str) -> Dict[str, int]:
        """
        Search guests by name (case-insensitive).
        
        Args:
            search_term: Search term to match against guest names
            
        Returns:
            Dict of matching guests
        """
        search_term = search_term.lower()
        matches = {
            name: points for name, points in self._guests_points.items()
            if search_term in name.lower()
        }
        return matches
    
    def get_top_guests(self, limit: int = 5) -> List[Tuple[str, int]]:
        """
        Get guests with the highest points.
        
        Args:
            limit: Maximum number of guests to return
            
        Returns:
            List of tuples (guest_name, points) sorted by points descending
        """
        sorted_guests = sorted(
            self._guests_points.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_guests[:limit]
    
    def get_expensive_apartments(self, limit: int = 5) -> List[Tuple[str, float]]:
        """
        Get apartments with the highest rates.
        
        Args:
            limit: Maximum number of apartments to return
            
        Returns:
            List of tuples (apartment_id, rate) sorted by rate descending
        """
        sorted_apartments = sorted(
            self._apartments.items(),
            key=lambda x: x[1],
            reverse=True
        )
        return sorted_apartments[:limit]


# Global storage manager instance
storage_manager = StorageManager()


def get_storage_manager() -> StorageManager:
    """
    Get the global storage manager instance.
    
    Returns:
        StorageManager: The global storage manager
    """
    return storage_manager
