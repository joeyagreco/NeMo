class Settings:
    def __init__(self, pingsToSave: int, pingOnlineThreshold: int, pageRefreshFrequency: int,
                 pingCriticalRefreshFrequency: int, pingKnownRefreshFrequency: int, pingScanFrequency: int):
        self.pingsToSave = pingsToSave
        self.pingOnlineThreshold = pingOnlineThreshold
        self.pageRefreshFrequency = pageRefreshFrequency
        self.pingCriticalRefreshFrequency = pingCriticalRefreshFrequency
        self.pingKnownRefreshFrequency = pingKnownRefreshFrequency
        self.pingScanFrequency = pingScanFrequency

    def __str__(self):
        return f"pingsToSave: {self.pingsToSave}\npingOnlineThreshold: {self.pingOnlineThreshold}\npageRefreshFrequency: {self.pageRefreshFrequency}\npingCriticalRefreshFrequency: {self.pingCriticalRefreshFrequency}\npingKnownRefreshFrequency: {self.pingKnownRefreshFrequency}\npingScanFrequency: {self.pingScanFrequency}"

    def __repr__(self):
        return f"pingsToSave: {self.pingsToSave}\npingOnlineThreshold: {self.pingOnlineThreshold}\npageRefreshFrequency: {self.pageRefreshFrequency}\npingCriticalRefreshFrequency: {self.pingCriticalRefreshFrequency}\npingKnownRefreshFrequency: {self.pingKnownRefreshFrequency}\npingScanFrequency: {self.pingScanFrequency}"
