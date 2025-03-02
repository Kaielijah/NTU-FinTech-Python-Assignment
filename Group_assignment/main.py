import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from watchlist import Watchlist
import theme as theme
from api_integration import StockSearchApp
from portfolio import PortfolioTracker
from visualization import VisualizationApp
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Portfolio Tracker")
        self.root.geometry("1080x800")

        self.name = ctk.StringVar()
        self.budget = ctk.StringVar()
        self.watchList = []  # Initialize an empty watchlist
        self.create_widgets()

    def create_widgets(self):
        theme.create_label(self.root, "Enter Your Name:").pack(pady=10)
        self.entry_name = ctk.CTkEntry(self.root, textvariable=self.name)
        self.entry_name.pack(pady=5)

        theme.create_label(self.root, "Enter Your Budget:").pack(pady=10)
        self.entry_budget = ctk.CTkEntry(self.root, textvariable=self.budget)
        self.entry_budget.pack(pady=5)

        theme.create_button(self.root, "Submit", self.submit_details).pack(pady=10)
        theme.create_button(self.root, "Reset", self.reset_fields).pack(pady=10)

        # View Search Stock Button    
        search_button = theme.create_button(self.root, text="Search Stock", command=self.open_stock_search)
        search_button.pack(pady=5)

        # View Manage Portfolio Button
        portfolio_button = theme.create_button(self.root, text="Manage Portfolio", command=self.open_portfolio)
        portfolio_button.pack(pady=5)

        # View Research Stock Button
        visualize_button = theme.create_button(self.root, text="Explore Stock", command=self.open_visualization)
        visualize_button.pack(pady=5)

        # View Watchlist Button
        watchlist_button = theme.create_button(self.root, text="View Watchlist", command=self.open_watchlist)
        watchlist_button.pack(pady=5)

    def submit_details(self):
        name = self.name.get().strip()  # Ensure no extra spaces
        budget = self.budget.get().strip()  # Ensure no extra spaces

        print(f"DEBUG: Name='{name}', Budget='{budget}'")  # Debug print

        if not name or not budget:
            CTkMessagebox(title="Error", message="Please enter a valid name and budget above 0.", icon="warning")
            return

        try:
            budget = float(budget)  # Convert budget to float
            if budget <= 0:
                raise ValueError  # Ensure budget is positive
        except ValueError:
            CTkMessagebox(title="Error", message="Budget must be a positive number.", icon="warning")
            return

        CTkMessagebox(title="Success", message=f"Welcome {name}! Your budget is ${budget:,.2f}", icon="check")

    def reset_fields(self):
        """Clears the input fields."""
        self.name.set("")
        self.budget.set(0.0)

    def open_stock_search(self):
        stock_window = ctk.CTkToplevel(self.root)
        StockSearchApp(stock_window, watchlist=self.watchList)

    def open_portfolio(self):
        portfolio_window = ctk.CTkToplevel(self.root)
        PortfolioTracker(portfolio_window)

    def open_visualization(self):
        visualization_window = ctk.CTkToplevel(self.root)
        VisualizationApp(visualization_window)

    def view_watchlist(self):
        """Display the watchlist in a messagebox."""
        watchlist_content = watchlist.view_watchlist()
        CTkMessagebox(title="Watchlist", message="Stock added", width=max(250, int(width)))

    def open_watchlist(self):
        watchlist_window = ctk.CTkToplevel(self.root)
        WatchlistApp(watchlist_window, self.watchList)


if __name__ == "__main__":
        root = ctk.CTk()
        app = MainApp(root)
        root.mainloop()

