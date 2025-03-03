import customtkinter as ctk
import theme as theme
from api_integration import StockSearchApp
from portfolio import PortfolioTracker
from visualization import VisualizationApp
from watchlist import Watchlist
import json

class DashboardApp:
    def __init__(self, root, user_name, budget):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1080x800")

        self.user_name = user_name
        self.budget = budget
        self.watchlist = []

        self.create_dashboard()

    def create_dashboard(self):
        """Displays the dashboard with a sidebar and user info."""
        
        self.user_label = theme.create_label(
            self.root, f"Welcome, {self.user_name}! Your budget: ${self.budget:,.2f}"
        )
        self.user_label.place(x=250, y=20)

        self.sidebar = ctk.CTkFrame(self.root, width=200, height=800)
        self.sidebar.pack(side="left", fill="y", padx=20, pady=40)  # Added padding

        self.sidebar_content = ctk.CTkFrame(self.sidebar)
        self.sidebar_content.pack(fill="both", expand=True)

        self.sidebar_buttons_frame = ctk.CTkFrame(self.sidebar_content)
        self.sidebar_buttons_frame.pack(fill="both", expand=True)

        self.create_sidebar_buttons()

        self.main_frame = ctk.CTkFrame(self.root, width=850, height=600)
        self.main_frame.place(x=220, y=80)

    def create_sidebar_buttons(self):
        """Create persistent buttons for the sidebar."""
        for widget in self.sidebar_buttons_frame.winfo_children():
            widget.destroy()

        buttons = [
            ("Price Checker", self.show_stock_search),
            ("Manage Portfolio", self.show_portfolio),
            ("Explore Stock", self.show_visualization),
        ]

        if hasattr(self, "watchlist") and self.watchlist:
            buttons.append(("View Watchlist", self.show_watchlist))

        for text, command in buttons:
            btn = theme.create_button(self.sidebar_buttons_frame, text=text, command=command)
            btn.pack(pady=16, padx=20, fill="x")  # Increased padding

    def clear_main_frame(self):
        """Clears the main content area before switching views."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_stock_search(self):
        self.clear_main_frame()
        StockSearchApp(self.main_frame, watchlist=self.watchlist)

    def show_portfolio(self):
        self.clear_main_frame()
        PortfolioTracker(self.main_frame)

    def show_visualization(self):
        self.clear_main_frame()
        VisualizationApp(self.main_frame)

    def show_watchlist(self):
        self.clear_main_frame()
        Watchlist(self.main_frame, watchlist=self.watchlist)

if __name__ == "__main__":
    root = ctk.CTk()
    app = DashboardApp(root, "Elijah", 99999.00)
    root.mainloop()
