import tkinter as tk

"""
Each of the following classes is a child class of their respective tk.Var class, used to access objects' member variables as tk variables.
"""

# TODO: bind to object member variable

class StringVar(tk.StringVar):
    def __init__(self, boundMember: str, master=None, name=None):
        super().__init__(master, name=name)
        self.target = boundMember
    
    def set(self, value):
        eval(f'{self.target} = "{value}"')
        return super().set(value)

    def get(self):
        value = eval(self.target)
        if isinstance(value, str):
            return value
        return str(value)




class IntVar(tk.IntVar):
    pass

class BooleanVar(tk.BooleanVar):
    pass

class DoubleVar(tk.DoubleVar):
    pass