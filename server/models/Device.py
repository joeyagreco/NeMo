from server.enums.DeviceRank import DeviceRank


class Device:
    def __init__(self, name: str, rank: DeviceRank, ipAddress: str, **params):
        self.name = name
        self.rank = rank
        self.ipAddress = ipAddress
        self.id = params.pop("id", None)
        self.lastAliveTimestamp = params.pop("lastAliveTimestamp",
                                             None)  # https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Timestamp.html
        self.pings = params.pop("pings", [])

    def __str__(self):
        return f"id: {self.id}\nname: {self.name}\nrank: {self.rank}\nipAddress: {self.ipAddress}\nlastAliveTimestamp: {self.lastAliveTimestamp}\npings: {self.pings}"

    def __repr__(self):
        return f"id: {self.id}\nname: {self.name}\nrank: {self.rank}\nipAddress: {self.ipAddress}\nlastAliveTimestamp: {self.lastAliveTimestamp}\npings: {self.pings}"
