import requests
import pandas as pd
import matplotlib.pyplot as plt
import sys
import tkinter
from datetime import datetime
from tkinter import messagebox

# 🎯 MarketStack API Key
API_KEY = "d04a9fcb4a835aba213c807a2bc6a0b7"

class StockSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Search")
        self.root.geometry("400x300")
        
        self.create_widgets()
    
    def create_widgets(self):
        tk.Label(self.root, text="Enter Stock Ticker:").pack(pady=5)
        self.ticker_entry = tk.Entry(self.root)
        self.ticker_entry.pack(pady=5)
        
        search_button = tk.Button(self.root, text="Search", command=self.search_stock)
        search_button.pack(pady=10)
        
        self.result_label = tk.Label(self.root, text="")
        self.result_label.pack(pady=10)
    
    def get_stock_price(self, symbol):
        api_key = "your_marketstack_api_key"
        url = f"http://api.marketstack.com/v1/eod?access_key={api_key}&symbols={symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "data" in data and len(data["data"]) > 0:
                return data["data"][0]["close"]
        return "API request failed"

    def search_stock(self):
        symbol = self.ticker_entry.get().upper()
        price = self.get_stock_price(symbol)
        if price != "API request failed":
            self.result_label.config(text=f"The current price of {symbol} is ${price}")
        else:
            messagebox.showerror("Error", price)