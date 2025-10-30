from datetime import datetime

def normalize_name(name: str) -> str:
    if not isinstance(name, str):
        return ""
    
    return name.replace("_", " ").title()

def denormalize_name(name: str) -> str:
    if not isinstance(name, str):
        return ""
    
    return name.lower().replace(" ", "_")

def parse_datetime(date_time: str) -> datetime | None:
    if not isinstance(date_time, str):
        return None

    for fmt in ("%Y-%m-%d %H:%M", "%d-%m-%Y %H:%M", "%d/%m/%Y %H:%M"):
        try:
            return datetime.strptime(date_time, fmt)
        except ValueError:
            continue
    return None