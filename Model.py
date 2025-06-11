from Core import intDict, rollPass
# from Weapon import Weapon

# class weaponGroup():
#     def __init__(self, weapon: Weapon, quantity: int = 1, ):
#         self.wpn = weapon
#         self.qty = quantity

class Model:
    def __init__(self):
        self.name = 'MODEL_NAME_PLACEHOLDER'
        self.toughness = 0
        self.save = 0
        self.invuln = 7 # 7 = no invuln
        self.health = 0
        self.weapons = [] # list of weaponGroups

    def __init__(self, toughness: int, save: int, health: int, invuln: int = 7, name: str = 'MODEL_NAME_PLACEHOLDER'):
        self.name = name
        self.toughness = toughness
        self.save = save
        self.invuln = invuln # 7 = no invuln
        self.health = health

    def failedSaves(self, wounds: intDict, rollMod: int = 0):
        
        # constrain required save roll to (1,7] (7 is an impossible save)
        failRoll = self.save - rollMod
        if failRoll > self.invuln:
            failRoll = self.invuln
        elif failRoll < 2:
            failRoll = 2

        # Calculate chance of failing each individual save roll
        failChance = failRoll - 1
        failChance /= 6

        return rollPass(wounds, failChance) # Return probability distribution of number of successful hits