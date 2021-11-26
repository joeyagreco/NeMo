class IPRange:

    def __init__(self, id: int, rangeStart: str, rangeEnd: str):
        self.id = id
        self.rangeStart = rangeStart
        self.rangeEnd = rangeEnd

    def __str__(self):
        return f"\nid: {self.id}\nrangeStart: {self.rangeStart}\nrangeEnd: {self.rangeEnd}"

    def __repr__(self):
        return f"\nid: {self.id}\nrangeStart: {self.rangeStart}\nrangeEnd: {self.rangeEnd}"
