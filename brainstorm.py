from Weapon import Weapon
from Model import Model
from Core import Distribution

# Basic damage calculation
wpn = Weapon(1,4,5,0,1)
mdl = Model(3,4,1)

def calcAttacks(wpn: Weapon, mdl: Model):
    return wpn.attacks()

def calcHits(wpn: Weapon, mdl: Model, attacks: Distribution, modifier: int = 0):
    # For each outcome in atkDist, create outcome in hitDist for each possible roll
    return wpn.hits(attacks, modifier)

def calcWounds(wpn: Weapon, mdl: Model, hits: Distribution):
    # For each outcome in hitDist, create outcome in wndDist for each possible roll
    return

def calcSavesFailed(wpn: Weapon, mdl: Model, wounds: Distribution):
    # For each outcome in wndDist, create outcome in svDist for each possible roll
    return

def calcDamage(wpn: Weapon, mdl: Model, failedSaves: Distribution):
    # For each outcome in svDist, create outcome in dmgDist for each possible roll
    return


dist = calcAttacks(wpn, mdl)
print(f'{dist}\n')

dist = calcHits(wpn, mdl, dist)
print(f'{dist}\n')

dist = calcWounds(wpn, mdl, dist)