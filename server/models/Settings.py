class Settings:
    def __init__(self,
                 pingsToSave: int,
                 pingOnlineThresholdPercentage: int,
                 pageRefreshFrequencySeconds: int,
                 pingCriticalRefreshFrequencySeconds: int,
                 pingKnownRefreshFrequencySeconds: int,
                 pingScanFrequencySeconds: int):
        self.pingsToSave = pingsToSave
        self.pingOnlineThresholdPercentage = pingOnlineThresholdPercentage
        self.pageRefreshFrequencySeconds = pageRefreshFrequencySeconds
        self.pingCriticalRefreshFrequencySeconds = pingCriticalRefreshFrequencySeconds
        self.pingKnownRefreshFrequencySeconds = pingKnownRefreshFrequencySeconds
        self.pingScanFrequencySeconds = pingScanFrequencySeconds

    def __str__(self):
        return f"\npingsToSave: {self.pingsToSave}\npingOnlineThresholdPercentage: {self.pingOnlineThresholdPercentage}\npageRefreshFrequencySeconds: {self.pageRefreshFrequencySeconds}\npingCriticalRefreshFrequencySeconds: {self.pingCriticalRefreshFrequencySeconds}\npingKnownRefreshFrequencySeconds: {self.pingKnownRefreshFrequencySeconds}\npingScanFrequencySeconds: {self.pingScanFrequencySeconds}"

    def __repr__(self):
        return f"\npingsToSave: {self.pingsToSave}\npingOnlineThresholdPercentage: {self.pingOnlineThresholdPercentage}\npageRefreshFrequencySeconds: {self.pageRefreshFrequencySeconds}\npingCriticalRefreshFrequencySeconds: {self.pingCriticalRefreshFrequencySeconds}\npingKnownRefreshFrequencySeconds: {self.pingKnownRefreshFrequencySeconds}\npingScanFrequencySeconds: {self.pingScanFrequencySeconds}"
