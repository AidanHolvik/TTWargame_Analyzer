from enum import Enum

class Side(Enum):
    GREATER = 1
    LESSER = -1

class Distribution:
    def __init__(self):
        self.outcomes = dict()
    
    def identity(self):
        self.outcomes = {}
        self.addOutcome(0,1)

        return self

    def addOutcome(self, value, quantity = 1):
        if value in self.keys():
            self.outcomes[str(value)] += quantity
        else:
            self.outcomes[str(value)] = quantity
        
        return self
    
    def keys(self):
        strKeys = self.outcomes.keys()
        intKeys = set()
        for key in strKeys:
            intKeys.add(int(key))
        
        return sorted(intKeys)
    
    def __imul__(self, mult):
        for key in self.keys():
            self[key] *= mult
        return self

    def __getitem__(self, index):
        return self.outcomes[str(index)]
        
    def __str__(self):
        output = ''
        for key in self.keys():
            output += str(key) + ' '
            if key < 10:
                output += ' '
            for i in range(self[key]):
                output += '|'
            output += f' {self[key]}\n'
        return output
    
    def __iter__(self):
        return iter(self.outcomes)
    
    def __next__(self):
        return next(self.outcomes)
    
    def rollSum(self, numDice: int = 1, numSides: int = 6):
        if numDice > 0:
            self.rollSum(numDice - 1, numSides) # recursive call
            newDist = {}
            for currSum in self.keys():
                for i in range(1, numSides + 1):
                    if str(currSum + i) in newDist.keys():
                        newDist[str(currSum + i)] += self[currSum]
                    else:
                        newDist[str(currSum + i)] = self[currSum]
            self.outcomes = newDist
        
        return self
    
    def rollThreshold(self, threshold: int, side: Side = Side.GREATER, passOn6: bool = False, failOn1: bool = False):
        numFailed = 0
        # roll 1d6 on self.outcomes, fail (and purge?) any values on the wrong side of n (by default, >= n succeeds)
        # if value * side < threshold * side: roll fails

        newDist = {}
        for prevRoll in self.keys():
            for i in range(1, 7):
                if (i * side.value < threshold * side.value or (failOn1 and i == 1)) and not (passOn6 and i == 6): # if roll fails, count failures
                    numFailed += self[prevRoll]
                else: # if roll succeeds add aoutcome to new distribution
                    if str(i) in newDist.keys():
                        newDist[str(i)] += self[prevRoll]
                    else:
                        newDist[str(i)] = self[prevRoll]
        
        self.outcomes = newDist
        return numFailed
    
    def totalOutcomes(self):
        total = 0
        for key in self.keys():
            total += self[key]
        
        return total
    



        

