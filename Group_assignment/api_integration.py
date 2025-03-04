import yfinance as yf
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import theme as theme
from watchlist import Watchlist

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

        self.container = ctk.CTkFrame(self.parent_frame)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        self.left_frame = ctk.CTkFrame(self.container, width=300)
        self.left_frame.pack(side="left", fill="y", padx=20)

        theme.create_label(self.left_frame, "Enter Company Name or Stock Ticker:").pack(pady=10)
        
        self.search_entry = theme.create_entry(self.left_frame)
        self.search_entry.configure(width=250)
        self.search_entry.pack(pady=10)

        search_button = theme.create_button(self.left_frame, "Search", self.search_stock)
        search_button.pack(pady=15)

        self.add_to_watchlist_var = ctk.IntVar()
        self.watchlist_frame = ctk.CTkFrame(self.left_frame)
        self.watchlist_frame.pack(pady=15)

        theme.create_label(self.watchlist_frame, "Add to Watchlist:").pack(side=ctk.LEFT, padx=15)
        
        yes_button = ctk.CTkRadioButton(self.watchlist_frame, text="Yes", variable=self.add_to_watchlist_var, value=1, command=self.toggle_watchlist_button)
        yes_button.pack(side=ctk.LEFT, padx=10)
        
        no_button = ctk.CTkRadioButton(self.watchlist_frame, text="No", variable=self.add_to_watchlist_var, value=0, command=self.toggle_watchlist_button)
        no_button.pack(side=ctk.LEFT, padx=10)

        self.save_button = theme.create_button(self.left_frame, "Save to Watchlist", self.save_to_watchlist)
        self.save_button.pack(pady=20)
        self.save_button.configure(state=ctk.DISABLED)

        self.right_frame = ctk.CTkFrame(self.container)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=20)

        theme.create_label(self.right_frame, "Current Price:").pack(pady=10)
        self.result_label = ctk.CTkLabel(self.right_frame, text="", justify=ctk.LEFT)
        self.result_label.pack(pady=15)

        self.watchlist_frame = theme.create_frame(self.parent_frame)
        self.watchlist_frame.pack(pady=10, padx=10, fill="x")
        self.watchlist_label = theme.create_label(self.watchlist_frame, "Watchlist:")
        self.watchlist_label.pack()
        
        self.watchlist_box = theme.create_listbox(self.watchlist_frame)
        self.watchlist_box.pack(fill="both", expand=True, padx=10, pady=5)

        self.view_watchlist_button = theme.create_button(self.right_frame, "View Watchlist", self.show_watchlist)
        self.view_watchlist_button.pack(pady=10)
        self.view_watchlist_button.pack_forget()

    def toggle_watchlist_button(self):
        """Enables 'Save to Watchlist' button if 'Yes' is selected."""
        if self.add_to_watchlist_var.get() == 1:
            self.save_button.configure(state=ctk.NORMAL)
        else:
            self.save_button.configure(state=ctk.DISABLED)

    def search_stock(self):
        """Search for stock ticker and display results using yfinance."""
        stock_ticker = self.search_entry.get().strip().upper()
        if not stock_ticker:
            CTkMessagebox(title="Error", message="Please enter a stock ticker.", icon="warning")
            return

        try:
            stock = yf.Ticker(stock_ticker)
            price = stock.history(period="1d")["Close"].iloc[0]
            self.result_label.configure(text=f"{stock_ticker}: ${price:.2f}")
        except:
            self.result_label.configure(text="Stock not found. Please check the ticker.")

    def save_to_watchlist(self):
        """Save stock to watchlist."""
        stock_ticker = self.search_entry.get().upper()
        if stock_ticker:
            self.watchlist_box.insert("end", f"{stock_ticker}\n")
    
    def show_watchlist(self):
        """Display watchlist contents with last fetched price and last update time."""
        watchlist_items = self.watchlist_box.get("1.0", "end").splitlines()
        if not watchlist_items or watchlist_items == [""]:
            CTkMessagebox(title="Watchlist", message="Your watchlist is empty.")
            return

        watchlist_data = []
        for stock_ticker in watchlist_items:
            stock_ticker = stock_ticker.strip().upper()
            if not stock_ticker:
                continue
            try:
                stock = yf.Ticker(stock_ticker)
                hist = stock.history(period="1d")
                if not hist.empty:
                    price = hist["Close"].iloc[0]
                    last_update = hist.index[-1].strftime("%Y-%m-%d %H:%M:%S")
                    watchlist_data.append(f"{stock_ticker}: ${price:.2f} (Last Updated: {last_update})")
                else:
                    watchlist_data.append(f"{stock_ticker}: Data Unavailable")
            except:
                watchlist_data.append(f"{stock_ticker}: Error Fetching Data")

        CTkMessagebox(title="Watchlist", message="\n".join(watchlist_data))