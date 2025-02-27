import sqlite3
from tkinter import messagebox

class PortfolioManager:
    def __init__(self):
        self.initialize_database()

    def initialize_database(self):
        conn = sqlite3.connect("portfolio.db")
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS portfolio (symbol TEXT, qty INTEGER, price REAL)")
        conn.commit()
        conn.close()

    def add_asset_to_portfolio(self, symbol, qty, price):
        conn = sqlite3.connect("portfolio.db")
        c = conn.cursor()
        c.execute("INSERT INTO portfolio VALUES (?, ?, ?)", (symbol, qty, price))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"Added {qty} of {symbol} at ${price} each to portfolio.")

    def display_portfolio(self):
        conn = sqlite3.connect("portfolio.db")
        c = conn.cursor()
        c.execute("SELECT * FROM portfolio")
        rows = c.fetchall()
        conn.close()

        print("Portfolio:")
        for row in rows:
            print(f"{row[0]}: {row[1]} shares at ${row[2]}")
