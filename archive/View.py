import tkinter as tk
from tkinter import ttk
from archive.Model import Database, Model, Unit
from abc import ABC, abstractmethod


"""
The view is responsible for:
    - Rendering data to the user in a specific format
    - Displaying the user interface elements
    - Updating the display when the Model changes
"""

class Window(ttk.Frame, ABC):
    def __init__(self, master: ttk.Frame, parentWindow: str, db: Database, **kw):
        super().__init__(master, **kw)
        self.master = master
        self.parent = parentWindow
        self.db = db
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
        repr = f'{self.type}(self.master, \'{self.parent}\', self.master.db'
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
    def __init__(self, master: ttk.Frame, parentWindow: str, db: Database, **kw):
        super().__init__(master, parentWindow, db, **kw)

        self.unitList = tk.Variable(self, [], 'unitNames')
        self.refreshUnitList()

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
        if self.db is not None:
            for unit in self.db.listUnits():
                self.unitNames.append(unit.name)
        self.unitList.set(self.unitNames)

    def btnCmdNew(self):
        editor = UnitEditor(self.master, self.__repr__(), self.db)
        editor.populate()
        self.goTo(editor)
    
    def btnCmdEdit(self):
        editor = UnitEditor(self.master, self.__repr__(), self.db)
        editor.populate(self.unitNames[self.listBox.curselection()[0]])
        self.goTo(editor)
    
    def btnCmdDelete(self):
        # TODO: delete assigned models
        self.db.deleteUnit(self.unitNames[self.listBox.curselection()[0]])
        self.refreshUnitList()


    
class UnitEditor(Window):
    def __init__(self, master: UnitList, parentWindow: str, db: Database, **kw):
        super().__init__(master, parentWindow, db, **kw)
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

        modelList = ModelList(self, self.db, self.prevName)

        # Buttons
        buttonFrame = ttk.Frame(self)
        cancelButton = ttk.Button(buttonFrame, text='Cancel', command=self.close)
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
            unit = self.db.readUnit(name) # TODO: handle error - failure to retrieve unit (readUnit returns None)
            self.name.set(unit.name)
            self.cost.set(unit.cost)
    
    def btnCmdSave(self):
        unit = Unit(self.name.get(), self.cost.get())
        if unit.name == None or unit.name.strip() == '':
            return

        if unit not in self.db.listUnits():
            if self.prevName is None:
                self.db.createUnit(unit)
                # TODO: assign models to the unit
            else:
                self.db.updateUnit(self.prevName, unit)
                # TODO: assign/unassign models to the unit
        elif unit.name == self.prevName:
            self.db.updateUnit(self.prevName, unit)
            # TODO: assign/unassign models to the unit
        
        # TODO: if saving fails, display popup message instead of closing the window
        self.close()
    
    
class ModelList(ttk.Frame):
    def __init__(self, master, db: Database, unit: str, **kw):
        super().__init__(master, **kw)
        self.master = master # master should be a unit editor
        self.db = db
        self.unit = unit
        
        self.modelList = tk.Variable(self, [], 'modelNames')
        self.refreshModelList()

        # on left: list of models for the specified unit
        listFrame = ttk.Frame(self)
        self.listBox = tk.Listbox(listFrame, listvariable=self.modelList)
        scrollbar = ttk.Scrollbar(listFrame, orient=tk.VERTICAL, command=self.listBox.yview)
        self.listBox['yscrollcommand'] = scrollbar.set

        self.listBox.pack(side=tk.LEFT)
        scrollbar.pack(side=tk.LEFT)

        # on right: buttons for managing models for the specified unit
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
        return 'ModelList'

    def refreshModelList(self):
        self.modelNames = []
        if self.db is not None:
            for model in self.db.listModels(self.unit):
                self.modelNames.append(model.name)
        self.modelList.set(self.modelNames)

    def btnCmdNew(self):
        editor = ModelEditor(self.master.master, self.__repr__(), self.db)
        editor.populate(self.unit)
        self.master.goTo(editor)
        pass
    
    def btnCmdEdit(self):
        # editor = ModelEditor(self.master, self.__repr__(), self.db)
        # editor.populate(self.unitNames[self.listBox.curselection()[0]])
        # self.goTo(editor)
        pass
    
    def btnCmdDelete(self):
        # TODO: delete assigned models
        self.db.deleteModel(self.unitNames[self.listBox.curselection()[0]])
        # self.refreshUnitList()
        pass


class ModelEditor(Window):
    def __init__(self, master: ModelList, parentWindow, db, **kw):
        super().__init__(master, parentWindow, db, **kw)
        self.unit = None
        self.prevName = None

        # TK vars for model data
        self.name = tk.StringVar(self, name='modelName')
        self.quantity = tk.IntVar(self, name='modelQuantity')
        self.toughness = tk.IntVar(self, name='modelToughness')
        self.save = tk.IntVar(self, name='modelSave')
        self.health = tk.IntVar(self, name='modelHealth')
        self.invuln = tk.IntVar(self, name='modelInvuln')
        self.isLeader = tk.BooleanVar(self, name='modelIsLeader')
        self.enabled = tk.BooleanVar(self, name='modelEnabled')

        # name frame
        nameFrame = ttk.Frame(self)
        nameLabel = ttk.Label(nameFrame, text='Name')
        nameField = ttk.Entry(nameFrame, textvariable=self.name)
        nameLabel.pack(side=tk.LEFT)
        nameField.pack(side=tk.LEFT)

        # Unit-related Frame
        unitFrame = ttk.Frame(self)
        qtyLabel = ttk.Label(unitFrame, text='Quantity')
        qtyField = ttk.Spinbox(unitFrame, from_=1, to=20, textvariable=self.quantity)
        # leaderLabel = ttk.Label(unitFrame, text='Leader')
        leaderField = ttk.Checkbutton(unitFrame, text='Leader', variable=self.isLeader)
        # enabledLabel = ttk.Label(unitFrame, text='Enabled')
        enabledField = ttk.Checkbutton(unitFrame, text='Enabled', variable=self.enabled)

        qtyLabel.pack(side=tk.LEFT)
        qtyField.pack(side=tk.LEFT)
        leaderField.pack(side=tk.LEFT)
        enabledField.pack(side=tk.LEFT)

        # Stats frame
        statFrame = ttk.Frame(self)
        toughnessLabel = ttk.Label(statFrame, text='T')
        toughnessField = ttk.Spinbox(statFrame, from_=1, to=99, textvariable=self.toughness)
        saveLabel = ttk.Label(statFrame, text='SV')
        saveField = ttk.Spinbox(statFrame, from_=2, to=7, textvariable=self.save)
        healthLabel = ttk.Label(statFrame, text='W')
        healthField = ttk.Spinbox(statFrame, from_=1, to=99, textvariable=self.health)
        invulnLabel = ttk.Label(statFrame, text='Invuln')
        invulnField = ttk.Spinbox(statFrame, from_=2, to=7, textvariable=self.invuln)

        toughnessLabel.grid(row=0, column=0)
        toughnessField.grid(row=1, column=0)

        saveLabel.grid(row=0, column=1)
        saveField.grid(row=1, column=1)

        healthLabel.grid(row=0, column=2)
        healthField.grid(row=1, column=2)

        invulnLabel.grid(row=2, column=0)
        invulnField.grid(row=2, column=1)


        # TODO: add weapon list
        weaponFrame = ttk.Frame(self)

        # Buttons
        buttonFrame = ttk.Frame(self)
        cancelButton = ttk.Button(buttonFrame, text='Cancel', command=self.close)
        saveButton = ttk.Button(buttonFrame, text='Save', command=self.btnCmdSave)
        cancelButton.pack(side=tk.LEFT)
        saveButton.pack(side=tk.RIGHT)

        nameFrame.pack()
        unitFrame.pack()
        statFrame.pack()
        weaponFrame.pack()
        buttonFrame.pack()
        

    @property
    def type(self):
        return 'ModelEditor'


    def populate(self, unitName: str, modelName: str = None):
        self.prevName = modelName
        if modelName is None: # new model
            self.name.set('')
            self.quantity.set(1)
            self.toughness.set(1)
            self.save.set(6)
            self.health.set(1)
            self.invuln.set(7)
            self.isLeader.set(False)
            self.enabled.set(True)
            
        else: # loading unit from DB
            model = self.db.readModel(unitName, modelName) # TODO: handle error - failure to retrieve unit (readUnit returns None)
            self.name.set(model.name)
            self.quantity.set(model.quantity)
            self.toughness.set(model.toughness)
            self.save.set(model.save)
            self.health.set(model.health)
            self.invuln.set(model.invuln)
            self.isLeader.set(model.isLeader)
            self.enabled.set(model.enabled)

    def btnCmdSave(self):
        model = Model(self.unit, self.name.get(), self.quantity.get(), self.toughness.get(), self.save.get(), self.health.get(), self.invuln.get(), self.isLeader.get(), self.enabled.get())
        
        if model.name == None or model.name.strip() == '':
            return
        
        if model not in self.db.listModels(model.unit):
            if self.prevName is None:
                self.db.createModel(model)
                # TODO: assign weapons to the model
            else:
                self.db.updateModel(self.unit, self.prevName, model)
                # TODO: assign/unassign weapons to the model
        elif model.name == self.prevName:
            self.db.updateModel(self.unit, self.prevName, model)
                # TODO: assign/unassign weapons to the model
        
        self.close()





# Main frame
class View(ttk.Frame):
    def __init__(self, master, db: Database = None, **kw):
        super().__init__(master, **kw)
        self.db = db

        unitList = UnitList(self, None, db)
        unitList.open()

        # TODO: add notebook component for navigation
    


    
    
