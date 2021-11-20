from server.models.Settings import Settings
from server.repositories.SettingsRepository import SettingsRepository


class SettingsService:

    def __init__(self):
        self.settingsRepository = SettingsRepository()

    def getSettings(self) -> Settings:
        return self.settingsRepository.getSettings()

    def updateSettings(self, settings: Settings) -> None:
        self.settingsRepository.updateSettings(settings)
