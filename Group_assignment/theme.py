import customtkinter as ctk
import json

# Load theme from JSON file
theme_file_path = "Sweetkind.json"
with open(theme_file_path, "r", encoding="utf-8") as file:
    THEME = json.load(file)

# Apply theme to widgets
def create_button(master, text, command, is_side_panel=False):
    button_color = THEME["CTkButton"]["fg_color"][0]
    hover_color = THEME["CTkButton"]["hover_color"][0]
    border_color = THEME["CTkButton"]["border_color"][0]
    text_color = THEME["CTkButton"]["text_color"][0]
    
    return ctk.CTkButton(
        master, text=text, command=command, 
        fg_color=button_color, hover_color=hover_color, 
        border_color=border_color, text_color=text_color
    )

def create_label(master, text):
    text_color = THEME["CTkLabel"]["text_color"][0]
    return ctk.CTkLabel(master, text=text, text_color=text_color)

def create_entry(master):
    fg_color = THEME["CTkEntry"]["fg_color"][0]
    border_color = THEME["CTkEntry"]["border_color"][0]
    text_color = THEME["CTkEntry"]["text_color"][0]
    return ctk.CTkEntry(master, fg_color=fg_color, border_color=border_color, text_color=text_color)

def create_frame(master):
    fg_color = THEME["CTkFrame"]["fg_color"][0]
    border_color = THEME["CTkFrame"]["border_color"][0]
    return ctk.CTkFrame(master, fg_color=fg_color, border_color=border_color)

def create_listbox(parent):
    return ctk.CTkTextbox(parent, height=100, wrap="none")

# Set global theme settings
ctk.set_appearance_mode("dark")
