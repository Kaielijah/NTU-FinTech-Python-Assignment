import tkinter as tk

class VisualizationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Visualization")
        self.root.geometry("400x300")
        
        tk.Label(self.root, text="Stock Visualization Coming Soon...").pack(pady=20)