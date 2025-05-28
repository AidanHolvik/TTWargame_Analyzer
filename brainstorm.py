from Weapon import Weapon
from Model import Model
from Core import Distribution

# Basic damage calculation
wpn = Weapon(1,4,5,0,1)
mdl = Model(3,4,1)

def calcAttacks(wpn: Weapon, mdl: Model):
    return wpn.attacks()

def calcHits(attacks: Distribution):
    # For each outcome in atkDist, create outcome in hitDist for each possible roll
    return

def calcWounds(hits: Distribution):
    # For each outcome in hitDist, create outcome in wndDist for each possible roll
    return

def calcSavesFailed(wounds: Distribution):
    # For each outcome in wndDist, create outcome in svDist for each possible roll
    return

def calcDamage(failedSaves: Distribution):
    # For each outcome in svDist, create outcome in dmgDist for each possible roll
    return

