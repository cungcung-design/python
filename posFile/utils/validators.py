def required(value, field_name):
    if value is None:
        return f"{field_name} is required."
    if not str(value).strip():
        return f"{field_name} is required."
    return None


def positive_number(value, field_name):
    try:
        number = float(value)
    except (ValueError, TypeError):
        return f"{field_name} must be a valid number."
    if number < 0:
        return f"{field_name} cannot be negative."
    return None


def positive_integer(value, field_name):
    try:
        number = int(value)
    except (ValueError, TypeError):
        return f"{field_name} must be a whole number."
    if number < 0:
        return f"{field_name} cannot be negative."
    return None
