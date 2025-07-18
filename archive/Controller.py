from archive.Model import Unit, Model, Database

"""
The controller is responsible for:
    - Receiving user input and interpreting it
    - Updating the Model based on user actions (using CRUD operations)
    - Selecting and displaying the appropriate View
"""

class Controller:
    def __init__(self, model: Database = None, view = None):
        self.model = model
        self.view = view
    
    def units(self):
        if self.model is None:
            return {}
        
        unitList = {}
        for row in self.model.listUnits():
            unitList[row[0]] = row
        
        return unitList
    
    def populateUnitEditor(self, unitName: str = None):
        if self.view is None:
            return
        editor = self.view.unitEditor

        if self.model is None:
            print('Error: Model is None')
            return
        
        if unitName == None:
            editor.name.set('')
            editor.cost.set(0)
            editor.prevName = None
        else:
            unit = self.model.readUnit(unitName)
            if unit is None:
                print('Error: could not retrieve unit')
                return
            
            editor.name.set(unit.name)
            editor.cost.set(unit.cost)
            editor.prevName = unit.name
    
    # TODO: method for opening the unit editor over all other frames

    def saveUnit(self):
        editor = self.view.unitEditor

        unit = Unit(editor.name.get(), editor.cost.get())

        # TODO: handle failure where new name is already taken

        if editor.prevName == None: # save new model
            self.model.createUnit(unit)
        else:
            # TODO: handle case where new name != old name and new name is taken:
            self.model.updateUnit(editor.prevName, unit)

        # TODO: popup on saving

            


    # TODO: method for closing unit editor

        





