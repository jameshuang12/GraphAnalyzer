"""
stock_class.py
--------------
Defines the Stock data class that fetches and holds OHLC price data
from the Polygon.io REST API for a given ticker and date range.

The API key is read from the POLYGON_API_KEY environment variable.
Copy .env.example to .env and fill in your key, or export the variable
before running the app.
"""

import os
from datetime import date

from dotenv import load_dotenv
from polygon import RESTClient

load_dotenv()


class Stock:
    """Holds daily OHLC data for *ticker* between *day_one* and *day_two*.

    Attributes:
        tick_name: The ticker symbol (e.g. "AAPL").
        day_one:   Start date of the range.
        day_two:   End date of the range.
        open:      List of daily open prices.
        high:      List of daily high prices.
        low:       List of daily low prices.
        close:     List of daily close prices.
    """

    def __init__(self, ticker: str, day_one: date, day_two: date) -> None:
        api_key = os.getenv("POLYGON_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "POLYGON_API_KEY is not set. "
                "Copy .env.example to .env and add your key."
            )

        self.tick_name = ticker
        self.day_one = day_one
        self.day_two = day_two

        client = RESTClient(api_key)
        aggs = client.get_aggs(ticker, 1, "day", day_one, day_two)

        self.open  = [bar.open  for bar in aggs]
        self.high  = [bar.high  for bar in aggs]
        self.low   = [bar.low   for bar in aggs]
        self.close = [bar.close for bar in aggs]
        # Keep raw bars for any callers that index into .items
        self.items = list(aggs)

    # ------------------------------------------------------------------
    # Dunder helpers
    # ------------------------------------------------------------------

    def __len__(self) -> int:
        """Number of trading days in the range (excludes weekends/holidays)."""
        return len(self.items)

    def __str__(self) -> str:
        return self.tick_name

    def __repr__(self) -> str:
        return (
            f"Stock(ticker={self.tick_name!r}, "
            f"day_one={self.day_one}, day_two={self.day_two}, "
            f"days={len(self)})"
        )
