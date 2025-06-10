import tkinter as tk
from tkinter import ttk

# Define root app class
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.geometry('400x400')
        self.title('TTWG Analyzer')

        self.pages = ttk.Notebook(self)
        self.pages.pack(fill='both', expand=True)
        
        frame = unitManagerFrame(self.pages, width=400, height=280)
        frame.pack(expand=True)
        self.pages.add(frame, text='Units')

        frame = analyzerFrame(self.pages, width=400, height=280)
        frame.pack(expand=True)
        self.pages.add(frame, text='Analyze')


# TODO: Class for weapon editor
# TODO: Class for model editor
# TODO: Class for unit editor



# TODO: Class for unit list
class unitManagerFrame(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)

        self.units = [] # list of unit names as strings

        list_items = tk.Variable(value=self.units) # TODO: populate list from saved units
        unitList = tk.Listbox(self, listvariable=list_items)

        # TODO: button frame
        btnFrame = ttk.Frame(self)
        btnAdd = ttk.Button(btnFrame, text='New Unit')
        btnEdit = ttk.Button(btnFrame, text='Edit Unit')
        btnRemove = ttk.Button(btnFrame, text='Remove Unit')
        # TODO: disable edit/remove buttons when no unit is selected, enable when a unit is selected
        # TODO: add button functionality via event binding

        testMsg = ttk.Label(self, text='TODO: Unit Manager Frame')
        testMsg.pack(side=tk.TOP)
        unitList.pack(side=tk.LEFT, ipadx=20, ipady= 20) # Unit Selection List
        btnFrame.pack(side=tk.LEFT)
        btnAdd.pack()
        btnEdit.pack()
        btnRemove.pack()


# TODO: Class for generating analysis (selecting units, etc.)
class analyzerFrame(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        testMsg = ttk.Label(self, text='TODO: Analysis Frame')
        testMsg.pack()
    

if __name__ == '__main__':
    app = App()
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    finally:
        app.mainloop()