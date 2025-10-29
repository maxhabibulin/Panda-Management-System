def validate_phone_id(phone_id: int) -> str | None:
    if not isinstance(phone_id, int):
        return "[Provided argument must be integer]"
    
    if phone_id < 0:
        return "[Negative number not allowed]"
    
    if len(str(phone_id)) != 8:
        return "[Phone ID must contain exactly 8 digits]"
    
    return None

def validate_positive_int(value: int, param_name: str = "value") -> str | None:
    if not isinstance(value, int):
        return f"[{param_name.capitalize()} must be an integer]"
    
    if value <= 0:
        return f"[{param_name.capitalize()} must be a positive number]"
    return None
