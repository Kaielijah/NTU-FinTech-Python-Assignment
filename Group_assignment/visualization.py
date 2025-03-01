import pandas as pd
import yfinance as yf
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt


def fetch_stock_data(tickers):
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


def filter_stocks(df, min_price=None, max_price=None, min_market_cap=None, min_volume=None):
    """Filter stocks based on given criteria."""
    if min_price is not None:
        df = df[df['Price'] >= min_price]
    if max_price is not None:
        df = df[df['Price'] <= max_price]
    if min_market_cap is not None:
        df = df[df['Market Cap'] >= min_market_cap]
    if min_volume is not None:
        df = df[df['Volume'] >= min_volume]
    return df


def calculate_portfolio_allocation(df, investments):
    """Calculate the portfolio allocation based on user input investments."""
    df['Investment'] = investments
    total_investment = sum(investments)
    df['Allocation (%)'] = (df['Investment'] / total_investment) * 100
    return df


def plot_pie_chart(df):
    """Display a pie chart for portfolio allocation."""
    labels = df['Ticker']
    sizes = df['Allocation (%)']

    plt.figure(figsize=(6, 6))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.title("Portfolio Allocation (%)")
    plt.show()


def add_stock():
    """Add a stock ticker and investment amount to the list."""
    ticker = entry_ticker.get().strip()
    investment = entry_investment.get().strip()
    if ticker and investment:
        try:
            investment = float(investment)
            stock_list.insert("", "end", values=(ticker, investment))
            entry_ticker.delete(0, tk.END)
            entry_investment.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Invalid investment amount. Please enter a number.")


def run_analysis():
    try:
        tickers = []
        investments = []
        for item in stock_list.get_children():
            ticker, investment = stock_list.item(item, "values")
            tickers.append(ticker)
            investments.append(float(investment))

        if not tickers:
            messagebox.showerror("Error", "Please add at least one stock.")
            return

        stocks_df = fetch_stock_data(tickers)
        allocated_stocks = calculate_portfolio_allocation(stocks_df, investments)

        for row in tree.get_children():
            tree.delete(row)

        for _, row in allocated_stocks.iterrows():
            tree.insert("", "end", values=(
            row['Ticker'], row['Price'], row['Market Cap'], row['Volume'], row['Sector'], row['Investment'],
            f"{row['Allocation (%)']:.2f}%"))

        plot_pie_chart(allocated_stocks)
    except ValueError:
        messagebox.showerror("Error",
                             "Invalid input: Ensure all investments are numbers and fields are correctly filled.")


# GUI setup
root = tk.Tk()
root.title("Stock Portfolio Allocation")
root.geometry("900x500")

tk.Label(root, text="Stock Ticker:").grid(row=0, column=0)
entry_ticker = tk.Entry(root)
entry_ticker.grid(row=0, column=1)

tk.Label(root, text="Investment:").grid(row=1, column=0)
entry_investment = tk.Entry(root)
entry_investment.grid(row=1, column=1)

tk.Button(root, text="Add Stock", command=add_stock).grid(row=2, column=0, columnspan=2)

stock_list = ttk.Treeview(root, columns=("Ticker", "Investment"), show="headings")
stock_list.heading("Ticker", text="Ticker")
stock_list.heading("Investment", text="Investment")
stock_list.grid(row=3, column=0, columnspan=2)

tk.Button(root, text="Run Analysis", command=run_analysis).grid(row=4, column=0, columnspan=2)

columns = ("Ticker", "Price", "Market Cap", "Volume", "Sector", "Investment", "Allocation (%)")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=100)
tree.grid(row=5, column=0, columnspan=2)

root.mainloop()