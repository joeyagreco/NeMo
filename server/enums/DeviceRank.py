from enum import Enum, unique, auto


@unique
class DeviceRank(Enum):
    CRITICAL = auto()
    KNOWN = auto()
    UNKNOWN = auto()
