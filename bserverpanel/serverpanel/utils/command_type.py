from enum import Enum

class CommandType(Enum):
    LINK = "LINK"
    ACCEPT_EULA = "ACCEPT_EULA"
    UNZIP = "UNZIP"
    OS_COMMAND = "OS_COMMAND"
    PROGRAM_COMMAND = "PROGRAM_COMMAND"
    KILL = "KILL"
    SHELL_SCRIPT = "SHELL_SCRIPT"
    WAIT = "WAIT"