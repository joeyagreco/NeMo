import datetime

from pythonping import ping
from pythonping.executor import ResponseList

from server.models.Ping import Ping


class Pinger:
    """
    Uses this library: https://pypi.org/project/pythonping/
    """

    @classmethod
    def ping(cls, ip: str) -> Ping:
        # pings the given IP Address once
        return cls.__wrapPing(ping(ip, verbose=False, count=1))

    @classmethod
    def __wrapPing(cls, pingResponse: ResponseList) -> Ping:
        """
        This takes a pingResponse that sends out 1 packet, if that packet is lost, the ping was a failure
        """
        newPing = Ping(pingResponse.packets_lost == 0, cls.__getCurrentTimestamp())
        return newPing

    @staticmethod
    def __getCurrentTimestamp() -> datetime:
        return datetime.datetime.now()
