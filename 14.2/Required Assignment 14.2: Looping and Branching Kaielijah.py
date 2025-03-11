import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import sys
from datetime import datetime
import matplotlib
import re

# Ensure GUI compatibility for Matplotlib
matplotlib.use("TkAgg")

def user_input():
    #welcome user and select a function
    word = '''

Welcome to Stock Master!
Please select a function to continue:

(1) Search for a stock code by keyword
(2) View stock trend by code

(sample input 1 or 2)
'''

    #TODO: 1. ask for user input using 'word' and save response in a str variable 'function'
    while True:
        function = input(
            "Please select a function to continue: \n\n(1) Search for a stock code by ticker\n(2) View stock trend by code\n\nSample input 1 or 2: ")
        try:
            function = int(function)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if function == 1:
            print(f"Selected: {function}")
            result = check_code()

            if result:
                input_keyword, ticker, check_code_next = result
                return word, function, input_keyword, check_code_next
            else:
                print("Invalid ticker. Returning to menu.")
                return user_input() # Restart menu
        elif function == 2:
            print(f"Selected: {function}")
            while True:
                input_keyword = input("Enter stock code: ").strip().upper()
                if not input_keyword:
                    print("No stock code entered. Returning to menu.")
                    return user_input()
                if re.match(r"^\d{2}-\d{2}-\d{4}$", input_keyword):  # Regex to detect date format
                    print(
                        "Error: The entered stock code looks like a date. Please enter a valid ticker symbol (e.g., AAPL, TSLA).")
                    continue  # Ask again

                if not input_keyword.isalnum() and "." not in input_keyword:
                    print("Invalid stock code format. Please enter a valid ticker (e.g., AAPL, TSLA, 600519.SS).")
                    continue  # Ask again

                break  # Valid input, exit loop
            # Proceed directly to view_trend() function
            return view_trend(input_keyword, word, function, None)
        else:
            print("Invalid input. Please enter either 1 or 2.")

def check_code():
    while True:
        input_keyword = input("Enter a keyword to search: ").strip()
        if input_keyword.lower() == 'exit':
            print("Exiting...")
            return None, None, None

        if not input_keyword.isalnum():
            print("Invalid input. Please enter a valid stock ticker keyword:")
            continue

        try:
            ticker = yf.Ticker(input_keyword)
            info = ticker.info

            if not info or 'symbol' not in info:
                print(f"No information found for ticker: {input_keyword}. Please try a different keyword.")
                return None, None, None

            print(f"Stock code for {input_keyword} is {info.get('symbol')}")
            print(f"Price (USD): {info.get('regularMarketPrice', 'N/A')}")

            return input_keyword, ticker, info

        except Exception as e:
            print(f"Error fetching data for {input_keyword}: {e}")
            return None, None, None


def view_trend(input_keyword, word, function, check_code_next):
    if not input_keyword:
        print("Invalid ticker. Returning to menu.")
        return user_input, None, None, None, None  # Ensure return to menu on failure

    print(f"Fetching trend data for ticker: {input_keyword}")

    # Validate Start Date Input
    while True:
        input_start = input("Enter start date (DD-MM-YYYY): ").strip()
        if re.match(r"^\d{2}-\d{2}-\d{4}$", input_start):  # Correct format
            try:
                start_date = datetime.strptime(input_start, "%d-%m-%Y").strftime("%Y-%m-%d")
                break  # Valid date, exit loop
            except ValueError:
                print("Invalid date. Please enter a valid date in DD-MM-YYYY format.")
        else:
            print("Invalid format. Please enter date in DD-MM-YYYY format.")

    # Validate End Date Input
    while True:
        input_end = input("Enter end date (DD-MM-YYYY): ").strip()
        if re.match(r"^\d{2}-\d{2}-\d{4}$", input_end):  # Correct format
            try:
                end_date = datetime.strptime(input_end, "%d-%m-%Y").strftime("%Y-%m-%d")
                break  # Valid date, exit loop
            except ValueError:
                print("Invalid date. Please enter a valid date in DD-MM-YYYY format.")
        else:
            print("Invalid format. Please enter date in DD-MM-YYYY format.")

    try:
        df = yf.download(input_keyword, start=start_date, end=end_date, auto_adjust=False)

        if df.empty:
            print("No data found for the given {input_keyword}. Returning to menu.")
            return user_input()
    except ValueError:
        print("Invalid date format. Please enter dates in DD-MM-YYYY format.")
        return user_input()

    # Flatten MultiIndex Columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    print(f"Flattened columns: {df.columns.tolist()}")

    required_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"Error: Missing required columns: {missing_cols}. Data may be unavailable for this stock.")
        return user_input()

    df[required_cols] = df[required_cols].apply(pd.to_numeric, errors='coerce')
    df.dropna(subset=required_cols, inplace=True)

    if df.empty:
        print("Error: No valid numerical data available after cleaning. Try another stock.")
        return user_input()

    # User Graph Selection
    print("""
    Please select type of graph.
    (1) Candle Stick
    (2) High
    (3) Low
    (4) Open
    (5) Close
    (6) Adj Close
    (7) Moving Average
    (8) Volume
    You may select multiple choices, separate each choice by a comma.
    """)

    graph_choices = input("Sample input for candlestick + High + Volume (e.g., 1,2,8): ").strip().split(",")

    if not graph_choices:
        print("No input received. Returning to menu.")
        return user_input()

    try:
        graph_choices = [int(choice) for choice in graph_choices if choice.isdigit()]
    except ValueError:
        print("Invalid graph choices. Please enter numbers between 1-8.")
        return user_input()

    valid_choices = {1, 2, 3, 4, 5, 6, 7, 8}
    invalid_inputs = [choice for choice in graph_choices if choice not in valid_choices]

    if invalid_inputs:
        print(f"Invalid selections detected: {invalid_inputs}. Please enter numbers between 1-8.")
        return user_input()

    print(f"Selected graphs before processing: {graph_choices}")



    # **Step 1: Handle Volume Graph (8) First**
    if 8 in graph_choices:
        graph_choices.remove(8)  # Remove volume graph to process separately
        print("Volume graph required. Remove volume graph from graph_choices")

        if graph_choices:
            print("Allocating space for volume graph and other graphs, then plotting volume graph.")
        else:
            print("Allocating space for volume graph only and plotting volume graph.")

        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df['Volume'], label='Volume', linestyle='dotted')
        plt.xlabel("Date")
        plt.ylabel("Volume")
        plt.legend()
        plt.grid()
        plt.show(block=False)
        plt.pause(0.1)

    # **Step 2: Check if Candlestick Graph (1) is Required**
    if 1 in graph_choices:
        graph_choices.remove(1)
        print("graph_choice contains 1 w/o 8")
        print("Candlestick chart required. Plotting candlestick chart.")

        df.index = pd.to_datetime(df.index)
        fig, ax = mpf.plot(df, type='candle', volume=True, title=f"Candlestick Chart for {input_keyword}",
                           style='charles', returnfig=True)
        plt.show(block=True)
        plt.pause(0.2)

    # **Step 3: Check if Moving Average Graph (7) is Required**
    ma_list = []
    if 7 in graph_choices:
        graph_choices.remove(7)
        print("graph_choice contains 7 w/o 8")
        print("Moving average graph required. Asking user for frequency.")

        ma_list = input("Please input the frequency for the moving average (e.g., 50,100): ").strip().split(",")
        try:
            ma_list = [int(ma) for ma in ma_list if ma.isdigit()]
        except ValueError:
            print("Invalid moving average input. Skipping.")
            ma_list = []

    # **Step 4: Plot Other Selected Graphs**
    if graph_choices:
        print(f"Plotting other selected graphs: {graph_choices}")

        plt.figure(figsize=(10, 6))

        if 2 in graph_choices:
            plt.plot(df.index, df['High'], label='High', linestyle='dashed')

        if 3 in graph_choices:
            plt.plot(df.index, df['Low'], label='Low', linestyle='dashed')

        if 4 in graph_choices:
            plt.plot(df.index, df['Open'], label='Open')

        if 5 in graph_choices:
            plt.plot(df.index, df['Close'], label='Close')

        if 6 in graph_choices:
            plt.plot(df.index, df['Adj Close'], label='Adj Close')

        plt.xlabel("Date")
        plt.ylabel("Stock Price")
        plt.title(f"Stock Trend for {input_keyword}")
        plt.legend()
        plt.grid()
        plt.show(block=False)
        plt.pause(0.1)

    # **Step 5: Generate Moving Average Graphs**
    for ma in ma_list:
        df[f"MA{ma}"] = df['Adj Close'].rolling(window=ma).mean()
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df['Adj Close'], label="Adj Close")
        plt.plot(df.index, df[f"MA{ma}"], label=f"{ma}-Day MA")
        plt.xlabel("Date")
        plt.ylabel("Stock Price")
        plt.legend()
        plt.grid()
        plt.show(block=False)
        plt.pause(0.1)

    # **Step 6: Ask User for Next Step**
    print("\nWould you like to:")
    print("1. Return to menu")
    print("2. Exit program")
    next_step = input("(Sample input: 1 or 2): ").strip()

    if next_step == "1":
        return user_input()  # Restart menu properly

    elif next_step == "2":
        print("Exiting program...")
        sys.exit()

    return user_input()


def input_to_date(input_start):
    try:
        date_obj = datetime.strptime(input_start, "%d-%m-%Y")
        return date_obj.year, date_obj.month, date_obj.day
    except ValueError:
        return None, None, None

def main():
    while True:
        word, function, input_keyword, check_code_next = user_input()

        if function == 1 and input_keyword:
            ticker, input_start, input_end, df, check_code_next = view_trend(input_keyword, word, function, check_code_next)

            if df is not None:
                print("Exiting program...")
                sys.exit()
                # print_end(word, function, input_keyword, check_code_next, code, input_start, input_end)

        # Ask the user if they want to return to the menu or exit
        while True:
            next_action = input("\nWould you like to:\n1. Return to menu\n2. Exit program\n(Sample input: 1 or 2): ").strip()
            if next_action == "1":
                user_input()
                break  # Restart the menu loop
            elif next_action == "2":
                print("Exiting program...")
                sys.exit()
            else:
                print("Invalid input. Please enter 1 or 2.")

# def print_end(word, function, input_keyword, check_code_next, code, input_start, input_end):
#     code, input_start, input_end, graph_choice, ma,
#     next_word, year, month, day, user_input_next,
#     view_trend_next, next_request_next):
#     print('---------------------------------------------------')
#     print('Below are the variables defined and their contents:')
#     print('---------------------------------------------------\n')
#     print(str(type(word))+ ' word : '+ word)
#     print(str(type(function))+ ' function : '+ function)
#     print(str(type(input_keyword))+ ' input_keyword : '+ input_keyword)
#     print(str(type(code))+ ' code : '+ code)
#     print(str(type(input_start))+ ' input_start : '+ input_start)
#     print(str(type(input_end))+ ' input_end : '+ input_end)
#     print(str(type(graph_choice)) + ' graph_choice : ' + str(graph_choice))
#     print(str(type(ma)) + ' ma : ' + str(ma))
#     print(str(type(next_word)) + ' next_word : ' + str(next_word))
#     print(str(type(year)) + ' year : ' + str(year))
#     print(str(type(month)) + ' month : ' + str(month))
#     print(str(type(day)) + ' day : ' + str(day))
#     print(str(type(user_input_next)) + ' user_input_next : ' + str(user_input_next))
#     print(str(type(check_code_next)) + ' check_code_next : ' + str(check_code_next))
#     print(str(type(view_trend_next)) + ' view_trend_next : ' + str(view_trend_next))
#     print(str(type(next_request_next)) + ' next_request_next : ' + str(next_request_next))
#   #function call

if __name__== "__main__":
  main()
