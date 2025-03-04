import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from watchlist import Watchlist
import theme as theme
from api_integration import StockSearchApp
from portfolio import PortfolioTracker
from visualization import VisualizationApp
from dashboard import DashboardApp  # Import the Dashboard class
import os
class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Portfolio Tracker")
        self.root.geometry("1080x800")

        self.name = ctk.StringVar()
        self.budget = ctk.StringVar()
        self.watchList = []  # Initialize an empty watchlist
        
        self.create_login_screen()

    def create_login_screen(self):
        """Creates the initial login screen for the user to enter details."""
        theme.create_label(self.root, "Enter Your Name:").pack(pady=10)
        self.entry_name = ctk.CTkEntry(self.root, textvariable=self.name)
        self.entry_name.pack(pady=5)

        theme.create_label(self.root, "Enter Your Budget:").pack(pady=10)
        self.entry_budget = ctk.CTkEntry(self.root, textvariable=self.budget)
        self.entry_budget.pack(pady=5)

        theme.create_button(self.root, "Submit", self.submit_details).pack(pady=10)
        theme.create_button(self.root, "Reset", self.reset_fields).pack(pady=10)

    def submit_details(self):
        """Validates user input and transitions to the dashboard if successful."""
        name = self.name.get().strip()  
        budget = self.budget.get().strip()  

        print(f"DEBUG: Name='{name}', Budget='{budget}'")  # Debugging output

        if not name or not budget:
            CTkMessagebox(title="Error", message="Please enter a valid name and budget above 0.", icon="warning")
            return

        try:
            budget = float(budget)
            if budget <= 0:
                raise ValueError
        except ValueError:
            CTkMessagebox(title="Error", message="Budget must be a positive number.", icon="warning")
            return

        # Clear the screen and move to the dashboard
        for widget in self.root.winfo_children():
            widget.destroy()

        # Initialize the Dashboard with user data
        self.dashboard = DashboardApp(self.root, name, budget, self.watchList)

    def reset_fields(self):
        """Clears the input fields."""
        self.name.set("")
        self.budget.set("")

if __name__ == "__main__":
    root = ctk.CTk()
    app = MainApp(root)
    root.mainloop()
