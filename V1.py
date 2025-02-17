import os
import requests
import matplotlib.pyplot as plt
import pandas as pd
import sys
from alpha_vantage.timeseries import TimeSeries
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")  # Fetch API Key from environment
API_KEY_BACKUP = os.getenv("ALPHA_VANTAGE_API_KEY_BACKUP")
def test_api_key(api_key):
    """Function to test if an API key is working"""
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=apple&apikey={api_key}"
    response = requests.get(url)
    
    # If API response contains an error or rate limit message, return False
    if response.status_code != 200 or "Error Message" in response.text or "Thank you for using Alpha Vantage" in response.text:
        print(f"DEBUG: API Key {api_key} failed. Trying another key...")
        return False
    return True

# Try primary API key, fallback to backup
if test_api_key(API_KEY):
    ACTIVE_API_KEY = API_KEY
else:
    print("DEBUG: Switching to backup API key.")
    if test_api_key(API_KEY_BACKUP):
        ACTIVE_API_KEY = API_KEY_BACKUP
    else:
        print("ERROR: Both API keys failed. Please check your keys or API limits.")
        exit(1)

# Now, use `ACTIVE_API_KEY` in your API requests
print("DEBUG: Using API Key ->", ACTIVE_API_KEY)
# print(data)  # Print stock details
def user_input():
    global ticker
    #welcome user and select a function
    #TODO : 1. Design a welcome message that ask user to select a function, assign this message to a string variable 'word'
    word = "Welcome to Stock Master!\n"
    print(f"{type(word)}" + " word :\n" + word)

    #TODO : 2. Define a string variable 'function' . (This variable will be used to hold user's choice of function.)
    while True:
        function = input("Please select a function to continue: \n\n(1) Search for a stock code by ticker\n(2) View stock trend by code\n\nSample input 1 or 2: ")
        try:
            function = int(function)  # Convert to integer
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if function == 1:
            next_step = 1
            print(f"Selected: {function}")
            
            input_keyword, ticker, check_code_next = check_code()
            view_trend(ticker)
            break
        elif function == 2:
            next_step = 2 
            print(f"Selected: {function}")
            break
        else :
            print("Invalid input. Please enter either 1 or 2.")
        
    return word,function,next_step

def check_code():

# ask user to input keyword
    global ticker
# TODO : 4. Define a string variable 'input_keyword' . (This variable will be used to hold user's input of keyword to search.)
    input_keyword = input("Enter a stock keyword to search: ")
    # print(f"Keyword entered: {input_keyword}")

    # Call search_ticker() to get the stock ticker
    ticker = search_ticker(input_keyword)

    if ticker:
        print(f"\nThe selected ticker symbol is: {ticker}")
    else:
        print("\nNo valid ticker found. Please try again.")
        return check_code()
    # print(f"Keyword entered: {input_keyword}"
    check_code_next = 1
    return input_keyword, ticker, check_code_next
    
# get source data (code provided), the source data is stored in code_dic, a dictionary with all tickers' company name as key and stock code as value
## using alpha advantage to fetch ticker and return results. Not sure where the source data is downloaded for us to use in this case, is code_dic hypothetical or is there an actual file? 
# Function to search for stock ticker based on a keyword
def search_ticker(keyword):
    url = f"https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords={keyword}&apikey={API_KEY}"
    
    response = requests.get(url)
    data = response.json()
# Get user input for company search
    if "bestMatches" in data:
        results = data["bestMatches"]
        if len(results) > 0:
            print("\nSearch Results:")
            for idx, match in enumerate(results[:5], start=1):  # Show top 5 results
                print(f"{idx}. {match['2. name']} ({match['1. symbol']})")
            
            # Ask user to choose from the results
            choice = input("\nEnter the number of the stock you want: ")
            try:
                choice = int(choice)
                if 1 <= choice <= len(results):
                    return results[choice - 1]["1. symbol"]
                else:
                    print("Invalid choice. Returning the first result.")
                    return results[0]["1. symbol"]
            except ValueError:
                print("Invalid input. Returning the first result.")
                return results[0]["1. symbol"]
        else:
            print("No matches found.")
            return None
    else:
        print("Error fetching data from code_dic. API rate limit is 25 requests per day")
        print(f"DEBUG: Loaded API Key: {API_KEY}")  # Add this before making API calls

        return None

    #ask for next step
    #TODO : 5. Define a string variable 'next_step' . (This variable will be used to hold user's choice of next step to take.)
    next_step = "2"
    return
    return input_keyword,next_step

def view_trend(ticker):
    print(f"\nGenerating trend graph for: {ticker}")

    #ask user to input stock code, start date and end date
    #TODO : 6. Define 3 string variables 'code','input_start','input_end' . (These variable will be used to hold user's choice of stock code,start date and end date)
    input_start = input("Enter start date (DD-MM-YYYY):")
    input_end = input("Enter end date (DD-MM-YYYY):")

    #convert string to datetime
    try:  
        input_start = datetime.strptime(input_start, "%d-%m-%Y")
        input_end = datetime.strptime(input_end, "%d-%m-%Y")
    except ValueError:
        print("Invalid date format. Please enter dates in DD-MM-YYYY format.")
        return view_trend(ticker)  # Retry input if incorrect
    
    #get source data (code provided), the source data is stored in df, a pandas dataframe
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY}&outputsize=compact"
    response = requests.get(url)
    data = response.json()
    if "Time Series (Daily)" not in data:
        print("Error fetching stock data. Check ticker symbol and API key.")
        return ticker, input_start, input_end, None, None, "view_trend_next"
    
    # Convert JSON to DataFrame
    df = pd.DataFrame.from_dict(data["Time Series (Daily)"], orient="index")
    df = df.astype(float)  # Convert all columns to float
    df.index = pd.to_datetime(df.index)  # Convert DataFrame index to datetime
    df = df[(df.index >= input_start) & (df.index <= input_end)]  # Correct filtering

    #ask for graph choice
    #TODO : 7. Define a string variable 'graph_choice' . (This variable will be used to hold user's choice of types of graphs to plot.)
    graph_choice = input("Choose the graph you wish to plot (line, bar, candlestick): \n")
    #manipulate choice input

    #draw graph based on input
    # Plot the data
    plt.figure(figsize=(10,5))
    
    if graph_choice.lower() == "line":
        plt.plot(df.index, df["4. close"], label="Closing Price", color='b')
    elif graph_choice.lower() == "bar":
        plt.bar(df.index, df["4. close"], color='g', label="Closing Price")
    else:
        print("Invalid choice. Defaulting to line chart.")
        plt.plot(df.index, df["4. close"], label="Closing Price", color='b')

    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.title(f"Stock Trend for {ticker}")
    plt.legend()
    plt.grid()
    plt.show()
    next_request()
    #TODO : 8. Define a int variable 'ma' with value 10 . (This variable will be used to hold user's choice of moving average graph frequency.)
    ma = 10
    #ask for next step
    #TODO : 9. Define a string variable 'next_step' . (This variable will be used to hold user's choice of next step to take.)
     
    while True:
        next_step = input("Would you like to \n1. Return to menu?\n 2. Exit program\n(sample input: 1 or 2)")
        try:
            next_step = int(next_step)  # Convert to integer
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if next_step == 1:
            print("Returning to main menu...")
            main()
            break
        elif next_step == 2:
            print("\nExiting program.")
            sys.exit()
            break
        else :
            print("Invalid input. Please enter either 1 or 2.") 

        return input_start,input_end,graph_choice,ma,next_step

def next_request():

    #ask user to select next step to proceed with
    #TODO : 10. Design a message that ask user to select next step to take, assign this message to a string variable 'next_word'
    # next_word = input("Would you like to continue or exit?")
    #TODO : 11. Define a string variable 'next_step' . (This variable will be used to hold user's choice of next step to take.)
    # next_step = input("Enter next step.")
    while True:
        next_step = input("Would you like to \n1. Return to menu?\n 2. Exit program\n(sample input: 1 or 2)")
        try:
            next_step = int(next_step)  # Convert to integer
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if next_step == 1:
            print("Returning to main menu...")
            main()
            break
        elif next_step == 2:
            print("\nExiting program.")
            sys.exit()
            break
        else :
            print("Invalid input. Please enter either 1 or 2.") 
    return next_word,next_step


def input_to_date(input_date):

    #string to integer
    #TODO: 12. Define 3 int variables 'year','month','day', initialise their values randomly
    year = str(input("Enter year"))
    month = str(input("Enter month"))
    day = str(input("Enter day"))
    #integer to datetime
    input_date = f"{int(day):02d}-{int(month):02d}-{int(year)}" #this updates to integer
    # print(type(input_date), input_date) # for checking output
    return year,month,day

def main():
    word,function,user_input_next = user_input()
    input_keyword, ticker, check_code_next = check_code()
    code,input_start,input_end,graph_choice,ma,view_trend_next = view_trend()
    next_word,next_request_next= next_request()
    year,month,day = input_to_date()

    print('---------------------------------------------------')
    print('Below are the variables defined and their contents:')
    print('---------------------------------------------------\n')
    print(str(type(word))+ ' word : '+ word)
    print(str(type(function))+ ' function : '+ function)
    print(str(type(input_keyword))+ ' input_keyword : '+ input_keyword)
    print(str(type(ticker)) + 'ticker : '+ ticker)
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
#   function call

if __name__== "__main__":
    main()