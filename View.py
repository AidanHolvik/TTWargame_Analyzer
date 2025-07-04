import tkinter as tk
from tkinter import ttk
from Model import Database, Model, Unit


"""
The view is responsible for:
    - Rendering data to the user in a specific format
    - Displaying the user interface elements
    - Updating the display when the Model changes
"""

# TODO: unit list (with buttons)
class UnitList(ttk.Frame):
    def __init__(self, master, model: Database = None, **kw):
        super().__init__(master, **kw)
        self.model = model

        self.unitList = tk.Variable(self, [], 'unitNames')
        self.refreshUnitList()

        # Listbox on left
        listFrame = ttk.Frame(self)
        listBox = tk.Listbox(listFrame, listvariable=self.unitList)
        scrollbar = ttk.Scrollbar(listFrame, orient=tk.VERTICAL, command=listBox.yview)
        listBox['yscrollcommand'] = scrollbar.set

        listBox.pack(side=tk.LEFT)
        scrollbar.pack(side=tk.LEFT)

        # buttons frame on right
        buttonFrame = ttk.Frame(self)
        self.btnNew = ttk.Button(buttonFrame, text='New', command=self.btnCmdNew)
        self.btnEdit = ttk.Button(buttonFrame, text='Edit')
        self.btnDelete = ttk.Button(buttonFrame, text='Delete')

        self.btnNew.pack()
        self.btnEdit.pack()
        self.btnDelete.pack()
        
        listFrame.pack(side=tk.LEFT)
        buttonFrame.pack(side=tk.LEFT)
    
    def refreshUnitList(self):
        unitNames = []
        if self.model is not None:
            for unit in self.model.listUnits():
                unitNames.append(unit.name)
        self.unitList.set(unitNames)
    

    def btnCmdNew(self):
        # hide all current frames
        # populate unit editor
        # pack UnitEditor frame
        pass
    # TODO: button editUnit
    # TODO: button deleteUnit


    
class UnitEditor(ttk.Frame):
    def __init__(self, master, model: Database = None, **kw):
        super().__init__(master, **kw)
        self.model = model
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

        # TODO: models frame

        # Buttons
        buttonFrame = ttk.Frame(self)
        cancelButton = ttk.Button(buttonFrame, text='Cancel')
        saveButton = ttk.Button(buttonFrame, text='Save', command=self.saveUnit)
        cancelButton.pack(side=tk.LEFT)
        saveButton.pack(side=tk.RIGHT)

        # Pack top-level frames
        nameFrame.pack()
        costFrame.pack()
        # TODO: pack models frame
        buttonFrame.pack()
    
    def populate(self, name: str = None):
        self.prevName = name
        if name is None: # new unit
            self.name.set('')
            self.cost.set(0)
        else: # loading unit from DB
            unit = self.model.readUnit(name) # TODO: handle error - failure to retrieve unit (readUnit returns None)
            self.name.set(unit.name)
            self.cost.set(unit.cost)
    
    def saveUnit(self):
        unit = Unit(self.name.get(), self.cost.get())
        if unit.name == None:
            return

        if unit not in self.model.listUnits():
            if self.prevName is None:
                self.model.createUnit(unit)
                # TODO: assign models to the unit
            else:
                self.model.updateUnit(self.prevName, unit)
                # TODO: assign/unassign models to the unit
        elif unit.name == self.prevName:
            self.model.updateUnit(self.prevName, unit)
            # TODO: assign/unassign models to the unit
    
    def hide(self):
        # TODO: pack_forget() self
        pass

    def show(self):
        pass
        



    


# Main frame
class View(ttk.Frame):
    def __init__(self, master, model: Database = None, **kw):
        super().__init__(master, **kw)
        self.model = model

        unitList = UnitList(self, model) # Testing
        unitEditor = UnitEditor(self, model)

        unitList.pack()

        # TODO: add notebook component for navigation
    


    
    
