import requests
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import theme as theme

API_KEY = "d04a9fcb4a835aba213c807a2bc6a0b7"

class StockSearchApp:
    def __init__(self, parent_frame, watchlist=None):
        """Initialize the Stock Search UI inside the provided frame."""
        self.parent_frame = parent_frame
        self.watchlist = watchlist if watchlist is not None else []

        self.create_widgets()

    def create_widgets(self):
        """Creates UI elements for stock search."""
        for widget in self.parent_frame.winfo_children():
            widget.destroy()  # Clear previous content

        # Create a main container frame for layout
        self.container = ctk.CTkFrame(self.parent_frame)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        # Left Section (Search Box & Watchlist)
        self.left_frame = ctk.CTkFrame(self.container, width=300)
        self.left_frame.pack(side="left", fill="y", padx=20)

        theme.create_label(self.left_frame, "Enter Company Name or Stock Ticker:").pack(pady=10)
        
        # Set width separately since `create_entry` does not support width
        self.search_entry = theme.create_entry(self.left_frame)
        self.search_entry.configure(width=250)
        self.search_entry.pack(pady=10)

        search_button = theme.create_button(self.left_frame, "Search", self.search_stock)
        search_button.pack(pady=15)

        # Add to Watchlist Radio Buttons
        self.add_to_watchlist_var = ctk.IntVar()
        self.watchlist_frame = ctk.CTkFrame(self.left_frame)
        self.watchlist_frame.pack(pady=15)

        theme.create_label(self.watchlist_frame, "Add to Watchlist:").pack(side=ctk.LEFT, padx=15)
        
        yes_button = ctk.CTkRadioButton(self.watchlist_frame, text="Yes", variable=self.add_to_watchlist_var, value=1, command=self.toggle_watchlist_button)
        yes_button.pack(side=ctk.LEFT, padx=10)
        
        no_button = ctk.CTkRadioButton(self.watchlist_frame, text="No", variable=self.add_to_watchlist_var, value=0, command=self.toggle_watchlist_button)
        no_button.pack(side=ctk.LEFT, padx=10)

        # Save to Watchlist Button (Initially Disabled)
        self.save_button = theme.create_button(self.left_frame, "Save to Watchlist", self.save_to_watchlist)
        self.save_button.pack(pady=20)
        self.save_button.configure(state=ctk.DISABLED)

        # Right Section (Search Results & Watchlist)
        self.right_frame = ctk.CTkFrame(self.container)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=20)

        theme.create_label(self.right_frame, "Results:").pack(pady=10)
        self.result_label = ctk.CTkLabel(self.right_frame, text="", justify=ctk.LEFT)
        self.result_label.pack(pady=15)

        # Watchlist Section with Scrollable View
        self.watchlist_title = theme.create_label(self.right_frame, "Watchlist:")
        self.watchlist_title.pack(pady=10)
        self.watchlist_box = ctk.CTkTextbox(self.right_frame, height=150, wrap="none")
        self.watchlist_box.pack(fill="both", expand=True, padx=10, pady=5)

        # View Watchlist Button (Initially Hidden)
        self.view_watchlist_button = theme.create_button(self.right_frame, "View Watchlist", self.show_watchlist)
        self.view_watchlist_button.pack(pady=10)
        self.view_watchlist_button.pack_forget()  # Initially hidden

    def toggle_watchlist_button(self):
        """Enables 'Save to Watchlist' button if 'Yes' is selected."""
        if self.add_to_watchlist_var.get() == 1:
            self.save_button.configure(state=ctk.NORMAL)
        else:
            self.save_button.configure(state=ctk.DISABLED)

    def search_stock(self):
        """Search for stock ticker and display results."""
        stock_ticker = self.search_entry.get().strip().upper()
        if not stock_ticker:
            CTkMessagebox(title="Error", message="Please enter a stock ticker.", icon="warning")
            return

        url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={stock_ticker}&apikey={API_KEY}"
        response = requests.get(url)
        data = response.json()

        if "Global Quote" in data and "05. price" in data["Global Quote"]:
            price = data["Global Quote"]["05. price"]
            self.result_label.configure(text=f"Current Price of {stock_ticker}: ${price}")
        else:
            self.result_label.configure(text="Stock not found. Please check the ticker.")

    def save_to_watchlist(self):
        """Save selected stock to the watchlist."""
        stock_ticker = self.search_entry.get().strip().upper()
        if stock_ticker and stock_ticker not in self.watchlist:
            self.watchlist.append(stock_ticker)
            self.watchlist_box.insert("end", f"{stock_ticker}\n")
            CTkMessagebox(title="Success", message=f"{stock_ticker} added to watchlist.")
            self.view_watchlist_button.pack()  # Show button when an item is added

    def show_watchlist(self):
        """Display the watchlist contents."""
        CTkMessagebox(title="Watchlist", message="\n".join(self.watchlist) if self.watchlist else "Watchlist is empty.")
