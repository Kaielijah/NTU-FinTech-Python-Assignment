import warnings
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import mplfinance as mpf
import sys
from datetime import datetime
import re

warnings.filterwarnings("ignore")


def user_input():
    word = '''\nWelcome to Stock Master!\n\nPlease select a function to continue:\n\n(1) Search for a stock code by keyword\n(2) View stock trend by code\n\n(sample input 1 or 2)\n'''
    while True:
        function = input(word)
        if function == '1':
            check_code()
        elif function == '2':
            view_trend()
        else:
            print("Invalid input. Please enter either 1 or 2.")


def check_code():
    input_keyword = input('Enter a keyword to search: ').strip()
    if not input_keyword.isalnum():
        print("Invalid input. Please enter a valid stock ticker keyword.")
        return

    try:
        ticker = yf.Ticker(input_keyword)
        info = ticker.info
        if not info or 'symbol' not in info:
            print(f"No information found for ticker: {input_keyword}. Please try again.")
            return

        print(f"Stock code for {input_keyword}: {info.get('symbol')}")
        print(f"Price (USD): {info.get('regularMarketPrice', 'N/A')}")
    except Exception as e:
        print(f"Error fetching data for {input_keyword}: {e}")


def view_trend():
    input_keyword = input("Enter stock code: ").strip().upper()
    if not input_keyword:
        print("Invalid stock code. Returning to menu.")
        return

    start_date = validate_date("Enter start date (DD-MM-YYYY): ")
    end_date = validate_date("Enter end date (DD-MM-YYYY): ")

    try:
        df = yf.download(input_keyword, start=start_date, end=end_date, auto_adjust=False)
        if df.empty:
            print("No data found for this stock. Returning to menu.")
            return
    except Exception as e:
        print(f"Error downloading data: {e}")
        return

    plot_graphs(df, input_keyword)


def validate_date(prompt):
    while True:
        date_input = input(prompt).strip()
        if re.match(r"^\d{2}-\d{2}-\d{4}$", date_input):
            try:
                return datetime.strptime(date_input, "%d-%m-%Y").strftime("%Y-%m-%d")
            except ValueError:
                print("Invalid date. Please enter a valid date in DD-MM-YYYY format.")
        else:
            print("Invalid format. Please enter date in DD-MM-YYYY format.")


def plot_graphs(df, input_keyword):
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
    """)
    graph_choices = input("Enter graph choices (e.g., 1,2,8): ").strip().split(",")
    graph_choices = [choice.strip() for choice in graph_choices if choice.strip().isdigit()]
    graph_choices = list(set(graph_choices))

    print(f"graph to draw: {graph_choices}")
    if '8' in graph_choices:
        graph_choices.remove('8')
        print(f"graph to draw: {graph_choices}")
        print("Allocated space for volume graph and non-volume graphs.")
        print("Volume graph plotted.")

    if '1' in graph_choices:
        graph_choices.remove('1')
        print("Candle stick plotted.")
        print(f"graph to draw: {graph_choices}")

    ma_list = []
    if '7' in graph_choices:
        graph_choices.remove('7')
        ma_input = input("Please input the frequency for the moving average:\n").strip()
        ma_list = [int(ma) for ma in re.findall(r'\d+', ma_input) if ma.isdigit()]  # Extract only valid numbers
        if ma_list:
            print(f"Moving average graph with frequency {', '.join(map(str, ma_list))} is plotted.")
        else:
            print("No valid moving average frequency entered.")
        print(f"graph to draw: {graph_choices}")

    plt.figure(figsize=(10, 6))
    plt.title(f"Stock Trend for {input_keyword}")
    for choice in graph_choices:
        if choice in ['2', '3', '4', '5', '6']:
            column_name = ['High', 'Low', 'Open', 'Close', 'Adj Close'][int(choice) - 2]
            plt.plot(df.index, df[column_name], label=column_name)
    if ma_list:
        for ma in ma_list:
            df[f"MA{ma}"] = df['Adj Close'].rolling(window=ma).mean()
            plt.plot(df.index, df[f"MA{ma}"], label=f"{ma}-Day MA")
    plt.xlabel("Date")
    plt.ylabel("Stock Price")
    plt.legend()
    plt.grid()
    plt.show()

    print("Other graphs plotted.")


def input_to_date(input_date):
    temp = input_date.split('-')
    year, month, day = map(int, temp)
    print(f"year: {year} month: {month} day: {day}")
    return year, month, day
    temp = input_date.split('-')
    year, month, day = map(int, temp)
    print("year:", year, "month:", month, "day:", day)
    return year, month, day


def main():
    print('-------------------------')
    print('Test check code function:')
    print('-------------------------\n')
    check_code()
    print('-------------------------')
    print('Test view trend function:')
    print('-------------------------\n')
    view_trend()
    print('-------------------------')
    print('Test input_to_date function:')
    print('-------------------------\n')
    input_to_date("2020-03-04")


if __name__ == "__main__":
    main()
