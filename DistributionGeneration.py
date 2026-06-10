import numpy as np
from scipy.fft import rfft, irfft, next_fast_len
from scipy.special import comb as choose
from scipy.stats import binom



# minimum sum must be tracked separately (in this case, based on num_dice)
def roll_dice(num_dice, num_sides):
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

    return pmf.tolist()



def test():

    # Weapon Profile
    wpn_attacks = "D6"  # Binomial distribution
    wpn_bs = 4  # Bernoulli sampling
    wpn_str = 3  # Bernoulli sampling
    wpn_ap = 1  # Bernoulli sampling
    wpn_damage = "1"  # Binomial distribution

    # Defender profile
    def_toughness = 3
    def_save = 4

    # calculate hit chance
    # TODO: add in modifiers, rerolls, etc.
    chance_to_hit = (7 - wpn_bs) / 6
    if chance_to_hit < 1/6:
        chance_to_hit = 1/6
    elif chance_to_hit > 5/6:
        chance_to_hit = 5/6

    # # calculate wound chance
    # # TODO: add in modifiers, rerolls, etc.
    # if wpn_str >= 2 * def_toughness:
    #     chance_to_wound = 5 / 6
    # elif wpn_str > def_toughness:
    #     chance_to_wound = 4 / 6
    # elif wpn_str * 2 <= def_toughness:
    #     chance_to_wound = 1 / 6
    # elif wpn_str <= def_toughness:
    #     chance_to_wound = 2 / 6
    # else:
    #     chance_to_wound = 3 / 6

    # # calculate chance of failing save
    # # TODO: add in modifiers, rerolls, invuln, etc.
    # chance_to_fail_save = (def_save - wpn_ap - 1) / 6
    # if chance_to_fail_save < 0:
    #     chance_to_fail_save = 0
    # elif chance_to_fail_save > 5/6:
    #     chance_to_fail_save = 5/6

    # attacks roll is 1d6
    attacks = roll_dice(2, 6)  # Binomial distribution for attacks (2d6)

    # calculate expected size of set from bernoulli sampling for each result to get expected number of hits
    # For each possible number of hits, calculate the chance of getting that many hits based on the number of attacks and the chance to hit
    hits = [0] * len(attacks)
    accumulator = 1
    for i in range(len(attacks)):
        hits[0] += attacks[i] * accumulator
        accumulator *= 1 - chance_to_hit

    for i in range(1, len(attacks)):  # iterate through number of hits
        accumulator = chance_to_hit**i
        hits[i] = attacks[i] * accumulator
        for j in range(i + 1, len(attacks)):  # iterate through number of attacks
            accumulator *= j / (
                j - i
            )  # update accumulator to reflect change in binomial coefficient (i.e., nCr(n, k) = nCr(n-1, k-1) * n / k)
            accumulator *= (
                1 - chance_to_hit
            )  # update accumulator to reflect change in probability of failure
            hits[i] += attacks[j] * accumulator

    # # calculate expected size of set from bernoulli sampling for each result to get expected number of wounds
    # # For each possible number of wounds, calculate the chance of getting that many wounds based on the number of hits and the chance to wound
    # wounds = [0] * len(hits)
    # accumulator = 1
    # for i in range(len(hits)):
    #     wounds[0] += hits[i] * accumulator
    #     accumulator *= 1 - chance_to_wound

    # for i in range(1, len(hits)):  # iterate through number of wounds
    #     accumulator = chance_to_wound**i
    #     wounds[i] = hits[i] * accumulator
    #     for j in range(i + 1, len(hits)):  # iterate through number of hits
    #         accumulator *= j / (
    #             j - i
    #         )  # update accumulator to reflect change in binomial coefficient (i.e., nCr(n, k) = nCr(n-1, k-1) * n / k)
    #         accumulator *= (
    #             1 - chance_to_wound
    #         )  # update accumulator to reflect change in probability of failure
    #         wounds[i] += hits[j] * accumulator

    # # calculate expected size of set from bernoulli sampling for each result to get expected number of failed saves
    # # For each possible number of failed saves, calculate the chance of getting that many failed saves based on the number of wounds and the chance to fail save
    # failed_saves = [0] * len(wounds)
    # accumulator = 1
    # for i in range(len(wounds)):
    #     failed_saves[0] += wounds[i] * accumulator
    #     accumulator *= 1 - chance_to_fail_save

    # for i in range(1, len(wounds)):  # iterate through number of failed saves
    #     accumulator = chance_to_fail_save**i
    #     failed_saves[i] = wounds[i] * accumulator
    #     for j in range(i + 1, len(wounds)):  # iterate through number of wounds
    #         accumulator *= j / (
    #             j - i
    #         )  # update accumulator to reflect change in binomial coefficient (i.e., nCr(n, k) = nCr(n-1, k-1) * n / k)
    #         accumulator *= (
    #             1 - chance_to_fail_save
    #         )  # update accumulator to reflect change in probability of failure
    #         failed_saves[i] += wounds[j] * accumulator

    # Testing outputs
    
    print("Attacks: [", end="")
    for i in range(len(attacks) - 1):
        print(f"  {i}: {attacks[i]},", end="")
    print(f"  {len(attacks) - 1}: {attacks[-1]} ]", end="\n\n")

    print("Hits: [", end="")
    for i in range(len(hits) - 1):
        print(f"  {i}: {hits[i]},", end="")
    print(f"  {len(hits) - 1}: {hits[-1]} ]", end="\n\n")
    
    # print("Wounds: [", end="")
    # for i in range(len(wounds) - 1):
    #     print(f"  {i}: {wounds[i]},", end="")
    # print(f"  {len(wounds) - 1}: {wounds[-1]} ]", end="\n\n")

    # print("Failed Saves: [", end="")
    # for i in range(len(failed_saves) - 1):
    #     print(f"  {i}: {failed_saves[i]},", end="")
    # print(f"  {len(failed_saves) - 1}: {failed_saves[-1]} ]", end="\n\n")


test()

