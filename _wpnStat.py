from abc import ABC, abstractmethod
from _Core import intDict, rollSum

# Interface
class wpnStat(ABC):
    @abstractmethod
    def __init__(self, value):
        pass
    
    @abstractmethod
    def __str__(self):
        pass
    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    def getDist(self):
        pass
    @abstractmethod
    def get(self):
        pass


# Constant int
class constStat(wpnStat):
    def __init__(self, value: int):
        self.dist = intDict()
        self.dist[value] = 1.0
        self.value = value

    def __str__(self):
        return f'{self.value}'

    def __repr__(self):
        return f'constStat({self.value})'
    
    def get(self):
        return self.value
    def getDist(self):
        return self.dist
    
    

# xdy[+z] roll distribution
class rollStat(wpnStat):
    def __init__(self, value: str):
        value = value.lower().strip().split('d')
        self.numDice = int(value[0])

        value = value[1].split('+')
        self.numSides = int(value[0])

        self.shift = 0
        if len(value) > 1:
            self.shift = int(value[1])
        
        self.dist = rollSum(self.numDice, self.numSides).shift(self.shift)
    
    def __str__(self):
        return f'"{self.numDice}d{self.numSides}+{self.shift}"'

    def __repr__(self):
        return f'rollStat("{self.numDice}d{self.numSides}+{self.shift}")'

    def get(self):
        return self.dist
    def getDist(self):
        return self.dist


