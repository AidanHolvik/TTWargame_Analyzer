import numpy as np
from numpy import ndarray
from scipy.fft import rfft, irfft, next_fast_len
from abc import ABC, abstractmethod


# Classes for representing a Markov tree
class AbstractNode(ABC):
    def __init__(self, damage: int | tuple[int, int, int]):
        if isinstance(damage, int):
            self.min = damage
            self.max = damage
        else:
            self.min = damage[0] + damage[2]  # min = num_dice + modifier
            self.max = (
                damage[0] * damage[1] + damage[2]
            )  # max = num_dice * num_sides + modifier

    @abstractmethod
    def dfs(
        self, probability: float
    ) -> (
        ndarray
    ):  # this class' implementation of dfs should only include debug statements
        pass


class Node(AbstractNode):
    def __init__(self, damage: int | tuple[int, int, int]):
        super().__init__(damage)
        self.children = []  # array of 2-tuples of type (Node, float)

    def add_child(self, new_child: AbstractNode, probability: float):
        self.children.append((new_child, probability))

    def dfs(self, probability: float) -> ndarray:
        super().dfs(probability)
        damage = np.zeros(self.max + 1)
        for node, success_chance in self.children:
            damage += node.dfs(probability * success_chance)

        return damage


class FailureNode(AbstractNode):
    def __init__(self, damage: int | tuple[int, int, int]):
        super().__init__(damage)
        self.child = None

    def dfs(self, probability: float) -> ndarray:
        super().dfs(probability)
        damage = np.zeros(self.max + 1)
        damage += self.child.complement(probability)
        return damage


class DamageNode(AbstractNode):
    def __init__(self, damage: int | tuple[int, int, int]):
        super().__init__(damage)
        if isinstance(damage, int):
            self.raw_pmf = np.zeros(self.max + 1, dtype=float)
            self.raw_pmf[damage] = 1.0
        else:
            num_dice = damage[0]
            num_sides = damage[1]
            modifier = damage[2]
            # Calculate distribution assuming all other rolls succeed
            fft_size = next_fast_len(self.max + 1, real=True)
            self.raw_pmf = np.zeros(fft_size)
            for i in range(1, num_sides + 1):
                self.raw_pmf[i] = 1

            cf = rfft(self.raw_pmf, n=fft_size)
            cf **= num_dice
            self.raw_pmf = irfft(cf, n=fft_size)
            self.raw_pmf = np.round(self.raw_pmf)

            self.raw_pmf = self.raw_pmf[: self.max + 1]
            self.raw_pmf /= num_sides**num_dice

    def dfs(self, probability: float) -> ndarray:
        super().dfs(probability)
        damage = np.zeros_like(self.raw_pmf)
        for i in range(self.min, self.max + 1):
            damage[i] = probability * self.raw_pmf[i]
        return damage

    def complement(self, probability) -> ndarray:
        damage = np.zeros_like(self.raw_pmf)
        damage[0] = probability
        return damage

class MarkovTree:
    def __init__(self, weapon: dict, defender: dict):
        self.core_attacks = weapon["attacks"]