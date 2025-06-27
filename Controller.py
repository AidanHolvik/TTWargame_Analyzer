from Model import Unit, Model, Database

"""
The controller is responsible for:
    - Receiving user input and interpreting it
    - Updating the Model based on user actions (using CRUD operations)
    - Selecting and displaying the appropriate View
"""

class Controller:
    def __init__(self, model, view):
        self.model = model
        self.view = view



