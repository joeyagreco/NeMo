from enum import Enum, unique, auto


@unique
class Status(Enum):
    ONLINE = auto()
    SHAKY = auto()
    OFFLINE = auto()

    @classmethod
    def list(cls):
        return list(map(lambda c: c, cls))

    @staticmethod
    def fromStr(label):
        if label.upper() in "ONLINE":
            return Status.ONLINE
        elif label.upper() in "SHAKY":
            return Status.SHAKY
        elif label.upper() in "OFFLINE":
            return Status.OFFLINE
        else:
            raise NotImplementedError
