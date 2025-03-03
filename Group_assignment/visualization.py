import pandas as pd
import yfinance as yf
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import matplotlib.pyplot as plt
import theme
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class VisualizationApp:
    def __init__(self, parent_frame):
        """Initialize the Visualization App inside the main frame."""
        self.parent_frame = parent_frame
        self.stocks = {}
        self.create_widgets()

    def create_widgets(self):
        """Creates UI elements for Stock Visualization."""
        for widget in self.parent_frame.winfo_children():
            widget.destroy()

        # Title label
        self.title_label = theme.create_label(self.parent_frame, "Stock Portfolio Allocation")
        self.title_label.pack(pady=10)

        # Input Fields
        self.input_frame = theme.create_frame(self.parent_frame)
        self.input_frame.pack(fill="x", padx=20, pady=10)
        
        theme.create_label(self.input_frame, "Stock Ticker:").pack()
        self.entry_ticker = theme.create_entry(self.input_frame)
        self.entry_ticker.pack()

        theme.create_label(self.input_frame, "Investment ($):").pack()
        self.entry_investment = theme.create_entry(self.input_frame)
        self.entry_investment.pack()

        # Add Button
        self.add_stock_button = theme.create_button(self.input_frame, "Add Stock", self.add_stock)
        self.add_stock_button.pack(pady=10)

        # Portfolio List Frame
        self.portfolio_list_frame = theme.create_frame(self.parent_frame)
        self.portfolio_list_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Run Analysis Button
        self.run_analysis_button = theme.create_button(self.parent_frame, "Run Analysis", self.run_analysis)
        self.run_analysis_button.pack(pady=10)

    def add_stock(self):
        """Adds stock to portfolio list."""
        ticker = self.entry_ticker.get().strip().upper()
        investment = self.entry_investment.get().strip()

        if not ticker or not investment:
            CTkMessagebox(title="Error", message="Please enter valid stock details.", icon="warning")
            return
        
        try:
            investment = float(investment)
        except ValueError:
            CTkMessagebox(title="Error", message="Investment must be a number.", icon="warning")
            return
        
        self.stocks[ticker] = investment
        stock_label = theme.create_label(self.portfolio_list_frame, f"{ticker}: ${investment}")
        stock_label.pack()

    def run_analysis(self):
        """Performs stock allocation visualization."""
        if not self.stocks:
            CTkMessagebox(title="Error", message="No stocks added. Please add stocks to analyze.", icon="warning")
            return
        
        tickers = list(self.stocks.keys())
        investments = list(self.stocks.values())
        
        # Create Pie Chart
        fig, ax = plt.subplots()
        ax.pie(investments, labels=tickers, autopct="%1.1f%%", startangle=90)
        ax.set_title("Portfolio Allocation")
        
        # Display in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=self.parent_frame)
        canvas_widget = canvas.get_tk_widget()
        canvas_widget.pack(pady=10)
        canvas.draw()