from Weapon import Weapon
from Model import Model
from Core import Outcome
import scipy.stats as stats

# Basic damage calculation
wpn = Weapon(1,4,5,0,1)
mdl = Model(3,4,1)

def calcAttacks():
    # Defaults to degenerate distribution, but may be different for weapons with variable attack counts
    return stats.randint(1,2)

def calcHits():
    # Binomial Poisson Distribution?
    return

def calcWounds():
    # Binomial Poisson Distribution?
    return

def calcSavesFailed():
    # Binomial Poisson Distribution?
    return

def calcDamage():
    # probability mass function(s)?
    return

print(calcAttacks().stats())