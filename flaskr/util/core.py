from abc import ABC
from .abilities import ModelAbility, Ability, Valued, choose_greater
from copy import deepcopy


class CoreObj(ABC):
    def __init__(self, id: int, name: str):
        self.id = id
        self.name = name


class Weapon(CoreObj):
    def __init__(
        self,
        id: int,
        name: str,
        attacks: int | tuple[int, int, int] = 1,
        skill: int = 4,
        strength: int = 1,
        ap: int = 0,
        damage: int | tuple[int, int, int] = 1,
        abilities: list[Ability] = [],
        quantity: int = 1,
    ):
        super().__init__(id, name)
        self._attacks = attacks
        self._skill = skill
        self._strength = strength
        self._ap = ap
        self._damage = damage
        self._abilities = abilities
        self._quantity = quantity

    def add_ability(self, ability: Valued) -> None:
        if ability not in self._abilities:
            self._abilities.append(ability)
        else:
            # get ability from list
            # if ability is valued, store higher of the 2 values in the list
            for i, ab in enumerate(self._abilities):
                if ab == ability:
                    if isinstance(ab, Valued) and type(ability) == type(ab):
                        self._abilities[i] = choose_greater(ab, ability)

    def remove_ability(self, ability: Ability) -> None:
        if ability in self._abilities:
            self._abilities.remove(ability)


class Model(CoreObj):
    def __init__(
        self,
        id: int,
        name: str,
        movement: int = 0,
        toughness: int = 1,
        save: int = 4,
        invuln: int = 7,
        health: int = 1,
        abilities: list[ModelAbility] = [],
        quantity: int = 1,
        weapons: dict[int, Weapon] = {},
    ):
        super().__init__(id, name)
        self._movement = movement
        self._toughness = toughness
        self._save = save
        self._invuln = invuln
        self._health = health
        self._abilities = abilities
        self._quantity = quantity
        self._weapons = weapons
    
    @property
    def abilities(self) -> list[ModelAbility]:
        return self._abilities
    
    @abilities.setter
    def abilities(self, abilities: list[ModelAbility]):
        self._abilities = abilities
    
    @property
    def weapons(self) -> dict[int, Weapon]:
        return self._weapons
    
    @weapons.setter
    def weapons(self, weapons: dict[int, Weapon]):
        self._weapons = weapons

    def add_ability(self, ability: ModelAbility) -> None:
        if ability not in self._abilities:
            self._abilities.append(ability)
        else:
            # get ability from list
            # if ability is valued, store higher of the 2 values in the list
            for i, ab in enumerate(self._abilities):
                if ab == ability:
                    if isinstance(ab, Valued) and type(ability) == type(ab):
                        self._abilities[i] = choose_greater(ab, ability)

    def remove_ability(self, ability: ModelAbility) -> None:
        if ability in self._abilities:
            self._abilities.remove(ability)


class Unit(CoreObj):
    def __init__(
        self,
        id: int,
        name: str,
        abilities: list[ModelAbility] = [],
        models: dict[int, Model] = {},
    ):
        super().__init__(id, name)
        self._abilities = abilities
        self._models = models

    @property
    def abilities(self) -> list[ModelAbility]:
        return self._abilities
    
    @abilities.setter
    def abilities(self, abilities: list[ModelAbility]):
        self._abilities = abilities
    
    @property
    def models(self) -> dict[int, Model]:
        return self._models
    
    @models.setter
    def models(self, models: dict[int, Model]):
        self._models = models

    def add_ability(self, ability: ModelAbility) -> None:
        if ability not in self._abilities:
            self.abilities.append(ability)
        else:
            # get ability from list
            # if ability is valued, store higher of the 2 values in the list
            for i, ab in enumerate(self.abilities):
                if ab == ability:
                    if isinstance(ab, Valued) and type(ability) == type(ab):
                        self.abilities[i] = choose_greater(ab, ability)

    def remove_ability(self, ability: ModelAbility) -> None:
            if ability in self.abilities:
                self.abilities.remove(ability)
    
    def get_weapons(self) -> list[Weapon]:
        weapons = []
        for model in self._models.values():
            weapons.extend(model._weapons.values())
        return weapons
