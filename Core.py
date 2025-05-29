from math import factorial

class intDict():
    def __init__(self):
        self.values = {}
    
    def keys(self):
        strKeys = self.values.keys()
        intKeys = set()
        for key in strKeys:
            intKeys.add(int(key))
        
        return sorted(intKeys)
    
    def __getitem__(self, index: int):
        if index in self.keys():
            return self.values[str(index)]
        else:
            return 0.0
    
    def __setitem__(self, index: int, value: int):
        self.values[str(index)] = value
    
    def __delitem__(self, index: int):
        del self.values[str(index)]
    
    def __str__(self):
        return str(self.values)
    
    def __iter__(self):
        return iter(self.values)
    
    def __next__(self):
        return next(self.values)
    
    def __add__(self, that):
        for key in that.keys():
            self[key] += that[key]

    
    def visualize(self):
        output = ''
        for i in self.keys():
            output += f'{i} '
            if i < 10:
                output += ' '
            for j in range(int(self[i] * 100)):
                output += '|'
            output += f' {self[i]*100:.2f}%\n'
        
        return output


def rollSum(numDice: int, numSides: int):
    if numDice < 0:
        return None
    elif numDice == 0:
        # base case
        pmf = intDict()
        pmf[0] = 1.0
        return pmf
    else:
        oldPmf = rollSum(numDice - 1, numSides)
        pmf = intDict()
        # For each sum in pmf
        for currSum in oldPmf.keys():
            # for each side, add to new sum's probability
            for i in range(1,numSides + 1):
                pmf[currSum + i] += oldPmf[currSum] / numSides
        
        return pmf


# Function for probability n rolls succeeding depending on amount of dice being rolled
def rollBinom(diceDist: intDict, passChance: float):
    # diceDist = probabilities for total number of incoming dice to roll

    newDist = intDict()

    # For each possible number of dice to roll:
    for numDice in diceDist.keys():
        # get probability distribution for number of successes (binomial pmf) rolling numDice dice with success chance passChance
        for numSuccesses in range(numDice + 1):
            prob = factorial(numDice) / factorial(numSuccesses)
            prob /= factorial(numDice - numSuccesses)
            prob *= passChance**numSuccesses
            prob *= (1-passChance)**(numDice-numSuccesses)

            newDist[numSuccesses] += prob * diceDist[numDice] # multiply pmf output by probabilities of number of dice, then add to new dist

    return newDist #return probability distribution for total number of successes

