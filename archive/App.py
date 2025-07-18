import tkinter as tk
from archive.Model import Database
from Controller import Controller
from View import View

# Contains root tkinter window, and has an instance of model, view, and controller.
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Tabletop Wargame Analyzer')

        # Create model
        model = Database('test')

        # Create view, place it on main window
        view = View(self, model)
        view.pack()


# Main application loop
if __name__ == '__main__':
    app = App()
    app.mainloop()


