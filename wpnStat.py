from abc import ABC, abstractmethod
from Core import intDict, rollSum

# Interface
class wpnStat(ABC):
    @abstractmethod
    def __init__(self, value):
        pass

    @abstractmethod
    def getDist(self):
        pass
    def get(self):
        pass


# Constant int
class constStat(wpnStat):
    def __init__(self, value: int):
        self.dist = intDict()
        self.dist[value] = 1.0
        self.value = value
    
    def get(self):
        return self.value
    def getDist(self):
        return self.dist
    
    

# xdy[+z] roll distribution
class rollStat(wpnStat):
    def __init__(self, value: str):
        value = value.lower().strip().split('d')
        numDice = int(value[0])

        value = value[1].split('+')
        numSides = int(value[0])

        shift = 0
        if len(value) > 1:
            shift = int(value[1])
        
        self.dist = rollSum(numDice, numSides).shift(shift)
    
    def get(self):
        return self.dist
    def getDist(self):
        return self.dist


