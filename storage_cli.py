#!/usr/bin/env python3
"""
Storage Management Command Line Interface

This script provides a command-line interface to view and manage
the in-memory storage of the Hotel Booking System.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from hotel_booking.storage_manager import get_storage_manager


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f"  {title}")
    print("=" * 60)


def print_storage_summary(storage_manager):
    """Print a summary of the current storage."""
    summary = storage_manager.get_storage_summary()
    
    print_header("STORAGE SUMMARY")
    print(f"Total Apartments: {summary['total_apartments']}")
    print(f"Total Guests: {summary['total_guests']}")
    print(f"Total Points: {summary['total_points']}")
    print(f"Total Apartment Value: ${summary['total_apartment_value']:.2f}")
    print(f"Average Rate: ${summary['average_rate']:.2f}")
    print(f"Average Points: {summary['average_points']:.1f}")


def print_apartments(storage_manager):
    """Print all apartments."""
    apartments = storage_manager.view_apartments()
    
    print_header("APARTMENTS")
    if not apartments:
        print("No apartments found.")
        return
    
    print(f"{'Apartment ID':<15} {'Rate (AUD)':<12}")
    print("-" * 30)
    for apt_id, rate in sorted(apartments.items()):
        print(f"{apt_id:<15} ${rate:<11.2f}")


def print_guests(storage_manager):
    """Print all guests."""
    guests = storage_manager.view_guests()
    
    print_header("GUESTS")
    if not guests:
        print("No guests found.")
        return
    
    print(f"{'Guest Name':<20} {'Points':<10}")
    print("-" * 35)
    for name, points in sorted(guests.items()):
        print(f"{name:<20} {points:<10}")


def print_top_guests(storage_manager, limit=5):
    """Print top guests by points."""
    top_guests = storage_manager.get_top_guests(limit)
    
    print_header(f"TOP {limit} GUESTS BY POINTS")
    if not top_guests:
        print("No guests found.")
        return
    
    print(f"{'Rank':<5} {'Guest Name':<20} {'Points':<10}")
    print("-" * 40)
    for i, (name, points) in enumerate(top_guests, 1):
        print(f"{i:<5} {name:<20} {points:<10}")


def print_expensive_apartments(storage_manager, limit=5):
    """Print most expensive apartments."""
    expensive_apts = storage_manager.get_expensive_apartments(limit)
    
    print_header(f"TOP {limit} MOST EXPENSIVE APARTMENTS")
    if not expensive_apts:
        print("No apartments found.")
        return
    
    print(f"{'Rank':<5} {'Apartment ID':<15} {'Rate (AUD)':<12}")
    print("-" * 37)
    for i, (apt_id, rate) in enumerate(expensive_apts, 1):
        print(f"{i:<5} {apt_id:<15} ${rate:<11.2f}")


def search_apartments(storage_manager):
    """Search apartments by ID."""
    search_term = input("Enter apartment ID search term: ").strip()
    if not search_term:
        print("Search term cannot be empty.")
        return
    
    matches = storage_manager.search_apartments(search_term)
    
    print_header(f"APARTMENT SEARCH RESULTS: '{search_term}'")
    if not matches:
        print("No apartments found matching the search term.")
        return
    
    print(f"{'Apartment ID':<15} {'Rate (AUD)':<12}")
    print("-" * 30)
    for apt_id, rate in sorted(matches.items()):
        print(f"{apt_id:<15} ${rate:<11.2f}")


def search_guests(storage_manager):
    """Search guests by name."""
    search_term = input("Enter guest name search term: ").strip()
    if not search_term:
        print("Search term cannot be empty.")
        return
    
    matches = storage_manager.search_guests(search_term)
    
    print_header(f"GUEST SEARCH RESULTS: '{search_term}'")
    if not matches:
        print("No guests found matching the search term.")
        return
    
    print(f"{'Guest Name':<20} {'Points':<10}")
    print("-" * 35)
    for name, points in sorted(matches.items()):
        print(f"{name:<20} {points:<10}")


def add_apartment(storage_manager):
    """Add a new apartment."""
    print_header("ADD NEW APARTMENT")
    
    apt_id = input("Enter apartment ID: ").strip()
    if not apt_id:
        print("Apartment ID cannot be empty.")
        return
    
    try:
        rate = float(input("Enter nightly rate (AUD): ").strip())
        if rate <= 0:
            print("Rate must be positive.")
            return
    except ValueError:
        print("Invalid rate. Please enter a valid number.")
        return
    
    if storage_manager.add_apartment(apt_id, rate):
        print(f"✓ Apartment '{apt_id}' added successfully with rate ${rate:.2f}")
    else:
        print(f"✗ Apartment '{apt_id}' already exists")


def update_apartment_rate(storage_manager):
    """Update apartment rate."""
    print_header("UPDATE APARTMENT RATE")
    
    apt_id = input("Enter apartment ID: ").strip()
    if not apt_id:
        print("Apartment ID cannot be empty.")
        return
    
    try:
        new_rate = float(input("Enter new nightly rate (AUD): ").strip())
        if new_rate <= 0:
            print("Rate must be positive.")
            return
    except ValueError:
        print("Invalid rate. Please enter a valid number.")
        return
    
    if storage_manager.update_apartment_rate(apt_id, new_rate):
        print(f"✓ Apartment '{apt_id}' rate updated to ${new_rate:.2f}")
    else:
        print(f"✗ Apartment '{apt_id}' not found")


def delete_apartment(storage_manager):
    """Delete an apartment."""
    print_header("DELETE APARTMENT")
    
    apt_id = input("Enter apartment ID to delete: ").strip()
    if not apt_id:
        print("Apartment ID cannot be empty.")
        return
    
    confirm = input(f"Are you sure you want to delete apartment '{apt_id}'? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Deletion cancelled.")
        return
    
    if storage_manager.delete_apartment(apt_id):
        print(f"✓ Apartment '{apt_id}' deleted successfully")
    else:
        print(f"✗ Apartment '{apt_id}' not found")


def add_guest(storage_manager):
    """Add a new guest."""
    print_header("ADD NEW GUEST")
    
    name = input("Enter guest name: ").strip()
    if not name:
        print("Guest name cannot be empty.")
        return
    
    try:
        initial_points = int(input("Enter initial points (default 0): ").strip() or "0")
        if initial_points < 0:
            print("Points cannot be negative.")
            return
    except ValueError:
        print("Invalid points. Please enter a valid number.")
        return
    
    if storage_manager.add_guest(name, initial_points):
        print(f"✓ Guest '{name}' added successfully with {initial_points} points")
    else:
        print(f"✗ Guest '{name}' already exists")


def update_guest_points(storage_manager):
    """Update guest points."""
    print_header("UPDATE GUEST POINTS")
    
    name = input("Enter guest name: ").strip()
    if not name:
        print("Guest name cannot be empty.")
        return
    
    try:
        new_points = int(input("Enter new points balance: ").strip())
        if new_points < 0:
            print("Points cannot be negative.")
            return
    except ValueError:
        print("Invalid points. Please enter a valid number.")
        return
    
    if storage_manager.update_guest_points(name, new_points):
        print(f"✓ Guest '{name}' points updated to {new_points}")
    else:
        print(f"✗ Guest '{name}' not found")


def delete_guest(storage_manager):
    """Delete a guest."""
    print_header("DELETE GUEST")
    
    name = input("Enter guest name to delete: ").strip()
    if not name:
        print("Guest name cannot be empty.")
        return
    
    confirm = input(f"Are you sure you want to delete guest '{name}'? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Deletion cancelled.")
        return
    
    if storage_manager.delete_guest(name):
        print(f"✓ Guest '{name}' deleted successfully")
    else:
        print(f"✗ Guest '{name}' not found")


def clear_storage_menu(storage_manager):
    """Clear storage menu."""
    print_header("CLEAR STORAGE")
    print("1. Clear all apartments")
    print("2. Clear all guests")
    print("3. Clear all storage")
    print("4. Reset to defaults")
    print("5. Back to main menu")
    
    choice = input("\nEnter your choice (1-5): ").strip()
    
    if choice == "1":
        confirm = input("Are you sure you want to clear all apartments? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            count = storage_manager.clear_all_apartments()
            print(f"✓ Cleared {count} apartments")
        else:
            print("Operation cancelled.")
    
    elif choice == "2":
        confirm = input("Are you sure you want to clear all guests? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            count = storage_manager.clear_all_guests()
            print(f"✓ Cleared {count} guests")
        else:
            print("Operation cancelled.")
    
    elif choice == "3":
        confirm = input("Are you sure you want to clear ALL storage? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            result = storage_manager.clear_all_storage()
            print(f"✓ Cleared {result['apartments_cleared']} apartments and {result['guests_cleared']} guests")
        else:
            print("Operation cancelled.")
    
    elif choice == "4":
        confirm = input("Are you sure you want to reset to defaults? (y/n): ").strip().lower()
        if confirm in ['y', 'yes']:
            result = storage_manager.reset_to_defaults()
            print(f"✓ Reset to {result['apartments_reset']} apartments and {result['guests_reset']} guests")
        else:
            print("Operation cancelled.")


def main_menu():
    """Display the main menu."""
    print_header("HOTEL BOOKING SYSTEM - STORAGE MANAGER")
    print("1. View storage summary")
    print("2. View all apartments")
    print("3. View all guests")
    print("4. View top guests by points")
    print("5. View most expensive apartments")
    print("6. Search apartments")
    print("7. Search guests")
    print("8. Add apartment")
    print("9. Update apartment rate")
    print("10. Delete apartment")
    print("11. Add guest")
    print("12. Update guest points")
    print("13. Delete guest")
    print("14. Clear storage")
    print("15. Exit")


def main():
    """Main function."""
    storage_manager = get_storage_manager()
    
    print("Welcome to the Hotel Booking System Storage Manager!")
    print("This tool allows you to view and manage the in-memory storage.")
    
    while True:
        try:
            main_menu()
            choice = input("\nEnter your choice (1-15): ").strip()
            
            if choice == "1":
                print_storage_summary(storage_manager)
            
            elif choice == "2":
                print_apartments(storage_manager)
            
            elif choice == "3":
                print_guests(storage_manager)
            
            elif choice == "4":
                limit = input("Enter number of top guests to show (default 5): ").strip()
                try:
                    limit = int(limit) if limit else 5
                    print_top_guests(storage_manager, limit)
                except ValueError:
                    print("Invalid number. Using default of 5.")
                    print_top_guests(storage_manager, 5)
            
            elif choice == "5":
                limit = input("Enter number of apartments to show (default 5): ").strip()
                try:
                    limit = int(limit) if limit else 5
                    print_expensive_apartments(storage_manager, limit)
                except ValueError:
                    print("Invalid number. Using default of 5.")
                    print_expensive_apartments(storage_manager, 5)
            
            elif choice == "6":
                search_apartments(storage_manager)
            
            elif choice == "7":
                search_guests(storage_manager)
            
            elif choice == "8":
                add_apartment(storage_manager)
            
            elif choice == "9":
                update_apartment_rate(storage_manager)
            
            elif choice == "10":
                delete_apartment(storage_manager)
            
            elif choice == "11":
                add_guest(storage_manager)
            
            elif choice == "12":
                update_guest_points(storage_manager)
            
            elif choice == "13":
                delete_guest(storage_manager)
            
            elif choice == "14":
                clear_storage_menu(storage_manager)
            
            elif choice == "15":
                print("\nThank you for using the Storage Manager!")
                break
            
            else:
                print("Invalid choice. Please enter a number between 1 and 15.")
            
            input("\nPress Enter to continue...")
            
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            break
        except Exception as e:
            print(f"\nError: {e}")
            input("Press Enter to continue...")


if __name__ == "__main__":
    main()
