class Weapon:
    def __init__(self):
        self.attacks = 0
        self.skill = 0
        self.strength = 0
        self.ap = 0
        self.damage = 0
        self.keywords = []

    def __init__(self, attacks, skill, strength, ap, damage):
        self.attacks = attacks
        self.skill = skill
        self.strength = strength
        self.ap = ap
        self.damage = damage
        self.keywords = []
    
    