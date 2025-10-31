from datetime import datetime

def normalize_name(name: str) -> str:
    """ 
    Convert a snake_case or lowercase name into a human-readable Title Case format.

    Example:
        >>> normalize_name("normalized_name")
        'Normalized Name'

    Args:
        name (str): Raw service name in snake_case or lowercase.

    Returns:
        str: Normalized name in Title Case, or an empty string if input is not str.
    """
    if not isinstance(name, str):
        return ""
    
    return name.replace("_", " ").title()

def denormalize_name(name: str) -> str:
    """
    Convert a human-readable name into a normalized snake_case format.

    Example:
        >>> denormalize_name("Denormalized Name")
        'denormalized_name'

    Args:
        name (str): Human-readable name.

    Returns:
        str: Normalized snake_case name, or an empty string if input is not str.
    """
    if not isinstance(name, str):
        return ""
    
    return name.lower().replace(" ", "_")

def parse_datetime(date_time: str) -> datetime | None:
    """
    Parse a date and time string into a datetime object.

    Supports multiple common formats:
    - YYYY-MM-DD HH:MM
    - DD-MM-YYYY HH:MM
    - DD/MM/YYYY HH:MM

    Example:
        >>> parse_datetime("2025-10-30 14:45")
        datetime.datetime(2025, 10, 30, 14, 45)

    Args:
        date_time (str): String representation of date and time.

    Returns:
        datetime | None: Datetime object if parsed successfully, otherwise None.
    """
    if not isinstance(date_time, str):
        return None

    for fmt in ("%Y-%m-%d %H:%M", "%d-%m-%Y %H:%M", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(date_time, fmt)
        except ValueError:
            continue
    return None