

import numpy as np
from scipy.fft import rfft, irfft, next_fast_len


class Node:
    def __init__(self, value: int):
        self.value = value
        self.probability = 0.0
        self.children = {}

    def add_child(self, child_node, probability: float):
        child_node.probability += probability * self.probability
        self.children[child_node.value] = (child_node, probability)
    
    def get_child_probability(self, child_node) -> float:
        if child_node.value in self.children:
            return self.children[child_node.value][1]
        else:
            return 0.0

    def set_child_probability(self, value, probability: float):
        if value in self.children:
            self.children[value][1] = probability
        else:
            raise ValueError("Child node not found in children.")

    def __repr__(self):
        return f"Node(value={self.value})"
    

class Tree:
    def __init__(self):
        self.root = Node('root')
        self.attacks = {}
        self.hits = {}
        self.wounds = {}
        self.failed_saves = {}
        self.damage = {}

    def calc_attacks(self, num_attacks: int):
        new_node = Node(num_attacks)
        self.root.add_child(new_node, 1.0)
        self.attacks[num_attacks] = new_node
    
    def calc_attacks(self, num_dice: int, num_sides: float):
        # use FFT to calculate the distribution of results from rolling num_dice dice with num_sides sides

        output_size = num_dice * num_sides - (num_dice - 1)
        fft_size = next_fast_len(output_size, real=True)

        pmf = np.zeros(fft_size)
        for i in range(0, num_sides):
            pmf[i] = 1

        # Compute the PMF of the sum of the dice using FFT
        cf = rfft(pmf, n=fft_size)
        cf **= num_dice  # Raise the characteristic function to the power of num_dice to model the sum of the dice
        pmf = irfft(cf, n=fft_size)
        pmf = np.round(pmf)  # Round to avoid floating-point issues

        # normalize and format the PMF
        total_outcomes = num_sides**num_dice

        pmf = pmf[:output_size]  # Trim to valid range
        pmf = (pmf / total_outcomes)  # Normalize to get probabilities

        # Create child nodes for each possible outcome of the attack rolls
        for i in range (num_dice, num_dice * num_sides + 1):
            if (pmf[i] > 0):
                new_node = Node(i)
                self.root.add_child(new_node, pmf[i])
                self.attacks[i] = new_node
        
    def calc_hits(self, hit_chance: float):     # TODO: add in modifiers, rerolls, etc.
        for attack_node in self.attacks.values():
            for i in range(0, attack_node.value + 1):
                

