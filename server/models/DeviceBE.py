from server.enums.DeviceRank import DeviceRank
from server.models.Device import Device


class DeviceBE(Device):
    """
    This class is used exclusively by the backend... it shadows what information is stored about this device in the database
    """

    def __init__(self, name: str, rank: DeviceRank, ipAddress: str, **params):
        super().__init__(name, rank, ipAddress, **params)
        # optional
        self.pings = params.pop("pings", [])  # List[Ping]

    def __str__(self):
        return super().__str__() + f"\npings: {self.pings}"

    def __repr__(self):
        return super().__repr__() + f"\npings: {self.pings}"
