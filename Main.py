from Weapon import Weapon
from Model import Model
from Core import intDict, rollSum, rollPass


wpn = Weapon('1d6+1',4,14,-3,3)
mdl = Model(3,4,1)

attacks = wpn.attacks()
print('attacks')
print(attacks.visualize())

hits = wpn.hits(attacks)
print('hits')
print(hits.visualize())

wounds = wpn.wounds(mdl, hits)
print('wounds')
print(wounds.visualize())

saves = mdl.failedSaves(wounds, wpn.ap.get())
print('failed saves')
print(saves.visualize())

damage = wpn.damage(mdl, saves)
print('damage')
print(damage.visualize())


# Flow:
# - Calculate modifiers to roll
# - calculate distribution
# - apply any modifiers to outcome (e.x. +1 attack from rapid fire)