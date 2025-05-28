from Core import Distribution, Side

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
        # TODO: if self.attacks is int, add single outcome
        # TODO: else if self.attacks is str, generate distribution
        attackDist = Distribution()
        attackDist.addOutcome(self.a, 1)
        return attackDist
    
    def hits(self, attacks: Distribution, modifier: int = 0):
        failed = attacks.rollThreshold(self.sk + modifier, Side.GREATER, passOn6=True, failOn1=True)

        output = 'F  '
        for i in range(failed):
            output += '|'
        output += f' {failed}'
        print(output)

        return attacks