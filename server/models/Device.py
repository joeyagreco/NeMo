from dataclasses import dataclass

from pandas import Timestamp


@dataclass
class Device:
    id: str
    name: str
    ipAddress: str
    lastAliveTimestamp: Timestamp  # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html
