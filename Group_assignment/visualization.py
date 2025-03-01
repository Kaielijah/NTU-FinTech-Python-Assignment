import pandas as pd
import yfinance as yf
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt


class VisualizationApp:
    def __init__(self, root):
        """Initialize the visualization GUI"""
        self.root = root
        self.root.title("Stock Portfolio Allocation")
        self.root.geometry("900x500")

        self.create_widgets()

    def create_widgets(self):
        """Create UI elements"""
        tk.Label(self.root, text="Stock Ticker:").grid(row=0, column=0)
        self.entry_ticker = tk.Entry(self.root)
        self.entry_ticker.grid(row=0, column=1)

        tk.Label(self.root, text="Investment:").grid(row=1, column=0)
        self.entry_investment = tk.Entry(self.root)
        self.entry_investment.grid(row=1, column=1)

        tk.Button(self.root, text="Add Stock", command=self.add_stock).grid(row=2, column=0, columnspan=2)

        self.stock_list = ttk.Treeview(self.root, columns=("Ticker", "Investment"), show="headings")
        self.stock_list.heading("Ticker", text="Ticker")
        self.stock_list.heading("Investment", text="Investment")
        self.stock_list.grid(row=3, column=0, columnspan=2)

        tk.Button(self.root, text="Run Analysis", command=self.run_analysis).grid(row=4, column=0, columnspan=2)

        columns = ("Ticker", "Price", "Market Cap", "Volume", "Sector", "Investment", "Allocation (%)")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.grid(row=5, column=0, columnspan=2)

    def fetch_stock_data(self, tickers):
        """Fetch stock data for given tickers."""
        data = []
        for ticker in tickers:
            stock = yf.Ticker(ticker)
            info = stock.info
            data.append({
                'Ticker': ticker,
                'Price': info.get('regularMarketPrice', None),
                'Market Cap': info.get('marketCap', None),
                'Volume': info.get('regularMarketVolume', None),
                'Sector': info.get('sector', 'Unknown')
            })
        return pd.DataFrame(data)

    def calculate_portfolio_allocation(self, df, investments):
        """Calculate the portfolio allocation based on user input investments."""
        df['Investment'] = investments
        total_investment = sum(investments)
        df['Allocation (%)'] = (df['Investment'] / total_investment) * 100
        return df

    def plot_pie_chart(self, df):
        """Display a pie chart for portfolio allocation."""
        labels = df['Ticker']
        sizes = df['Allocation (%)']

        plt.figure(figsize=(6, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
        plt.title("Portfolio Allocation (%)")
        plt.show()

    def add_stock(self):
        """Add a stock ticker and investment amount to the list."""
        ticker = self.entry_ticker.get().strip()
        investment = self.entry_investment.get().strip()
        if ticker and investment:
            try:
                investment = float(investment)
                self.stock_list.insert("", "end", values=(ticker, investment))
                self.entry_ticker.delete(0, tk.END)
                self.entry_investment.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Error", "Invalid investment amount. Please enter a number.")

    def run_analysis(self):
        """Perform portfolio analysis and visualization"""
        try:
            tickers = []
            investments = []
            for item in self.stock_list.get_children():
                ticker, investment = self.stock_list.item(item, "values")
                tickers.append(ticker)
                investments.append(float(investment))

            if not tickers:
                messagebox.showerror("Error", "Please add at least one stock.")
                return

            stocks_df = self.fetch_stock_data(tickers)
            allocated_stocks = self.calculate_portfolio_allocation(stocks_df, investments)

            for row in self.tree.get_children():
                self.tree.delete(row)

            for _, row in allocated_stocks.iterrows():
                self.tree.insert("", "end", values=(
                    row['Ticker'], row['Price'], row['Market Cap'], row['Volume'], row['Sector'], row['Investment'],
                    f"{row['Allocation (%)']:.2f}%"))

            self.plot_pie_chart(allocated_stocks)
        except ValueError:
            messagebox.showerror("Error",
                                 "Invalid input: Ensure all investments are numbers and fields are correctly filled.")


# Function to launch visualization when called from main.py
def start_visualization():
    root = tk.Toplevel()  # Open in a new window
    app = VisualizationApp(root)
    root.mainloop()


# ONLY run the GUI if this script is executed directly
if __name__ == "__main__":
    root = tk.Tk()
    app = VisualizationApp(root)
    root.mainloop()
