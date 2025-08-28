"""
Data storage and management for the Hotel Booking System (Part 2).
"""

import logging
import re
from typing import Dict, Any

from .config import APARTMENTS, GUESTS_POINTS, SUPPLEMENTARY_ITEMS

logger = logging.getLogger(__name__)

# In-memory stores
_guests_points: Dict[str, int] = GUESTS_POINTS.copy()
_apartments: Dict[str, Dict[str, Any]] = {k: dict(v) for k, v in APARTMENTS.items()}
_items: Dict[str, float] = SUPPLEMENTARY_ITEMS.copy()

# Order history: guest -> list of order dicts
_orders_by_guest: Dict[str, list] = {}


# ---------- Listing / viewing ----------

def list_apartments() -> Dict[str, Dict[str, Any]]:
    """Return copy of apartments (id -> {rate, capacity})."""
    return {k: dict(v) for k, v in _apartments.items()}

def get_all_apartments() -> Dict[str, float]:
    """Backward-compat view: id -> rate only."""
    return {k: float(v["rate"]) for k, v in _apartments.items()}

def list_items() -> Dict[str, float]:
    """Return copy of supplementary items (id -> price)."""
    return dict(_items)

def get_all_guests() -> Dict[str, int]:
    """Copy of guests and their points."""
    return dict(_guests_points)


# ---------- Lookups ----------

def get_rate(apartment_id: str) -> float:
    """Nightly rate for id (case-insensitive); 0.0 if not found."""
    aid = apartment_id.lower()
    for k, v in _apartments.items():
        if k.lower() == aid:
            return float(v["rate"])
    logger.warning("Unknown apartment ID: %s", apartment_id)
    return 0.0

def get_capacity(apartment_id: str) -> int:
    """Capacity (beds) for id; 0 if not found."""
    aid = apartment_id.lower()
    for k, v in _apartments.items():
        if k.lower() == aid:
            return int(v["capacity"])
    return 0


# ---------- Guests & Points ----------

def add_points(guest_name: str, earned: int) -> int:
    """Add positive points for guest (create if new). Returns new total."""
    if not guest_name.strip():
        raise ValueError("Guest name cannot be empty")
    if earned < 0:
        raise ValueError("Earned points cannot be negative")
    new_total = _guests_points.get(guest_name, 0) + earned
    _guests_points[guest_name] = new_total
    logger.info("Added %s points to %s. New total: %s", earned, guest_name, new_total)
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
    logger.info("Deducted %s points from %s. New total: %s", points, guest_name, new_total)
    return new_total

def get_guest_points(guest_name: str) -> int:
    """Current points for guest (0 if missing)."""
    return _guests_points.get(guest_name, 0)


# ---------- Admin upserts ----------

_APT_ID_RE = re.compile(r"U\d+[A-Za-z][A-Za-z0-9]*")

def upsert_apartment(apartment_id: str, rate: float, capacity: int) -> None:
    """
    Add/update apartment with validation: U + digits + name (e.g., U12swan).
    """
    if not _APT_ID_RE.fullmatch(apartment_id):
        raise ValueError("Invalid apartment id format (e.g., U12swan)")
    if rate <= 0:
        raise ValueError("Rate must be positive")
    if capacity <= 0:
        raise ValueError("Capacity must be positive")
    _apartments[apartment_id] = {"rate": float(rate), "capacity": int(capacity)}
    logger.info("Apartment saved: %s (rate=%.2f, cap=%d)", apartment_id, rate, capacity)

def upsert_items_bulk(line: str) -> None:
    """
    Add/update multiple items from a line like:
      'toothpaste 5.2, shampoo 8.2'
    If any price invalid -> raise ValueError so caller can re-prompt the whole line.
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
    logger.info("Supplementary items upserted: %s", list(changes.keys()))


# ---------- Order history ----------

def record_order(guest: str, summary: dict) -> None:
    """
    Append an order summary for a guest.
    Keys (expected):
      apartment_id, nights, items(dict id->qty),
      pre_total, redeemed_points, final_total, earned_points
    """
    _orders_by_guest.setdefault(guest, []).append(summary)

def get_orders_for_guest(guest: str) -> list:
    return list(_orders_by_guest.get(guest, []))
