import customtkinter as ctk
from customtkinter import CTk, CTkCanvas, CTkEntry, CTkButton
from CTkMessagebox import CTkMessagebox
import theme as theme

class PortfolioTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Portfolio Tracker")
        self.root.geometry("600x500")
        
        self.create_widgets()

    def create_widgets(self):
        title_label = ctk.CTkLabel(self.root, text="Portfolio Tracker", font=("Helvetica", 16, "bold"))
        title_label.pack(pady=10)

        name_label = ctk.CTkLabel(self.root, text="Enter Your Name:")
        name_label.pack()
        name_entry = ctk.CTkEntry(self.root, textvariable=self.name)
        name_entry.pack(pady=5)

        submit_button = ctk.CTkButton(self.root, text="Submit", command=self.submit_details)
        submit_button.pack(pady=10)

    def display_message(self):
        messagebox.showinfo("Success", "Portfolio Tracker Initialized!")
