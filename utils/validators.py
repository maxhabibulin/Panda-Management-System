"""
Input validation utilities.

These functions validate common input types and return error messages or None if validation passes.
"""

def validate_phone_id(phone_id: int) -> str | None:
    """
    Validate phone ID format.

    Rules:
    - Must be integer
    - Must be non-negative  
    - Must be exactly 8 digits

    Args:
        phone_id (int): Phone number to validate

    Returns:
        str | None: Error message if invalid, None if valid
    """
    if not isinstance(phone_id, int):
        return "[Provided argument must be integer]"
    
    if phone_id < 0:
        return "[Negative number not allowed]"
    
    if len(str(phone_id)) != 8:
        return "[Phone ID must contain exactly 8 digits]"
    
    return None

def validate_positive_int(value: int, param_name: str = "value") -> str | None:
    """
    Validate that a value is a positive integer.

    Args:
        value (int): Value to check
        param_name (str): Parameter name for error messages (default: "value")

    Returns:
        str | None: Error message if invalid, None if valid
    """
    if not isinstance(value, int):
        return f"[{param_name.capitalize()} must be an integer]"
    
    if value <= 0:
        return f"[{param_name.capitalize()} must be a positive number]"
    return None
