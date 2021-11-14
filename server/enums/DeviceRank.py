from enum import Enum, unique, auto


@unique
class DeviceRank(Enum):
    CRITICAL = auto()
    KNOWN = auto()
    UNKNOWN = auto()

    @classmethod
    def list(cls):
        return list(map(lambda c: c, cls))

    @staticmethod
    def fromStr(label):
        if label.upper() in "CRITICAL":
            return DeviceRank.CRITICAL
        elif label.upper() in "KNOWN":
            return DeviceRank.KNOWN
        elif label.upper() in "UNKNOWN":
            return DeviceRank.UNKNOWN
        else:
            raise NotImplementedError
