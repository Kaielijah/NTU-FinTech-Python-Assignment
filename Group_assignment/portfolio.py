import customtkinter as ctk
from tkinter import ttk, messagebox
import sqlite3
from CTkMessagebox import CTkMessagebox
import theme as theme

class PortfolioTracker:
    def __init__(self, parent_frame):
        self.parent_frame = parent_frame  # Assigning correct reference
        self.title_label = theme.create_label(self.parent_frame, "Financial Portfolio Tracker")
        self.title_label.pack(pady=10)

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
        add_frame = ttk.LabelFrame(self.parent_frame, text="Add Transaction")
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

        self.transaction_type_var = ctk.StringVar(value="buy")
        ttk.Label(add_frame, text="Transaction Type:").grid(row=3, column=0, padx=5, pady=5)
        transaction_type_dropdown = ttk.Combobox(add_frame, textvariable=self.transaction_type_var, values=["buy", "sell"])
        transaction_type_dropdown.grid(row=3, column=1, padx=5, pady=5)

        ttk.Button(add_frame, text="Add Transaction", command=self.add_transaction).grid(row=4, column=0, columnspan=2, pady=10)

        # View Portfolio Section
        self.portfolio_frame = theme.create_frame(self.parent_frame)
        self.portfolio_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Transaction History Section
        self.transaction_frame = theme.create_frame(self.parent_frame)
        self.transaction_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Initial Data Load
        self.view_portfolio()
        self.view_transaction_history()

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

        # Refresh portfolio details and transaction history
        self.update_portfolio()
        self.update_transaction_history()

    def clear_entries(self):
        self.asset_name_entry.delete(0, ctk.END)
        self.quantity_entry.delete(0, ctk.END)
        self.purchase_price_entry.delete(0, ctk.END)

    def view_portfolio(self):
        self.update_portfolio()
    
    def update_portfolio(self):
        for widget in self.portfolio_frame.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(self.portfolio_frame, columns=("Asset Name", "Quantity", "Average Price"), show="headings")
        tree.heading("Asset Name", text="Asset Name")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Average Price", text="Average Price")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

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
                asset_holdings[asset_name]["total_price"] -= quantity * price

        for asset_name, holdings in asset_holdings.items():
            quantity = holdings["quantity"]
            if quantity > 0:
                average_price = holdings["total_price"] / quantity
                tree.insert("", "end", values=(asset_name, quantity, average_price))

    def view_transaction_history(self):
        self.update_transaction_history()

    def update_transaction_history(self):
        for widget in self.transaction_frame.winfo_children():
            widget.destroy()

        tree = ttk.Treeview(self.transaction_frame, columns=("Asset Name", "Transaction Type", "Quantity", "Price", "Date"), show="headings")
        tree.heading("Asset Name", text="Asset Name")
        tree.heading("Transaction Type", text="Transaction Type")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Price", text="Price")
        tree.heading("Date", text="Date")
        tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.cursor.execute("SELECT asset_name, transaction_type, quantity, price, transaction_date FROM transactions")
        transactions = self.cursor.fetchall()
        for row in transactions:
            tree.insert("", "end", values=row)
