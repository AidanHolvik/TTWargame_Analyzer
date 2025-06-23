import tkinter as tk
from tkinter import ttk
from mvcController import Controller
import mvcModel as Model

# Define root app class
class App(tk.Tk):
    def __init__(self, controller: Controller):
        super().__init__()
        self.controller = Controller('TTWGAnalyzer.db')
        self.geometry('400x400')
        self.title('TTWG Analyzer')

        # TODO: add top menu bar for saving changes, loading database, etc.

        self.pages = ttk.Notebook(self)
        self.pages.pack(fill='both', expand=True)
        
        frame = unitManagerFrame(self.pages, self.controller, width=400, height=280)
        frame.pack(expand=True)
        self.pages.add(frame, text='Units')

        frame = weaponEditor('test', self.controller, self.pages, width=400, height=280)
        frame.pack(expand=True, fill=tk.BOTH)
        self.pages.add(frame, text='Weapons')



# TODO: Class for model editor
# TODO: Class for unit editor


# TODO: custom tkinter variable classes for bound vars


# TODO: Class for unit list
class unitManagerFrame(ttk.Frame):
    def __init__(self, master, controller: Controller, **kw):
        super().__init__(master, **kw)
        self.controller = controller

        print(controller.units)

        list_items = tk.Variable(value=controller.units) # TODO: populate list from saved units
        unitList = tk.Listbox(self, listvariable=list_items)

        # initialize elements
        btnFrame = ttk.Frame(self)
        btnAdd = ttk.Button(btnFrame, text='New Unit')
        btnEdit = ttk.Button(btnFrame, text='Edit Unit')
        btnRemove = ttk.Button(btnFrame, text='Remove Unit')
        
        # TODO: disable edit/remove buttons when no unit is selected, enable when a unit is selected
        # TODO: add button functionality via event binding

        # pack elements
        unitList.pack(side=tk.LEFT, ipadx=20, ipady= 20) # Unit Selection List
        btnFrame.pack(side=tk.LEFT)
        btnAdd.pack()
        btnEdit.pack()
        btnRemove.pack()

# TODO: pass weapon object to weaponEditor to bind its member variables to tk variables?
class weaponEditor(ttk.Frame):
    def __init__(self, weapon: str, controller: Controller, master, **kw):
        super().__init__(master, **kw)
        self.controller = controller

        self.wpnName = tk.StringVar(self, name = 'weapon name')
        self.wpnAttacks = tk.StringVar(self, name = 'weapon attacks')
        self.wpnStrength = tk.IntVar(self, name = 'weapon strength')
        self.wpnAp = tk.IntVar(self, name = 'weapon ap')
        self.wpnDamage = tk.IntVar(self, name = 'weapon damage')

        self.loadWeapon(weapon)


        # Name input
        nameFrame = ttk.Frame(self)
        lblName = ttk.Label(nameFrame, text='Name')
        txtName = ttk.Entry(nameFrame, textvariable=self.wpnName)
        lblName.pack(side=tk.LEFT)
        txtName.pack(side=tk.LEFT)


        # Stat Inputs
        statFrame = ttk.Frame(self)
        lblAttacks = ttk.Label(statFrame, text='A')
        lblStrength = ttk.Label(statFrame, text='S')
        lblAp = ttk.Label(statFrame, text='AP')
        lblDamage = ttk.Label(statFrame, text='D')

        txtAttacks = ttk.Entry(statFrame, textvariable=self.wpnAttacks, width=7)
        spinStrength = ttk.Spinbox(statFrame, from_=1, to=99, wrap=True, textvariable=self.wpnStrength, width=5)
        spinAp = ttk.Spinbox(statFrame, to=9, wrap=True, textvariable=self.wpnAp, width=5)
        txtDamage = ttk.Entry(statFrame, textvariable=self.wpnDamage, width=7)

        statFrame.rowconfigure(0)
        statFrame.rowconfigure(1)
        statFrame.columnconfigure(0)
        statFrame.columnconfigure(1)
        statFrame.columnconfigure(2)
        statFrame.columnconfigure(3)
        lblAttacks.grid(row=0, column=0)
        lblStrength.grid(row=0, column=1)
        lblAp.grid(row=0, column=2)
        lblDamage.grid(row=0, column=3)
        txtAttacks.grid(row=1, column=0, padx=5)
        spinStrength.grid(row=1, column=1, padx=5)
        spinAp.grid(row=1, column=2, padx=5)
        txtDamage.grid(row=1, column=3, padx=5)

        # Buttons
        btnFrame = ttk.Frame(self)
        btnApply = ttk.Button(btnFrame, text='Done', command=self.doSave)
        btnCancel = ttk.Button(btnFrame, text='Cancel', command=self.doCancel)
        btnApply.pack(side=tk.LEFT)
        btnCancel.pack(side=tk.RIGHT)


        nameFrame.pack()
        statFrame.pack(pady=20)
        btnFrame.pack()
    
    def loadWeapon(self, weapon: str):
        self.wpn = self.controller.weapons[weapon]

        self.wpnName.set(self.wpn.name)
        self.wpnAttacks.set(self.wpn.attacks)
        self.wpnStrength.set(self.wpn.strength)
        self.wpnAp.set(self.wpn.ap)
        self.wpnDamage.set(self.wpn.damage)


    def doCancel(self):
        # TODO: revert changes?
        # TODO: close popup frame (self)
        self.destroy()
        pass

    def doSave(self):
        # TODO: if self.wpn.name == self.wpnName: update weapon object
        # TODO: elif self.wpnName not in database: add new weapon (self.wpnName), delete old weapon (self.weapon.name) (renaming weapon and optionally updating stats)
        # TODO: else fail to save, warn user, do not close window 
        pass
        
    
    # method for populating fields from loaded record
    def load(self, weapon: str):
        wpn = self.controller.weapons[weapon]

        self.wpnName.set(wpn.name)
        self.wpnAttacks.set(wpn.attacks)
        self.wpnStrength.set(wpn.strength)
        self.wpnAp.set(wpn.ap)
        self.wpnDamage.set(wpn.damage)
    
    def clear(self):
        self.wpnName.set('')
        self.wpnAttacks.set('1')
        self.wpnStrength.set(1)
        self.wpnAp.set(0)
        self.wpnDamage.set('1')


# TODO: Class for generating analysis (selecting units, etc.)
class analyzerFrame(ttk.Frame):
    def __init__(self, master, controller: Controller, **kw):
        super().__init__(master, **kw)
        testMsg = ttk.Label(self, text='TODO: Analysis Frame')
        testMsg.pack()
    

if __name__ == '__main__':
    controller = Controller('TTWGAnalyzer.db')
    # testWeapon = Model.Weapon('test', 2, 3, 4, 5)
    # testWeapon.saveNew('TTWGAnalyzer.db')
    app = App(controller)
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        app.mainloop()