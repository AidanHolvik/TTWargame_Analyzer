from abc import ABC
from enum import Enum, auto
from .roll_notation import RollNotation as Roll


class ModelAbilityType(Enum):
    ERROR = 0
    FEEL_NO_PAIN = auto()  # o
    AP_ON_CRIT_WOUND = auto()  # o
    FNP_ON_PSYCHIC = auto()  # o
    FNP_ON_MORTAL_WOUNDS = auto()  # o
    RESIST_STRONG_ATTACKS = auto()  # o

    def is_offensive(self) -> bool:
        match self:
            case ModelAbilityType.AP_ON_CRIT_WOUND:
                return True
            case _:
                return False


class WeaponAbilityType(Enum):
    ERROR = 0
    ANTI = auto()  # o
    BLAST = auto()  # x
    CLEAVE = auto()  # x
    CLOSE_QUARTERS = auto()  # o
    DEVASTATING_WOUNDS = auto()  # x
    INDIRECT_FIRE = auto()  # o
    LETHAL_HITS = auto()  # x
    MELTA = auto()  # x
    PSYCHIC = auto()  # o
    RAPID_FIRE = auto()  # x
    SUSTAINED_HITS = auto()  # o
    TORRENT = auto()  # x
    TWIN_LINKED = auto()  # x
    CONVERSION = auto()  # o

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
            # case WeaponAbilityType.HEAVY:
            #     return "HEAVY"
            # case WeaponAbilityType.IGNORES_COVER:
            #     return "IGNORES COVER"
            case WeaponAbilityType.INDIRECT_FIRE:
                return "INDIRECT FIRE"
            # case WeaponAbilityType.LANCE:
            #     return "LANCE"
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


class Ability(ABC):
    def __init__(self, ability):
        self.ab = ability
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
                type(self.ab) == type(other.ab) and self.ab == other.ab and self.is_active()
            )
        else:
            return type(self.ab) == type(other) and self.ab == other and self.is_active()


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
        super().__init__(ability)
        self.name = name

    def is_offensive(self) -> bool:
        return self.ab.is_offensive()

    def __str__(self):
        return self.name


class ModelAbilityValued(ModelAbility, Valued):
    def __init__(
        self,
        name: str,
        ability: ModelAbilityType,
        value: int | str | tuple[int, int, int] = 1,
    ):
        ModelAbility.__init__(name, ability)
        Valued.__init__(value)


class WeaponAbility(Ability):
    def __init__(self, ability: WeaponAbilityType):
        super().__init__(ability)

    def __str__(self):
        return str(self.ab)


class WeaponAbilityValued(WeaponAbility, Valued):
    def __init__(
        self, ability: WeaponAbilityType, value: int | str | tuple[int, int, int]
    ):
        WeaponAbility.__init__(ability)
        Valued.__init__(value)

    def __str__(self):
        return f"{str(self.ab)} {self.value}"


class WeaponAbilityKeyworded(WeaponAbilityValued):
    def __init__(
        self,
        ability: WeaponAbilityType,
        value: int | str | tuple[int, int, int],
        target_keyword: str,
    ):
        super().__init__(ability, value)
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
