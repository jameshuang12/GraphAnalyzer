# GraphAnalyzer Background
Welcome to our personal projects. We are a group of Computer Science majors from Vanderbilt University engaged in diverse projects aimed at showcasing our programming prowess and expanding our skill sets within the realm of coding.

Our project, Graph Analyzer, revolves around facilitating consumer interaction with company stock data. Through this application, users are prompted to specify a company's stock shares and provide two distinct dates, enabling the extraction of the company's stock performance within the specified timeframe. This sophisticated program remains adept at procuring real-time market share data, generating an array of informative charts, and presenting tailored investment strategies to the consumer.

The consumer has the option to see the percentage change, stock prices, RSI value, ADX value, moving average value, and the invested value net worth between the two dates. Furthermore, the software possesses the functionality to accept a user-specified value, subsequently utilizing our proprietary algorithm to determine the optimal withdrawal date for the specified amount.

In essence, Graph Analyzer showcases our team's dedication to harnessing computational proficiency for the analysis of financial data, providing users with invaluable insights to inform their investment decisions.

# Skillset
API, Python, PyQt5, Matplotlib

# How to Use
The "stock_class.py' is the module created to retrieve the company's stock shares from Polygon's API. 
To get this module's import, execute:
`pip install polygon-api-client`

This module is engineered to the company's name, initial and final dates, high, low, close, and open values. Complementing this, the "StockSymbols.csv" file was designed to facilitate the program's identification of specific company stock symbols. The execution sequence subsequently involves interfacing with "confirm_input.py," ensuring congruence between the consumer's input and corresponding symbols.

"confirm_input.py" constitutes the second Python file, responsible for parsing the CSV file when the consumer provides their desired date range. The program then stores the acquired data, undertakes error validation for input accuracy, and constructs a comprehensive hashmap with all values between the specified date range.

With data preservation and error checking mechanisms in place, "gui.py" is then executed. This module initializes the primary window within the graphical user interface (GUI). As part of this initialization process, the program integrates "stocks.jpg" for aesthetics and leverages "main.py" to compute various functions.

Guiding the consumer's journey, the primary window solicits the consumer's designated company of interest. Upon successful validation of the company's initials, the interface seamlessly transitions to the secondary GUI. In this subsequent interface, users are prompted to provide the initial date parameter. Lastly, the third window provides all the information of the consumer's request and options the consumer can choose from to execute. This would range from percentage change, stock prices, RSI value, ADX value, moving average value, and the invested value net worth between the two dates.

# API Reference
The API used to get all the stock's data was provided by Polygon.

# Additional Information
Currently, more features that are being added to Graph Analyzer. Thoughout the file, comments are written to assist you with guidance through our code. 
