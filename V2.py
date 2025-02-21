import requests
import pandas as pd
import matplotlib.pyplot as plt
import sys
from datetime import datetime

# 🎯 MarketStack API Key
API_KEY = "68b985ad2a427a0049d9808e3373bfed"

# Global variables to retain user input and selections
word = "Welcome to Stock Master!\n"
function = None
input_keyword = None
ticker = None
input_start = None
input_end = None
graph_choice = None
ma = None
next_word = None

def user_input():
    global function, ticker, input_keyword
    word = "Welcome to Stock Master!"
    print(f"{type(word)} word :\n" + word)
    
    while True:
        function_input = input("Please select a function to continue: \n\n(1) Search for a stock code by ticker\n(2) View stock trend by code\n\n(sample input 1 or 2): ")
        try:
            function_input = int(function_input)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if function_input == 1:
            function = "Search for a stock code by ticker"  # Assign descriptive text
            input_keyword, ticker = check_code()
            view_trend(ticker)
            break
        elif function_input == 2:
            function = "View stock trend by code"  # Assign descriptive text
            ticker = input("Enter stock ticker: ")
            view_trend(ticker)
            break
        else:
            print("Invalid input. Please enter either 1 or 2.")
    
    return word, function


def check_code():
    global ticker
    input_keyword = input("Enter a stock keyword to search: ")
    ticker = search_ticker(input_keyword)
    return input_keyword, ticker

def search_ticker(keyword):
    url = f"http://api.marketstack.com/v1/tickers?access_key={API_KEY}&search={keyword}"
    response = requests.get(url)
    data = response.json()
    
    if "data" in data and len(data["data"]) > 0:
        print("\nAvailable tickers:")
        for idx, stock in enumerate(data["data"][:5], start=1):
            print(f"{idx}. {stock['symbol']}")
        
        choice = input("\nEnter the number of the stock you want: ")
        try:
            choice = int(choice)
            if 1 <= choice <= len(data["data"]):
                return data["data"][choice - 1]["symbol"]
            else:
                print("Invalid choice. Returning the first result.")
                return data["data"][0]["symbol"]
        except ValueError:
            print("Invalid input. Returning the first result.")
            return data["data"][0]["symbol"]
    else:
        print("No matches found.")
        return None

def view_trend(ticker):
    global input_start, input_end, graph_choice, ma
    print(f"\nGenerating trend graph for: {ticker}")
    input_start = input("Enter start date (DD-MM-YYYY):")
    input_end = input("Enter end date (DD-MM-YYYY):")
    
    try:  
        input_start = datetime.strptime(input_start, "%d-%m-%Y").date()
        input_end = datetime.strptime(input_end, "%d-%m-%Y").date()
    except ValueError:
        print("Invalid date format. Please enter dates in DD-MM-YYYY format.")
        return view_trend(ticker)
    
    url = f"http://api.marketstack.com/v1/eod?access_key={API_KEY}&symbols={ticker}&date_from={input_start}&date_to={input_end}"
    response = requests.get(url)
    data = response.json()
    
    if "data" not in data or len(data["data"]) == 0:
        print("Error fetching stock data. Check ticker symbol and API key.")
        return
    
    df = pd.DataFrame(data["data"])
    df["date"] = pd.to_datetime(df["date"])
    df.sort_values("date", inplace=True)
    
    graph_choice = input("Choose the graph you wish to plot (line, bar, candlestick): \n")
    ma = input("Enter Moving Average period (default: 10): ")
    ma = int(ma) if ma.isdigit() else 10
    
    plt.figure(figsize=(10, 5))
    
    if graph_choice.lower() == "line":
        plt.plot(df["date"], df["close"], label="Closing Price", color='b')
    elif graph_choice.lower() == "bar":
        plt.bar(df["date"], df["close"], color='g', label="Closing Price")
    else:
        print("Invalid choice. Defaulting to line chart.")
        plt.plot(df["date"], df["close"], label="Closing Price", color='b')
    
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.title(f"Stock Trend for {ticker}")
    plt.legend()
    plt.grid()
    plt.show()
    
    next_request()

def next_request():
    global next_word
    next_word_input = input("Would you like to \n1. Return to menu?\n 2. Exit program\n(sample input: 1 or 2): ")

    if next_word_input == "1":
        next_word = "Return to menu"  # Assign meaningful description
        user_input()
    else:
        next_word = "Exit program"  # Assign meaningful description
        print("\nExiting program.")
        variable_print()
        sys.exit()

def variable_print():
    print('---------------------------------------------------')
    print('Below are the variables defined and their contents:')
    print('---------------------------------------------------\n')
    print(f"<class 'str'> word : {word}")
    print(f"<class 'int'> function : {function}")
    print(f"<class 'str'> input_keyword : {input_keyword}")
    print(f"<class 'str'> ticker : {ticker}")
    print(f"<class 'datetime.date'> input_start : {input_start}")
    print(f"<class 'datetime.date'> input_end : {input_end}")
    print(f"<class 'str'> graph_choice : {graph_choice}")
    print(f"<class 'int'> ma : {ma}")
    print(f"<class 'str'> next_word : {next_word}")
    print(f"<class 'str'> check_code_next : what is the next step?")
    print(f"<class 'str'> view_trend_next : what is the next step?")

def main():
    global word, function, input_keyword, ticker, input_start, input_end
    global graph_choice, ma, next_word
    word, function = user_input()
    variable_print()

if __name__ == "__main__":
    main()
