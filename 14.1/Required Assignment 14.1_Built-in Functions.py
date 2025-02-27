import requests
import pandas as pd
import matplotlib.pyplot as plt
import sys
from datetime import datetime

# 🎯 MarketStack API Key
API_KEY = "d04a9fcb4a835aba213c807a2bc6a0b7"

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

#welcome user and select a function
#TODO : 1. Design a welcome message that ask user to select a function, assign this message to a string variable 'word'

def user_input():
    global function, ticker, input_keyword
    word = "Welcome to Stock Master!"
    print(f"{type(word)} word :\n" + word)
#TODO : 2. Define a string variable 'function' . (This variable will be used to hold user's choice of function.)
    while True:
        function_input = input("Please select a function to continue: \n\n(1) Search for a stock code by ticker\n(2) View stock trend by code\n\n(sample input 1 or 2): ")
        try:
            function_input = int(function_input) # Convert to integer
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
# ask user to input keyword
    global ticker
# TODO : 4. Define a string variable 'input_keyword' . (This variable will be used to hold user's input of keyword to search.)
    input_keyword = input("Enter a stock keyword to search: ")
    ticker = search_ticker(input_keyword)
    return input_keyword, ticker

# get source data (code provided), the source data is stored in code_dic, a dictionary with all tickers' company name as key and stock code as value
## using alpha advantage to fetch ticker and return results. Not sure where the source data is downloaded for us to use in this case, is code_dic hypothetical or is there an actual file? 
# Function to search for stock ticker based on a keyword

def search_ticker(keyword):
    url = f"http://api.marketstack.com/v1/tickers?access_key={API_KEY}&search={keyword}"
    response = requests.get(url)
    data = response.json()
    # Get user input for company search
    if "data" in data and len(data["data"]) > 0:
        print("\nAvailable tickers:")
        for idx, stock in enumerate(data["data"][:5], start=1):
            print(f"{idx}. {stock['symbol']}")
    # Ask user to choose from the results
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

    if not ticker:
        print("Error: Invalid ticker. Please try again.")
        return user_input()

    print(f"\nValidating ticker: {ticker}...")

    # Validate ticker using MarketStack API before proceeding
    validation_url = f"http://api.marketstack.com/v1/tickers/{ticker}?access_key={API_KEY}"
    validation_response = requests.get(validation_url).json()

    if "error" in validation_response or "data" not in validation_response:
        print(f"Error: '{ticker}' is not a recognized ticker symbol.")
        
        # Suggest valid tickers
        print("\n🔍 Searching for similar tickers...")
        search_url = f"http://api.marketstack.com/v1/tickers?access_key={API_KEY}&search={ticker}"
        search_response = requests.get(search_url).json()
        
        if "data" in search_response and len(search_response["data"]) > 0:
            print("\nAvailable tickers:")
            for idx, stock in enumerate(search_response["data"][:5], start=1):
                print(f"{idx}. {stock['symbol']} - {stock['name']}")
            
            # Ask user to choose from the results
            choice = input("\nEnter the number of the stock you want: ")
            try:
                choice = int(choice)
                if 1 <= choice <= len(search_response["data"]):
                    ticker = search_response["data"][choice - 1]["symbol"]
                    print(f"✅ Selected Ticker: {ticker}")
                else:
                    print("Invalid choice. Returning to main menu.")
                    return user_input()
            except ValueError:
                print("Invalid input. Returning to main menu.")
                return user_input()
        else:
            print("❌ No similar tickers found. Returning to main menu.")
            return user_input()

    # Proceed to fetch stock data
    print(f"\nGenerating trend graph for: {ticker}")
    input_start = input("Enter start date (DD-MM-YYYY): ")
    input_end = input("Enter end date (DD-MM-YYYY): ")

    try:
        input_start = datetime.strptime(input_start, "%d-%m-%Y").date()
        input_end = datetime.strptime(input_end, "%d-%m-%Y").date()
    except ValueError:
        print("Invalid date format. Please enter dates in DD-MM-YYYY format.")
        return view_trend(ticker)

    # Fetch historical stock data
    url = f"http://api.marketstack.com/v1/eod?access_key={API_KEY}&symbols={ticker}&date_from={input_start}&date_to={input_end}"
    response = requests.get(url)
    data = response.json()

    if "data" not in data or len(data["data"]) == 0:
        print("❌ Error fetching stock data. Check ticker symbol and API key.")
        return user_input()

    # Convert JSON to DataFrame
    df = pd.DataFrame(data["data"])
    df["date"] = pd.to_datetime(df["date"])
    df.sort_values("date", inplace=True)

    # Ask for graph choice
    graph_choice = input("Choose the graph you wish to plot (line, bar, candlestick): \n")
    ma = input("Enter Moving Average period (default: 10): ")
    ma = int(ma) if ma.isdigit() else 10

    # Plot the data
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

#TODO : 8. Define a int variable 'ma' with value 10 . (This variable will be used to hold user's choice of moving average graph frequency.)

def next_request():
    #ask user to select next step to proceed with
    #TODO : 10. Design a message that ask user to select next step to take, assign this message to a string variable 'next_word'
    # next_word = input("Would you like to continue or exit?")
    #TODO : 11. Define a string variable 'next_word' . (This variable will be used to hold user's choice of next step to take.)
    # next_word = input("Enter next step.")
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
    print(str(type(word))+ ' word : '+ word)
    print(str(type(function))+ ' function : '+ function)
    print(str(type(input_keyword))+ ' input_keyword : '+ input_keyword)
    print(str(type(code))+ ' code : '+ code)
    print(str(type(input_start))+ ' input_start : '+ input_start)
    print(str(type(input_end))+ ' input_end : '+ input_end)
    print(str(type(graph_choice))+ ' graph_choice : '+ graph_choice)
    print(str(type(ma))+ ' ma : '+ str(ma))
    print(str(type(next_word))+ ' next_word : '+ next_word)
    print(str(type(year))+ ' year : '+ str(year))
    print(str(type(month))+ ' month : '+ str(month))
    print(str(type(day))+ ' day : '+ str(day))
    print(str(type(user_input_next))+ ' user_input_next : '+ user_input_next)
    print(str(type(check_code_next))+ ' check_code_next : '+ check_code_next)
    print(str(type(view_trend_next))+ ' view_trend_next : '+ view_trend_next)
    print(str(type(next_request_next))+ ' next_request_next : '+ next_request_next)
  #function call

def main():
    global word, function, input_keyword, ticker, input_start, input_end
    global graph_choice, ma, next_word
    word, function = user_input()
    variable_print()

if __name__ == "__main__":
    main()