import unittest
from unittest.mock import patch

from server.models.Settings import Settings
from server.services.SettingsService import SettingsService


class Test_SettingsService(unittest.TestCase):

    def setUp(self):
        self.settingsService = SettingsService()

    @patch("server.services.SettingsService.SettingsRepository.getSettings")
    def test_getSettings_happyPath(self, mockGetSettings):
        dummySettings = Settings(1, 2, 3, 4, 5, 6)
        mockGetSettings.return_value = dummySettings
        response = self.settingsService.getSettings()
        self.assertEqual(1, response.pingsToSave)
        self.assertEqual(2, response.pingOnlineThresholdPercentage)
        self.assertEqual(3, response.pageRefreshFrequencySeconds)
        self.assertEqual(4, response.pingCriticalRefreshFrequencySeconds)
        self.assertEqual(5, response.pingKnownRefreshFrequencySeconds)
        self.assertEqual(6, response.pingScanFrequencySeconds)

    @patch("server.services.SettingsService.SettingsRepository.updateSettings")
    def test_updateSettings_happyPath(self, mockUpdateSettings):
        dummySettings = Settings(1, 2, 3, 4, 5, 6)
        self.settingsService.updateSettings(dummySettings)
        mockUpdateSettings.assert_called_once_with(dummySettings)
