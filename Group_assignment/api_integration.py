import requests
import tkinter as tk
from tkinter import messagebox
import watchlist  # Import watchlist module

API_KEY = "d04a9fcb4a835aba213c807a2bc6a0b7"

class StockSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Search")
        self.root.geometry("500x400")

        self.ticker = None  # Store the found ticker
        self.company_name = None  # Store the company name
        self.current_price = None  # Store the stock price

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Enter Company Name or Stock Ticker:").pack(pady=5)
        self.search_entry = tk.Entry(self.root)
        self.search_entry.pack(pady=5)

        search_button = tk.Button(self.root, text="Search", command=self.search_stock)
        search_button.pack(pady=10)

        self.result_label = tk.Label(self.root, text="", justify=tk.LEFT)
        self.result_label.pack(pady=10)

        # Add to Watchlist Radio Button
        self.add_to_watchlist_var = tk.IntVar()  # 1 = Yes, 0 = No
        self.watchlist_frame = tk.Frame(self.root)
        self.watchlist_frame.pack(pady=5)

        tk.Label(self.watchlist_frame, text="Add to Watchlist:").pack(side=tk.LEFT)
        tk.Radiobutton(self.watchlist_frame, text="Yes", variable=self.add_to_watchlist_var, value=1).pack(side=tk.LEFT)
        tk.Radiobutton(self.watchlist_frame, text="No", variable=self.add_to_watchlist_var, value=0).pack(side=tk.LEFT)

        # Save to Watchlist Button
        self.save_button = tk.Button(self.root, text="Save to Watchlist", command=self.save_to_watchlist, state=tk.DISABLED)
        self.save_button.pack(pady=10)

    def search_stock(self):
        """Search for a stock ticker based on user input (company name or ticker) and fetch its price."""
        search_query = self.search_entry.get().strip()

        if not search_query:
            messagebox.showerror("Error", "Please enter a company name or ticker.")
            return

        # API request to search for company/ticker
        search_url = f"http://api.marketstack.com/v1/tickers?access_key={API_KEY}&search={search_query}"
        response = requests.get(search_url)
        data = response.json()

        if "data" in data and len(data["data"]) > 0:
            self.ticker = data["data"][0]["symbol"]  # Get first search result
            self.company_name = data["data"][0].get("name", "Unknown Company")

            # Fetch current stock price
            self.current_price = self.get_stock_price(self.ticker)

            result_text = f"Company: {self.company_name}\nTicker: {self.ticker}\nPrice: ${self.current_price}"
            self.result_label.config(text=result_text)

            # Enable the save button
            self.save_button.config(state=tk.NORMAL)

        else:
            self.result_label.config(text="No results found.")
            self.save_button.config(state=tk.DISABLED)  # Disable the save button if no result found

    def get_stock_price(self, symbol):
        """Fetch the latest stock price for the given symbol."""
        price_url = f"http://api.marketstack.com/v1/eod/latest?access_key={API_KEY}&symbols={symbol}"
        response = requests.get(price_url)

        if response.status_code == 200:
            data = response.json()
            if "data" in data and len(data["data"]) > 0:
                return round(data["data"][0]["close"], 2)  # Round price to 2 decimal places
        return "Unavailable"

    def save_to_watchlist(self):
        """Save the searched stock to the watchlist if selected."""
        if self.add_to_watchlist_var.get() == 1:  # If user selects "Yes"
            if self.ticker and self.company_name:
                watchlist.add_to_watchlist(self.ticker, self.company_name)
                messagebox.showinfo("Success", f"{self.ticker} added to your watchlist.")
            else:
                messagebox.showerror("Error", "No valid stock selected to add.")
        else:
            messagebox.showinfo("Info", "Stock not added to watchlist.")
