import tkinter as tk
from tkinter import messagebox

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Portfolio Tracker")
        self.root.geometry("500x450")
        self.root.config(bg="white")  # Set a light background

        self.name = tk.StringVar()
        self.budget = tk.DoubleVar()

        self.create_widgets()

    def create_widgets(self):
        # Input Section with Labels
        frame_input = tk.Frame(self.root, bg="white")
        frame_input.pack(pady=20)

        tk.Label(frame_input, text="Enter Your Name:", font=("Arial", 12, "bold"), bg="white", fg="black").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(frame_input, textvariable=self.name, font=("Arial", 12), width=25, relief="solid", bd=1).grid(row=0, column=1, padx=10, pady=5)

        tk.Label(frame_input, text="Enter Your Budget:", font=("Arial", 12, "bold"), bg="white", fg="black").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        tk.Entry(frame_input, textvariable=self.budget, font=("Arial", 12), width=25, relief="solid", bd=1).grid(row=1, column=1, padx=10, pady=5)

        # Buttons Section with Styling
        frame_buttons = tk.Frame(self.root, bg="white")
        frame_buttons.pack(pady=10)

        tk.Button(frame_buttons, text="Submit", font=("Arial", 12), width=14, bg="#4CAF50", fg="white", relief="raised", command=self.submit_details).grid(row=0, column=0, padx=10, pady=10)
        tk.Button(frame_buttons, text="Reset", font=("Arial", 12), width=14, bg="#f44336", fg="white", relief="raised", command=self.reset_fields).grid(row=0, column=1, padx=10, pady=10)

        # Feature Buttons
        tk.Button(self.root, text="Search Stock", font=("Arial", 12), bg="#2196F3", fg="white", width=20, relief="raised", command=self.open_stock_search).pack(pady=5)
        tk.Button(self.root, text="Manage Portfolio", font=("Arial", 12), bg="#FF9800", fg="white", width=20, relief="raised", command=self.open_portfolio).pack(pady=5)
        tk.Button(self.root, text="Visualize Stock Data", font=("Arial", 12), bg="#9C27B0", fg="white", width=20, relief="raised", command=self.open_visualization).pack(pady=5)

        # Label for Portfolio Status
        self.label_portfolio = tk.Label(self.root, text="Portfolio View", font=("Arial", 14, "bold"), bg="white", fg="#333333")
        self.label_portfolio.pack(pady=20)

    def submit_details(self):
        if not self.name.get() or not self.budget.get():
            messagebox.showerror("Error", "Please enter both name and budget.")
        else:
            messagebox.showinfo("Success", f"Welcome {self.name.get()}! Your budget is ${self.budget.get():,.2f}")

    def reset_fields(self):
        self.name.set("")
        self.budget.set(0.0)
        self.label_portfolio.config(text="Portfolio View")

    def open_stock_search(self):
        stock_window = tk.Toplevel(self.root)
        stock_window.title("Stock Search")

    def open_portfolio(self):
        portfolio_window = tk.Toplevel(self.root)
        portfolio_window.title("Manage Portfolio")

    def open_visualization(self):
        visualization_window = tk.Toplevel(self.root)
        visualization_window.title("Stock Visualization")

if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
