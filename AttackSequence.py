import numpy as np
from numpy import ndarray as array
from scipy.fft import rfft, irfft, next_fast_len
from abc import ABC, abstractmethod
from typing import overload

# Classes for representing a Markov tree
class AbstractNode(ABC):
    @abstractmethod
    @overload
    def __init__(self, damage:int):
        self.min = damage
        self.max = damage

    @abstractmethod
    @overload
    def __init__(self, damage:tuple[int,int,int]):
        self.min = damage[0] + damage[2]                # min = num_dice + modifier
        self.max = damage[0] * damage[1] + damage[2]    # max = num_dice * num_sides + modifier

    @abstractmethod
    def dfs(self, probability:float) -> array:
        pass


# TODO: represent probabilities as integers to avoid issues with fft?
class Node(AbstractNode):
    @overload
    def __init__(self, damage:int):
        super().__init__(damage)
        self.children = []  # array of 2-tuples of type (Node, float)
    
    @overload
    def __init__(self, damage:tuple[int,int,int]):
        super().__init__(damage)
        self.children = []
    
    def add_child(self, new_child:AbstractNode, probability:float):
        self.children.append((new_child, probability))
    
    def dfs(self, probability:float) -> array:
        damage = np.zeros(self.fft_size)
        for node, success_chance in self.children:
            damage += node.dfs(probability * success_chance)
            if isinstance(node, DamageNode):
                damage += node.complement(probability * (1 - success_chance))

# TODO: represent probabilities as integers to avoid issues with fft?
class DamageNode(AbstractNode):
    @overload
    def __init__(self, damage:int):
        super().__init__(damage)
        self.raw_pmf = np.zeros(self.max + 1)
        self.raw_pmf[damage] = 1

    @overload
    def __init__(self, damage:tuple[int,int,int]):
        super().__init__(damage)
        
        # Calculate distribution assuming all other rolls succeed
        fft_size = next_fast_len(self.max + 1, real=True)
        self.raw_pmf = np.zeros(fft_size)
        for i in range(1, num_sides+1):
            self.raw_pmf[i] = 1
        
        cf = rfft(self.raw_pmf, n=fft_size)
        cf **= num_dice
        self.raw_pmf = irfft(cf, n=fft_size)
        self.raw_pmf = np.round(self.raw_pmf)

        self.raw_pmf = self.raw_pmf[:self.max + 1]
        self.raw_pmf /= num_sides**num_dice

    
    def dfs(self, probability:float) -> array:
        damage = np.zeros_like(self.raw_pmf)
        for i in range(self.min, self.max + 1):
            damage[i] = probability * self.raw_pmf[i]
        return damage
    
    def complement(self, probability) -> array:
        damage = np.zeros_like(self.raw_pmf)
        damage[0] = probability * self.raw_pmf[0]
        return damage


""" Main """
weapon = {
    'attacks': 1,                       # int | tuple[int,int,int]
    'skill': 4,                         # int
    'strength': 5,                      # int
    'ap': 0,                            # int
    'damage': 1,                        # int | tuple[int,int,int]
    'keywords': [('rapid fire', 1)]     # list[str | tuple[str,int]]
}
defender = {
    'toughness': 3,
    'save': 4
}



# Process attacks value into a binomial distribution
if isinstance(weapon['attacks'], int):
    output_size = weapon['attacks'] + 1
    attacks = np.zeros(output_size)
    attacks[weapon['attacks']] = 1.0
else:
    num_dice = weapon['attacks'][0]
    num_sides = weapon['attacks'][1]
    modifier = weapon['attacks'][2]
    output_size = (num_dice * num_sides) + modifier + 1
    fft_size = next_fast_len(output_size, real=True)

    pmf = np.zeros(fft_size)
    for i in range(1, num_sides + 1):
        pmf[i] = 1
    
    cf = rfft(pmf, n=fft_size)
    cf **= num_dice
    pmf = irfft(cf, n=fft_size)
    pmf = np.round(pmf)             # round to avoid issues with floats

    # Apply modifier to values of possible outcomes
    if modifier > 0:
        for i in range(num_sides * num_dice, 0, -1):
            pmf[i + modifier] = pmf[i]
            pmf[i] = 0
    elif modifier < 0:
        for i in range(num_dice, num_sides * num_dice + 1):
            pmf[i + modifier] = pmf[i]
            pmf[i] = 0

    pmf = pmf[:output_size]     # trim trailing zeroes
    pmf /= num_sides ** num_dice    # normalize to a total probability of 1
    attacks = pmf



# Get distribution of damage for an individual attack
root = Node(weapon['damage'])

hit_roll = Node(weapon['damage'])
probability = (7 - weapon['skill']) / 6
# TODO: Consider rerolls
root.add_child(hit_roll, probability)
# TODO: consider keywords, etc.

wound_roll = Node(weapon['damage'])
if weapon['strength'] >= 2 * defender['toughness']:
    probability = 5/6
elif weapon['strength'] > defender['toughness']:
    probability = 4/6
elif 2 * weapon['strength'] <= defender['toughness']:
    probability = 1/6
elif weapon['strength'] < defender['toughness']:
    probability = 2/6
else:
    probability = 3/6
# TODO: consider rerolls

hit_roll.add_child(wound_roll, probability)
# TODO: consider keywords, etc.

save_roll = Node(weapon['damage'])
probability = (defender['save'] + weapon['ap'] - 1) / 6
wound_roll.add_child(save_roll, probability)
# TODO: consider rerolls, keywords, etc.

damage_roll = DamageNode(weapon['damage'])
save_roll.add_child(damage_roll)
# TODO: Consider keywords, rerolls, etc.

damage = root.dfs(1.0)

# TODO: rescale damage to fit max total damage
# TODO: calculate mixture distribution to get total damage

# NOTE: the final distribution is a mixture distribution? of the damage distributions across all possible numbers of attacks
"""
    final_distribution = np.zeros(0 to max damage)
    For each possible # of attacks n:
        damage_conv = convolution of n copies of the damage array (can treat damage_conv as an accumulator to improve efficiency)
        final_distribution += damage_conv * attacks[n]
    
    This should give the final distribution of damage in O(nmlog(m)) time for n possible numbers of attacks and a maximum damage per attack of m
"""
if attacks.size == 0:           # if there are 0 attacks, there is a 100% chance of dealing 0 damage
    final_damage = np.ones(1)
else:
    max_damage = (attacks.size - 1) * (damage.size - 1)
    fft_size = next_fast_len(max_damage + 1, real=True)
    final_damage = np.zeros(fft_size)

    # TODO: resize damage distribution to fit max total damage then get its CF
    # TODO: accumulator = damage CF

    """TODO:
        for each index i>0 in attacks:
            if attacks[i] > 0:
                final_damage += accumulator * attacks[i]
                accumulator
            

    """
    final_damage = final_damage[0:max_damage+1]  # trim trailing zeroes





class AttackSequence():
    def __init__(self, weapon:dict, defender:dict):
        self.root = Node()
        self.weapon = weapon
        self.defender = defender
        self.attacks = None
        self.damage_roll = None
        # TODO: Set attacks distribution using fft
    
    # TODO: construct Markov chain from weapon/defender stats
    def construct_chain(self):
        hit = Node() # node for successful hit roll
        prob = (7 - self.weapon['skill']) / 6
        # TODO: consider rerolls, etc.
        self.root.add_child(hit, prob)

        wound = Node() # node for successful wound roll
        # TODO: Set prob based on weapon['strength'] and defender['toughness']
        hit.add_child(wound, prob)

        failed_save = Node() # Node for failed save roll
        # TODO: Set prob based on defender['save'] and weapon['ap']
        wound.add_child(failed_save, prob)

        # TODO: process weapon['damage'] into num_dice, num_sides, and modifier
        damage = DamageNode(self.weapon['damage'])
        failed_save.add_child(damage, prob)
        


    # Perform dfs on the markov chain to determine damage per attack
    def calculate_damage(self):
        self.root.dfs(1.0)

    # use fft to convolve attacks with damage_roll to get distribution of total damage
    def final_distribution(self):
        pass
    
    