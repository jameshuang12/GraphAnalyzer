# GraphAnalyzer

A desktop stock analysis tool built with Python and PyQt6. Enter a ticker symbol and date range to retrieve real-time OHLC data from the Polygon.io API and explore a suite of technical indicators and investment tools.

## Features

- **Percentage change** — overall return between two dates
- **Stock price chart** — OHLC candlestick-style line chart
- **RSI (Relative Strength Index)** — momentum oscillator with overbought/oversold bands
- **ADX (Average Directional Index)** — trend strength with +DI / −DI lines
- **Moving average crossover** — 20-day vs 50-day SMA signal
- **Investment calculator** — dollar gain/loss on a hypothetical position
- **Buy recommendation** — combined RSI + ADX + MA crossover signal

## Requirements

- Python 3.13+
- A free [Polygon.io](https://polygon.io) API key

## Setup

1. **Clone the repo**
   ```bash
   git clone https://github.com/jameshuang12/GraphAnalyzer.git
   cd GraphAnalyzer
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your API key**
   ```bash
   cp .env.example .env
   # Edit .env and replace the placeholder with your Polygon.io key
   ```

4. **Run the app**
   ```bash
   python main.py
   ```
   Or on Windows, double-click `run.bat`.

## Project Structure

| File | Purpose |
|------|---------|
| `main.py` | Entry point — creates the QApplication and applies the global stylesheet |
| `gui.py` | All PyQt6 windows (ticker input → date selection → results) |
| `main_functions.py` | Business logic: validation, Stock construction, technical indicators |
| `stock_class.py` | Polygon.io API wrapper — fetches OHLC data into a Stock object |
| `confirm_input.py` | Input validation helpers (ticker lookup, date range checks) |
| `StockSymbols.csv` | ~8 000 valid ticker symbols used for ticker validation |
| `.env.example` | Template for your POLYGON_API_KEY |

## Tech Stack

Python · PyQt6 · Matplotlib · Polygon.io API

## Authors

James Huang, Jeff Zheng, Bryan Back — Computer Science, Vanderbilt University

## License

MIT — see [LICENSE.txt](LICENSE.txt)
