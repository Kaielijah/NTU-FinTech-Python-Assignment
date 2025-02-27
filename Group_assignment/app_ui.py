import tkinter as tk
from tkinter import messagebox

class PortfolioTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Portfolio Tracker")
        self.root.geometry("600x500")
        
        self.create_widgets()

    def create_widgets(self):
        title_label = tk.Label(self.root, text="Portfolio Tracker", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        name_label = tk.Label(self.root, text="Enter Your Name:")
        name_label.pack()
        name_entry = tk.Entry(self.root)
        name_entry.pack(pady=5)

        submit_button = tk.Button(self.root, text="Submit", command=self.display_message)
        submit_button.pack(pady=10)

    def display_message(self):
        messagebox.showinfo("Success", "Portfolio Tracker Initialized!")
