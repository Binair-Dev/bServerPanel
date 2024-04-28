from enum import Enum

class CommandType(Enum):
    LINK = "LINK"
    COMMAND_LINE = "COMMAND_LINE"
    ACCEPT_EULA = "ACCEPT_EULA"
    UNZIP = "UNZIP"