from Weapon import Weapon
from Model import Model
from Core import intDict, rollSum, rollBinom


wpn = Weapon('1d6',4,5,0,1)
mdl = Model(3,4,1)

def calcAttacks(wpn: Weapon, mdl: Model):
    return 

# attacks = rollSum(1,6)
attacks = wpn.attacks()
print(attacks.visualize())

hits = wpn.hits(attacks)
print(hits.visualize())

