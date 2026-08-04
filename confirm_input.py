"""
confirm_input.py
----------------
Validation helpers for user-supplied ticker symbols and date strings.
All public functions return a bool so callers only need to branch on
True / False — no exception handling required at the GUI layer.
"""

import csv
import os
import re
from datetime import date
from dateutil import relativedelta


# ---------------------------------------------------------------------------
# Ticker validation
# ---------------------------------------------------------------------------

def generate_hashmap(user_data: str) -> bool:
    """Return True if *user_data* is a valid ticker in StockSymbols.csv."""
    ticker_set = _load_tickers(os.path.join(os.path.dirname(__file__), "StockSymbols.csv"))
    return _is_valid_ticker(ticker_set, user_data)


def _load_tickers(filename: str) -> set:
    """Read the CSV and return a set of ticker symbols."""
    tickers: set = set()
    with open(filename, "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                tickers.add(row[0])
    return tickers


def _is_valid_ticker(tickers: set, user_data: str) -> bool:
    """Return True if *user_data* is a 1-5 uppercase-letter ticker that exists
    in *tickers*.  Carets are also allowed (e.g. index symbols like ^GSPC)."""
    if not re.fullmatch(r"[A-Z\^]{1,5}", user_data):
        return False
    return user_data in tickers


# ---------------------------------------------------------------------------
# Date validation
# ---------------------------------------------------------------------------

def user_input_dates_plus_current_date(year: str, month: str, day: str) -> bool:
    """Return True if the date string components form a valid date that falls
    within the past two years (Polygon free-tier limit)."""
    today = date.today()
    return _is_valid_date_within_range(today, year, month, day)


def _is_valid_date_within_range(today: date, user_year: str, user_month: str, user_day: str) -> bool:
    """Parse and range-check the three string components.  Returns False for
    any non-numeric input, out-of-range values, future dates, or dates older
    than two years."""
    parsed = _parse_date(user_year, user_month, user_day)
    if parsed is None:
        return False

    if parsed > today:
        return False

    delta = relativedelta.relativedelta(today, parsed)
    return delta.years < 2


def _parse_date(year_str: str, month_str: str, day_str: str) -> date | None:
    """Convert three digit strings to a date object, returning None on any
    invalid input instead of raising."""
    if not all(_is_digits(v) for v in (year_str, month_str, day_str)):
        return None
    try:
        return date(int(year_str), int(month_str), int(day_str))
    except ValueError:
        return None


def _is_digits(value: str | None) -> bool:
    """Return True only when *value* is a non-empty string of digit characters."""
    return isinstance(value, str) and value.isdigit()
