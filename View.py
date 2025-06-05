import tkinter as tk
from tkinter import ttk

# Define root app class
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.pages = ttk.Notebook(self)
        self.pages.pack(fill='both', expand=True)
        
        frame = unitManagerFrame(self.pages, width=400, height=280)
        frame.pack(fill='both', expand=True)
        self.pages.add(frame, text='Units')

        frame = weaponManagerFrame(self.pages, width=400, height=280)
        frame.pack(fill='both', expand=True)
        self.pages.add(frame, text='Weapons')

        frame = analyzerFrame(self.pages, width=400, height=280)
        frame.pack(fill='both', expand=True)
        self.pages.add(frame, text='Analyze')


# TODO: Class for weapon editor
# TODO: Class for model editor
# TODO: Class for unit editor

# TODO: Class for weapon list
class weaponManagerFrame(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        testMsg = ttk.Label(self, text='TODO: Weapon Manager Frame')

        # TODO: scrollable list of weapon profiles (treeview)
        # TODO: 'new' button
        # TODO: 'edit' button
        # TODO: 'remove' button (with confirmation popup)
        # TODO: toast messages for successfully adding/editing/removing items from the list

        testMsg.pack()

# TODO: class for weapon profile editor

# TODO: Class for unit list
class unitManagerFrame(ttk.Frame):
    def __init__(self, master, **kw):
        super().__init__(master, **kw)
        testMsg = ttk.Label(self, text='TODO: Unit Manager Frame')
        testMsg.pack()


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