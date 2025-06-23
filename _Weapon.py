from _Core import intDict, rollSum, rollPass
from _Core import rollSumCompounding as compound
from _Model import Model
from _wpnStat import *

from abc import ABC, abstractmethod

class Weapon:
    def __init__(self):
        self.name = 'New Weapon Profile'
        self.atk = constStat(0)
        self.skill = constStat(0)
        self.str = constStat(0)
        self.ap = constStat(0)
        self.dmg = constStat(0)

    def __init__(self, attacks: int|str, skill: int, strength: int|str, ap: int, damage: int|str, name: str = 'New Weapon Profile'):
        self.name = name

        if type(attacks) == int:
            self.atk = constStat(attacks)
        else:
            self.atk = rollStat(attacks)

        self.skill = constStat(skill)

        if type(strength) == int:
            self.str = constStat(strength)
        else:
            self.str = rollStat(strength)

        self.ap = constStat(ap)

        if type(damage) == int:
            self.dmg = constStat(damage)
        else:
            self.dmg = rollStat(damage)
        
    def __repr__(self):
        return f'Weapon({str(self.atk)}, {str(self.skill)}, {str(self.str)}, {str(self.ap)}, {str(self.dmg)}, name = "{self.name}")'
    
    def attacks(self):
        dist = self.atk.getDist()
        # TODO: use strategy patterns to handle keywords/abilities which affect number of attacks (such as rapid-fire)
        return dist
    

    def hits(self, attacks: intDict, rollMod: int = 0):

        # constrain required hit roll to (1,6]
        passRoll = self.skill.get() - rollMod
        if passRoll > 6:
            passRoll = 6
        elif passRoll < 2:
            passRoll = 2

        # Calculate chance of passing each individual hit roll
        hitChance = 7 - passRoll
        hitChance /= 6

        return rollPass(attacks, hitChance) # Return probability distribution of number of successful hits
    
    def wounds(self, mdl: Model, hits: intDict, rollMod: int = 0):
        # compare self.strength to mdl.toughness
        if self.str.get() * 2 <= mdl.toughness: # 6 to pass 
            passRoll = 6
        elif self.str.get() < mdl.toughness: # 5 to pass 
            passRoll = 5
        elif self.str.get() == mdl.toughness: # 4 to pass 
            passRoll = 4
        elif self.str.get() < mdl.toughness * 2: # 3 to pass 
            passRoll = 3
        else: # 2 to pass 
            passRoll = 2
        
        # Constrain required roll to (1,6]
        passRoll -= rollMod
        if passRoll < 2:
            passRoll = 2
        elif passRoll > 6:
            passRoll = 6


        # TODO: add strategy pattern for mdl somewhere around here to handle rules like 'if attacker strength > defender toughness, subtract 1 from wound roll'

        # Calculate chance of passing each individual wound roll
        woundChance = 7 - passRoll
        woundChance /= 6

        return rollPass(hits, woundChance)
    
    def damage(self, mdl: Model, failedSaves: intDict): # TODO: modify to manually compound rolls instead of using a method for it
        damage = intDict()

        for numFailed in failedSaves.keys():
            dmgDist = intDict() # reset compounded dmg probabilities
            dmgDist[0] = 1.0
            for i in range(numFailed): # Compound damage probabilities
                dmgDist = dmgDist.compound(self.dmg.getDist())
            dmgDist = dmgDist * failedSaves[numFailed] # multiply damage distribution for n failed saves by probability of failing n saves
            damage = damage + dmgDist
        
        # TODO: use strategy patterns to handle abilities, keywords, etc. which affect damage
        
        return damage
            
    

