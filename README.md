# GraphAnalyzer

Welcome to our personal project. We are a group of Computer Science majors from Vanderbilt University engaged in diverse projects aimed at showcasing our programming prowess and expanding our skill sets within the realm of coding.

Our project, GraphAnalyzer, revolves around facilitating consumer interaction with company stock data. Through this application, users are prompted to specify a company's stock ticker and provide two distinct dates, enabling the extraction of the company's stock performance within the specified timeframe. This sophisticated program remains adept at procuring real-time market share data, generating an array of informative charts, and presenting tailored investment strategies to the consumer.

The consumer has the option to see the percentage change, stock prices, RSI value, ADX value, moving average value, and the invested value net worth between the two dates. Furthermore, the software possesses the functionality to accept a user-specified value, subsequently utilizing our proprietary algorithm to determine the optimal withdrawal date for the specified amount.

In essence, GraphAnalyzer showcases our team's dedication to harnessing computational proficiency for the analysis of financial data, providing users with invaluable insights to inform their investment decisions.

## Skillset

API · Python · PyQt6 · Matplotlib

## How to Use

**`stock_class.py`** is the module created to retrieve the company's stock data from Polygon's API. It reads your API key from the environment and constructs a `Stock` object holding OHLC values, high, low, close, and open prices for the requested date range.

**`StockSymbols.csv`** facilitates the program's identification of specific company stock symbols. **`confirm_input.py`** interfaces with this file to validate that the consumer's ticker input matches a known symbol, and performs date range validation.

**`main_functions.py`** is the business-logic layer — it exposes methods for computing RSI, ADX, moving average crossover, percentage change, and the buy recommendation algorithm. It has no knowledge of Qt widgets.

**`gui.py`** initializes and manages the three PyQt6 windows that guide the consumer's journey: ticker entry → date selection → results. The results window provides all requested information and options the consumer can choose from, ranging from percentage change, stock prices, RSI value, ADX value, moving average value, and the invested value net worth between the two dates.

**`main.py`** is the entry point — it creates the QApplication, applies the global stylesheet, and launches the first window.

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
   # Edit .env and add your Polygon.io API key
   ```

4. **Run the app**
   ```bash
   python main.py
   ```
   On Windows, double-click `run.bat`.

## API Reference

Stock data is provided by [Polygon.io](https://polygon.io). A free API key is required and must be set as `POLYGON_API_KEY` in your `.env` file.

## Additional Information

More features are actively being added to GraphAnalyzer. Comments are written throughout the codebase to assist with guidance.

## Authors

James Huang, Jeff Zheng, Bryan Back — Computer Science, Vanderbilt University

## License

MIT — see [LICENSE.txt](LICENSE.txt)
