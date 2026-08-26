import numpy as np
from numpy import ndarray
from math import ceil
from scipy.fft import rfft, irfft, next_fast_len
from .markov import Node, DamageNode, FailureNode
from .roll_notation import RollNotation as Roll, addModifier, addDice
from copy import deepcopy


class UnitAttackSequence:
    # def __init__(self, weapons: dict[int, Weapon], defender: Model):
    def __init__(self, weapons: dict, defender: dict):
        self.sequences = {}
        self.max_damage = 0
        
        for id in weapons.keys():
            self.sequences[id] = WeaponAttackSequence(
                weapons[id], defender, weapons[id]["quantity"]
            )
            self.max_damage += self.sequences[id].max_damage

    def damage(self):
        if self.max_damage == 0.0:
            return [0.0]
        results = {}
        fft_size = next_fast_len(self.max_damage + 1, real=True)
        for id in self.sequences.keys():
            results[id] = self.sequences[id].damage()

        # use fft to sum damages as random variables
        cf = rfft(np.ones(1), fft_size)
        for dist in results:
            temp = rfft(results[dist], fft_size)
            cf *= temp

        total = irfft(cf, fft_size)[0 : self.max_damage + 1]
        total *= 100  # convert probabilities to percentages

        # restore zeroes which were converted to extremely small values due to floating point error
        for i in range(total.size):
            if total[i] < 1.0e-17:
                total[i] = 0.0

        return deepcopy(total.tolist())
            


class WeaponAttackSequence:
    def __init__(self, weapon: dict, defender: dict, weapon_quantity: int = 1, defender_quantity: int = 1):
        self.weapon = {}
        for key in weapon.keys():
            self.weapon[key] = weapon[key]

        attacks = []
        attacks.append(Roll.toValue(self.weapon["attacks"]))
        damage = []
        damage.append(Roll.toValue(self.weapon["damage"]))
        
        self.weapon["attacks"] = Roll.toValue(self.weapon["attacks"])
        if weapon['abilities'] and AbilityType.RAPID_FIRE in weapon['abilities']:       # Modify number of attack dice if RAPID_FIRE ability is present and active
            value = self.weapon["abilities"][self.weapon["abilities"].index(AbilityType.RAPID_FIRE)].value
            if isinstance(value, int):
                self.weapon["attacks"] = addModifier(self.weapon["attacks"], value)
            else:
                attacks.append(value)
        if weapon['abilities'] and AbilityType.BLAST in weapon['abilities']:            # Modify number of attack dice if BLAST ability is present and active
            value = self.weapon["abilities"][self.weapon["abilities"].index(AbilityType.BLAST)].value
            if isinstance(value, int):
                self.weapon["attacks"] = addDice(self.weapon["attacks"], value * (defender_quantity // 5))
            else:
                attacks.append(value)
        if weapon['abilities'] and AbilityType.CLEAVE in weapon['abilities']:           # Modify number of attack dice if CLEAVE ability is present and active
            value = self.weapon["abilities"][self.weapon["abilities"].index(AbilityType.CLEAVE)].value
            if isinstance(value, int):
                self.weapon["attacks"] = addDice(self.weapon["attacks"], value * (defender_quantity // 5))
            else:
                attacks.append(value)
        self.weapon["attacks"] = Roll.applyQuantity(self.weapon['attacks'], weapon_quantity)
        
        self.weapon["damage"] = Roll.toValue(self.weapon["damage"])
        if weapon['abilities'] and AbilityType.MELTA in weapon['abilities']:            # Modify damage if MELTA ability is present and active
                value = self.weapon["abilities"][self.weapon["abilities"].index(AbilityType.MELTA)].value
                if isinstance(value, int):
                    self.weapon["damage"] = addModifier(self.weapon["damage"], value)
                else:
                    damage.append(value)

            
        self.defender = defender
        self.max_damage = Roll.max(self.weapon["attacks"]) * Roll.max(
            self.weapon["damage"]
        )
        if weapon['abilities'] and AbilityType.SUSTAINED_HITS in weapon['abilities']:
            value = self.weapon["abilities"][self.weapon["abilities"].index(AbilityType.SUSTAINED_HITS)].value
            self.max_damage *= value

    # returns the PMF of the number of dice going into the attack sequence
    def __num_attacks(self) -> ndarray:
        output_size = Roll.max(self.weapon["attacks"]) + 1
        if Roll.isStatic(self.weapon["attacks"]):
            pmf = np.zeros(output_size)
            pmf[Roll.max(self.weapon["attacks"])] = 1
        else:
            num_dice = self.weapon["attacks"][0]
            num_sides = self.weapon["attacks"][1]
            modifier = self.weapon["attacks"][2]
            fft_size = next_fast_len(output_size, real=True)

            # Generate pmf for one die
            pmf = np.zeros(fft_size)
            for i in range(1, num_sides + 1):
                pmf[i] = 1

            # Convolve pmf for one die to get the distribution of the sum of random variables
            cf = rfft(pmf, n=fft_size)
            cf **= num_dice
            pmf = irfft(cf, n=fft_size)
            pmf = np.round(pmf)  # round to mitigate floating point error

            # shift values over by modifier indices
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
        return pmf

    # Returns the PMF of the damage dealt by an individual die after going through the entire attack sequence
    def __damage_per_attack(self) -> ndarray:
        hit_roll = Node(self.weapon["damage"])
        wound_roll = Node(self.weapon["damage"])
        save_roll = Node(self.weapon["damage"])
        damage_roll = DamageNode(self.weapon["damage"])
        failed_roll = FailureNode(self.weapon["damage"])
        failed_roll.child = damage_roll

        # model chance to hit with an attack
        crit_chance = 1
        # TODO: modify crit chance if abilities demand it

        if self.weapon['abilities'] and AbilityType.TORRENT in self.weapon['abilities']:
            probability = 6
            crit_chance = 0
        else:
            probability = (7 - self.weapon["skill"])
        
        fail_chance = 6 - probability
        
        if self.weapon['abilities'] and AbilityType.LETHAL_HITS in self.weapon['abilities']:
            probability -= crit_chance
            crit_chance /= 6
        
            hit_roll.add_child(save_roll, crit_chance)
        
        probability /= 6

        hit_roll.add_child(wound_roll, probability)
        if fail_chance > 0:
            hit_roll.add_child(failed_roll, fail_chance / 6)

        # model chance to wound with a successful hit
        crit_chance = 1
        # TODO: if ANTI-X against defender, modify crit_chance accordingly

        if self.weapon["strength"] >= 2 * self.defender["toughness"]:
            probability = 5
        elif self.weapon["strength"] > self.defender["toughness"]:
            probability = 4
        elif 2 * self.weapon["strength"] <= self.defender["toughness"]:
            probability = 1
        elif self.weapon["strength"] < self.defender["toughness"]:
            probability = 2
        else:
            probability = 3
        fail_chance = 6 - probability
        
        if self.weapon['abilities'] and AbilityType.DEVASTATING_WOUNDS in self.weapon['abilities']:
            probability -= crit_chance
            crit_chance /= 6
        
            wound_roll.add_child(damage_roll, crit_chance)
        
        probability /= 6
        fail_chance /= 6

        wound_roll.add_child(save_roll, probability)
        if self.weapon['abilities'] and AbilityType.TWIN_LINKED in self.weapon['abilities']:
            wound_reroll = Node(self.weapon["damage"])
            wound_roll.add_child(wound_reroll, fail_chance)
            
            if self.weapon['abilities'] and AbilityType.DEVASTATING_WOUNDS in self.weapon['abilities']:
                wound_reroll.add_child(damage_roll, crit_chance)
            wound_reroll.add_child(save_roll, probability)
            wound_reroll.add_child(failed_roll, fail_chance)
        else:
            wound_roll.add_child(failed_roll, fail_chance)

        # model chance for a successful wound to survive the defender's save roll
        probability = (self.defender["save"] + self.weapon["ap"] - 1) / 6
        if probability > 1:
            probability = 1.0
        save_roll.add_child(damage_roll, probability)
        save_roll.add_child(failed_roll, 1.0 - probability)

        return hit_roll.dfs(1.0)

    def damage(self):
        attacks = self.__num_attacks()
        single_damage = self.__damage_per_attack()

        # calculate maxima and minima, and ideal size for the fft's inputs
        min_attacks = Roll.min(self.weapon["attacks"])
        fft_size = next_fast_len(self.max_damage + 1, real=True)

        # represent damage per attack as its characteristic function, then use it to calculate the total damage distribution
        total_damage = np.zeros_like(single_damage)
        single_damage = rfft(single_damage, fft_size)

        # If it is possible to have zero attacks, inititalize the probability of dealing 0 damage to be the probability of having 0 attacks
        if not (attacks[0] == 0):
            total_damage[0] = attacks[0]
        total_damage = rfft(
            total_damage, fft_size
        )  # represent total_damage as its characteristic function

        # Initialize the accumulator
        accumulator = np.ones_like(total_damage)
        for num_attacks in range(1, min_attacks):
            accumulator *= single_damage

        # Calculate mixture distribution to get total damage
        if min_attacks == 0:
            min_attacks = 1
        for num_attacks in range(min_attacks, attacks.size):
            accumulator *= single_damage
            total_damage += accumulator * attacks[num_attacks]

        # Convert the resulting mixture distribution back into its PMF
        total_damage = irfft(total_damage, fft_size)
        total_damage = total_damage[0 : self.max_damage + 1]
        # total_damage *= 100  # convert probabilities to percentages

        # restore zeroes which were converted to extremely small values due to floating point error
        for i in range(total_damage.size):
            if total_damage[i] < 1.0e-17:
                total_damage[i] = 0.0

        return deepcopy(total_damage)
    
    # applies modifiers to a value in the appropriate order (x, +, /, -). replace the value if necessary before modifying.
    def __modify_value(self, value: int, mult: int = 1, add: int = 0, div: int = 1, sub: int = 0, min: int|None = None, max: int|None = None) -> int:
        value *= mult
        value += add
        value /= div
        value -= sub
        if min is not None and value < min:
            value = min
        elif max is not None and value > max:
            value = max
        return ceil(value)
