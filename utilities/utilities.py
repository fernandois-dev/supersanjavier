




def num_or_zero(value):
    """
    Returns the value if it is numeric, otherwise returns 0.
    """
    return value if isinstance(value, (int, float)) else 0

def to_number_or_zero(value):
    """
    Tries to convert the value to a number. If it fails, returns 0.
    """
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0