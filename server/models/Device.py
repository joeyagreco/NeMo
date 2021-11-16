from server.enums.DeviceRank import DeviceRank


class Device:
    def __init__(self, name: str, rank: DeviceRank, ipAddress: str, **params):
        self.name = name
        self.rank = rank
        self.ipAddress = ipAddress
        # optional
        self.id = params.pop("id", None)

    def __str__(self):
        return f"id: {self.id}\nname: {self.name}\nrank: {self.rank}\nipAddress: {self.ipAddress}"

    def __repr__(self):
        return f"id: {self.id}\nname: {self.name}\nrank: {self.rank}\nipAddress: {self.ipAddress}"
