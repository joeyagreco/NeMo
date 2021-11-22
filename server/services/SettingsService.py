from server.decorators.utilDecorators import timeMethod
from server.models.Settings import Settings
from server.repositories.SettingsRepository import SettingsRepository


class SettingsService:

    def __init__(self):
        self.settingsRepository = SettingsRepository()

    @timeMethod
    def getSettings(self) -> Settings:
        return self.settingsRepository.getSettings()

    @timeMethod
    def updateSettings(self, settings: Settings) -> None:
        self.settingsRepository.updateSettings(settings)
