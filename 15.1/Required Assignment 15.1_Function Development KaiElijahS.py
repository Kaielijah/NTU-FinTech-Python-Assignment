import warnings
import yfinance as yf
import pandas as pd
import pandas_datareader.data as pdr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import sys
from datetime import datetime
import re
import requests
import os

warnings.filterwarnings("ignore")


def user_input():
    word = '''\nWelcome to Stock Master!\n\nPlease select a function to continue:\n\n(1) Search for a stock code by keyword\n(2) View stock trend by code\n\n(sample input 1 or 2)\n'''
    next_step = '1'
    while next_step == '1':
        function = str(input(word))
        if function == '1':
            check_code()
        elif function == '2':
            view_trend()
        next_step = next_request()

# Load Nasdaq-listed stocks from the text file
NASDAQ_FILE_PATH = os.path.join(os.path.dirname(__file__), "nasdaqtraded.txt")


def load_stock_data():
    """Load and clean stock data from the Nasdaq-listed text file."""
    try:
        # Load the file
        df = pd.read_csv(NASDAQ_FILE_PATH, sep="|", dtype=str)

        # Display the first few rows for debugging
        # print("\nLoaded DataFrame Columns:", df.columns)
        # print("First 5 rows of DataFrame:\n", df.head())

        # Ensure column names are properly stripped of extra spaces
        df.columns = df.columns.str.strip()  # Remove leading/trailing spaces
        if 'Security Name' not in df.columns:
            print("Error: 'Security Name' column not found. Available columns:", df.columns)
            return None

        return df
    except FileNotFoundError:
        print(f"Error: File not found at {NASDAQ_FILE_PATH}. Please check the file path.")
        return None
    except Exception as e:
        print(f"Error loading stock data: {e}")
        return None


def check_code():
    """Search for stock ticker by keyword from local Nasdaq-listed stocks file."""
    df = load_stock_data()
    if df is None:
        print("Failed to load stock data. Please check the file.")
        return

    while True:
        input_keyword = input("Enter a stock keyword to search: ").strip().lower()

        # Filter stocks based on keyword search (limit to 5 results)
        filtered_df = df[df["Security Name"].str.lower().str.contains(input_keyword, na=False)].head(5)

        if filtered_df.empty:
            print(f"No matches found for '{input_keyword}'. Please try again.")
            continue  # Restart loop instead of recursion

        break  # Exit loop when valid results are found

    print("\nAvailable tickers:")
    tickers = []
    for idx, row in enumerate(filtered_df.itertuples(), start=1):
        tickers.append(row.Symbol)
        print(f"{idx}. {row.Symbol} - {row._1}")  # _1 corresponds to 'Security Name'

    # Ask user to select a stock ticker
    while True:
        try:
            selection = int(input("\nEnter the number of the stock you want: "))
            if 1 <= selection <= len(tickers):
                selected_ticker = tickers[selection - 1]
                break
            else:
                print("Invalid selection. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

    print(f"\nValidating ticker: {selected_ticker}...")

    # Fetch stock details using yfinance
    stock_data = yf.Ticker(selected_ticker)
    info = stock_data.info

    if not info or "symbol" not in info:
        print(f"Error: '{selected_ticker}' is not recognized as a valid ticker symbol.")
        print("🔍 Searching for similar tickers...\n")

        # Secondary search for variations of the ticker
        alt_tickers = [ticker for ticker in tickers if ticker.startswith(selected_ticker[:4])]
        if not alt_tickers:
            print("No alternative tickers found.")
            return

        print("Available alternative tickers:")
        for idx, ticker in enumerate(alt_tickers, start=1):
            print(f"{idx}. {ticker}")

        # Ask user to select an alternative ticker
        while True:
            try:
                selection = int(input("\nEnter the number of the alternative stock you want: "))
                if 1 <= selection <= len(alt_tickers):
                    selected_ticker = alt_tickers[selection - 1]
                    break
                else:
                    print("Invalid selection. Please enter a number from the list.")
            except ValueError:
                print("Invalid input. Please enter a number.")

        print(f"\nSelected Ticker: {selected_ticker}")

    else:
        print(f"\nSelected Ticker: {selected_ticker}")

    # Print stock information
    print(f"\nStock code: {info.get('symbol', selected_ticker)}")
    print(f"Price (USD): {info.get('regularMarketPrice', 'N/A')}")
    print(f"Security name: {info.get('longName', 'N/A')}")
    print(f"Security exchange: {info.get('exchange', 'N/A')}")
    print(f"Security sector: {info.get('sector', 'N/A')}")
    print(f"Security industry: {info.get('industry', 'N/A')}")

    return selected_ticker


def view_trend():
    code = input('Please input the code of the stock requested:\n').strip().upper()

    while True:
        try:
            start_date = validate_date("Enter start date (DD-MM-YYYY): ")
            end_date = validate_date("Enter end date (DD-MM-YYYY): ")
            print(f"start: {start_date}")
            print(f"end: {end_date}")
            break
        except ValueError:
            print("The format of the date you entered is incorrect. Please try again.")

    # Download stock data
    df = yf.download(code, start=start_date, end=end_date, auto_adjust=True)

    if df.empty:
        print(f"No data found for '{code}' in the given date range. Possibly delisted or incorrect ticker.")
        return

    # Check for MultiIndex (flatten column names)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)  # Removes 'AAPL' from ('Open', 'AAPL')

    # Convert to numeric & drop invalid rows
    required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
    df = df[required_columns].apply(pd.to_numeric, errors='coerce')  # Convert non-numeric to NaN
    df.dropna(inplace=True)  # Remove rows with missing values

    if df.empty:
        print("❌ No valid numerical data available for plotting. Try another stock.")
        return

    # User selects graph types
    graph_choice = input(
        '''\nPlease select type of graph.\n(1) Candle Stick\n(2) High\n(3) Low\n(4) Open\n(5) Close\n(6) Adj Close\n(7) Moving Average\n(8) Volume\n\nYou may select multiple choices, separate each choice by comma.\n\nSample input for candle stick + High + Volume:\n1,2,8\n\n'''
    )
    graph_choice = graph_choice.split(',')

    plt.figure(figsize=(10, 6))
    plt.title(f"Stock Trend for {code}")

    if '8' in graph_choice and 'Volume' in df.columns:
        graph_choice.remove('8')
        print("Allocated space for volume graph and non-volume graphs.")
        print("Volume graph plotted.")
        plt.plot(df.index, df['Volume'], label='Volume', linestyle='dotted')

    if '1' in graph_choice:
        graph_choice.remove('1')
        if all(col in df.columns for col in ['Open', 'High', 'Low', 'Close']):
            print("Candle stick plotted.")
            df.index = pd.to_datetime(df.index)  # Ensure index is in datetime format
            mpf.plot(df, type='candle', volume=('Volume' in df.columns), title=f"Candlestick Chart for {code}", style='charles')
        else:
            print("Error: Missing required columns for candlestick chart.")

    for choice in graph_choice:
        column_map = {'2': 'High', '3': 'Low', '4': 'Open', '5': 'Close'}
        column_name = column_map.get(choice)
        if column_name in df.columns:
            plt.plot(df.index, df[column_name], label=column_name)

    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.legend()
    plt.grid()
    plt.show()
    print("Other graphs plotted.")


def next_request():
    next_word = input('''\nWould you like to\n1. return to menu\n2. exit program\n(sample input : 1 or 2)\n''').strip()

    if next_word == "1":
        return user_input()  # Restart menu properly

    elif next_word == "2":
        print("Exiting program...")
        sys.exit()

    return user_input()
    # return input(next_word).strip()

def input_to_date(input_date):
    temp = input_date.split('-')
    year, month, day = map(int, temp)
    print(f"day: {day} month: {month} year: {year}")
    return year, month, day
    temp = input_date.split('-')
    year, month, day = map(int, temp)
    print(f"day: {day} month: {month} year: {year}")
    return year, month, day

def validate_date(prompt):
    """Ensure the user inputs a date in DD-MM-YYYY format and return a datetime object."""
    while True:
        date_input = input(prompt).strip()
        if re.match(r"^\d{2}-\d{2}-\d{4}$", date_input):
            try:
                return datetime.strptime(date_input, "%d-%m-%Y")  # ✅ Returns datetime object
            except ValueError:
                print("Invalid date. Please enter a valid date in DD-MM-YYYY format.")
        else:
            print("Invalid format. Please enter date in DD-MM-YYYY format.")

def main():
    print('-------------------------')
    print('Test functions:')
    print('-------------------------\n')
    user_input()


if __name__ == "__main__":
    main()
