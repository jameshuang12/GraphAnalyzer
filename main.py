from datetime import datetime
import stock_class
import confirm_input
import numpy as np

def main():
    user_data = confirm_input.userInput()

    clientData = stock_class.Stock(user_data[0], user_data[1], user_data[2])
    per_change = percentageChange(clientData)

    while True:
        rsi_function(clientData) #write in conditions for 50 days, reorder
        moving_avg_crossover(clientData)
        investment(clientData, per_change)
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


def percentageChange(clientData):
    """ Get the percentage change of the two dates given by the user.

    :param clientData: All the data needed from the given dates
    :return: the percent change between the first to the second
    """
    print('For the first date')
    data1 = _ask_user_for_data()
    print('For the second date')
    data2 = _ask_user_for_data()

    first_call = getattr(clientData, str(data1))
    sec_call = getattr(clientData, str(data2))

    change = int((sec_call[-1] / first_call[0]) * 100)

    if change < 100:
        print('The percentage change had a decline of ' + str(change) + '%')
    else:
        print('The percentage change had a growth of ' + str(change) + '%')

    return change


def _ask_user_for_data():
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


def rsi_function(clientData):
    gaincounter = 0
    losscounter = 0
    gain = 0
    loss = 0

    for i in range(9, 0, -1):
        if clientData.close[-i] < clientData.close[-i - 1]:
            gaincounter += 1
            gain += clientData.close[-i - 1] - clientData.close[-i]
        else:
            losscounter += 1
            loss += abs(clientData.close[-i] - clientData.close[-i - 1])

    avg_gain = gain / gaincounter

    avg_loss = loss / losscounter

    rsi = 100 - 100 / (1 + (avg_gain / avg_loss))

    if rsi > 70.000:
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

def should_i_buy():
    """
    :param: rsi function value, ADX function value, moving average value(Calculation TBD)
    :return: statement that will tell user whether to buy stock or not based on the three indicating factors
    """
    return 1


def investment(clientData, percent_change):
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

    investmentAmount = int(amount * (percentageChange(clientData) / 100))

    if investmentAmount < amount:
        total = int(amount - investmentAmount)
        print('If you invested on ' + str(clientData.day1) + ' with the amount of $' + str(amount) + ' ,then you'
                                                                                                     " would've lost $" + str(
            total) + " if you withdraw on " + str(clientData.day2) + ".")
    else:
        total = investmentAmount - amount
        print('If you invested on ' + str(clientData.day1) + ' with the amount of $' + str(amount) + ' ,then you'
                                                                                                     " would've gained $" + str(
            total) + " if you withdraw on " + str(clientData.day2) + ".")


def moving_avg_crossover(clientData):
    """
    WHAT IT DOES


    """
    price_data = getattr(clientData, str(_ask_user_for_data()))
    moving_avg_range = _ask_user_for_range(price_data)

    long_subset = price_data[-(moving_avg_range[0]):]
    short_subset = price_data[-(moving_avg_range[1]):]

    compare = 'greater'
    decision = 'should'

    if (sum(short_subset) / len(short_subset)) <= (sum(long_subset) / len(long_subset)):
        compare = 'less'
        decision = 'should not'

    print(f"Because short-term moving average (${int(sum(short_subset) / len(short_subset))}) is "
          f"{compare} than long-term moving average (${int(sum(long_subset) / len(long_subset))}"
          f"), you {decision} invest in {clientData.tick_name} on {clientData.day2}.")


def _ask_user_for_range(data_range):
    """
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

if __name__ == '__main__':
    main()
