import os
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import theme as theme
import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf  # for candlestick charts
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd


class Watchlist:
    def __init__(self, root, watchlist=None):
        self.root = root
        self.watchlist = watchlist if watchlist is not None else []  # Store watchlist in memory

        # Watchlist UI
        ctk.CTkLabel(self.root, text="Your Watchlist", font=("Arial", 16, "bold")).pack(pady=5)

        self.watchlist_listbox = ctk.CTkTextbox(self.root, height=200, state="disabled")
        self.watchlist_listbox.pack(pady=5, padx=10, fill="both", expand=True)

        # Filters BELOW watchlist textbox
        self.filter_frame = ctk.CTkFrame(self.root)
        self.filter_frame.pack(pady=5, padx=10, fill="both")

        # Dropdowns for Filters (with self.update_chart)
        self.date_filter = ctk.CTkComboBox(self.filter_frame, values=["1 Month", "3 Months", "6 Months", "1 Year"], command=self.update_chart)
        self.date_filter.grid(row=0, column=0, padx=5)

        self.chart_type = ctk.CTkComboBox(self.filter_frame, values=["Heikin Ashi", "Line"], command=self.update_chart)
        self.chart_type.grid(row=0, column=1, padx=5)

        # Bind click event to watchlist items
        self.watchlist_listbox.bind("<Button-1>", self.show_stock_chart)

        self.update_watchlist_display()

    def update_watchlist_display(self):
        """Update the watchlist display with the current stocks."""
        self.watchlist_listbox.configure(state="normal")
        self.watchlist_listbox.delete("1.0", "end")

        for ticker, company_name in self.watchlist:
            self.watchlist_listbox.insert("end", f"{ticker} - {company_name}\n")

        self.watchlist_listbox.configure(state="disabled")

    def show_stock_chart(self, event):
        """Show the stock chart when a stock in the watchlist is clicked."""
        try:
            if not self.watchlist:
                CTkMessagebox(title="Error", message="Watchlist is empty. Please add stocks.", icon="warning")
                return

            index = self.watchlist_listbox.index(f"@{event.x},{event.y}")
            selected_index = int(index.split(".")[0]) - 1

            if 0 <= selected_index < len(self.watchlist):
                ticker = self.watchlist[selected_index][0]
                self.plot_stock_chart(ticker)
            else:
                CTkMessagebox(title="Error", message="Invalid selection. Please select a stock from the watchlist.", icon="warning")

        except Exception as e:
            print(f"Error in show_stock_chart(): {e}")
            CTkMessagebox(title="Error", message="Something went wrong. Please try again.", icon="cancel")

    def update_chart(self, _=None):
        """Update the stock chart when filters change."""
        selected_ticker = self.watchlist_listbox.get("1.0", "1.end").split(" - ")[0]
        if selected_ticker:
            self.plot_stock_chart(selected_ticker)


    def plot_stock_chart(self, ticker):
        """Plot the stock chart using Heikin Ashi candles or selected chart type."""
        
        try:
            period_map = {
                "1 Month": "1mo",
                "3 Months": "3mo",
                "6 Months": "6mo",
                "1 Year": "1y"
            }
            selected_period = period_map.get(self.date_filter.get(), "1mo")  # Default to 1 month
            selected_chart_type = self.chart_type.get()

            stock_data = yf.download(ticker, period=selected_period, interval="1d")

            # ✅ Drop rows with missing values
            stock_data.dropna(inplace=True)

            if stock_data.empty:
                CTkMessagebox(title="Error", message=f"No data available for {ticker}.", icon="warning")
                return

            if selected_chart_type == "Heikin Ashi":
                # ✅ Compute Heikin Ashi candles
                stock_data['HA_Close'] = (stock_data['Open'] + stock_data['High'] + stock_data['Low'] + stock_data['Close']) / 4
                stock_data['HA_Open'] = (stock_data['Open'].shift(1) + stock_data['Close'].shift(1)) / 2
                stock_data['HA_High'] = stock_data[['High', 'HA_Open', 'HA_Close']].max(axis=1)
                stock_data['HA_Low'] = stock_data[['Low', 'HA_Open', 'HA_Close']].min(axis=1)
                heikin_ashi_data = stock_data[['HA_Open', 'HA_High', 'HA_Low', 'HA_Close']]
                heikin_ashi_data.columns = ['Open', 'High', 'Low', 'Close']

                # ✅ Fix `SettingWithCopyWarning`
                heikin_ashi_data = heikin_ashi_data.copy()
                heikin_ashi_data.dropna(inplace=True)

                fig, ax = plt.subplots(figsize=(10, 5))
                mpf.plot(heikin_ashi_data, type='candle', style='charles', ax=ax)
                ax.set_title(f"Heikin Ashi Chart for {ticker}")


            else:  # Line chart
                fig, ax = plt.subplots(figsize=(10, 5))
                ax.plot(stock_data.index, stock_data["Close"], label="Close Price", color="blue")
                ax.set_title(f"Line Chart for {ticker}")
                ax.legend()

            plt.show()

        except Exception as e:
            print(f"Error in plot_stock_chart(): {e}")
            CTkMessagebox(title="Error", message="Error generating the stock chart.", icon="cancel")
