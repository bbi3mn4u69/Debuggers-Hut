"""
Main application entry point for the Hotel Booking System (Part 2).
Menu-driven program, extra-bed rule, reward redemption, and order history.
"""

import logging
import sys

from .data_store import (
    get_rate, get_capacity, add_points, spend_points, get_guest_points,
    list_apartments, list_items, upsert_apartment, upsert_items_bulk,
    record_order, get_orders_for_guest, get_all_guests, get_all_apartments
)
from .calculations import (
    compute_total_cost, points_round_half_up, calc_items_subtotal,
    required_extra_beds, apply_points_redemption
)
from .receipt import print_receipt
from .io_prompts import (
    prompt_guest_name, prompt_num_guests, prompt_existing_apartment_id,
    prompt_checkin, prompt_checkout, prompt_nights_1_to_7, prompt_booking_date,
    prompt_item_id_existing, prompt_quantity_positive, prompt_yes_no,
    prompt_upsert_apartment_line, prompt_items_bulk_line,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout), logging.FileHandler("hotel_booking.log")],
)
logger = logging.getLogger(__name__)


# ---------- Core booking flow ----------

def run_booking() -> bool:
    """
    One complete booking in Part 2:
    - inputs (+ validation)
    - capacity & extra-bed rule
    - supplementary items flow
    - optional reward redemption
    - receipt + points update + history
    """
    try:
        logger.info("Starting booking")
        guest_name = prompt_guest_name()
        num_guests = prompt_num_guests()
        apartment_id = prompt_existing_apartment_id()
        checkin = prompt_checkin()
        checkout = prompt_checkout()
        nights = prompt_nights_1_to_7()
        booking_date = prompt_booking_date()

        # Capacity & extra bed rule
        capacity = get_capacity(apartment_id)
        beds_needed = required_extra_beds(num_guests, capacity)
        extra_bed_qty = 0
        if beds_needed > 0:
            print("Warning: the number of guests exceeds the unit capacity.")
            if prompt_yes_no("Add extra bed(s)? (max 2; each adds capacity +2)"):
                extra_bed_qty = prompt_quantity_positive(max_allowed=2)
                # After adding beds, ensure feasible
                if capacity + extra_bed_qty * 2 < num_guests:
                    print("Booking cannot proceed: capacity still insufficient.")
                    return False
            else:
                print("Booking cannot proceed due to capacity.")
                return False

        # Apartment cost
        rate = get_rate(apartment_id)
        apt_cost = compute_total_cost(rate, nights)

        # Supplementary items (allow multiple)
        items_catalog = list_items()
        ordered_items: dict[str, int] = {}

        # If extra beds were added, charge per bed per night
        if extra_bed_qty:
            ordered_items["extra_bed"] = ordered_items.get("extra_bed", 0) + extra_bed_qty * nights

        continue_ordering = prompt_yes_no("Do you want to order a supplementary item?")

        while continue_ordering:
            iid = prompt_item_id_existing()
            qty = prompt_quantity_positive()

            if not iid or qty is None or qty <= 0:
                print("Invalid item ID or quantity. Please try again.")
                # Ask directly if they want to try another item (stay in loop or exit)
                continue_ordering = prompt_yes_no("Do you want to order another supplementary item?")
                continue

            # Compute tentative total BEFORE saving
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

            # Only this prompt controls the next iteration
            continue_ordering = prompt_yes_no("Do you want to order another supplementary item?")



        supp_subtotal = calc_items_subtotal(ordered_items, items_catalog) if ordered_items else 0.0
        pre_total = apt_cost + supp_subtotal

        # Reward redemption (100 pts -> $10; earned from pre_total)
        current_pts = get_guest_points(guest_name)
        discount_amount = 0.0
        spent_points = 0
        final_total = pre_total

        if current_pts >= 100 and pre_total >= 10 and prompt_yes_no(
            f"You have {current_pts} points. Redeem now? (100pts = $10)"
        ):
            while True:
                try:
                    blocks = int(input("Enter how many 100-point blocks to redeem: ").strip())
                    final_total, spent_points = apply_points_redemption(pre_total, current_pts, blocks)
                    discount_amount = pre_total - final_total
                    break
                except ValueError:
                    print("Error: enter a whole number of blocks.")

        earned = points_round_half_up(pre_total)  # earned from pre-discount total

        # Print receipt (with optional supplementary section)
        supp_items_list = (
            [(iid, ordered_items[iid], items_catalog[iid]) for iid in ordered_items] if ordered_items else None
        )
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

        # Update points (spend then earn)
        if spent_points:
            spend_points(guest_name, spent_points)
        add_points(guest_name, earned)
        new_balance = get_guest_points(guest_name)

        # Save order history
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
        print(f"\n[Info] Guest '{guest_name}' now has {new_balance} reward points.")
        logger.info("Booking completed")
        return True

    except KeyboardInterrupt:
        print("\nBooking cancelled by user.")
        logger.info("Booking cancelled by user")
        raise
    except Exception as e:
        logger.error("Booking error: %s", e)
        print("Booking failed:", e)
        return False


# ---------- Menu ----------

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
            # add/update supplementary items
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
                logger.info("Application terminated by user")
                return
            else:
                print("Please choose 1–7.")
        except KeyboardInterrupt:
            print("\nGoodbye!")
            logger.info("Application terminated by user")
            return


def main() -> None:
    try:
        run_once()
    except Exception as e:
        logger.error("Fatal error: %s", e)
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
