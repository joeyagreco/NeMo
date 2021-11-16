from server.enums.DeviceRank import DeviceRank
from server.models.Device import Device


class DeviceBE(Device):
    def __init__(self, name: str, rank: DeviceRank, ipAddress: str, **params):
        super().__init__(name, rank, ipAddress, **params)
        # optional
        self.pings = params.pop("pings", [])

    def __str__(self):
        return super().__str__() + f"\npings: {self.pings}"

    def __repr__(self):
        return super().__repr__() + f"\npings: {self.pings}"
