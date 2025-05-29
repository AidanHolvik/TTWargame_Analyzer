from scipy import stats

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
        if type(self.a) == int: # constant attacks number
            self.dist = stats.randint(self.a, self.a + 1)
        else:
            # Interpret string to get number of dice and number of faces on dice
            return
        # TODO: if self.attacks is int, use scipy randint with only one possible outcome
        # TODO: else if self.attacks is str, use scipy randint with outcomes 1-6 or 1-3
        return 
    
    def hits(self, attacks, modifier):
        # use scale parameter to shift distribution by modifier
        return 
    