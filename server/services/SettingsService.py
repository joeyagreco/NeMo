from server.models.Settings import Settings
from server.repositories.SettingsRepository import SettingsRepository


class SettingsService:

    def __init__(self):
        self.settingsRepository = SettingsRepository()

    def getSettings(self) -> Settings:
        settings = Settings(10, 90, 10, 10, 30, 60)
        return settings
