from enum import Enum, unique, auto


@unique
class DeviceRank(Enum):
    CRITICAL = auto()
    KNOWN = auto()
    UNKNOWN = auto()

    @classmethod
    def list(cls):
        return list(map(lambda c: c, cls))
