from Core import intDict, rollSum, rollBinom

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
            dist = intDict()
            dist[self.a] = 1.0
        elif type(self.a) == str: # roll for number of attacks
            dice = self.a.strip().split('d') # must be of the format xdy
            dist = rollSum(int(dice[0]), int(dice[1]))

        return dist
    
    def hits(self, attacks: intDict, rollMod: int = 0):

        # Calculate chance of hit based on self.sk and rollMod
        hitChance = (7 - self.sk) + rollMod
        if hitChance > 5:
            hitChance = 5
        elif hitChance < 1:
            hitChance = 1
        hitChance /= 6

        return rollBinom(attacks, hitChance) # Return probability distribution of number of successful hits
    