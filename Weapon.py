from Core import Distribution

class Weapon:
    def __init__(self):
        self.a = 0
        self.sk = 0
        self.s = 0
        self.ap = 0
        self.d = 0
        self.keywords = []

    def __init__(self, attacks: int | str, skill: int, strength: int, ap: int, damage: int | str):
        self.a = attacks
        self.sk = skill
        self.s = strength
        self.ap = ap
        self.d = damage
        self.keywords = []
    
    def attacks(self):
        attackDist = Distribution()
        attackDist.addOutcome(self.a, 1)
        return attackDist
    
    