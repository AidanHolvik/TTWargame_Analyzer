from mvcModel import *

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
    
    
    