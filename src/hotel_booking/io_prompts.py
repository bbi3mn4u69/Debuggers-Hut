"""
User input handling and validation for the Hotel Booking System (Part 2).
"""


from .config import DATE_FORMAT
from .data_store import list_apartments, list_items



DATE_FORMAT = "d/m/yyyy"
_DATETIME_FORMAT = "%d/%m/%Y"


# ---------- Part 1 prompts (kept) ----------

def prompt_guest_name() -> str:
    while True:
        try:
            name = input("Enter the guest's name: ").strip()
            if not name:
                print("Error: Guest name cannot be empty. Please try again.")
                continue
            if len(name) > 100:
                print("Error: Guest name is too long. Please use a shorter name.")
                continue
         
            return name
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise
        except Exception as e:
           
            print("An error occurred. Please try again.")

def prompt_num_guests() -> int:
    while True:
        try:
            num = int(input("Enter number of guests: ").strip())
            if num <= 0:
                print("Error: Number of guests must be positive.")
                continue
            if num > 20:
                print("Error: Maximum 20 guests allowed.")
                continue
          
            return num
        except ValueError:
            print("Error: Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise

def prompt_apartment_id() -> str:
    while True:
        try:
            apartment_id = input("Enter apartment ID (e.g., U12swan): ").strip()
            if not apartment_id:
                print("Error: Apartment ID cannot be empty.")
                continue
            if len(apartment_id) > 20:
                print("Error: Apartment ID is too long.")
                continue
           
            return apartment_id
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise

def _validate_date(date_str: str) -> bool:
    """
    Validate Australian date format d/m/yyyy without using datetime.
    Accepts 1-2 digit day, 1-2 digit month, and 4-digit year (>= 1900).
    Checks day limits per month and leap years.
    """
    s = date_str.strip()
    # Basic structure: a/b/c where c is 4 digits
    parts = s.split("/")
    if len(parts) != 3:
        return False
    d_s, m_s, y_s = parts[0].strip(), parts[1].strip(), parts[2].strip()
    if not (d_s.isdigit() and m_s.isdigit() and y_s.isdigit() and len(y_s) == 4):
        return False
    d, m, y = int(d_s), int(m_s), int(y_s)
    if y < 1900:  # arbitrary lower bound
        return False
    if not (1 <= m <= 12):
        return False

    # days per month
    month_days = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

    # leap year adjustment
    is_leap = (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0))
    if m == 2 and is_leap:
        max_day = 29
    else:
        max_day = month_days[m]

    return 1 <= d <= max_day


def prompt_checkin() -> str:
    while True:
        try:
            checkin = input(f"Enter check-in date ({DATE_FORMAT}): ").strip()
            if not checkin:
                print("Error: Check-in date cannot be empty.")
                continue
            if not _validate_date(checkin):
                print(f"Error: Invalid date. Use {DATE_FORMAT}.")
                continue
         
            return checkin
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise

def prompt_checkout() -> str:
    while True:
        try:
            checkout = input(f"Enter check-out date ({DATE_FORMAT}): ").strip()
            if not checkout:
                print("Error: Check-out date cannot be empty.")
                continue
            if not _validate_date(checkout):
                print(f"Error: Invalid date. Use {DATE_FORMAT}.")
                continue
          
            return checkout
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise

def prompt_length_of_stay() -> int:
    while True:
        try:
            nights = int(input("Enter length of stay (nights): ").strip())
            if nights <= 0:
                print("Error: Length of stay must be positive.")
                continue
            if nights > 365:
                print("Error: Maximum stay is 365 nights.")
                continue
         
            return nights
        except ValueError:
            print("Error: Please enter a valid number.")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise

def prompt_booking_date() -> str:
    while True:
        try:
            booking_date = input(f"Enter booking date ({DATE_FORMAT}): ").strip()
            if not booking_date:
                print("Error: Booking date cannot be empty.")
                continue
            if not _validate_date(booking_date):
                print(f"Error: Invalid date. Use {DATE_FORMAT}.")
                continue
            
            return booking_date
        except KeyboardInterrupt:
            print("\nOperation cancelled by user.")
            raise


# ---------- Part 2 additions ----------

def prompt_yes_no(msg: str) -> bool:
    while True:
        ans = input(f"{msg} (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Error: please enter y or n.")

def prompt_existing_apartment_id() -> str:
    """Prompt until the id exists (case-insensitive)."""
    aps = list_apartments()
    while True:
        aid = prompt_apartment_id()
        matches = [k for k in aps.keys() if k.lower() == aid.lower()]
        if matches:
            return matches[0]
        print("Error: Apartment id not found. Please try again.")

def prompt_nights_1_to_7() -> int:
    while True:
        try:
            n = int(input("Enter length of stay (nights, 1-7): ").strip())
            if 1 <= n <= 7:
                return n
            print("Error: nights must be an integer between 1 and 7.")
        except ValueError:
            print("Error: please enter a whole number.")

def prompt_item_id_existing() -> str:
    items = list_items()
    while True:
        iid = input("Enter supplementary item id: ").strip()
        if iid in items:
            return iid
        print("Error: item id not found. Please try again.")

def prompt_quantity_positive(max_allowed: int | None = None) -> int:
    while True:
        try:
            q = int(input("Enter quantity: ").strip())
            if q <= 0:
                print("Error: quantity must be > 0.")
                continue
            if max_allowed is not None and q > max_allowed:
                print(f"Error: maximum allowed is {max_allowed}.")
                continue
            return q
        except ValueError:
            print("Error: please enter a whole number.")

def prompt_upsert_apartment_line() -> tuple[str, float, int]:
    """
    Expect: apartment_id rate capacity
    ID format is validated downstream in data_store.upsert_apartment.
    """
    while True:
        line = input("Enter: apartment_id rate capacity: ").strip()
        parts = line.split()
        if len(parts) != 3:
            print("Error: please enter exactly three fields.")
            break
        aid, rate_s, cap_s = parts
        try:
            rate = float(rate_s)
            cap = int(cap_s)
            return aid, rate, cap
        except ValueError:
            print("Error: rate must be a number and capacity an integer.")
            break

def prompt_items_bulk_line() -> str:
    """
    Example: 'toothpaste 5.2, shampoo 8.2'
    Validation of price/format occurs in data_store.upsert_items_bulk.
    """
    return input("Enter items list (item price, item price, ...): ").strip()
