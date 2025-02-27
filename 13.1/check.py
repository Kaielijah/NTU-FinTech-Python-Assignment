import requests
import pandas as pd
import matplotlib.pyplot as plt
import sys
from datetime import datetime

# 🎯 MarketStack API Key
API_KEY = "68b985ad2a427a0049d9808e3373bfed"

def user_input():
    print("Welcome to Stock Master!\n")

    while True:
        choice = input("Select a function:\n1. Search for a stock code by ticker\n2. View stock trend by code\n(Enter 1 or 2): ")

        if choice == "1":
            keyword = input("Enter stock keyword: ")
            ticker = search_ticker(keyword)
            if ticker:
                view_trend(ticker)
            break
        elif choice == "2":
            ticker = input("Enter stock ticker: ")
            view_trend(ticker)
            break
        else:
            print("Invalid input. Please enter 1 or 2.")

def search_ticker(keyword):
    url = f"http://api.marketstack.com/v1/tickers?access_key={API_KEY}&search={keyword}"
    response = requests.get(url).json()
    
    if "data" in response and response["data"]:
        print("\nAvailable tickers:")
        for i, stock in enumerate(response["data"][:5], start=1):
            print(f"{i}. {stock['symbol']}")
        
        try:
            choice = int(input("\nEnter the number of your stock choice: "))
            return response["data"][choice - 1]["symbol"] if 1 <= choice <= len(response["data"]) else response["data"][0]["symbol"]
        except ValueError:
            return response["data"][0]["symbol"]
    
    print("No matches found.")
    return None

def view_trend(ticker):
    print(f"\nFetching stock data for: {ticker}")
    
    start_date = input("Enter start date (DD-MM-YYYY): ")
    end_date = input("Enter end date (DD-MM-YYYY): ")

    try:
        start_date = datetime.strptime(start_date, "%d-%m-%Y").date()
        end_date = datetime.strptime(end_date, "%d-%m-%Y").date()
    except ValueError:
        print("Invalid format. Use DD-MM-YYYY.")
        return view_trend(ticker)

    url = f"http://api.marketstack.com/v1/eod?access_key={API_KEY}&symbols={ticker}&date_from={start_date}&date_to={end_date}"
    response = requests.get(url).json()

    if "data" not in response or not response["data"]:
        print("Error fetching data. Check ticker and API key.")
        return

    df = pd.DataFrame(response["data"])
    df["date"] = pd.to_datetime(df["date"])
    df.sort_values("date", inplace=True)

    graph_type = input("Choose graph type (line, bar): ").strip().lower()
    moving_avg = input("Enter Moving Average period (default 10): ")
    moving_avg = int(moving_avg) if moving_avg.isdigit() else 10

    plt.figure(figsize=(10, 5))

    if graph_type == "bar":
        plt.bar(df["date"], df["close"], color='g', label="Closing Price")
    else:
        plt.plot(df["date"], df["close"], label="Closing Price", color='b')

    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.title(f"Stock Trend: {ticker}")
    plt.legend()
    plt.grid()
    plt.show()

    next_step()

def next_step():
    choice = input("1. Return to menu\n2. Exit\n(Enter 1 or 2): ")

    if choice == "1":
        user_input()
    else:
        print("Exiting program.")
        sys.exit()

if __name__ == "__main__":
    user_input()
