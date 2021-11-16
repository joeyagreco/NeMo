from server.enums.DeviceRank import DeviceRank
from server.models.Device import Device


class DeviceFE(Device):
    """
    This class is used by the front end... it holds values that are used by the backend and some are derived instead of explicitly stored
    """

    def __init__(self, name: str, rank: DeviceRank, ipAddress: str, **params):
        super().__init__(name, rank, ipAddress, **params)
        self.lastAliveTimestamp = params.pop("lastAliveTimestamp",
                                             None)  # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html
        self.status = params.pop("status", None)

    def __str__(self):
        return super().__str__() + f"\nlastAliveTimestamp: {self.lastAliveTimestamp}\nstatus: {self.status}"

    def __repr__(self):
        return super().__repr__() + f"\nlastAliveTimestamp: {self.lastAliveTimestamp}\nstatus: {self.status}"
