import os

WATCHLIST_FILE = "watchlist.txt"

def add_to_watchlist(ticker, company_name):
    """Add a stock ticker to the watchlist file."""
    with open(WATCHLIST_FILE, "a") as file:
        file.write(f"{ticker} - {company_name}\n")

def view_watchlist():
    """Read and display the watchlist."""
    if not os.path.exists(WATCHLIST_FILE):
        return "Watchlist is empty."
    
    with open(WATCHLIST_FILE, "r") as file:
        return file.read()

def clear_watchlist():
    """Clear the watchlist."""
    if os.path.exists(WATCHLIST_FILE):
        os.remove(WATCHLIST_FILE)
        return "Watchlist cleared."
    return "Watchlist is already empty."
