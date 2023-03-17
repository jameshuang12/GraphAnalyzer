from polygon import RESTClient
# This key was generated specifically for us to access Polygon API database
client = RESTClient("ub3XXNePvsNTCCHX3Wd3wNknwrm1pzbZ")

# Program Description: This program is used to create a class template to store
# all the value from the specified company.
class Stock():
    def __init__(self, company_name, day_one, day_two):
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
        aggs = client.get_aggs(
            self.tick_name,
            1,
            "day",
            self.day_one,
            self.day_two
        )

        # Inserts open, high, low, and close to a list
        # by collecting between the two dates specified
        for i in range(len(aggs)):
            self.open.append(aggs[i].open)
            self.high.append(aggs[i].high)
            self.low.append(aggs[i].low)
            self.close.append(aggs[i].close)

        # Inserts each of the items in a list into another list that will be
        # capable to compute the rsi function
        for i in range(len(aggs)):
            self.items.append(aggs[i])

    def __str__(self):
        """
        :return: The stock abbreviation of the company name
        """
        return f"{self.tick_name}"

    def __len__(self):
        """
        :return: The total amount of stocks added to the list, not counting weekends or holidays
        """
        return len(self.items)