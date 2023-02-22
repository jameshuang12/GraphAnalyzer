# GraphAnalyzer Background
Welcome to our personal project. We are all Computer Science Majors at Vanderbilt University working on various projects to showcase our skills and learn new skillsets in the coding world. Graph Analyzer intakes two specific dates from a specific company’s stock shares. The program is capable of designing a line chart of two dates. In addition, the program has the ability to compare and provide investing strategies for the comsumer. The comsumer has the option to see the percentage change, stock prices, rsi value, adx value, moving average value, and the invested value net worth between the two dates. Moreover, the program can take a value specified by the consumer and export the best date to withdraw that amount through our algorithm.

# Skillset
API, Python, PyQt5, Matplotlib

# Additional Information
There are currently more features that are being added to the GUI of Graph Analyzer. Thoughout the file, there are comments made to help guide you through our code. 

# API Reference
The API used to get all the stock's data was provided by Polygon.

# How to Use
The stock_class.py was the first python file created to collect the company's stock shares from the Polygon's API. The file will save the company's name, first date, second date, high, low, close, and open. In addition, the StockSymbols.csv was created to help the program find the initials of the specific company's stock shares. This runs through the confirm_input.py. 
Confirm_input.py is the second python file created to read the csv file whenever the user's input the date they are requesting. The program then will save the data, check for errors if the input is incorrect, and create a hashmap for all the values within the two dates.
Once the values are all saved and there are no errors, the gui.py will now start it's action. First, it initializes the first window in the GUI. Throughout the initialization, the program will use stocks.jpg for design and main.py to compute certain values that will be needed for the consumer. In addition, there are extra functions in the first GUI that perform certain action. The first window will ask for the consumer's company they are interested in. Once the company's initial is valid, it will open up the second GUI. The second GUI will ask for the first dates.
