import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

class PortfolioTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Financial Portfolio Tracker")

        # Database Connection
        self.conn = sqlite3.connect("portfolio.db")
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_name TEXT,
                transaction_type TEXT, -- "buy" or "sell"
                quantity REAL,
                price REAL,
                transaction_date TEXT -- Or INTEGER for timestamp
            )
        """)
        self.conn.commit()

        # GUI Elements
        self.create_widgets()

    def create_widgets(self):
        # Add Transaction Frame
        add_frame = ttk.LabelFrame(self.root, text="Add Transaction")
        add_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(add_frame, text="Asset Name:").grid(row=0, column=0, padx=5, pady=5)
        self.asset_name_entry = ttk.Entry(add_frame)
        self.asset_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(add_frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Price:").grid(row=2, column=0, padx=5, pady=5)
        self.purchase_price_entry = ttk.Entry(add_frame)
        self.purchase_price_entry.grid(row=2, column=1, padx=5, pady=5)

        self.transaction_type_var = tk.StringVar(value="buy")
        ttk.Label(add_frame, text="Transaction Type:").grid(row=3, column=0, padx=5, pady=5)
        transaction_type_dropdown = ttk.Combobox(add_frame, textvariable=self.transaction_type_var, values=["buy", "sell"])
        transaction_type_dropdown.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(add_frame, text="Add Transaction", command=self.add_transaction).grid(row=4, column=0, columnspan=2, pady=10)

        # View Portfolio Button
        ttk.Button(self.root, text="View Portfolio", command=self.view_portfolio).pack(pady=10)

    def add_transaction(self):
        asset_name = self.asset_name_entry.get()
        transaction_type = self.transaction_type_var.get()
        try:
            quantity = float(self.quantity_entry.get())
            price = float(self.purchase_price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input for quantity or price.")
            return

        self.cursor.execute("INSERT INTO transactions (asset_name, transaction_type, quantity, price, transaction_date) VALUES (?, ?, ?, ?, datetime('now'))",
                            (asset_name, transaction_type, quantity, price))
        self.conn.commit()
        messagebox.showinfo("Success", "Transaction added successfully.")
        self.clear_entries()

    def clear_entries(self):
        self.asset_name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.purchase_price_entry.delete(0, tk.END)

    def view_portfolio(self):
        portfolio_window = tk.Toplevel(self.root)
        portfolio_window.title("Portfolio Details")

        tree = ttk.Treeview(portfolio_window, columns=("Asset Name", "Quantity", "Average Price"), show="headings")
        tree.heading("Asset Name", text="Asset Name")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Average Price", text="Average Price")
        tree.pack(padx=10, pady=10)

        # Calculate current holdings
        asset_holdings = {}
        self.cursor.execute("SELECT asset_name, transaction_type, quantity, price FROM transactions")
        transactions = self.cursor.fetchall()

        for asset_name, transaction_type, quantity, price in transactions:
            if asset_name not in asset_holdings:
                asset_holdings[asset_name] = {"quantity": 0, "total_price": 0}

            if transaction_type == "buy":
                asset_holdings[asset_name]["quantity"] += quantity
                asset_holdings[asset_name]["total_price"] += quantity * price
            elif transaction_type == "sell":
                asset_holdings[asset_name]["quantity"] -= quantity

        for asset_name, holdings in asset_holdings.items():
            quantity = holdings["quantity"]
            if quantity > 0:
                average_price = holdings["total_price"] / quantity
                tree.insert("", tk.END, values=(asset_name, quantity, average_price))

        ttk.Button(portfolio_window, text = "View Transaction History", command = lambda: self.view_transaction_history(portfolio_window)).pack(pady=10)

    def view_transaction_history(self, portfolio_window):
        transaction_history_window = tk.Toplevel(portfolio_window)
        transaction_history_window.title("Transaction History")

        tree = ttk.Treeview(transaction_history_window, columns=("Asset Name", "Transaction Type", "Quantity", "Price", "Date"), show="headings")
        tree.heading("Asset Name", text="Asset Name")
        tree.heading("Transaction Type", text="Transaction Type")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Price", text="Price")
        tree.heading("Date", text="Date")
        tree.pack(padx=10, pady=10)

        self.cursor.execute("SELECT asset_name, transaction_type, quantity, price, transaction_date FROM transactions")
        transactions = self.cursor.fetchall()
        for row in transactions:
            tree.insert("", tk.END, values=row)

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = PortfolioTracker(root)
    root.mainloop()