from polygon import RESTClient
client = RESTClient("ub3XXNePvsNTCCHX3Wd3wNknwrm1pzbZ")

class Stock():
    first_open = ''
    first_high = ''
    first_low = ''
    first_close = ''
    
    sec_open = ''
    sec_high = ''
    sec_low = ''
    sec_close = ''

    def __init__(self, tick_name, day1, day2):
        self.tick_name = tick_name
        self.day1 = day1
        self.day2 = day2

        aggs = client.get_aggs(
            self.tick_name,
            1,
            "day",
            self.day1,
            self.day2
        )

        index = aggs.__len__() - 1

        Stock.first_open = aggs[0].open
        Stock.first_high = aggs[0].high
        Stock.first_low = aggs[0].low
        Stock.first_close = aggs[0].close

        Stock.sec_open = aggs[index].open
        Stock.sec_high = aggs[index].high
        Stock.sec_low = aggs[index].low
        Stock.sec_close = aggs[index].close
    

    def __str__(self):
        return f"{self.tick_name}"
