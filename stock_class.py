from polygon import RESTClient
client = RESTClient("ub3XXNePvsNTCCHX3Wd3wNknwrm1pzbZ")

class Stock():
    def __init__(self, tick_name, day1, day2):
        self.tick_name = tick_name
        self.day1 = day1
        self.day2 = day2

        self.high = []
        self.low = []
        self.close = []
        self.open = []

        aggs = client.get_aggs(
            self.tick_name,
            1,
            "day",
            self.day1,
            self.day2
        )
            
        for i in range(len(aggs)):
            self.open.append(aggs[i].open)
            self.high.append(aggs[i].high)
            self.low.append(aggs[i].low)
            self.close.append(aggs[i].close)      


    def __str__(self):
        return f"{self.tick_name}"
