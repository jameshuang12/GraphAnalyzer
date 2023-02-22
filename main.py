from datetime import datetime
import stock_class
import confirm_input
from datetime import date

'''
for now, class Main will not be tha main class for the entire GUI. it is just the main class for it to be
instantiated. 
'''

class Main():

    #for the first window GUI
    def nameActivate(self, user_data):
        confirmData = confirm_input.userInput(user_data)
        return confirmData

    #for the second window
    def dateActivate(self, year, month, day):
        user_date = confirm_input.userInputDate(year, month, day)
        return user_date

    def compareDates(self, yearOne, monthOne, dayOne, yearTwo, monthTwo, dayTwo):
        yearOne = int(yearOne)
        monthOne = int(monthOne)
        dayOne = int(dayOne)
        yearTwo = int(yearTwo)
        monthTwo = int(monthTwo)
        dayTwo = int(dayTwo)

        firstDate = date(yearOne, monthOne, dayOne)
        secondDate = date(yearTwo, monthTwo, dayTwo)

        return firstDate, secondDate

    '''
    for now, the stockActivator will be solely done in the backend, and then the functions below will be
    made in a third window that will show the graph, the investment and trading options and their 
    respective graphs
    '''

    def stockActivator(self, user_data, user_date_one, user_date_two):
        clientData = stock_class.Stock(user_data, user_date_one, user_date_two)

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

    def moving_avg_crossover(self, clientData):
        """Calculates the short-term and long-term moving averages for each date
        :param clientData: All the data needed from the given dates
        :returns: list of long-term and short-term moving averages
        """
        short_term_ma = []
        long_term_ma = []

        # Utilizes user-input to retrieve relevant data from clientData object
        price_data = getattr(clientData, str(self._ask_user_for_data()))
        # Asks user for what range to use for long-term and short-term
        moving_avg_range = self._ask_user_for_range(price_data)

        # Calculates long-term moving average for each day and appends it to long-term list
        for i in range(len(price_data) - moving_avg_range[0] + 1):
            sum_long_subset = sum(price_data[i: i + moving_avg_range[0]])
            long_term_ma.append(sum_long_subset / moving_avg_range[0])

        # Calculates short-term moving average for each day and appends it to short-term list
        for i in range(len(price_data) - moving_avg_range[1] + 1):
            sum_short_subset = sum(price_data[i: i + moving_avg_range[1]])
            short_term_ma.append(sum_short_subset / moving_avg_range[1])

        return short_term_ma[-1] > long_term_ma[-1], long_term_ma, short_term_ma

    def _ask_user_for_range(data_price):
        """Ask user for valid range to use for calculating long-term and short-term
           moving average
        :param data_price: the type of data (open, close, high, low) being used
        :returns: int tuple with valid long and short-term range
        """
        sentence = ('Please choose the range (day) for the long-term moving average \n'
                    '1. 200, 2. 100, 3. 50, 4. 25, 5. 10 \nEnter numeric range here: ')

        # Prompts user for long range until a valid input is received
        while True:
            long_range = str(input(sentence))
            # If input is not any of the five in the list
            if long_range not in ['200', '100', '50', '25', '10']:
                print('Invalid input (options are 200, 100, 50, 25, 10)')
                continue
            # If input range is longer the range for price
            elif int(long_range) > len(data_price):
                print('Option must be within range of the two dates')
                continue
            else:
                long_range = int(long_range)
                break

        # Prompts user for short range until a valid input is received
        while True:
            short_range = str(input(sentence.replace("long-term", "short-term")))
            # If input is not any of the five in the list
            if short_range not in ['200', '100', '50', '25', '10']:
                print('Invalid input (options are 200, 100, 50, 25, 10)')
                continue
            # If input short range is greater than long range
            elif int(short_range) >= long_range:
                print('Range for short-term must be less than long-term')
                continue
            else:
                short_range = int(short_range)
                break

        return long_range, short_range

    def average_dir_index(self, clientData, period):
        """Calculates the average direction index (ADX) for a specific period
        param: ClientData: All the data needed from the given dates
        param: period: specific time range used to calculate the average (usually 14)
        returns: list for average directional index, positive directional index,
                 and negative directional index
        """
        dir_index = []
        avg_dir_index = []

        # Calculates true range, positive and negative directional movement
        trueRange, posdm, negdm = self._dm_and_tr_calc(clientData)
        # Smooths the true range, positive and negative directional movement over the period
        s_tr, s_positive, s_negative = self._smooth_calc(trueRange, posdm, negdm, period)
        # Calculates both the negative and positive directional index
        pos_di, neg_di = self._directional_index(s_positive, s_negative, s_tr)

        # Calculates the daily directional index using positive and negative directional index
        for i in range(len(pos_di)):
            dir_index.append((abs(pos_di[i] - neg_di[i])) / (abs(pos_di[i] + neg_di[i])) * 100)

        # Smooths (averages) the directional index and appends it to the ADX list
        for i in range(len(dir_index) - period + 1):
            sum_dx = sum(dir_index[i: i + period])
            avg_dir_index.append(sum_dx / period)

        return ((avg_dir_index[-1] > 20) and (pos_di[-1] > neg_di[-1])), avg_dir_index, pos_di, neg_di

    def _dm_and_tr_calc(self,clientData):
        """Calculates true range, positive and negative directional movement (dm)

        param clientData: All the data needed from the given dates
        returns: list for true range, positive dm, and negative dm
        """
        true_range = []
        positive_dm = []
        negative_dm = []

        # Iterating through each day in the clientData day range
        for i in range(1, clientData.day_range):
            # Retrieves necessary values from clientData for day i calculations
            curr_high = clientData.high[i]
            curr_low = clientData.low[i]
            prev_high = clientData.high[i - 1]
            prev_low = clientData.low[i - 1]
            prev_close = clientData.close[i - 1]

            # Calculates day i's positive and negative movement
            pos_movement = curr_high - prev_high
            neg_movement = prev_low - curr_low

            # Appends positive movement or 0 (whichever is greater) to positive dm and 0 to
            # negative dm if positive is greater than negative, else the reverse
            if pos_movement > neg_movement:
                positive_dm.append(max(pos_movement, 0))
                negative_dm.append(0)
            else:
                positive_dm.append(0)
                negative_dm.append(max(neg_movement, 0))

            # Appends to true range the max value between current high - current low,
            # current high - previous close, and current low - previous close
            true_range.append(max(abs(curr_high - curr_low), abs(curr_high - prev_close),
                                  abs(curr_low - prev_close)))

        return true_range, positive_dm, negative_dm

    def _smooth_calc(self, tr_data, pos_mov, neg_mov, period):
        """Smooths the true range, positive and negative directiona movement (dm) by period

        param: tr_data: true range data for each day between the range
        param: pos_mov: positive dm for each day between rhe range
        param: neg_mov: negative dm for each day between rhe range
        param: period: period range that's used to average the values
        returns: smooth true range, smooth positive dm, and smooth negative dm
        """
        smooth_true_range = []
        smooth_positive = []
        smooth_negative = []

        # Uses the period to calculate the average true range, positive dm, and negative dm, and
        # then appends each value to their respective list
        for i in range(len(tr_data) - period + 1):
            # Calculates the sum of the data in the period range
            sum_tr = sum(tr_data[i: i + period])
            sum_pos = sum(pos_mov[i: i + period])
            sum_neg = sum(neg_mov[i: i + period])
            # Divides the sum by the period and appends to the respective "smooth" list
            smooth_true_range.append(sum_tr / period)
            smooth_positive.append(sum_pos / period)
            smooth_negative.append(sum_neg / period)

        return smooth_true_range, smooth_positive, smooth_negative

    def _directional_index(self, s_pos_dm, s_neg_dm, avg_tr):
        """Calculates the negative and positive directional index
        param: s_pos_dm: smooth positive directional movement based on the stock
        param: s_neg_dm: smooth negative directional movement based on the stock
        param: avg_tr: average true range based on the stock
        returns: positive and negative directional index
        """
        positive_di = []
        negative_di = []

        # Calculates the negative and positive directional index and append it
        for i in range(len(s_pos_dm)):
            # Divides each smooth value by the respective avg true range and multiply it by 100
            positive_di.append((s_pos_dm[i] / avg_tr[i]) * 100)
            negative_di.append((s_neg_dm[i] / avg_tr[i]) * 100)

        return positive_di, negative_di

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

        return rsi_values[-1] < 30, rsi_values

    def buy_or_not(self, clientData):
        """
        :param: rsi function value, ADX function value, moving average value(Calculation TBD)
        :return: statement that will tell user whether to buy stock or not based on
                 the three indicating factors
        """
        rsi_decision, rsi_value = self.rsi_function(clientData, 14)
        adx_decision, adx_value, pos_dir, neg_dir = self.average_dir_index(clientData, 14)
        ma_decision, long_ma, short_ma = self.moving_avg_crossover(clientData)

        print("Moving Average Results: Short term - " + str(round(short_ma[-1], 2)) +
              " ||| Long term - " + str(round(long_ma[-1], 2)))
        print("Average Dir Index Results: ADX value - " + str(round(adx_value[-1], 2)) +
              "||| Positive movement - " + str(round(pos_dir[-1], 2)) +
              "||| Negative movement - " + str(round(neg_dir[-1], 2)))
        print("RSI Results: " + str(round(rsi_value[-1], 2)))

        if (ma_decision + adx_decision + rsi_decision >= 2):
            print("Prediction: BUY " + clientData.tick_name)
        else:
            print("Prediction: DO NOT BUY " + clientData.tick_name)

        return


if __name__ == '__main__':
    main_instance = Main()

