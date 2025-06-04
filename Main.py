import tkinter as tk
from tkinter import ttk
from Weapon import Weapon
from Model import Model
from Core import intDict, rollSum, rollPass


# Define GUI
root = tk.Tk()

# message = tk.Label(root, text='Hello World')
# message.pack()

# Keep the window from instantly closing
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    root.mainloop()