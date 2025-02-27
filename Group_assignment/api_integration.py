import requests
import pandas as pd
import matplotlib.pyplot as plt
import sys
import tkinter
from datetime import datetime

# 🎯 MarketStack API Key
API_KEY = "d04a9fcb4a835aba213c807a2bc6a0b7"

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