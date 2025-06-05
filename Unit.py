from Model import Model

class ModelGroup():
    def __init__(self, mdl: Model, quantity: int = 1, isLeader: bool = False):
        self.qty = quantity # number of models in the group
        self.mdl = mdl # the model type of this group
        self.isLeader = isLeader

class Unit():
    def __init__(self):
        self.name = 'UNIT_NAME_PLACEHOLDER' # name of the unit
        self.cost = 0 # points cost
        self.modelGroups = [] # the model groups the unit is composed of