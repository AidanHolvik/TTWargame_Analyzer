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

        self.unitNames = []
        self.unitList = tk.Variable(self, [], 'unitNames')
        self.refreshUnitList()
        self.selectedUnit = ''

        self.rootFrame = ttk.Frame(self)
        self.unitEditor = UnitEditor(self, model)

        # Listbox on left
        listFrame = ttk.Frame(self.rootFrame)
        self.listBox = tk.Listbox(listFrame, listvariable=self.unitList)
        scrollbar = ttk.Scrollbar(listFrame, orient=tk.VERTICAL, command=self.listBox.yview)
        self.listBox['yscrollcommand'] = scrollbar.set

        self.listBox.pack(side=tk.LEFT)
        scrollbar.pack(side=tk.LEFT)

        # buttons frame on right
        buttonFrame = ttk.Frame(self.rootFrame)
        self.btnNew = ttk.Button(buttonFrame, text='New', command=self.btnCmdNew)
        self.btnEdit = ttk.Button(buttonFrame, text='Edit', command=self.btnCmdEdit)
        self.btnDelete = ttk.Button(buttonFrame, text='Delete', command=self.btnCmdDelete)

        self.btnNew.pack()
        self.btnEdit.pack()
        self.btnDelete.pack()

        
        listFrame.pack(side=tk.LEFT)
        buttonFrame.pack(side=tk.LEFT)

        # self.unitEditor.grid(column=0, row=0, padx=5, pady=5, sticky='nsew')
        self.rootFrame.grid(column=0, row=0)
        

        
    
    def refreshUnitList(self):
        self.unitNames = []
        if self.model is not None:
            for unit in self.model.listUnits():
                self.unitNames.append(unit.name)
        self.unitList.set(self.unitNames)
    
    

    def btnCmdNew(self):
        # populate unit editor
        self.unitEditor.populate()
        # Bring unit editor frame to front
        self.rootFrame.grid_forget()
        self.unitEditor.grid(column=0, row=0)
    
    def btnCmdEdit(self):
        # populate unit editor
        self.unitEditor.populate(self.unitNames[self.listBox.curselection()[0]])
        # Bring unit editor frame to front
        self.rootFrame.grid_forget()
        self.unitEditor.grid(column=0, row=0)
    
    def btnCmdDelete(self):
        # TODO: delete assigned models
        self.model.deleteUnit(self.unitNames[self.listBox.curselection()[0]])
        self.refreshUnitList()


    
class UnitEditor(ttk.Frame):
    def __init__(self, master: UnitList, model: Database = None, **kw):
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
        cancelButton = ttk.Button(buttonFrame, text='Cancel', command=self.btnCmdCancel)
        saveButton = ttk.Button(buttonFrame, text='Save', command=self.btnCmdSave)
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
    
    def btnCmdSave(self):
        unit = Unit(self.name.get(), self.cost.get())
        print(unit)
        if unit.name == None or unit.name.strip() == '':
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
        
        self.master.refreshUnitList()
    
    def btnCmdCancel(self):
        self.grid_forget()
        self.master.rootFrame.grid(column=0, row=0)
        



    


# Main frame
class View(ttk.Frame):
    def __init__(self, master, model: Database = None, **kw):
        super().__init__(master, **kw)
        self.model = model

        unitList = UnitList(self, model) # Testing
        unitEditor = UnitEditor(self, model)

        unitList.pack()

        # TODO: add notebook component for navigation
    


    
    
