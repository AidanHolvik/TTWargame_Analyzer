
class RollNotation:
    def toValue(roll: str) -> int | tuple[int,int,int]:
        if roll.isdecimal():
            value = int(roll)
            return value
        else:
            value = [int(1), int(0), int(0)]
            roll = roll.lower().partition("d")
            if roll[0].isdecimal():
                value[0] = int(roll[0])

            roll = roll[2].partition("+")
            if roll[0].isdecimal():
                value[1] = int(roll[0])

            if roll[2].isdecimal():
                value[2] = int(roll[2])
                
            return (value[0], value[1], value[2])

    def fromValue(value: int | tuple[int,int,int]) -> str:
        if isinstance(value, int):
            return str(value)
        
        output = f'{value[0]}'
        if value[1] != 1:
            output += f'D{value[1]}'
        if value[2] != 0:
            output += f'+{value[2]}'
        
        return output



