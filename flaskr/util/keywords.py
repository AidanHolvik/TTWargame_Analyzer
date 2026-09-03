from enum import Enum

class Keyword(Enum):
    BATTLELINE = 1
    SWARM = 2
    INFANTRY = 3
    BEAST = 4
    MOUNTED = 5
    MONSTER = 6
    VEHICLE = 7
    AIRCRAFT = 8
    FRAME = 9

    CHARACTER = 10
    EPIC_HERO = 11
    WALKER = 12
    TITANIC = 13
    TOWERING = 14
    FORTIFICATION = 15
    PSYKER = 16
    ARTILLERY = 17

    GRENADES = 18
    SMOKE = 19
    FLY = 20
    TRANSPORT = 21
    DEDICATED_TRANSPORT = 22

    IMPERIUM = 23
    CHAOS = 24
    DAEMON = 25

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