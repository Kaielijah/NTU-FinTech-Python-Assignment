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
            CREATE TABLE IF NOT EXISTS assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                asset_name TEXT,
                quantity REAL,
                purchase_price REAL
            )
        """)
        self.conn.commit()

        # GUI Elements
        self.create_widgets()

    def create_widgets(self):
        # Add Asset Frame
        add_frame = ttk.LabelFrame(self.root, text="Add Asset")
        add_frame.pack(padx=10, pady=10, fill="x")

        ttk.Label(add_frame, text="Asset Name:").grid(row=0, column=0, padx=5, pady=5)
        self.asset_name_entry = ttk.Entry(add_frame)
        self.asset_name_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Quantity:").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_entry = ttk.Entry(add_frame)
        self.quantity_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(add_frame, text="Purchase Price:").grid(row=2, column=0, padx=5, pady=5)
        self.purchase_price_entry = ttk.Entry(add_frame)
        self.purchase_price_entry.grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(add_frame, text="Add Asset", command=self.add_asset).grid(row=3, column=0, columnspan=2, pady=10)

        # View Portfolio Button
        ttk.Button(self.root, text="View Portfolio", command=self.view_portfolio).pack(pady=10)

    def add_asset(self):
        asset_name = self.asset_name_entry.get()
        try:
            quantity = float(self.quantity_entry.get())
            purchase_price = float(self.purchase_price_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Invalid input for quantity or purchase price.")
            return

        self.cursor.execute("INSERT INTO assets (asset_name, quantity, purchase_price) VALUES (?, ?, ?)",
                            (asset_name, quantity, purchase_price))
        self.conn.commit()
        messagebox.showinfo("Success", "Asset added successfully.")
        self.clear_entries()

    def clear_entries(self):
        self.asset_name_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.purchase_price_entry.delete(0, tk.END)

    def view_portfolio(self):
        portfolio_window = tk.Toplevel(self.root)
        portfolio_window.title("Portfolio Details")

        tree = ttk.Treeview(portfolio_window, columns=("ID", "Asset Name", "Quantity", "Purchase Price"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Asset Name", text="Asset Name")
        tree.heading("Quantity", text="Quantity")
        tree.heading("Purchase Price", text="Purchase Price")
        tree.pack(padx=10, pady=10)

        self.cursor.execute("SELECT * FROM assets")
        rows = self.cursor.fetchall()
        for row in rows:
            tree.insert("", tk.END, values=row)

        # Modify Asset button and Function.
        ttk.Button(portfolio_window, text = "Modify Asset", command = lambda: self.modify_asset(tree, portfolio_window)).pack(pady=10)

    def modify_asset(self, tree, portfolio_window):
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Select an asset to modify.")
            return

        item_id = tree.item(selected_item, "values")[0]

        modify_window = tk.Toplevel(portfolio_window)
        modify_window.title("Modify Asset")

        ttk.Label(modify_window, text="New Quantity:").grid(row=0, column=0, padx=5, pady=5)
        new_quantity_entry = ttk.Entry(modify_window)
        new_quantity_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(modify_window, text="New Purchase Price:").grid(row=1, column=0, padx=5, pady=5)
        new_price_entry = ttk.Entry(modify_window)
        new_price_entry.grid(row=1, column=1, padx=5, pady=5)

        def update_asset():
            try:
                new_quantity = float(new_quantity_entry.get())
                new_price = float(new_price_entry.get())
            except ValueError:
                messagebox.showerror("Error", "Invalid input.")
                return

            self.cursor.execute("UPDATE assets SET quantity = ?, purchase_price = ? WHERE id = ?",
                                (new_quantity, new_price, item_id))
            self.conn.commit()
            messagebox.showinfo("Success", "Asset modified.")
            modify_window.destroy()
            self.view_portfolio() #refresh the view.

        ttk.Button(modify_window, text="Update", command=update_asset).grid(row=2, column=0, columnspan=2, pady=10)

    def __del__(self):
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

if __name__ == "__main__":
    root = tk.Tk()
    app = PortfolioTracker(root)
    root.mainloop()