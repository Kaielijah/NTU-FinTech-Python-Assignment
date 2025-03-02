import customtkinter as ctk
import theme as theme
from api_integration import StockSearchApp
from portfolio import PortfolioTracker
from visualization import VisualizationApp
from watchlist import Watchlist

class DashboardApp:
    def __init__(self, root, user_name, budget):
        self.root = root
        self.root.title("Dashboard")
        self.root.geometry("1080x800")

        self.user_name = user_name
        self.budget = budget

        self.sidebar_visible = False  # Track if sidebar is open

        self.create_dashboard()

    def create_dashboard(self):
        """Displays the dashboard with a hamburger menu for navigation."""
        # Welcome Message
        theme.create_label(self.root, f"Welcome, {self.user_name}! Your budget: ${self.budget:,.2f}").pack(pady=20)

        # Hamburger Menu Button (☰)
        self.menu_button = ctk.CTkButton(
            self.root,
            text="☰",
            width=50, height=40,
            font=("Arial", 20, "bold"),
            command=self.toggle_sidebar
        )
        self.menu_button.place(x=10, y=10)

        # Sidebar Frame (Initially Hidden)
        self.sidebar = ctk.CTkFrame(self.root, width=200, height=800)
        self.sidebar.place(x=-200, y=0)

        # Sidebar Menu Buttons
        self.create_sidebar_buttons()

        # Main Content Frame (for displaying different sections)
        self.main_frame = ctk.CTkFrame(self.root, width=850, height=600)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

    def create_dashboard(self):
        """Displays the dashboard with a hamburger menu for navigation."""
        # Welcome Message
        theme.create_label(self.root, f"Welcome, {self.user_name}! Your budget: ${self.budget:,.2f}").pack(pady=20)

        # Sidebar Frame (Initially Hidden)
        self.sidebar = ctk.CTkFrame(self.root, width=200, height=800)
        self.sidebar.place(x=-200, y=0)  # Start off-screen

        # Main Content Frame (for displaying different sections)
        self.main_frame = ctk.CTkFrame(self.root, width=850, height=600)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Create Hamburger Menu Button (☰) and Bring to Front
        self.menu_button = ctk.CTkButton(
            self.root,
            text="☰",
            width=50, height=40,
            font=("Arial", 20, "bold"),
            command=self.toggle_sidebar
        )
        self.menu_button.place(x=10, y=10)  # Always in the top-left corner
        self.menu_button.lift()  # Bring to front

    def create_sidebar_buttons(self):
        """Create buttons for the sidebar menu."""
        for widget in self.sidebar.winfo_children():
            widget.destroy()  # Clear previous widgets to avoid duplication

        buttons = [
            ("Price Checker", self.show_stock_search),
            ("Manage Portfolio", self.show_portfolio),
            ("Explore Stock", self.show_visualization),
            ("View Watchlist", self.show_watchlist)
        ]

        for text, command in buttons:
            btn = theme.create_button(self.sidebar, text=text, command=command)
            btn.pack(pady=5, fill="x", padx=10)  # Fill width to align properly

    def toggle_sidebar(self):
        """Show or hide the sidebar when the hamburger menu is clicked."""
        if self.sidebar_visible:
            self.sidebar.place(x=-200, y=0)  # Hide sidebar
        else:
            self.sidebar.place(x=0, y=0)  # Show sidebar
            self.create_sidebar_buttons()  # Ensure buttons are recreated
            self.sidebar.lift()  # Bring sidebar to the front

        self.sidebar_visible = not self.sidebar_visible  # Toggle state


    def clear_main_frame(self):
        """Clears the main content area before switching views."""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_stock_search(self):
        """Display the Stock Search UI inside the main content area."""
        self.clear_main_frame()
        StockSearchApp(self.main_frame)

    def show_portfolio(self):
        """Display the Portfolio Tracker UI inside the main content area."""
        self.clear_main_frame()
        PortfolioTracker(self.main_frame)

    def show_visualization(self):
        """Display the Visualization UI inside the main content area."""
        self.clear_main_frame()
        VisualizationApp(self.main_frame)

    def show_watchlist(self):
        """Display the Watchlist UI inside the main content area."""
        self.clear_main_frame()
        Watchlist(self.main_frame)

if __name__ == "__main__":
    root = ctk.CTk()
    app = DashboardApp(root, "Elijah", 99999.00)  # Example user
    root.mainloop()
