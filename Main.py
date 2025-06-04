from Weapon import Weapon
from Model import Model
from Core import intDict, rollSum, rollPass
import mvcView as gui


app = gui.App()
try:
    from ctypes import windll
    windll.shcore.SetProcessDpiAwareness(1)
finally:
    app.mainloop()