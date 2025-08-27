#!/usr/bin/env python3
"""
Simple entry point script for the Hotel Booking System.
This allows running the application without installing the package.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from hotel_booking.main import main

if __name__ == "__main__":
    main()
