from pandas import Timestamp


class Ping:
    def __init__(self, success: bool, timestamp: Timestamp):
        self.success = success
        self.timestamp = timestamp

    def __str__(self):
        return f"success: {self.success}\ntimestamp: {self.timestamp}"

    def __repr__(self):
        return f"success: {self.success}\ntimestamp: {self.timestamp}"
