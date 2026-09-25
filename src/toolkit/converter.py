from decimal import Decimal

distance = ["mm", "cm", "m", "km"]
mass = ["g", "kg"]
temperature = ["c", "f", "k"]

def validation():

    if from_unit in distance and value<0:
        raise ValueError("Distance can't be < 0")
    
    if (from_unit in mass and value<0):
        raise ValueError("Mass can't be < 0")

    #DIFFERENT TYPES
    if where_unit(to_unit) != where_unit(from_unit):
        raise ValueError("Different types")

    #NOT NUMBER
    if (not isinstance(value, float)):
        raise ValueError("Not number")

    #UNKNOWN UNIT OR INVALID CHARACTER
    if where_unit(to_unit)=="ERROR" or where_unit(from_unit)=="ERROR":
        raise ValueError("Unknown unit or invalid character")

    if where_unit(from_unit) == "TEMP":
        if (value<=-273 and from_unit=="c") or (value<=0 and from_unit=="k") or (value<=-459.67 and from_unit=="f"):
            raise ValueError("Too low")



def where_unit(unit):
    if unit in distance:
        return "DISTANCE"
    elif unit in mass:
        return "MASS"
    elif unit in temperature:
        return "TEMP"
    else:
        return "ERROR"


def converter():
    convertation = value
    if where_unit(from_unit) == "DISTANCE":
        difference = distance.index(to_unit) - distance.index(from_unit)
        if difference > 0:
            for i in range(distance.index(from_unit), distance.index(to_unit)):
                convertation /= 10**(i+1)
        else:
            for i in range(distance.index(to_unit), distance.index(from_unit)):
                convertation *= 10**(i+1)

    if where_unit(from_unit) == "MASS":
        if from_unit == "kg" and to_unit == "g":
            convertation *= 1000
        elif from_unit == "g" and to_unit == "kg":
            convertation /= 1000

    if where_unit(from_unit) == "TEMP":
        if from_unit == "c" and to_unit == "k":
            convertation += 273
        elif from_unit == "k" and to_unit == "c":
            convertation -= 273
        elif from_unit == "c" and to_unit == "f":
            convertation = convertation * 1.8 + 32
        elif from_unit == "f" and to_unit == "c":
            convertation = (convertation - 32) * (5/9)
        elif from_unit == "f" and to_unit == "k":
            convertation = (convertation + 459.67) * (5/9)
        elif from_unit == "k" and to_unit == "f":
            convertation = convertation * 1.8 - 459.67
                
        
    return Decimal(convertation).quantize(Decimal('1.000000'))


def convert(args):
    global value, from_unit, to_unit
    value, from_unit, to_unit = float(args.value), args.from_unit.lower(), args.to_unit.lower()
    validation()
    result = converter()
    return float(result)