from polygon import RESTClient

# This key was generated specifically for us to access Polygon API database
client = RESTClient("ub3XXNePvsNTCCHX3Wd3wNknwrm1pzbZ")


class Stock:
    """
    This class is created to store all the values from the user's specified company.
    The class will initialize the company name, day 1, and day 2. For the stock information,
    it will collect the item, high, low, open, and close. The client will go into the API and
    access all the information needed.
    """

    def __init__(self, company_name:str, day_one:str, day_two:str):
        """
        Calls the constructor using the Stock object that will have to accept all 3 parameters.
        :param company_name: The name of the specified company
        :param day_one: The first stock date requested by the user
        :param day_two: THe second stock date requested by the user
        """

        self.tick_name = company_name
        self.day_one = day_one
        self.day_two = day_two
        self.items = []
        self.high = []
        self.low = []
        self.close = []
        self.open = []

        # This is the client info of the company
        self.aggregate_bars = client.get_aggs(
            self.tick_name,
            1,
            "day",
            self.day_one,
            self.day_two
        )

        self.get_stock_information(self.aggregate_bars)

    def __str__(self):
        """
        :return: The abbreviation of the company's stock name
        """
        return f"{self.tick_name}"

    def __len__(self):
        """
        :return: The total amount of stocks added to the list, not counting weekends or holidays
        """
        return len(self.items)

    def get_stock_information(self, aggregate_bars) -> None:
        """
        Inserts open, high, low, and close to a list by collecting the values from
        the two dates specified by the consumer
        :param aggregate_bars: All the information from the stock company
        :return: None
        """
        for i in range(len(aggregate_bars)):
            self.open.append(aggregate_bars[i].open)
            self.high.append(aggregate_bars[i].high)
            self.low.append(aggregate_bars[i].low)
            self.close.append(aggregate_bars[i].close)
            # Inserts each of the items in a list that will be
            # capable to compute the rsi function
            self.items.append(aggregate_bars[i])
