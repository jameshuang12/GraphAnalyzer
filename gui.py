"""
gui.py
------
PyQt5 GUI for the Graph Analyzer stock tool.

Window flow:
  GraphAnalyzerNameWindow  →  GraphAnalyzerDateWindow  →  GraphAnalyzerStockWindow

A single Main instance is created in the first window and passed to each
subsequent window so the business-logic layer is not re-instantiated needlessly.
"""

import sys
from datetime import date, timedelta

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import (
    QApplication, QCheckBox, QDateEdit, QDialog, QGridLayout, QGroupBox,
    QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QVBoxLayout,
    QWidget,
)
from matplotlib import style

from main_functions import Main

# ---------------------------------------------------------------------------
# Shared constants
# ---------------------------------------------------------------------------

APP_FONT      = QtGui.QFont("Helvetica Neue", 18)
INPUT_FONT    = QtGui.QFont("Verdana", 18)
INFO_FONT     = QtGui.QFont("Helvetica Neue", 13)
TITLE_FONT    = QtGui.QFont("Helvetica Neue", 36)
UNDERLINE_FONT = QtGui.QFont("Helvetica Neue", 13)

PRIMARY_COLOR   = "#29c455"   # search / confirm buttons
SECONDARY_COLOR = "#4a90d9"   # action buttons
DANGER_COLOR    = "#e05c5c"   # exit button

WINDOW_ICON = "stocks.jpg"


# ---------------------------------------------------------------------------
# Base window
# ---------------------------------------------------------------------------

class _BaseWindow(QMainWindow):
    """Shared behaviour for all Graph Analyzer windows."""

    def __init__(self, title: str, main: Main) -> None:
        super().__init__()
        self.main = main
        self.setWindowTitle(title)
        self.setWindowIcon(QtGui.QIcon(WINDOW_ICON))
        self.setFont(APP_FONT)

    # ------------------------------------------------------------------
    def show_warning(self, title: str, message: str) -> None:
        """Display a modal warning dialog."""
        msg = QMessageBox(self)
        msg.setWindowTitle(title)
        msg.setText(message)
        msg.setIcon(QMessageBox.Warning)
        msg.exec_()

    # ------------------------------------------------------------------
    def _center_on_screen(self) -> None:
        screen = QApplication.primaryScreen().availableGeometry()
        fg = self.frameGeometry()
        fg.moveCenter(screen.center())
        self.move(fg.topLeft())

    @staticmethod
    def _apply_plot_style() -> None:
        """Set up a consistent matplotlib style for every chart."""
        mpl.rcParams["toolbar"] = "None"
        plt.style.use("dark_background")
        style.use("ggplot")


# ---------------------------------------------------------------------------
# Window 1 – ticker entry
# ---------------------------------------------------------------------------

class GraphAnalyzerNameWindow(_BaseWindow):
    """Prompt the user for a stock ticker symbol."""

    def __init__(self) -> None:
        super().__init__("Graph Analyzer", Main())

        layout = QGridLayout()
        central = QWidget(self)
        central.setLayout(layout)
        self.setCentralWidget(central)

        prompt = QLabel("Enter a ticker symbol to get started:")
        prompt.setFont(APP_FONT)
        layout.addWidget(prompt, 0, 0, 1, 2)

        self._ticker_input = QLineEdit()
        self._ticker_input.setFixedHeight(60)
        self._ticker_input.setFont(INPUT_FONT)
        self._ticker_input.setPlaceholderText("e.g. AAPL, MSFT, TSLA")
        layout.addWidget(self._ticker_input, 1, 0)

        search_btn = QPushButton("Search")
        search_btn.setFixedHeight(60)
        search_btn.setStyleSheet(f"QPushButton {{ background-color: {PRIMARY_COLOR}; }}")
        search_btn.clicked.connect(self._on_search)
        layout.addWidget(search_btn, 1, 1)

        self._ticker_input.returnPressed.connect(self._on_search)

        self.setMinimumWidth(480)
        self._center_on_screen()

    # ------------------------------------------------------------------
    def _on_search(self) -> None:
        ticker = self._ticker_input.text().strip().upper()
        if not self.main.validate_ticker(ticker):
            self.show_warning("Invalid Ticker", f'"{ticker}" was not found. Check the symbol and try again.')
            self._ticker_input.clear()
            return
        self.hide()
        self._date_window = GraphAnalyzerDateWindow(ticker, self.main)
        self._date_window.show()


# ---------------------------------------------------------------------------
# Window 2 – date range entry
# ---------------------------------------------------------------------------

class GraphAnalyzerDateWindow(_BaseWindow):
    """Collect a start and end date for the stock query."""

    def __init__(self, ticker: str, main: Main) -> None:
        super().__init__("Graph Analyzer – Select Dates", main)
        self._ticker = ticker
        self._first_date: date | None = None

        layout = QGridLayout()
        central = QWidget(self)
        central.setLayout(layout)
        self.setCentralWidget(central)

        self._prompt = QLabel(
            f"Stock found: <b>{ticker}</b><br>"
            "Enter the <b>start</b> date (must be within the past two years):"
        )
        self._prompt.setTextFormat(Qt.RichText)
        self._prompt.setFont(APP_FONT)
        self._prompt.setWordWrap(True)
        layout.addWidget(self._prompt, 0, 0, 1, 2)

        self._date_edit = QDateEdit()
        self._date_edit.setCalendarPopup(True)
        self._date_edit.setDisplayFormat("yyyy-MM-dd")
        self._date_edit.setDate(
            QDate.currentDate().addMonths(-6)
        )
        self._date_edit.setFixedHeight(55)
        self._date_edit.setFont(INPUT_FONT)
        layout.addWidget(self._date_edit, 1, 0)

        today_label = QLabel(f"Today: {date.today()}")
        today_label.setFont(INFO_FONT)
        layout.addWidget(today_label, 2, 0)

        confirm_btn = QPushButton("Confirm")
        confirm_btn.setFixedHeight(55)
        confirm_btn.setStyleSheet(f"QPushButton {{ background-color: {PRIMARY_COLOR}; }}")
        confirm_btn.clicked.connect(self._on_confirm)
        layout.addWidget(confirm_btn, 1, 1)

    # ------------------------------------------------------------------
    def _on_confirm(self) -> None:
        qdate = self._date_edit.date()
        year  = str(qdate.year())
        month = str(qdate.month())
        day   = str(qdate.day())

        if not self.main.validate_date(year, month, day):
            self.show_warning(
                "Invalid Date",
                "Date must be a real calendar date within the past two years."
            )
            return

        picked = date(qdate.year(), qdate.month(), qdate.day())

        if self._first_date is None:
            self._first_date = picked
            self._prompt.setText(
                f"Start date: <b>{picked}</b><br>"
                "Now enter the <b>end</b> date:"
            )
        else:
            if picked <= self._first_date:
                self.show_warning("Invalid Date", "End date must be after the start date.")
                return
            self.hide()
            self._stock_window = GraphAnalyzerStockWindow(
                self._ticker, self._first_date, picked, self.main
            )
            self._stock_window.show()


# ---------------------------------------------------------------------------
# Window 3 – analysis dashboard
# ---------------------------------------------------------------------------

class GraphAnalyzerStockWindow(_BaseWindow):
    """Main analysis dashboard: charts, indicators, and investment tools."""

    def __init__(self, ticker: str, day_one: date, day_two: date, main: Main) -> None:
        super().__init__("Graph Analyzer", main)

        try:
            self._stock = main.build_stock(ticker, day_one, day_two)
        except Exception as exc:
            self.show_warning("API Error", f"Could not fetch data for {ticker}:\n{exc}")
            return

        if len(self._stock) == 0:
            self.show_warning(
                "No Data",
                f"No trading days found for {ticker} between {day_one} and {day_two}.\n"
                "Try a wider date range or a different ticker."
            )
            return

        layout = QGridLayout()
        central = QWidget(self)
        central.setLayout(layout)
        self.setCentralWidget(central)

        self._build_title(layout)
        self._build_action_buttons(layout)
        self._build_info_panel(layout)

        self.setMinimumSize(820, 580)
        self._center_on_screen()

    # ------------------------------------------------------------------
    # Layout helpers
    # ------------------------------------------------------------------

    def _build_title(self, layout: QGridLayout) -> None:
        title = QLabel(self._stock.tick_name)
        title.setFont(TITLE_FONT)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title, 0, 0, 1, 7)

    def _build_action_buttons(self, layout: QGridLayout) -> None:
        btn_style = f"QPushButton {{ background-color: {SECONDARY_COLOR}; color: white; }}"

        buttons = [
            ("Open Graph",    self._show_price_graph,     2, 0),
            ("Investment",    self._open_investment_dialog, 3, 0),
            ("RSI",           self._show_rsi_graph,        4, 0),
            ("ADX",           self._show_adx_graph,        5, 0),
            ("Moving Avg",    self._open_mov_avg_dialog,   6, 0),
            ("Should I buy?", self._show_buy_recommendation, 7, 0),
        ]
        for label, slot, row, col in buttons:
            btn = QPushButton(label)
            btn.setFont(INFO_FONT)
            btn.setFixedHeight(50)
            btn.setStyleSheet(btn_style)
            btn.clicked.connect(slot)
            layout.addWidget(btn, row, col, 1, 2)

        exit_btn = QPushButton("Exit")
        exit_btn.setFont(INFO_FONT)
        exit_btn.setFixedHeight(50)
        exit_btn.setStyleSheet(f"QPushButton {{ background-color: {DANGER_COLOR}; color: white; }}")
        exit_btn.clicked.connect(self._confirm_exit)
        layout.addWidget(exit_btn, 8, 0, 1, 2)

    def _build_info_panel(self, layout: QGridLayout) -> None:
        stock = self._stock
        info_group = QGroupBox("Price Summary")
        info_group.setFont(INFO_FONT)
        info_layout = QVBoxLayout()

        rows = [
            f"Start date:   {stock.day_one}",
            f"End date:     {stock.day_two}",
            f"Trading days: {len(stock)}",
        ]
        if len(stock) > 0:
            last = len(stock) - 1
            rows += [
                "",
                f"Open  (start): ${stock.open[0]:.2f}",
                f"High  (start): ${stock.high[0]:.2f}",
                f"Low   (start): ${stock.low[0]:.2f}",
                f"Close (start): ${stock.close[0]:.2f}",
                "",
                f"Open  (end):   ${stock.open[last]:.2f}",
                f"High  (end):   ${stock.high[last]:.2f}",
                f"Low   (end):   ${stock.low[last]:.2f}",
                f"Close (end):   ${stock.close[last]:.2f}",
            ]
        else:
            rows.append("No trading data for this range.")

        for text in rows:
            lbl = QLabel(text)
            lbl.setFont(INFO_FONT)
            info_layout.addWidget(lbl)

        info_group.setLayout(info_layout)
        layout.addWidget(info_group, 1, 3, 9, 4)

    # ------------------------------------------------------------------
    # Chart actions
    # ------------------------------------------------------------------

    def _show_price_graph(self) -> None:
        stock = self._stock
        self._apply_plot_style()
        plt.plot(stock.high, color="black")
        plt.xlabel(f"From {stock.day_one} to {stock.day_two} (trading days)")
        plt.ylabel("Price ($)")
        plt.title(stock.tick_name)
        plt.show()

    def _show_rsi_graph(self) -> None:
        stock = self._stock
        _, rsi_values = self.main.rsi(stock, 14)
        approx_start = stock.day_two - timedelta(days=21)

        self._apply_plot_style()
        fig, ax = plt.subplots()
        ax.plot(rsi_values, color="black")
        ax.axhline(y=30, color="red",  label="Oversold (30)")
        ax.axhline(y=70, color="blue", label="Overbought (70)")
        ax.text(len(rsi_values) - 1, 31, "30", color="red",  ha="right")
        ax.text(len(rsi_values) - 1, 71, "70", color="blue", ha="right")
        ax.set_xlabel(f"From ~{approx_start} to {stock.day_two}")
        ax.set_ylabel("RSI")
        ax.set_title(f"{stock.tick_name} – RSI (14)")
        ax.legend()
        plt.show()

    def _show_adx_graph(self) -> None:
        stock = self._stock
        _, adx, pos_di, neg_di = self.main.average_directional_index(stock, 14)
        adx_padded = [np.nan] * 13 + adx

        self._apply_plot_style()
        fig, ax = plt.subplots()
        ax.plot(adx_padded, color="black",  label="ADX")
        ax.plot(pos_di,     color="blue",   label="+DI")
        ax.plot(neg_di,     color="purple", label="-DI")
        ax.axhline(y=25, color="red",    label="Weak trend (25)")
        ax.axhline(y=50, color="yellow", label="Moderate trend (50)")
        ax.axhline(y=75, color="green",  label="Strong trend (75)")
        ax.set_xlabel(f"From {stock.day_one} to {stock.day_two}")
        ax.set_ylabel("ADX / ±DI")
        ax.set_title(f"{stock.tick_name} – ADX (14)")
        ax.legend()
        plt.show()

    # ------------------------------------------------------------------
    # Moving average dialog
    # ------------------------------------------------------------------

    def _open_mov_avg_dialog(self) -> None:
        """Show a dialog to choose MA parameters, then plot."""
        while True:
            dialog = QDialog(self)
            dialog.setWindowTitle("Moving Average Options")

            short_options = ["10", "25", "50", "100"]
            long_options  = ["25", "50", "100", "200"]
            price_options = ["close", "open", "high", "low"]

            short_boxes = self._checkbox_group("Short-term window", short_options)
            long_boxes  = self._checkbox_group("Long-term window",  long_options)
            price_boxes = self._checkbox_group("Price type",        price_options)

            ok_btn = QPushButton("Plot")
            ok_btn.clicked.connect(dialog.accept)

            dlg_layout = QVBoxLayout()
            for group in (short_boxes[0], long_boxes[0], price_boxes[0]):
                dlg_layout.addWidget(group)
            dlg_layout.addWidget(ok_btn)
            dialog.setLayout(dlg_layout)

            if dialog.exec_() != QDialog.Accepted:
                break  # user closed / cancelled

            short = next((int(c.text()) for c in short_boxes[1] if c.isChecked()), None)
            long  = next((int(c.text()) for c in long_boxes[1]  if c.isChecked()), None)
            price = next((c.text()      for c in price_boxes[1] if c.isChecked()), None)

            if short is None or long is None or price is None:
                self.show_warning("Missing Selection", "Please select one option from each group.")
                continue
            if short >= long:
                self.show_warning("Invalid Selection", "Long-term window must be larger than short-term.")
                continue
            if long >= len(self._stock):
                self.show_warning("Invalid Selection",
                                  "Long-term window must be smaller than the number of trading days available.")
                continue

            self._show_mov_avg_graph(short, long, price)
            break

    @staticmethod
    def _checkbox_group(title: str, options: list[str]) -> tuple[QGroupBox, list[QCheckBox]]:
        """Build a single-select checkbox group and return (group_widget, checkboxes)."""
        group = QGroupBox(title)
        layout = QVBoxLayout()
        boxes: list[QCheckBox] = []

        for opt in options:
            cb = QCheckBox(opt)
            cb.stateChanged.connect(
                lambda state, o=opt, bs=boxes: GraphAnalyzerStockWindow._enforce_single(state, o, bs)
            )
            layout.addWidget(cb)
            boxes.append(cb)

        group.setLayout(layout)
        return group, boxes

    @staticmethod
    def _enforce_single(state: int, option: str, boxes: list[QCheckBox]) -> None:
        """Uncheck all boxes except the one just checked (radio-button behaviour)."""
        if state == Qt.Checked:
            for cb in boxes:
                if cb.text() != option:
                    cb.setChecked(False)

    def _show_mov_avg_graph(self, short: int, long: int, price: str) -> None:
        stock = self._stock
        _, long_ma, short_ma = self.main.moving_avg_crossover(stock, short, long, price)
        long_padded = [np.nan] * (long - short) + long_ma

        self._apply_plot_style()
        fig, ax = plt.subplots()
        ax.plot(long_padded, color="red",  label=f"{long}-day MA")
        ax.plot(short_ma,    color="blue", label=f"{short}-day MA")
        ax.set_xlabel("Trading days")
        ax.set_ylabel(f"{price.capitalize()} price ($)")
        ax.set_title(f"{stock.tick_name} – Moving Average Crossover")
        ax.legend()
        plt.show()

    # ------------------------------------------------------------------
    # Investment dialog
    # ------------------------------------------------------------------

    def _open_investment_dialog(self) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle("Investment Calculator")

        label  = QLabel(f"Amount invested on {self._stock.day_one} ($):")
        label.setFont(INFO_FONT)
        entry  = QLineEdit()
        entry.setPlaceholderText("e.g. 1000")
        ok_btn = QPushButton("Calculate")

        ok_btn.clicked.connect(lambda: self._calculate_investment(entry.text(), dialog))

        dlg_layout = QGridLayout()
        dlg_layout.addWidget(label,  0, 0)
        dlg_layout.addWidget(entry,  0, 1)
        dlg_layout.addWidget(ok_btn, 1, 1)
        dialog.setLayout(dlg_layout)
        dialog.show()

    def _calculate_investment(self, raw: str, dialog: QDialog) -> None:
        try:
            amount = float(raw)
            if amount < 0:
                raise ValueError
        except ValueError:
            self.show_warning("Invalid Input", "Please enter a positive number.")
            return

        is_gain, pct = self.main.percentage_change(self._stock)
        result = self.main.investment_return(pct, amount)
        formatted_amount = f"${amount:,.2f}"
        direction = "gained" if is_gain else "lost"
        sign      = "+" if is_gain else ""

        msg = QMessageBox(self)
        msg.setWindowTitle("Investment Result")
        msg.setText(
            f"Invested on {self._stock.day_one}: {formatted_amount}\n"
            f"Result on   {self._stock.day_two}: ${result:,} {direction}\n"
            f"Percent change: {sign}{pct}%"
        )
        msg.exec_()
        dialog.accept()

    # ------------------------------------------------------------------
    # Buy recommendation
    # ------------------------------------------------------------------

    def _show_buy_recommendation(self) -> None:
        msg = QMessageBox(self)
        msg.setWindowTitle("Buy Recommendation")
        msg.setText(self.main.buy_recommendation(self._stock))
        msg.exec_()

    # ------------------------------------------------------------------
    # Exit
    # ------------------------------------------------------------------

    def _confirm_exit(self) -> None:
        reply = QMessageBox.question(
            self, "Quit",
            "Are you sure you want to quit?",
            QMessageBox.Yes | QMessageBox.No,
        )
        if reply == QMessageBox.Yes:
            QApplication.instance().quit()
