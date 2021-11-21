from pythonping import ping
from pythonping.executor import ResponseList


class Pinger:
    """
    Uses this library: https://pypi.org/project/pythonping/
    """

    @staticmethod
    def ping(ip: str, **kwargs) -> ResponseList:
        count = kwargs.pop("count", 1)
        verbose = kwargs.pop("verbose", False)
        return ping(ip, verbose=verbose, count=count)
