import numpy as np
from numpy import ndarray as array
from scipy.fft import rfft, irfft, next_fast_len
from abc import ABC, abstractmethod


# Classes for representing a Markov tree
class AbstractNode(ABC):
    def __init__(self, damage: int | tuple[int, int, int]):
        if isinstance(damage, int):
            self.min = damage
            self.max = damage
        else:
            self.min = damage[0] + damage[2]                    # min = num_dice + modifier
            self.max = damage[0] * damage[1] + damage[2]        # max = num_dice * num_sides + modifier

    @abstractmethod
    def dfs(self, probability: float) -> array:
        pass


class Node(AbstractNode):
    def __init__(self, damage: int| tuple[int, int, int]):
        super().__init__(damage)
        self.children = []  # array of 2-tuples of type (Node, float)


    def add_child(self, new_child: AbstractNode, probability: float):
        self.children.append((new_child, probability))

    def dfs(self, probability: float) -> array:
        damage = np.zeros(self.max + 1)
        for node, success_chance in self.children:
            damage += node.dfs(probability * success_chance)


class FailureNode(AbstractNode):
    def __init__(self, damage: int | tuple[int, int, int]):
        super().__init__(damage)
        self.child = None

    def dfs(self, probability:float) -> array:
        return self.child.complement(probability)


class DamageNode(AbstractNode):
    def __init__(self, damage: int | tuple[int, int, int]):
        super().__init__(damage)
        if isinstance(damage, int):
            self.raw_pmf = np.zeros(self.max + 1)
            self.raw_pmf[damage] = 1
        else:
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

    def dfs(self, probability: float) -> array:
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
    "attacks": 1,  # int | tuple[int,int,int]
    "skill": 4,  # int
    "strength": 5,  # int
    "ap": 0,  # int
    "damage": 1,  # int | tuple[int,int,int]
    "keywords": [("rapid fire", 1)],  # list[str | tuple[str,int]]
}
defender = {"toughness": 3, "save": 4}


""" v   PMF (number of attacks)   v """
# Process attacks value into a binomial distribution
if isinstance(weapon["attacks"], int):
    output_size = weapon["attacks"] + 1
    attacks = np.zeros(output_size)
    attacks[weapon["attacks"]] = 1.0
else:
    num_dice = weapon["attacks"][0]
    num_sides = weapon["attacks"][1]
    modifier = weapon["attacks"][2]
    output_size = (num_dice * num_sides) + modifier + 1
    fft_size = next_fast_len(output_size, real=True)

    pmf = np.zeros(fft_size)
    for i in range(1, num_sides + 1):
        pmf[i] = 1

    cf = rfft(pmf, n=fft_size)
    cf **= num_dice
    pmf = irfft(cf, n=fft_size)
    pmf = np.round(pmf)  # round to avoid issues with floats

    # Apply modifier to values of possible outcomes
    if modifier > 0:
        for i in range(num_sides * num_dice, 0, -1):
            pmf[i + modifier] = pmf[i]
            pmf[i] = 0
    elif modifier < 0:
        for i in range(num_dice, num_sides * num_dice + 1):
            pmf[i + modifier] = pmf[i]
            pmf[i] = 0

    pmf = pmf[:output_size]  # trim trailing zeroes
    pmf /= num_sides**num_dice  # normalize to a total probability of 1
    attacks = pmf

""" v   PMF (damage per attack)   v """
# Get distribution of damage for an individual attack
hit_roll = Node(weapon["damage"])
wound_roll = Node(weapon["damage"])
save_roll = Node(weapon["damage"])
damage_roll = DamageNode(weapon["damage"])
fail_sequence = FailureNode(weapon["damage"])
fail_sequence.child = damage_roll

probability = (7 - weapon["skill"]) / 6
# TODO: Consider rerolls
hit_roll.add_child(wound_roll, probability)
hit_roll.add_child(fail_sequence, 1.0 - probability)
# TODO: consider keywords, etc.

if weapon["strength"] >= 2 * defender["toughness"]:
    probability = 5 / 6
elif weapon["strength"] > defender["toughness"]:
    probability = 4 / 6
elif 2 * weapon["strength"] <= defender["toughness"]:
    probability = 1 / 6
elif weapon["strength"] < defender["toughness"]:
    probability = 2 / 6
else:
    probability = 3 / 6
# TODO: consider rerolls

wound_roll.add_child(save_roll, probability)
wound_roll.add_child(fail_sequence, 1.0 - probability)
# TODO: consider keywords, etc.

probability = (defender["save"] + weapon["ap"] - 1) / 6
if probability > 1.0:
    probability = float(1.0)
save_roll.add_child(damage_roll, probability)
save_roll.add_child(fail_sequence, 1.0 - probability)
# TODO: consider rerolls, keywords, etc.

damage = hit_roll.dfs(float(1.0))

""" v   PMF (total damage)   v """
# Determine size of the total damage distribution (for fft purposes)
if isinstance(weapon["attacks"], int):
    min_attacks = weapon["attacks"]
    fft_size = weapon["attacks"]
else:
    min_attacks = (
        weapon["attacks"][0] + weapon["attacks"][2]
    )  # min_attacks = num_dice + modifier
    fft_size = weapon["attacks"][0] * weapon["attacks"][1] + weapon["attacks"][2]

if isinstance(weapon["damage"], int):
    fft_size *= weapon["damage"]
else:
    fft_size *= weapon["damage"][0] * weapon["damage"][1] + weapon["damage"][2]

fft_size += 1
fft_size = next_fast_len(fft_size, real=True)

# represent damage as its characteristic function, then use it to determine total damage
""" v   CF (damage)   v """
damage = rfft(damage, fft_size)
""" v   CF (total damage)   v """
if (
    not attacks[0] == 0
):  # if it is possible to have 0 attacks, add that probability to the probability of achieving 0 total damage
    total_damage = np.zeros(1)
    total_damage[0] = attacks[0]
    total_damage = rfft(total_damage, fft_size)
else:  # otherwise, just initialize total_damage to an array of zeroes
    total_damage = np.zeros_like(damage)

# Calculate mixture distribution to get total damage
accumulator = np.ones_like(damage)
for i in range(1, min_attacks):
    accumulator *= damage

if min_attacks == 0:
    min_attacks = 1
for i in range(min_attacks, attacks.size):
    accumulator *= damage
    total_damage += accumulator * attacks[i]

""" v   PMF (total damage)   v """
# convert mixture distribution back to a PMF
total_damage = irfft(total_damage, fft_size)

print(total_damage)

