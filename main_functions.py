"""
main_functions.py
-----------------
Business-logic layer between the GUI and the data model.

The Main class exposes methods for validating user input, constructing
Stock objects, and computing technical indicators (RSI, ADX, moving
average crossover).  It has no knowledge of Qt widgets.
"""

from datetime import date

import confirm_input
import stock_class
from stock_class import Stock


class Main:
    """Stateless service class.  The GUI instantiates this once and calls
    its methods to validate input and perform calculations."""

    # ------------------------------------------------------------------
    # Input validation (Window 1 & 2)
    # ------------------------------------------------------------------

    def validate_ticker(self, ticker: str) -> bool:
        """Return True if *ticker* maps to a known symbol in StockSymbols.csv."""
        return confirm_input.generate_hashmap(ticker)

    def validate_date(self, year: str, month: str, day: str) -> bool:
        """Return True if the three string components form a valid date within
        the past two years."""
        return confirm_input.user_input_dates_plus_current_date(year, month, day)

    def parse_dates(
        self,
        year_one: str, month_one: str, day_one: str,
        year_two: str, month_two: str, day_two: str,
    ) -> tuple[date, date]:
        """Convert six validated date strings into two date objects."""
        first = date(int(year_one), int(month_one), int(day_one))
        second = date(int(year_two), int(month_two), int(day_two))
        return first, second

    # ------------------------------------------------------------------
    # Stock construction (Window 2 → 3)
    # ------------------------------------------------------------------

    def build_stock(self, ticker: str, day_one: date, day_two: date) -> Stock:
        """Fetch OHLC data from Polygon and return a Stock instance."""
        return stock_class.Stock(ticker, day_one, day_two)

    # ------------------------------------------------------------------
    # Financial calculations
    # ------------------------------------------------------------------

    def percentage_change(self, stock: Stock) -> tuple[bool, int]:
        """Return (is_positive, percent_change) from close[0] to close[-1]."""
        change = int(((stock.close[-1] - stock.close[0]) / stock.close[0]) * 100)
        return change >= 0, change

    def investment_return(self, percent_change: int, amount: float) -> int:
        """Return the dollar gain/loss on *amount* given *percent_change*."""
        return int(amount * (percent_change / 100))

    # ------------------------------------------------------------------
    # Technical indicators
    # ------------------------------------------------------------------

    def rsi(self, stock: Stock, period: int = 14) -> tuple[bool, list[float]]:
        """Compute RSI over the last *period* days.

        Returns (is_oversold, rsi_values) where is_oversold is True when
        the final RSI value is below 30.
        """
        rsi_values: list[float] = []
        closes = stock.close

        for i in range(period):
            gain = loss = 0.0
            gain_count = loss_count = 0

            for j in range(period - 1, 0, -1):
                curr = closes[-period + i + j + 1]
                prev = closes[-period + i + j]
                if curr < prev:
                    gain += prev - curr
                    gain_count += 1
                else:
                    loss += abs(curr - prev)
                    loss_count += 1

            avg_gain = gain / gain_count if gain_count > 0 else 0.0
            avg_loss = loss / loss_count if loss_count > 0 else 0.0

            if avg_loss == 0:
                rsi_value = 100.0
            elif avg_gain == 0:
                rsi_value = 0.0
            else:
                rsi_value = 100 - (100 / (1 + avg_gain / avg_loss))

            rsi_values.append(rsi_value)

        return rsi_values[-1] < 30, rsi_values

    def moving_avg_crossover(
        self,
        stock: Stock,
        short_term: int,
        long_term: int,
        price_type: str,
    ) -> tuple[bool, list[float], list[float]]:
        """Compute short- and long-term simple moving averages.

        Returns (short_above_long, long_term_ma, short_term_ma).
        """
        prices: list[float] = getattr(stock, price_type)

        long_ma = [
            sum(prices[i: i + long_term]) / long_term
            for i in range(len(prices) - long_term + 1)
        ]
        short_ma = [
            sum(prices[i: i + short_term]) / short_term
            for i in range(len(prices) - short_term + 1)
        ]

        return short_ma[-1] > long_ma[-1], long_ma, short_ma

    def average_directional_index(
        self, stock: Stock, period: int = 14
    ) -> tuple[bool, list[float], list[float], list[float]]:
        """Compute ADX, +DI, and -DI for *stock* over *period* days.

        Returns (should_buy, adx_values, pos_di, neg_di).
        should_buy is True when ADX > 20 and +DI > -DI (uptrend with strength).
        """
        true_range, pos_dm, neg_dm = self._dm_and_tr(stock)
        s_tr, s_pos, s_neg = self._smooth(true_range, pos_dm, neg_dm, period)
        pos_di, neg_di = self._directional_index(s_pos, s_neg, s_tr)

        dx = [
            abs(pos_di[i] - neg_di[i]) / abs(pos_di[i] + neg_di[i]) * 100
            for i in range(len(pos_di))
        ]
        adx = [
            sum(dx[i: i + period]) / period
            for i in range(len(dx) - period + 1)
        ]

        should_buy = adx[-1] > 20 and pos_di[-1] > neg_di[-1]
        return should_buy, adx, pos_di, neg_di

    def buy_recommendation(self, stock: Stock) -> str:
        """Combine RSI, ADX, and MA crossover signals into a buy/hold call."""
        rsi_buy, _ = self.rsi(stock, 14)
        adx_buy, _, _, _ = self.average_directional_index(stock, 14)
        ma_buy, _, _ = self.moving_avg_crossover(stock, 20, 50, "close")

        signals = rsi_buy + adx_buy + ma_buy
        action = "BUY" if signals >= 2 else "DO NOT BUY"
        return f"Prediction: {action} {stock.tick_name}"

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _dm_and_tr(
        self, stock: Stock
    ) -> tuple[list[float], list[float], list[float]]:
        """Calculate true range, positive DM, and negative DM for each day."""
        true_range: list[float] = []
        pos_dm: list[float] = []
        neg_dm: list[float] = []

        for i in range(len(stock.items)):
            curr_high  = stock.high[i]
            curr_low   = stock.low[i]
            prev_high  = stock.high[i - 1]
            prev_low   = stock.low[i - 1]
            prev_close = stock.close[i - 1]

            up_move   = curr_high - prev_high
            down_move = prev_low  - curr_low

            if up_move > down_move:
                pos_dm.append(max(up_move, 0.0))
                neg_dm.append(0.0)
            else:
                pos_dm.append(0.0)
                neg_dm.append(max(down_move, 0.0))

            true_range.append(
                max(
                    abs(curr_high - curr_low),
                    abs(curr_high - prev_close),
                    abs(curr_low  - prev_close),
                )
            )

        return true_range, pos_dm, neg_dm

    def _smooth(
        self,
        tr: list[float],
        pos: list[float],
        neg: list[float],
        period: int,
    ) -> tuple[list[float], list[float], list[float]]:
        """Rolling average of true range and ±DM over *period* days."""
        smooth_tr  = [sum(tr [i: i + period]) / period for i in range(len(tr)  - period + 1)]
        smooth_pos = [sum(pos[i: i + period]) / period for i in range(len(pos) - period + 1)]
        smooth_neg = [sum(neg[i: i + period]) / period for i in range(len(neg) - period + 1)]
        return smooth_tr, smooth_pos, smooth_neg

    def _directional_index(
        self,
        s_pos: list[float],
        s_neg: list[float],
        avg_tr: list[float],
    ) -> tuple[list[float], list[float]]:
        """Convert smoothed ±DM to ±DI by dividing by average true range."""
        pos_di = [(s_pos[i] / avg_tr[i]) * 100 for i in range(len(s_pos))]
        neg_di = [(s_neg[i] / avg_tr[i]) * 100 for i in range(len(s_pos))]
        return pos_di, neg_di
