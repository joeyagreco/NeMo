from datetime import datetime


class Ping:
    def __init__(self, id: int, success: bool, timestamp: datetime):
        self.id = id
        self.success = success
        self.timestamp = timestamp

    def __str__(self):
        return f"\nid: {self.id}\nsuccess: {self.success}\ntimestamp: {self.timestamp}"

    def __repr__(self):
        return f"\nid: {self.id}\nsuccess: {self.success}\ntimestamp: {self.timestamp}"
