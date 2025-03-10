import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import sys
from datetime import datetime
import matplotlib

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
            function = int(function)  # Convert to integer
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if function == 1:
            next_step = 1
            print(f"Selected: {function}")
            result = check_code()

            if result:
                input_keyword, ticker, check_code_next = result
            else:
                input_keyword, ticker, check_code_next = None, None, None  # Handle case where function returns None

            if ticker:
                view_trend(input_keyword, word, function, check_code_next)
            else:
                print("Invalid ticker. Returning to menu.")
            return word,function,ticker
        elif function == 2:
            next_step = 2
            print(f"Selected: {function}")
            break
        else:
            print("Invalid input. Please enter either 1 or 2.")

    return word,function,next_step


def check_code():

    #ask user to input keyword
    #TODO: 2. ask for user to input keyword and save response into a string variable 'input_keyword'
    while True:
        input_keyword = input("Enter a keyword to search: ").strip()
        if input_keyword.lower() == 'exit':
            print("Exiting...")
            return None, None, None

        if not input_keyword.isalnum(): # execute this is invalid
            print("Invalid input. Please enter a valid stock ticker keyword:")
            continue # prompt again
        try:
            ticker = yf.Ticker(input_keyword)
            info = ticker.info #get ticker info
            if not info:
                print(f"No information found for ticker: {input_keyword}. Please try a different keyword.")
                return None, None, None

            if 'symbol' in info: # If valid info is found, print and return
                print(f"Stock code for {input_keyword} is {info.get('symbol')}")
                # print(f"Name: {info.get('longName', 'N/A')}")
                # print(f"Sector: {info.get('sector', 'N/A')}")
                # print(f"Industry: {info.get('industry', 'N/A')}")
                print(f"Price (USD): {info.get('regularMarketPrice', 'N/A')}")

                return input_keyword, ticker, info

        except Exception as e:
                print(f"Error fetching data for {input_keyword}: {e}")
                print("Please try a different keyword or check your connection.")
                return None, None, None
    #get source data (code provided), the source data is stored in code_dic, a dictionary with all tickers' company name as key and stock code as value
    #filter out tickers containing user's keyword
    #ask for next step


def view_trend(input_keyword, word, function, check_code_next):
    if not input_keyword:
        print("Invalid ticker. Returning to menu.")
        return None, None, None, None, None, None  # Ensure all variables are returned

    print(f"Fetching trend data for ticker: {input_keyword}")

    try:
        input_start = input("Enter start date (DD-MM-YYYY): ").strip()
        input_end = input("Enter end date (DD-MM-YYYY): ").strip()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user. Returning to menu...")
        return None, None, None, None, None, None

    try:
        start_date = datetime.strptime(input_start, "%d-%m-%Y").strftime("%Y-%m-%d")
        end_date = datetime.strptime(input_end, "%d-%m-%Y").strftime("%Y-%m-%d")
        df = yf.download(input_keyword, start=start_date, end=end_date, auto_adjust=False)

        if df.empty:
            print("No data found for the given ticker and date range. Returning to menu.")
            return None, None, None, None, None, None

    except ValueError:
        print("Invalid date format. Please enter dates in DD-MM-YYYY format.")
        return None, None, None, None, None, None

    # Flatten MultiIndex Columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = [col[0] for col in df.columns]

    print(f"Flattened columns: {df.columns.tolist()}")

    required_cols = ['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        print(f"Error: Missing required columns: {missing_cols}. Data may be unavailable for this stock.")
        return None, None, None, None, None, None

    df[required_cols] = df[required_cols].apply(pd.to_numeric, errors='coerce')
    df.dropna(subset=required_cols, inplace=True)

    if df.empty:
        print("Error: No valid numerical data available after cleaning. Try another stock.")
        return None, None, None, None, None, None

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
        return None, None, None, None, None, None

    try:
        graph_choices = [int(choice) for choice in graph_choices if choice.isdigit()]
    except ValueError:
        print("Invalid graph choices. Please enter numbers between 1-8.")
        return None, None, None, None, None, None

    valid_choices = {1, 2, 3, 4, 5, 6, 7, 8}
    invalid_inputs = [choice for choice in graph_choices if choice not in valid_choices]

    if invalid_inputs:
        print(f"Invalid selections detected: {invalid_inputs}. Please enter numbers between 1-8.")
        return None, None, None, None, None, None

    print(f"Selected graphs: {graph_choices}")

    #  **Move Moving Average Input BEFORE Graph Generation**
    # TODO: 5. ask user to input moving average frequency and save response into a int variable 'ma'
    ma_list = []
    if 7 in graph_choices:
        ma_list = input("Please input the frequency for the moving average (e.g., 100, 20): ").strip().split(",")
        try:
            ma_list = [int(ma) for ma in ma_list if ma.isdigit()]
        except ValueError:
            print("Invalid moving average input. Skipping.")
            ma_list = []

    # Close previous figures before opening new ones
    plt.close('all')

    #  **Fix Candlestick Chart Display Order**
    if 1 in graph_choices:
        print(f"Generating candlestick chart for {input_keyword}...")
        df.index = pd.to_datetime(df.index)
        fig, ax = mpf.plot(df, type='candle', volume=True, title=f"Candlestick Chart for {input_keyword}", style='charles', returnfig=True)
        fig.show()

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

    if 8 in graph_choices:
        plt.plot(df.index, df['Volume'], label='Volume', linestyle='dotted')

    if any(choice in graph_choices for choice in [2, 3, 4, 5, 6, 8]):
        plt.xlabel("Date")
        plt.ylabel("Stock Price / Volume")
        plt.title(f"Stock Trend for {input_keyword}")
        plt.legend()
        plt.grid()
        plt.show(block=True)

    #  **Generate Moving Average Graphs**
    for ma in ma_list:
        df[f"MA{ma}"] = df['Adj Close'].rolling(window=ma).mean()
        plt.figure(figsize=(10, 6))
        plt.plot(df.index, df['Adj Close'], label="Adj Close")
        plt.plot(df.index, df[f"MA{ma}"], label=f"{ma}-Day MA")
        plt.xlabel("Date")
        plt.ylabel("Stock Price")
        plt.legend()
        plt.grid()
        plt.show(block=True)

    #  **Ask User for Next Step**
    print("""
    Would you like to:
    1. Return to menu
    2. Exit program
    (Sample input: 1 or 2)
    """)
    # ask for next step
    next_step = input().strip()
    if next_step == "1":
        next_word, next_request_next = next_request()
        return input_keyword, input_start, input_end, graph_choices, ma_list, "Completed", next_word


    elif next_step == "2":

        print("Exiting program...")

        year, month, day = input_to_date()

        print_end(str(word), str(function), input_keyword, check_code_next,
                  input_keyword, input_start, input_end, graph_choices, ma_list,
                  "Exited", year, month, day, None,
                  "Completed", None)

        sys.exit(0)

    return ticker, input_start, input_end, graph_choices, ma_list, "Completed"


def next_request():

    #ask user to select next step to proceed with
    next_word = '''
Would you like to
1. return to menu
2. exit program
(sample input : 1 or 2)
'''

    #TODO: 6. ask for user input using 'next_word' and save response in a str variable 'next_step'
    next_step = input("Would you like to return to menu or exit program? (1 or 2) ")
    #return
    return next_word,next_step


def input_to_date():

    #string to integer

    year = 2020
    month = 2
    day = 2

    #integer to datetime

    #return
    return year,month,day

def main():
    word, function, input_keyword, check_code_next = user_input()
    code, input_start, input_end, graph_choice, ma, view_trend_next = view_trend(input_keyword, word, function, check_code_next)

    next_word, next_request_next = next_request()
    year, month, day = input_to_date()

    print_end(word, function, input_keyword, check_code_next,
              code, input_start, input_end, graph_choices, ma,
              next_word, year, month, day, None,
              view_trend_next, next_request_next)

    # input_keyword, check_code_next = check_code()
    # Ensure view_trend() runs and captures variables correctly
    try:
        code, input_start, input_end, graph_choice, ma, view_trend_next = view_trend(word, function, input_keyword, check_code_next)
    except TypeError:
        print("Error occurred in view_trend() function. Skipping variable capture.")

    # Get next step request
    next_word, next_request_next = next_request()

    # Ensure all date-related variables are captured
    year, month, day = input_to_date()

def print_end(word, function, input_keyword, check_code_next,
    code, input_start, input_end, graph_choice, ma,
    next_word, year, month, day, user_input_next,
    view_trend_next, next_request_next):
    print('---------------------------------------------------')
    print('Below are the variables defined and their contents:')
    print('---------------------------------------------------\n')
    print(str(type(word))+ ' word : '+ word)
    print(str(type(function))+ ' function : '+ function)
    print(str(type(input_keyword))+ ' input_keyword : '+ input_keyword)
    print(str(type(code))+ ' code : '+ code)
    print(str(type(input_start))+ ' input_start : '+ input_start)
    print(str(type(input_end))+ ' input_end : '+ input_end)
    print(str(type(graph_choice)) + ' graph_choice : ' + str(graph_choice))
    print(str(type(ma)) + ' ma : ' + str(ma))
    print(str(type(next_word)) + ' next_word : ' + str(next_word))
    print(str(type(year)) + ' year : ' + str(year))
    print(str(type(month)) + ' month : ' + str(month))
    print(str(type(day)) + ' day : ' + str(day))
    print(str(type(user_input_next)) + ' user_input_next : ' + str(user_input_next))
    print(str(type(check_code_next)) + ' check_code_next : ' + str(check_code_next))
    print(str(type(view_trend_next)) + ' view_trend_next : ' + str(view_trend_next))
    print(str(type(next_request_next)) + ' next_request_next : ' + str(next_request_next))
  #function call

if __name__== "__main__":
  main()
