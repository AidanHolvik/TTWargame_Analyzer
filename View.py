import tkinter as tk
from tkinter import ttk
from Controller import Controller


"""
The view is responsible for:
    - Rendering data to the user in a specific format
    - Displaying the user interface elements
    - Updating the display when the Model changes
"""

# TODO: unit list (with buttons)

# TODO: unit editor (with buttons)

# Main frame
class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = None

        # TODO: add notebook component for navigation
    
