"""
Configuration settings for the Hotel Booking System (Part 2).
"""

# Apartments now include capacity (beds). Default capacity is 2.
APARTMENTS = {
    "U12swan":  {"rate": 95.0,  "capacity": 2},
    "U209duck": {"rate": 106.7, "capacity": 2},
    "U49goose": {"rate": 145.2, "capacity": 2},
}

# Existing guests and their accumulated reward points
GUESTS_POINTS = {
    "Alyssa": 20,
    "Luigi": 32,
}

# Default supplementary items (id -> price)
# Notes:
# - car_park: per night
# - breakfast: per person
# - toothpaste: per tube
# - extra_bed: per bed per night
SUPPLEMENTARY_ITEMS = {
    "car_park":   25.0,
    "breakfast":  18.0,
    "toothpaste":  5.2,
    "extra_bed":  30.0,
}

# Application settings
HOTEL_NAME = "Debuggers Hut Serviced Apartments"
CURRENCY = "AUD"
DATE_FORMAT = "d/m/yyyy"
