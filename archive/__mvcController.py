from __mvcModel import *

class Controller():
    def __init__(self, db: str):
        self.db = Database(db)
    
    @property
    def units(self):
        return self.db.units
    @property
    def models(self):
        return self.db.models
    @property
    def weapons(self):
        return self.db.weapons
    @property
    def keywords(self):
        return self.db.keywords
    
    def addWeapon(self, name: str):
        pass
        
    def removeWeapon(self, name: str):
        if name in self.weapons.keys():
            del self.weapons[name]
    
    
    
    