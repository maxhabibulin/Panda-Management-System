def normalize_name(name: str) -> str:
    if not isinstance(name, str):
        return " "
    
    return name.replace("_", " ").title()


def denormalize_name(name: str) -> str:
    if not isinstance(name, str):
        return " "
    
    return name.lower().replace(" ", "_")
