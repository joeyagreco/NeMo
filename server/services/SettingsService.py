from server.decorators.utilDecorators import timer
from server.models.Settings import Settings
from server.repositories.SettingsRepository import SettingsRepository


class SettingsService:

    def __init__(self):
        self.settingsRepository = SettingsRepository()

    @timer
    def getSettings(self) -> Settings:
        return self.settingsRepository.getSettings()

    @timer
    def updateSettings(self, settings: Settings) -> None:
        self.settingsRepository.updateSettings(settings)
