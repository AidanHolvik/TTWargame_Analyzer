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
class UnitList(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)

        unitList = self.controller.listUnits()
        listVar = tk.Variable(self, unitList.keys(), 'unitNames')

        # Listbox on left
        listFrame = ttk.Frame(self)
        listBox = tk.Listbox(listFrame, listvariable=listVar)
        scrollbar = ttk.Scrollbar(listFrame, orient=tk.VERTICAL, command=listBox.yview)
        listBox['yscrollcommand'] = scrollbar.set

        listBox.pack(side=tk.LEFT)
        scrollbar.pack(side=tk.LEFT)

        # buttons frame on right
            # New
            # Edit
            # Delete
        
        listFrame.pack()
    
    @property
    def controller(self) -> Controller:
        return self.master.controller
    


    

# TODO: unit editor (with buttons)

# Main frame
class View(ttk.Frame):
    def __init__(self, master, controller: Controller = None):
        super().__init__(master)
        self.controller = None

        unitList = UnitList(self) # Testing

        # TODO: add notebook component for navigation
    
    
