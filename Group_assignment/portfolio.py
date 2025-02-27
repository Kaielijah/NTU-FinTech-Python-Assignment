import tkinter as tk

class PortfolioManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Portfolio Management")
        self.root.geometry("400x300")
        
        tk.Label(self.root, text="Portfolio Management Coming Soon...").pack(pady=20)