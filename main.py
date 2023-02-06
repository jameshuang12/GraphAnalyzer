from datetime import datetime
import stock_class
import confirm_input

'''
for now, class Main will not be tha main class for the entire GUI. it is just the main class for it to be
instantiated. 
'''

class Main():

    #for the first window
    def activate(self, user_data):
        confirmData = confirm_input.userInput(user_data)

        return confirmData

    #for the second window
    def userInputDate(user_data):
        return user_data

    '''
    for now, the stockActivator will be solely done in the backend, and then the functions below will be
    made in a third window that will show the graph, the investment and trading options and their 
    respective graphs
    '''
    def stockActivator(self, user_data):
        clientData = stock_class.Stock(user_data[0], user_data[1], user_data[2])

        return clientData

    def stockActivate(self, clientData):
        per_change = self.percentageChange(clientData)

        while True:
            if len(clientData.items) > 25:
                period = len(clientData.items)
                self.investment(clientData, per_change)
                self.moving_avg_crossover(clientData)
                self.rsi_function(clientData, period)
                self.average_dir_index(clientData, period)

            while True:
                answer = str(input('Would you like to run again for this stock? (y/n): '))
                if answer in ('y', 'n'):
                    break
                print("invalid input.")
            if answer == 'y':
                continue
            else:
                print("Goodbye")
                break


    def percentageChange(self, clientData):
        """ Get the percentage change of the two dates given by the user.

        :param self: All the data needed from the given dates
        :return: the percent change between the first to the second
        """
        print('For the first date')
        data1 = self._ask_user_for_data()
        print('For the second date')
        data2 = self._ask_user_for_data()

        first_call = getattr(clientData, str(data1))
        sec_call = getattr(clientData, str(data2))

        change = int((sec_call[-1] / first_call[0]) * 100)

        if change < 100:
            print('The percentage change had a decline of ' + str(change) + '%')
        else:
            print('The percentage change had a growth of ' + str(change) + '%')

        return change


    def _ask_user_for_data(self):
        """ Ask the user for the specific data they want provided by the stock market

        :param yourmom: All the data needed from the given dates
        :return: the data the user wants to use
        """
        print('Please choose from the options below you would like to use')
        print('1. open, 2. high, 3. low, 4. close')
        data = str(input('Enter the data here: '))

        while data not in ['high', 'open', 'low', 'close']:
            data = str(input('Incorrect input, options are open, high , low, close: '))

        return data


    def investment(self, clientData, percent_change):
        """ Calcualates the investment amount for the user

        :param clientData: All the data needed from the given dates
        :return: the amount gained or lost
        """
        while True:
            amount = str(input('Enter the amount you would like to invest: $'))
            if not amount.isdigit():
                print('Invalid input (requires numeric amount)')
                continue
            else:
                amount = int(amount)
                break

        investmentAmount = int(amount * (percent_change / 100))
        total = abs(int(amount - investmentAmount))

        if investmentAmount < amount:
            print('If you invested on ' + str(clientData.day1) + ' with the amount of $' + str(amount) + ' ,then you'
                                                                                                         " would've lost $" + str(
                total) + " if you withdraw on " + str(clientData.day2) + ".")
        else:
            print('If you invested on ' + str(clientData.day1) + ' with the amount of $' + str(amount) + ' ,then you'
                                                                                                         " would've gained $" + str(
                total) + " if you withdraw on " + str(clientData.day2) + ".")


    def moving_avg_crossover(self,clientData):
        """
        WHAT IT DOES
        """
        short_term_ma = []
        long_term_ma = []

        price_data = getattr(clientData, str(self._ask_user_for_data()))
        moving_avg_range = self._ask_user_for_range(price_data)

        for i in range(len(price_data) - moving_avg_range[0] + 1):
            sum_long_subset = sum(price_data[i: i + moving_avg_range[0]])
            long_term_ma.append(sum_long_subset / moving_avg_range[0])

        for i in range(len(price_data) - moving_avg_range[1] + 1):
            sum_short_subset = sum(price_data[i: i + moving_avg_range[1]])
            short_term_ma.append(sum_short_subset / moving_avg_range[1])
        print("moving average works!")
        return long_term_ma, short_term_ma

    def rsi_function(self, clientData, period):
        rsi_values = []
        for i in range(period):
            gaincounter = 0
            losscounter = 0
            gain = 0
            loss = 0
            for j in range(period - 1, 0, -1):
                if clientData.close[-period + i + j + 1] < clientData.close[-period + i + j]:
                    gaincounter += 1
                    gain += clientData.close[-period + i + j] - clientData.close[-period + i + j + 1]
                else:
                    losscounter += 1
                    loss += abs(clientData.close[-period + i + j + 1] - clientData.close[-period + i + j])
            avg_gain = gain / gaincounter
            avg_loss = loss / losscounter
            rsi = 100 - 100 / (1 + (avg_gain / avg_loss))
            rsi_values.append(rsi)

        print("RSI values works!")
        return rsi_values

    '''    if rsi > 70.000:
            print("The RSI index is " + str(rsi) + ", meaning the stock is currently being overbought"
                                              " and the stock will have a bearish trend in the near future."
                                              " It is strongly not recommended to buy the stock now.")
        elif 70.000 > rsi > 50.000:
            print("The RSI index is " + str(rsi) + ", meaning the stock is being bought more than it is being sold."
                                              " Buying the stock today is encouraged as it is following a "
                                              "bullish trend but it is recommended to either hold for long term or"
                                              "sell it in the near future")
    
        elif 50.00 > rsi > 30.000:
            print("The RSI index is " + str(rsi) + ", meaning the stock is being sold more than it is being bought."
                                              " Buying the stock today is not encouraged as it following a bearish"
                                              " trend but is recommended to buy later")
        else:
            print("The RSI index is " + str(rsi) + ", meaning the stock is currently being oversold and the stock will"
                                              " have a bullish trend in the near future. It is strongly recommended"
                                              " to buy the stock now")
    '''


    def average_dir_index(self, clientData, period):
        dir_index = []
        avg_dir_index = []

        trueRange, posdm, negdm = self._dm_and_tr_calc(clientData)
        s_tr, s_positive, s_negative = self._smooth_calc(trueRange, posdm, negdm, period)
        pos_di, neg_di = self._directional_index(s_positive, s_negative, s_tr)

        for i in range(len(pos_di)):
            dir_index.append((abs(pos_di[i] - neg_di[i])) / (abs(pos_di[i] + neg_di[i])) * 100)

        for i in range(len(dir_index) - period + 1):
            sum_dx = sum(dir_index[i: i + period])
            avg_dir_index.append(sum_dx / period)

        print("adx works!")
        return avg_dir_index, pos_di, neg_di


    def _dm_and_tr_calc(self,clientData):
        true_range = []
        positive_dm = []
        negative_dm = []

        for i in range(1, len(clientData.items)):
            curr_high = clientData.high[i]
            curr_low = clientData.low[i]
            prev_high = clientData.high[i - 1]
            prev_low = clientData.low[i - 1]
            prev_close = clientData.close[i - 1]

            pos_movement = curr_high - prev_high
            neg_movement = prev_low - curr_low

            if pos_movement > neg_movement:
                positive_dm.append(max(pos_movement, 0))
                negative_dm.append(0)
            else:
                positive_dm.append(0)
                negative_dm.append(max(neg_movement, 0))

            true_range.append(max(abs(curr_high - curr_low), abs(curr_high - prev_close),
                                  abs(curr_low - prev_close)))

        return true_range, positive_dm, negative_dm


    def _smooth_calc(self,tr_data, pos_mov, neg_mov, period):
        smooth_true_range = []
        smooth_positive = []
        smooth_negative = []

        for i in range(len(tr_data) - period + 1):
            sum_tr = sum(tr_data[i: i + period])
            sum_pos = sum(pos_mov[i: i + period])
            sum_neg = sum(neg_mov[i: i + period])
            smooth_true_range.append(sum_tr / period)
            smooth_positive.append(sum_pos / period)
            smooth_negative.append(sum_neg / period)

        return smooth_true_range, smooth_positive, smooth_negative


    def _directional_index(self,s_pos_dm, s_neg_dm, avg_tr):
        positive_di = []
        negative_di = []

        for i in range(len(s_pos_dm)):
            positive_di.append((s_pos_dm[i] / avg_tr[i]) * 100)
            negative_di.append((s_neg_dm[i] / avg_tr[i]) * 100)

        return positive_di, negative_di


    def _ask_user_for_range(self, data_range):
        """
        WHAT IT DOES
        """
        sentence = ('Please choose the range (day) for the long-term moving average \n'
                    '1. 200, 2. 100, 3. 50, 4. 25, 5. 10 \nEnter numeric range here: ')

        while True:
            long_range = str(input(sentence))
            if long_range not in ['200', '100', '50', '25', '10']:
                print('Invalid input (options are 200, 100, 50, 25, 10)')
                continue
            elif int(long_range) > len(data_range):
                print('Option must be within range of the two dates')
                continue
            else:
                long_range = int(long_range)
                break

        while True:
            short_range = str(input(sentence.replace("long-term", "short-term")))
            if short_range not in ['200', '100', '50', '25', '10']:
                print('Invalid input (options are 200, 100, 50, 25, 10)')
                continue
            elif int(short_range) >= long_range:
                print('Range for short-term must be less than long-term')
                continue
            else:
                short_range = int(short_range)
                break

        return long_range, short_range


    def buy_or_not(self):
        """
        :param: rsi function value, ADX function value, moving average value(Calculation TBD)
        :return: statement that will tell user whether to buy stock or not based on the three indicating factors
        """
        return 1


if __name__ == '__main__':
    main_instance = Main()
    main_instance.activate()
