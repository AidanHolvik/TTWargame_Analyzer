class RollNotation:
    def isStatic(roll: str | tuple[int, int, int]) -> bool:
        if isinstance(roll, str):
            roll = __class__.toValue(roll)
        return roll[1] == 1

    def min(roll: str | tuple[int,int,int]) -> int:
        if isinstance(roll, str):
            roll = __class__.toValue(roll)
        return roll[0] + roll[2]

    def max(roll: str | tuple[int, int, int]) -> int:
        if isinstance(roll, str):
            roll = __class__.toValue(roll)
        return roll[0] * roll[1] + roll[2]

    def applyQuantity(roll: tuple[int,int,int], quantity:int) -> tuple[int,int,int]:
        return (roll[0] * quantity, roll[1], roll[2] * quantity)

    def toValue(roll: str) -> tuple[int, int, int]:
        value = [1, 1, 0]
        if roll.isdecimal():
            value[0] = int(roll)
            return value
        else:
            roll = roll.lower().partition("d")
            if not roll[1]:
                roll = roll[0].partition("+")
                if roll[0].isdecimal():
                    value[0] = int(roll[0])
                if roll[2].isdecimal():
                    value[2] = int(roll[2])
            else:
                if roll[0].isdecimal():
                    value[0] = int(roll[0])
                roll = roll[2].partition("+")
                if roll[0].isdecimal():
                    value[1] = int(roll[0])
                if roll[2].isdecimal():
                    value[2] = int(roll[2])
            return (value[0], value[1], value[2])

    def fromValue(value: tuple[int, int, int]) -> str:
        if __class__.isStatic(value):
            return str(value[0] + value[2])

        output = f"{value[0]}"
        if value[1] != 1:
            output += f"D{value[1]}"
        if value[2] != 0:
            output += f"+{value[2]}"
        return output
