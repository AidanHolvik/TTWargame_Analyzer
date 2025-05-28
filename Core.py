from enum import Enum

class Side(Enum):
    GREATER = 1
    LESSER = -1

# class Outcome:
#     def __init__(self):
#         self.value = 0
#         self.quantity = 0

#     def __init__(self, value, quantity: int):
#         self.value = value
#         self.quantity = quantity
    
#     def __lt__(self, that):
#         return self.value < that.value
    
#     def __le__(self, that):
#         return self.value <= that.value
    
#     def __eq__(self, that):
#         return self.value == that.value
    
#     def __add__(self, that):
#         result = Outcome(self.value, self.quantity + that.quantity)
#         return result
    
#     def __iadd__(self, that):
#         self.quantity += that.quantity
#         return self
    
#     def __str__(self):
#         return f'({self.value}:{self.quantity})'

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
        
        return intKeys
    
    def __imul__(self, mult):
        for key in self.keys():
            self[key] *= mult
        return self

    def __getitem__(self, index):
        return self.outcomes[str(index)]
        
    def __str__(self):
        return str(self.outcomes)
    
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
    
    def threshold(self, threshold: int, side: Side = Side.GREATER):
        numFailed = 0
        # look at self.outcomes, fail (and purge?) any values on the wrong side of n (by default, >= n succeeds)
        # if value * side < threshold * side: roll fails

        # How to indicate failed rolls? (maybe use string keys in self.outcomes?)
        
        return numFailed
    
    def totalOutcomes(self):
        total = 0
        for key in self.keys():
            total += self[key]
        
        return total
    



        

