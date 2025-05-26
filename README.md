# TTWargame_Analyzer
A tool for visualizing and analyzing distributions of outcomes for tabletop wargames.


## Classes
All steps must consider target unit's stats and abilities
1. generate dist of number of attacks (consider abilities)
2. generate dist of number of hits (consider abilities,etc)
3. generate dist of number of wounds (consider abilities)
4. generate dist of number of failed saves (consider ap/cover/abilities)
5. Generate dist of damage dealt / models killed (consider feel-no-pain)


## IDEAS
- replace/modify class methods when applicable in order to represent keywords/abilities
- could use cumulative distribution function to represent the binary nature of the rolls (succeed/fail)
    - Or maybe use survival function for probablility that a roll succeeds

- individual die rolls can be represented with a discrete uniform (randint) distribution