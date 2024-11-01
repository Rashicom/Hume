
def len_to_mm(unit,value):
    """
    Convert a given value from a specified unit to mm (Millimeters).
    """
    if unit.lower() == "cm" :
        return value * 10
    return value

def temp_to_degree(unit, value):
    """
    Convert a given value from a specified unit to degrees.
    """
    # degree faranhight to degree celcius
    if unit.lower() == "degree fahrenheit" :
        return (value - 32) * 5 / 9
    return value