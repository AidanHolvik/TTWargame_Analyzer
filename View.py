import tkinter as tk
from tkinter import ttk
from Model import Database, Model, Unit
from abc import ABC, abstractmethod


"""
The view is responsible for:
    - Rendering data to the user in a specific format
    - Displaying the user interface elements
    - Updating the display when the Model changes
"""

class Window(ttk.Frame, ABC):
    def __init__(self, master: ttk.Frame, parentWindow: str, model: Database, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.parent = parentWindow
        self.model = model
        self.kw = kw
    
    @property
    @abstractmethod
    def type(self):
        pass

    def open(self):
        self.grid(column=0, row=0)

    def hide(self):
        self.grid_forget()

    def goTo(self, destination):
        self.hide()
        destination.open()
        self.destroy
    
    def close(self):
        self.goTo(eval(self.parent))

    def __repr__(self):
        repr = f'{self.type}(self.master, \'{self.parent}\', self.master.model'
        if self.kw is not None:
            for key in self.kw.keys():
                repr += f', {key}='
                if type(self.kw[key]) == str:
                    repr += f'"{self.kw[key]}"'
                else:
                    repr += f'{self.kw[key]}'
        
        repr += ')'
        return repr
    


    


# TODO: unit list (with buttons)
class UnitList(Window):
    def __init__(self, master: ttk.Frame, parentWindow: str, model: Database, **kw):
        super().__init__(master, parentWindow, model, **kw)

        self.unitNames = []
        self.unitList = tk.Variable(self, [], 'unitNames')
        self.refreshUnitList()
        self.selectedUnit = ''

        # Listbox on left
        listFrame = ttk.Frame(self)
        self.listBox = tk.Listbox(listFrame, listvariable=self.unitList)
        scrollbar = ttk.Scrollbar(listFrame, orient=tk.VERTICAL, command=self.listBox.yview)
        self.listBox['yscrollcommand'] = scrollbar.set

        self.listBox.pack(side=tk.LEFT)
        scrollbar.pack(side=tk.LEFT)

        # buttons frame on right
        buttonFrame = ttk.Frame(self)
        self.btnNew = ttk.Button(buttonFrame, text='New', command=self.btnCmdNew)
        self.btnEdit = ttk.Button(buttonFrame, text='Edit', command=self.btnCmdEdit)
        self.btnDelete = ttk.Button(buttonFrame, text='Delete', command=self.btnCmdDelete)

        self.btnNew.pack()
        self.btnEdit.pack()
        self.btnDelete.pack()

        
        listFrame.pack(side=tk.LEFT)
        buttonFrame.pack(side=tk.LEFT)
        
    @property
    def type(self):
        return 'UnitList'

    def refreshUnitList(self):
        self.unitNames = []
        if self.model is not None:
            for unit in self.model.listUnits():
                self.unitNames.append(unit.name)
        self.unitList.set(self.unitNames)

    def btnCmdNew(self):
        editor = UnitEditor(self.master, self.__repr__(), self.model)
        editor.populate()
        self.goTo(editor)
    
    def btnCmdEdit(self):
        editor = UnitEditor(self.master, self.__repr__(), self.model)
        editor.populate(self.unitNames[self.listBox.curselection()[0]])
        self.goTo(editor)
    
    def btnCmdDelete(self):
        # TODO: delete assigned models
        self.model.deleteUnit(self.unitNames[self.listBox.curselection()[0]])
        self.refreshUnitList()


    
class UnitEditor(Window):
    def __init__(self, master: UnitList, parentWindow: str, model: Database, **kw):
        super().__init__(master, parentWindow, model, **kw)
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

        modelList = ModelList(self, self, self.model)

        # Buttons
        buttonFrame = ttk.Frame(self)
        cancelButton = ttk.Button(buttonFrame, text='Cancel', command=self.btnCmdCancel)
        saveButton = ttk.Button(buttonFrame, text='Save', command=self.btnCmdSave)
        cancelButton.pack(side=tk.LEFT)
        saveButton.pack(side=tk.RIGHT)

        # Pack top-level frames
        nameFrame.pack()
        costFrame.pack()
        modelList.pack()
        buttonFrame.pack()
    
    @property
    def type(self):
        return 'UnitEditor'
    
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
        
        # TODO: if saving fails, display popup message instead of closing the window
        self.close()
    
    def btnCmdCancel(self):
        self.close()
        
    
class ModelList(ttk.Frame):
    def __init__(self, master, model: Database, **kw):
        super().__init__(master, **kw)
        self.master = master # master should be a unit editor
        self.model = model
        
        # on left: list of models for the specified unit
        # on right: buttons for managing models for the specified unit


    


# Main frame
class View(ttk.Frame):
    def __init__(self, master, model: Database = None, **kw):
        super().__init__(master, **kw)
        self.model = model

        unitList = UnitList(self, None, model)
        unitList.open()

        # TODO: add notebook component for navigation
    


    
    
