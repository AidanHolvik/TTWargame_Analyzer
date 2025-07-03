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
        self.controller = None

        unitList = {}
        if self.controller is not None:
            unitList = self.controller.listUnits()
        listVar = tk.Variable(self, list(unitList.keys()), 'unitNames')

        # Listbox on left
        listFrame = ttk.Frame(self)
        listBox = tk.Listbox(listFrame, listvariable=listVar)
        scrollbar = ttk.Scrollbar(listFrame, orient=tk.VERTICAL, command=listBox.yview)
        listBox['yscrollcommand'] = scrollbar.set

        listBox.pack(side=tk.LEFT)
        scrollbar.pack(side=tk.LEFT)

        # buttons frame on right
        buttonFrame = ttk.Frame(self)
        btnNew = ttk.Button(buttonFrame, text='New')
        btnEdit = ttk.Button(buttonFrame, text='Edit')
        btnDelete = ttk.Button(buttonFrame, text='Delete')

        btnNew.pack()
        btnEdit.pack()
        btnDelete.pack()
        
        listFrame.pack(side=tk.LEFT)
        buttonFrame.pack(side=tk.LEFT)
    
    @property
    def controller(self) -> Controller:
        return self._controller
    @controller.setter
    def controller(self, value: Controller):
        self._controller = value
        # TODO: refresh this widget
    
    


    

# TODO: unit editor (with buttons)

# Main frame
class View(ttk.Frame):
    def __init__(self, master, controller: Controller = None):
        super().__init__(master)
        self._controller = None

        self.unitList = UnitList(self) # Testing
        self.unitList.pack()

        # TODO: add notebook component for navigation
    
    @property
    def controller(self) -> Controller:
        return self._controller
    @controller.setter
    def controller(self, value: Controller):
        self._controller = value
        self.unitList.controller = self.controller
    


    
    
