from enum import Enum

class CommandType(Enum):
    LINK = "LINK"
    COMMAND_LINE = "COMMAND_LINE"
    ACCEPT_EULA = "ACCEPT_EULA"
    UNZIP = "UNZIP"
    OS_COMMAND = "OS_COMMAND"
    PROGRAM_COMMAND = "PROGRAM_COMMAND"
    KILL = "KILL"