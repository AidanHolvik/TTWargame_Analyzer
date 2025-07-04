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
    def __init__(self, master, controller: Controller = None, **kw):
        super().__init__(master, **kw)
        self.controller = controller

        # TODO: this code block (below) is handling behaviour which should be handled by the controller
        unitList = {}
        if self.controller is not None:
            unitList = self.controller.listUnits()
        listVar = tk.Variable(self, list(unitList.keys()), 'unitNames')
        # TODO: this code block (above) is handling behaviour which should be handled by the controller

        # Listbox on left
        listFrame = ttk.Frame(self)
        listBox = tk.Listbox(listFrame, listvariable=listVar)
        scrollbar = ttk.Scrollbar(listFrame, orient=tk.VERTICAL, command=listBox.yview)
        listBox['yscrollcommand'] = scrollbar.set

        listBox.pack(side=tk.LEFT)
        scrollbar.pack(side=tk.LEFT)

        # buttons frame on right
        buttonFrame = ttk.Frame(self)
        self.btnNew = ttk.Button(buttonFrame, text='New')
        self.btnEdit = ttk.Button(buttonFrame, text='Edit')
        self.btnDelete = ttk.Button(buttonFrame, text='Delete')

        self.btnNew.pack()
        self.btnEdit.pack()
        self.btnDelete.pack()
        
        listFrame.pack(side=tk.LEFT)
        buttonFrame.pack(side=tk.LEFT)
    
class UnitEditor(ttk.Frame):
    def __init__(self, master, controller: Controller = None, **kw):
        super().__init__(master, **kw)
        self.controller = controller
        self.prevName = None
    
        self.name = tk.StringVar(self, name='unitName')
        self.cost = tk.IntVar(self, name='unitCost')

        # Unit Name
        nameFrame = ttk.Frame(self)
        nameLabel = ttk.Label(nameFrame, text='Name')
        nameField = ttk.Entry(nameFrame, textvariable=self.name)
        nameLabel.pack(side=tk.LEFT)
        nameField.pack(side=tk.LEFT)

        # Unit Cost
        costFrame = ttk.Frame(self)
        costLabel = ttk.Label(costFrame, text='Points Cost')
        costField = ttk.Spinbox(costFrame, from_=0, to=9999, textvariable=self.cost)
        costLabel.pack(side=tk.LEFT)
        costField.pack(side=tk.LEFT)

        # TODO: unit models

        # TODO: buttons
        buttonFrame = ttk.Frame(self)
        self.cancelButton = ttk.Button(buttonFrame, text='Cancel')
        self.saveButton = ttk.Button(buttonFrame, text='Save')
        self.cancelButton.pack(side=tk.LEFT)
        self.saveButton.pack(side=tk.RIGHT)

        # Pack top-level frames
        nameFrame.pack()
        costFrame.pack()
        buttonFrame.pack()

    


    

# TODO: unit editor (with buttons)

# Main frame
class View(ttk.Frame):
    def __init__(self, master, controller: Controller = None, **kw):
        super().__init__(master, **kw)
        self.controller = controller

        self.unitList = UnitList(self, controller) # Testing
        self.unitEditor = UnitEditor(self, controller)

        self.unitEditor.pack()

        # TODO: add notebook component for navigation
    


    
    
