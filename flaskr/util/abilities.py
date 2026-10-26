from abc import ABC, abstractmethod
from enum import Enum, auto
from .roll_notation import RollNotation as Roll

# Enables abilities to be identified by a consistent ID in the database and code
class AbilityID(Enum):
    # Weapon abilities
    ANTI = 1
    BLAST = 2
    CLEAVE = 3
    CLOSE_QUARTERS = 4
    DEVASTATING_WOUNDS = 5
    INDIRECT_FIRE = 6
    LETHAL_HITS = 7
    MELTA = 8
    PSYCHIC = 9
    RAPID_FIRE = 10
    SUSTAINED_HITS = 11
    TORRENT = 12
    TWIN_LINKED = 13
    CONVERSION = 14

    # Unit/Model abilities
    FEEL_NO_PAIN = 15
    AP_ON_CRIT_WOUND = 16
    FNP_ON_PSYCHIC = 17
    FNP_ON_MORTAL_WOUNDS = 18
    RESIST_STRONG_ATTACKS = 19


class AbilityEnum(Enum,ABC):
    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def is_offensive(self) -> bool:
        """Returns True if the ability may activate when attacking, False otherwise."""
        pass

    @abstractmethod
    def extra_values(self) -> int:
        """Returns the number of extra values associated with the ability. Should return 2 if the ability is keyworded, return 1 if the ability is valued, and 0 otherwise."""
        pass

class ModelAbilityType(AbilityEnum):
    FEEL_NO_PAIN = AbilityID.FEEL_NO_PAIN.value
    AP_ON_CRIT_WOUND = AbilityID.AP_ON_CRIT_WOUND.value
    FNP_ON_PSYCHIC = AbilityID.FNP_ON_PSYCHIC.value
    FNP_ON_MORTAL_WOUNDS = AbilityID.FNP_ON_MORTAL_WOUNDS.value
    RESIST_STRONG_ATTACKS = AbilityID.RESIST_STRONG_ATTACKS.value

    def __str__(self):
        match self:
            case ModelAbilityType.FEEL_NO_PAIN:
                return "FEEL NO PAIN"
            case ModelAbilityType.AP_ON_CRIT_WOUND:
                return "AP on critical wound rolls"
            case ModelAbilityType.FNP_ON_PSYCHIC:
                return "FEEL NO PAIN against psychic attacks"
            case ModelAbilityType.FNP_ON_MORTAL_WOUNDS:
                return "FEEL NO PAIN against mortal wounds"
            case ModelAbilityType.RESIST_STRONG_ATTACKS:
                return "-1 to wound rolls when STRENGTH > TOUGHNESS"
            case _:
                return "ERROR"

    def is_offensive(self) -> bool:
        match self:
            case ModelAbilityType.AP_ON_CRIT_WOUND:
                return True
            case _:
                return False
    
    def extra_values(self) -> int:
        match self:
            case ModelAbilityType.FEEL_NO_PAIN:
                return 1
            case ModelAbilityType.AP_ON_CRIT_WOUND:
                return 1
            case ModelAbilityType.FNP_ON_PSYCHIC:
                return 1
            case ModelAbilityType.FNP_ON_MORTAL_WOUNDS:
                return 1
            case _:
                return 0


class WeaponAbilityType(AbilityEnum):
    ANTI = AbilityID.ANTI.value
    BLAST = AbilityID.BLAST.value
    CLEAVE = AbilityID.CLEAVE.value
    CLOSE_QUARTERS = AbilityID.CLOSE_QUARTERS.value
    DEVASTATING_WOUNDS = AbilityID.DEVASTATING_WOUNDS.value
    INDIRECT_FIRE = AbilityID.INDIRECT_FIRE.value
    LETHAL_HITS = AbilityID.LETHAL_HITS.value
    MELTA = AbilityID.MELTA.value
    PSYCHIC = AbilityID.PSYCHIC.value
    RAPID_FIRE = AbilityID.RAPID_FIRE.value
    SUSTAINED_HITS = AbilityID.SUSTAINED_HITS.value
    TORRENT = AbilityID.TORRENT.value
    TWIN_LINKED = AbilityID.TWIN_LINKED.value
    CONVERSION = AbilityID.CONVERSION.value

    def __str__(self):
        match self:
            case WeaponAbilityType.ANTI:
                return "ANTI"
            case WeaponAbilityType.BLAST:
                return "BLAST"
            case WeaponAbilityType.CLEAVE:
                return "CLEAVE"
            case WeaponAbilityType.CLOSE_QUARTERS:
                return "CLOSE QUARTERS"
            case WeaponAbilityType.DEVASTATING_WOUNDS:
                return "DEVASTATING WOUNDS"
            case WeaponAbilityType.INDIRECT_FIRE:
                return "INDIRECT FIRE"
            case WeaponAbilityType.LETHAL_HITS:
                return "LETHAL HITS"
            case WeaponAbilityType.MELTA:
                return "MELTA"
            case WeaponAbilityType.PSYCHIC:
                return "PSYCHIC"
            case WeaponAbilityType.RAPID_FIRE:
                return "RAPID FIRE"
            case WeaponAbilityType.SUSTAINED_HITS:
                return "SUSTAINED HITS"
            case WeaponAbilityType.TORRENT:
                return "TORRENT"
            case WeaponAbilityType.TWIN_LINKED:
                return "TWIN-LINKED"
            case WeaponAbilityType.CONVERSION:
                return "CONVERSION"
            case _:
                return "ERROR"

    def is_offensive(self) -> bool:
        return True
    
    def extra_values(self) -> int:
        match self:
            case WeaponAbilityType.ANTI:
                return 2
            case WeaponAbilityType.BLAST:
                return 1
            case WeaponAbilityType.CLEAVE:
                return 1
            case WeaponAbilityType.MELTA:
                return 1
            case WeaponAbilityType.RAPID_FIRE:
                return 1
            case WeaponAbilityType.SUSTAINED_HITS:
                return 1
            case _:
                return 0



class Ability(ABC):
    def __init__(self, ability, name: str = None):
        self.ab = ability
        if name is None:
            self.name = str(ability)
        else:
            self.name = name
        self._active = True

    def deactivate(self):
        self._active = False

    def activate(self):
        self._active = True

    def is_active(self) -> bool:
        return self.active

    def is_offensive(self) -> bool:
        return self.ab.is_offensive()

    def __eq__(self, other):
        if type(self) == type(other):
            return (
                type(self.ab) == type(other.ab)
                and self.ab == other.ab
                and self.is_active()
            )
        else:
            return (
                type(self.ab) == type(other) and self.ab == other and self.is_active()
            )


class Valued(ABC):
    def __init__(self, value: int | str | tuple[int, int, int]):
        super().__init__()
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value: int | str | tuple[int, int, int]):
        if isinstance(value, str):  # value is a string
            value = Roll.toValue(value)
        if isinstance(value, int):  # value is an integer
            self._value = 0 if value < 0 else value
        else:  # value is a tuple
            if value[0] < 0 or value[1] < 0:
                self._value = 0
            else:
                self._value = value


class ModelAbility(Ability):
    def __init__(self, ability: ModelAbilityType, name: str):
        super().__init__(ability, name)

    def is_offensive(self) -> bool:
        return self.ab.is_offensive()

    def __str__(self):
        return self.name


class ModelAbilityValued(ModelAbility, Valued):
    def __init__(
        self,
        ability: ModelAbilityType,
        name: str,
        value: int | str | tuple[int, int, int] = 1,
    ):
        ModelAbility.__init__(self, ability, name)
        Valued.__init__(self, value)
    
    def __str__(self):
        return f"{self.name} {self.value}"


class WeaponAbility(Ability):
    def __init__(self, ability: WeaponAbilityType, name: str = None):
        super().__init__(ability, name)

    def __str__(self):
        return str(self.ab)


class WeaponAbilityValued(WeaponAbility, Valued):
    def __init__(
        self,
        ability: WeaponAbilityType,
        value: int | str | tuple[int, int, int],
        name: str = None,
    ):
        WeaponAbility.__init__(self, ability, name)
        Valued.__init__(self, value)

    def __str__(self):
        return f"{str(self.ab)} {self.value}"


class WeaponAbilityKeyworded(WeaponAbilityValued):
    def __init__(
        self,
        ability: WeaponAbilityType,
        value: int | str | tuple[int, int, int],
        target_keyword: str,
        name: str = None,
    ):
        super().__init__(ability, value, name)
        self.keyword = target_keyword

    def __str__(self):
        return f"{str(self.ab)}-{self.keyword} {self.value}"

    def __eq__(self, other):
        if isinstance(other, WeaponAbilityKeyworded):
            return super().__eq__(other) and self.keyword == other.keyword
        return False


def choose_greater(ab1: Valued, ab2: Valued) -> Valued:
    if ab1.value >= ab2.value:
        return ab1
    else:
        return ab2


def choose_lesser(ab1: Valued, ab2: Valued) -> Valued:
    if ab1.value <= ab2.value:
        return ab1
    else:
        return ab2
