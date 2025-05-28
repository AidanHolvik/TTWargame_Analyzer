from Core import Distribution, Side

class Weapon:
    def __init__(self):
        self.a = 0
        self.sk = 0
        self.s = 0
        self.ap = 0
        self.d = 0
        self.keywords = []

    def __init__(self, attacks, skill: int, strength: int, ap: int, damage):
        self.a = attacks
        self.sk = skill
        self.s = strength
        self.ap = ap
        self.d = damage
        self.keywords = []
    
    def attacks(self):
        # TODO: if self.attacks is int, use 
        # TODO: else if self.attacks is str, use scipy randint
        return 
    
    def hits(self, attacks, modifier):

        return 