from Weapon import Weapon
from Model import Model
from Core import intDict, rollSum, rollBinom


wpn = Weapon(1,4,5,0,1)
mdl = Model(3,4,1)

def calcAttacks(wpn: Weapon, mdl: Model):
    return 

# attacks = rollSum(1,6)
attacks = intDict()
attacks[1] = 1
print(attacks.visualize())

hits = rollBinom(attacks, 3/6)
print(hits.visualize())

