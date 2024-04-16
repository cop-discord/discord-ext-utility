from .color import *
from .message import *
from .converters import *
from .regex import *
from .globals import *

def apply() -> bool:
    from logging import getLogger
    logger = getLogger(__name__)
    logger.info(f"Setting up Overwrites..")
    from . import color, message, regex
    from .converters import channel, emoji, member, internal, message, role, user
    logger.info("Overwrites Set Successfully!")
    return True
    
