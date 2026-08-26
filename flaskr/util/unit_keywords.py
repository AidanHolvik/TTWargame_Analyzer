from enum import Enum, auto

class Keyword(Enum):
    BATTLELINE = auto()
    SWARM = auto()
    INFANTRY = auto()
    BEAST = auto()
    MOUNTED = auto()
    MONSTER = auto()
    VEHICLE = auto()
    AIRCRAFT = auto()
    FRAME = auto()

    CHARACTER = auto()
    EPIC_HERO = auto()
    WALKER = auto()
    TITANIC = auto()
    TOWERING = auto()
    FORTIFICATION = auto()
    PSYKER = auto()
    ARTILLERY = auto()

    GRENADES = auto()
    SMOKE = auto()
    FLY = auto()
    TRANSPORT = auto()
    DEDICATED_TRANSPORT = auto()

    IMPERIUM = auto()
    CHAOS = auto()
    DAEMON = auto()

    def __str__(self):
        match self:
            case Keyword.BATTLELINE:
                return "BATTLELINE"
            case Keyword.SWARM:
                return "SWARM"
            case Keyword.INFANTRY:
                return "INFANTRY"
            case Keyword.BEAST:
                return "BEAST"
            case Keyword.MOUNTED:
                return "MOUNTED"
            case Keyword.MONSTER:
                return "MONSTER"
            case Keyword.VEHICLE:
                return "VEHICLE"
            case Keyword.AIRCRAFT:
                return "AIRCRAFT"
            case Keyword.FRAME:
                return "FRAME"

            case Keyword.CHARACTER:
                return "CHARACTER"
            case Keyword.EPIC_HERO:
                return "EPIC HERO"
            case Keyword.WALKER:
                return "WALKER"
            case Keyword.TITANIC:
                return "TITANIC"
            case Keyword.TOWERING:
                return "TOWERING"
            case Keyword.FORTIFICATION:
                return "FORTIFICATION"
            case Keyword.PSYKER:
                return "PSYKER"

            case Keyword.GRENADES:
                return "GRENADES"
            case Keyword.SMOKE:
                return "SMOKE"
            case Keyword.FLY:
                return "FLY"
            case Keyword.TRANSPORT:
                return "TRANSPORT"
            case Keyword.DEDICATED_TRANSPORT:
                return "DEDICATED TRANSPORT"

            case Keyword.IMPERIUM:
                return "IMPERIUM"
            case Keyword.CHAOS:
                return "CHAOS"
            case Keyword.DAEMON:
                return "DAEMON"
            case _:
                return "ERROR"