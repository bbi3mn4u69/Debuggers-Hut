
"""
Nguyen Quang Huy Pham 
s4181834
Attempted All 3 Tasks
"""

import sys
from typing import Dict, Any
"""
CONFIG
"""
APARTMENTS = {
    "U12swan":  {"rate": 95.0,  "capacity": 2},
    "U209duck": {"rate": 106.7, "capacity": 2},
    "U49goose": {"rate": 145.2, "capacity": 2},
}

GUESTS_POINTS = {
    "Alyssa": 300,
    "Luigi": 32,
}


SUPPLEMENTARY_ITEMS = {
    "car_park":   25.0,
    "breakfast":  18.0,
    "toothpaste":  5.2,
    "extra_bed":  30.0,
}

HOTEL_NAME = "Debuggers Hut Serviced Apartments"
CURRENCY = "AUD"
DATE_FORMAT = "d/m/yyyy"

"""
DATA STORAGE
"""


# in-memory stores
_guests_points: Dict[str, int] = GUESTS_POINTS.copy()
_apartments: Dict[str, Dict[str, Any]] = {k: dict(v) for k, v in APARTMENTS.items()}
_items: Dict[str, float] = SUPPLEMENTARY_ITEMS.copy()

# order history: guest -> list of order dicts
_orders_by_guest: Dict[str, list] = {}


# ---------- listing and viewing ----------

def list_apartments() -> Dict[str, Dict[str, Any]]:
    """ copy of apartments (id -> {rate, capacity})."""
    return {k: dict(v) for k, v in _apartments.items()}

def get_all_apartments() -> Dict[str, float]:
    """backward-compat view: id -> rate only."""
    return {k: float(v["rate"]) for k, v in _apartments.items()}

def list_items() -> Dict[str, float]:
    """supplementary items (id -> price)."""
    return dict(_items)

def get_all_guests() -> Dict[str, int]:
    return dict(_guests_points)


def get_rate(apartment_id: str) -> float:
    """for id (case-insensitive); 0.0 if not found."""
    aid = apartment_id.lower()
    for k, v in _apartments.items():
        if k.lower() == aid:
            return float(v["rate"])
    return 0.0

def get_capacity(apartment_id: str) -> int:
    """(beds) for id; 0 if not found."""
    aid = apartment_id.lower()
    for k, v in _apartments.items():
        if k.lower() == aid:
            return int(v["capacity"])
    return 0


# ---------- guest and point ----------

def add_points(guest_name: str, earned: int) -> int:
    """Add positive points for guest (create if new). Returns new total."""
    if not guest_name.strip():
        raise ValueError("Guest name cannot be empty")
    if earned < 0:
        raise ValueError("Earned points cannot be negative")
    new_total = _guests_points.get(guest_name, 0) + earned
    _guests_points[guest_name] = new_total
 
    return new_total

def spend_points(guest_name: str, points: int) -> int:
    """Spend (deduct) points from guest. Returns new balance."""
    if points < 0:
        raise ValueError("Points to spend cannot be negative")
    balance = _guests_points.get(guest_name, 0)
    if points > balance:
        raise ValueError("Insufficient points")
    new_total = balance - points
    _guests_points[guest_name] = new_total

    return new_total

def get_guest_points(guest_name: str) -> int:
    """Current points for guest (0 if missing)."""
    return _guests_points.get(guest_name, 0)


# ---------- upsert part ----------

def _is_valid_apartment_id(apartment_id: str) -> bool:
    if not apartment_id or apartment_id[0] != "U":
        return False
    i = 1
    while i < len(apartment_id) and apartment_id[i].isdigit():
        i += 1
    if i == 1:
        return False
    if i >= len(apartment_id) or not apartment_id[i].isalpha():
        return False
    for ch in apartment_id[i:]:
        if not ch.isalnum():
            return False
    return True

def upsert_apartment(apartment_id: str, rate: float, capacity: int) -> None:
    if not _is_valid_apartment_id(apartment_id):
        raise ValueError("Invalid apartment id format (e.g., U12swan)")
    if rate <= 0:
        raise ValueError("Rate must be positive")
    if capacity <= 0:
        raise ValueError("Capacity must be positive")
    _apartments[apartment_id] = {"rate": float(rate), "capacity": int(capacity)}


def upsert_items_bulk(line: str) -> None:
    """
    we can upsert bulk of item by the following syntax:
      'toothpaste 5.2, shampoo 8.2'
    """
    if not line.strip():
        raise ValueError("Empty input")
    pairs = [p.strip() for p in line.split(",") if p.strip()]
    changes = {}
    for p in pairs:
        parts = p.split()
        if len(parts) != 2:
            raise ValueError("Each entry must be 'item price'")
        iid, price_s = parts
        try:
            price = float(price_s)
        except ValueError:
            raise ValueError(f"Invalid price for '{iid}'")
        if price <= 0:
            raise ValueError(f"Price for '{iid}' must be > 0")
        changes[iid] = price
    _items.update(changes)

# ---------- order history ----------

def record_order(guest: str, summary: dict) -> None:
    _orders_by_guest.setdefault(guest, []).append(summary)
def get_orders_for_guest(guest: str) -> list:
    return list(_orders_by_guest.get(guest, []))

"""
CACULATION
"""

def compute_total_cost(rate: float, nights: int) -> float:
    if rate < 0:
        raise ValueError("Rate cannot be negative")
    
    if nights < 0:
        raise ValueError("Number of nights cannot be negative")
    
    total = rate * nights
    return total


def points_round_half_up(amount_aud: float) -> int:
    if amount_aud < 0:
        raise ValueError("Amount cannot be negative")
    
    points = int(amount_aud + 0.5)

    return points


def calculate_discount(original_cost: float, discount_percentage: float) -> float:
    """
    Calculate discount amount.
    
    Args:
        original_cost: Original cost in AUD
        discount_percentage: Discount percentage (0-100)
        
    Returns:
        float: Discount amount in AUD
    """
    if not 0 <= discount_percentage <= 100:
        raise ValueError("Discount percentage must be between 0 and 100")
    
    if original_cost < 0:
        raise ValueError("Original cost cannot be negative")
    
    discount = original_cost * (discount_percentage / 100)
    return round(discount, 2)


def calculate_final_cost(original_cost: float, discount_amount: float = 0.0) -> float:
    if original_cost < 0:
        raise ValueError("Original cost cannot be negative")
    
    if discount_amount < 0:
        raise ValueError("Discount amount cannot be negative")
    
    final_cost = original_cost - discount_amount
    return max(0, final_cost)  # Ensure cost doesn't go below zero


def calc_items_subtotal(items_with_qty: dict[str, int], price_lookup: dict[str, float]) -> float:
    total = 0.0
    for iid, qty in items_with_qty.items():
        price = float(price_lookup[iid])
        total += price * int(qty)
    return total

def required_extra_beds(num_guests: int, capacity: int) -> int:
    if num_guests <= capacity:
        return 0
    deficit = num_guests - capacity
    beds = (deficit + 1) // 2  
    return min(2, beds)

def apply_points_redemption(pre_total: float, guest_points: int, redeem_blocks: int) -> tuple[float, int]:
    if redeem_blocks < 0:
        redeem_blocks = 0
    # max blocks allowed by balance and by pre_total
    max_by_points = guest_points // 100
    max_by_total = int(pre_total // 10)
    spend_blocks = min(redeem_blocks, max_by_points, max_by_total)
    discount = spend_blocks * 10.0
    return max(0.0, pre_total - discount), spend_blocks * 100

"""
RECEIPT PRINTING
"""
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
    except Exception as e:
        print("Error: Could not print receipt properly.")

def format_currency(amount: float) -> str:
    return f"${amount:.2f} ({CURRENCY})"

"""
IO PROMPT
"""

DATE_FORMAT = "d/m/yyyy"
_DATETIME_FORMAT = "%d/%m/%Y"

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
    validate the date
    """
    s = date_str.strip()
    parts = s.split("/")
    if len(parts) != 3:
        return False
    d_s, m_s, y_s = parts[0].strip(), parts[1].strip(), parts[2].strip()
    if not (d_s.isdigit() and m_s.isdigit() and y_s.isdigit() and len(y_s) == 4):
        return False
    d, m, y = int(d_s), int(m_s), int(y_s)
    if y < 1900: 
        return False
    if not (1 <= m <= 12):
        return False
    month_days = {1:31, 2:28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}
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

# ---------- prompt yes/no ----------

def prompt_yes_no(msg: str) -> bool:
    while True:
        ans = input(f"{msg} (y/n): ").strip().lower()
        if ans in ("y", "yes"):
            return True
        if ans in ("n", "no"):
            return False
        print("Error: please enter y or n.")

def prompt_existing_apartment_id() -> str:
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
    return input("Enter items list (item price, item price, ...): ").strip()

"""
Main application 
"""

# ---------- core booking flow ----------

def run_booking() -> bool:
    try:
        guest_name = prompt_guest_name()
        num_guests = prompt_num_guests()
        apartment_id = prompt_existing_apartment_id()
        
        rate = get_rate(apartment_id)
        print(f"Rate for {apartment_id}: ${rate:.2f} per night")
        
        checkin = prompt_checkin()
        checkout = prompt_checkout()
        nights = prompt_nights_1_to_7()
        booking_date = prompt_booking_date()

        
        capacity = get_capacity(apartment_id)
        beds_needed = required_extra_beds(num_guests, capacity)
        extra_bed_qty = 0
        if beds_needed > 0:
            print("Warning: the number of guests exceeds the unit capacity.")
            if prompt_yes_no("Add extra bed(s)? (max 2; each adds capacity +2)"):
                extra_bed_qty = prompt_quantity_positive(max_allowed=2)
                if capacity + extra_bed_qty * 2 < num_guests:
                    print("Booking cannot proceed: capacity still insufficient.")
                    return False
            else:
                print("Booking cannot proceed due to capacity.")
                return False

        rate = get_rate(apartment_id)
        apt_cost = compute_total_cost(rate, nights)

        items_catalog = list_items()
        ordered_items: dict[str, int] = {}

        if extra_bed_qty:
            ordered_items["extra_bed"] = ordered_items.get("extra_bed", 0) + extra_bed_qty * nights

        continue_ordering = prompt_yes_no("Do you want to order a supplementary item?")

        while continue_ordering:
            iid = prompt_item_id_existing()
            unit_price = items_catalog[iid]
            print(f"Price for {iid}: ${unit_price:.2f}")
           
            qty = prompt_quantity_positive()

            if not iid or qty is None or qty <= 0:
                print("Invalid item ID or quantity. Please try again.")
                continue_ordering = prompt_yes_no("Do you want to order another supplementary item?")
                continue

            tentative_items = dict(ordered_items)
            tentative_items[iid] = tentative_items.get(iid, 0) + qty
            tentative_total = calc_items_subtotal(tentative_items, items_catalog)

            print(f"Item: {iid}\nQuantity: {qty}\nTotal Cost (if added): {tentative_total:.2f}")
            confirm = prompt_yes_no("Confirm this item?")

            if confirm:
                ordered_items[iid] = ordered_items.get(iid, 0) + qty
                print(f"Saved. Total cost so far: {tentative_total:.2f}")
            else:
                print("Item cancelled.")

            continue_ordering = prompt_yes_no("Do you want to order another supplementary item?")

        supp_subtotal = calc_items_subtotal(ordered_items, items_catalog) if ordered_items else 0.0
        pre_total = apt_cost + supp_subtotal

        current_pts = get_guest_points(guest_name)
        discount_amount = 0.0
        spent_points = 0
        final_total = pre_total
        
        if current_pts >= 100 and pre_total >= 10 and prompt_yes_no(
        f"You have {current_pts} points. Redeem now? (100pts = $10)"):
            max_blocks = min(current_pts // 100, int(pre_total // 10))
            print(f"You can redeem up to {max_blocks} block(s) of 100 points "
                    f"({max_blocks*100} pts = ${max_blocks*10}).")
            while True:
                try:
                    blocks = int(input("Enter how many 100-point blocks to redeem: ").strip())
                    if 0 <= blocks <= max_blocks:
                        final_total, spent_points = apply_points_redemption(pre_total, current_pts, blocks)
                        discount_amount = pre_total - final_total
                        break
                    else:
                        print(f"Error: please enter a number between 0 and {max_blocks}.")
                except ValueError:
                    print("Error: enter a whole number.")
                    
        earned = points_round_half_up(pre_total) 

        supp_items_list = (
            [(iid, ordered_items[iid], items_catalog[iid]) for iid in ordered_items] if ordered_items else None
        )
        
        # print receipt
        print_receipt(
            guest_name=guest_name,
            num_guests=num_guests,
            apartment_id=apartment_id,
            apartment_rate=rate,
            checkin=checkin,
            checkout=checkout,
            length_of_stay=nights,
            booking_date=booking_date,
            total_cost=final_total,
            reward_points=earned,
            discount_amount=discount_amount,
            supp_items=supp_items_list,
            supp_subtotal=supp_subtotal if ordered_items else None,
        )

        if spent_points:
            spend_points(guest_name, spent_points)
        add_points(guest_name, earned)
        new_balance = get_guest_points(guest_name)

        record_order(
            guest_name,
            {
                "apartment_id": apartment_id,
                "nights": nights,
                "items": dict(ordered_items),
                "pre_total": pre_total,
                "redeemed_points": spent_points,
                "final_total": final_total,
                "earned_points": earned,
            },
        )
        return True

    except KeyboardInterrupt:
        print("\nBooking cancelled by user.")
        raise
    except Exception as e:
        print("Booking failed:", e)
        return False

# ---------- menu ----------

def run_once() -> None:
    print("Welcome to the Hotel Booking System!")
    print("=" * 50)
    while True:
        print("\nMenu:")
        print("1) Make a booking")
        print("2) Add/update apartment")
        print("3) Add/update supplementary items (bulk)")
        print("4) Display existing guests")
        print("5) Display existing products")
        print("6) Display a guest booking & order history")
        print("7) Exit")
        choice = input("Select (1-7): ").strip()
        try:
            # make a booking
            if choice == "1":
                run_booking()
            # add/update apartment
            elif choice == "2":
                while True:
                    try:
                        aid, rate, cap = prompt_upsert_apartment_line()
                        upsert_apartment(aid, rate, cap)
                        print("Apartment saved.")
                        break
                    except Exception as e:
                        print("Error:", e)
                        break
            # upsert supplementary items
            elif choice == "3":
                while True:
                    try:
                        line = prompt_items_bulk_line()
                        upsert_items_bulk(line)
                        print("Items saved.")
                        break
                    except Exception as e:
                        print("Error:", e)
                        break
            # display existing guest
            elif choice == "4":
                print("Guests and points:")
                for name, pts in get_all_guests().items():
                    print(f"  {name}: {pts} pts")
            # display existing product
            elif choice == "5":
                print("Apartments:")
                for aid, info in list_apartments().items():
                    print(f"  {aid}: ${info['rate']:.2f}, capacity={info['capacity']}")
                print("\nSupplementary items:")
                for iid, price in list_items().items():
                    print(f"  {iid}: ${price:.2f}")
            # display guest booking and order history
            elif choice == "6":
                name = prompt_guest_name()
                orders = get_orders_for_guest(name)
                if not orders:
                    print("No history for this guest (or invalid name).")
                else:
                    print(f"\nThis is the booking and order history for {name}.")
                    for idx, o in enumerate(orders, 1):
                        print(
                            f"{idx}. Apt {o['apartment_id']} x{o['nights']} nights; "
                            f"Items: {o['items']} | "
                            f"Pre: ${o['pre_total']:.2f} | "
                            f"Redeemed: {o['redeemed_points']} pts | "
                            f"Final: ${o['final_total']:.2f} | "
                            f"Earned: {o['earned_points']} pts"
                        )
            # user terminate
            elif choice == "7":
                print("Goodbye!")
                return
            else:
                print("Please choose 1–7.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            return

def main() -> None:
    try:
        run_once()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()


