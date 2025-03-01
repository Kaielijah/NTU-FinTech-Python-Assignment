import tkinter as tk
import visualization
from api_integration import StockSearchApp
from portfolio import PortfolioTracker
from visualization import VisualizationApp

class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Portfolio Tracker")
        self.root.geometry("500x400")

        self.name = tk.StringVar()
        self.budget = tk.DoubleVar()

        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Enter Your Name:").pack()
        tk.Entry(self.root, textvariable=self.name).pack(pady=5)

        tk.Label(self.root, text="Enter Your Budget:").pack()
        tk.Entry(self.root, textvariable=self.budget).pack(pady=5)

        submit_button = tk.Button(self.root, text="Submit", command=self.submit_details)
        submit_button.pack(pady=10)

        search_button = tk.Button(self.root, text="Search Stock", command=self.open_stock_search)
        search_button.pack(pady=5)

        portfolio_button = tk.Button(self.root, text="Manage Portfolio", command=self.open_portfolio)
        portfolio_button.pack(pady=5)

        visualize_button = tk.Button(self.root, text="Visualize Stock Data", command=self.open_visualization)
        visualize_button.pack(pady=5)

    def submit_details(self):
        if not self.name.get() or not self.budget.get():
            tk.messagebox.showerror("Error", "Please enter both name and budget.")
        else:
            tk.messagebox.showinfo("Success", f"Welcome {self.name.get()}! Your budget is ${self.budget.get()}")

    def open_stock_search(self):
        stock_window = tk.Toplevel(self.root)
        StockSearchApp(stock_window)

    def open_portfolio(self):
        portfolio_window = tk.Toplevel(self.root)
        PortfolioTracker(portfolio_window)

    def open_visualization(self):
        visualization_window = tk.Toplevel(self.root)
        VisualizationApp(visualization_window)


if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()