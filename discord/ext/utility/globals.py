from typing import Optional, Any
GLOBALS = {}

def set_global(name: str, value: Any):
    GLOBALS[name] = value

def get_global(name: str):
    try:
        return GLOBALS[name]
    except:
        raise ValueError(f"Global {name} hasn't been set")