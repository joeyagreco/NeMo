import datetime
import unittest
from unittest.mock import patch

from server.enums.DeviceRank import DeviceRank
from server.enums.Status import Status
from server.models.DeviceBE import DeviceBE
from server.models.Ping import Ping
from server.models.Settings import Settings
from server.services.DeviceService import DeviceService


class Test_DeviceService(unittest.TestCase):

    def setUp(self):
        self.deviceService = DeviceService()

    @patch("server.services.DeviceService.DeviceRepository.getAllDevices")
    @patch("server.services.DeviceService.PingRepository.getPingsByDeviceId")
    @patch("server.services.DeviceService.SettingsService.getSettings")
    def test_getAllDevicesFE_happyPath(self, mockGetSettings, mockGetPingsByDeviceId, mockGetAllDevices):
        dummyDeviceBE = DeviceBE("n", DeviceRank.CRITICAL, "1.1.1.1", id=1)
        dummyPing1 = Ping(True, datetime.datetime(2020, 1, 2, 10, 11, 12, 13))
        dummyPing2 = Ping(True, datetime.datetime(2020, 1, 2, 10, 11, 13, 13))
        dummySettings = Settings(None, 50, None, None, None, None)
        mockGetAllDevices.return_value = [dummyDeviceBE]
        mockGetPingsByDeviceId.return_value = [dummyPing1, dummyPing2]
        mockGetSettings.return_value = dummySettings
        response = self.deviceService.getAllDevicesFE()
        self.assertEqual(1, len(response))
        self.assertEqual("n", response[0].name)
        self.assertEqual(DeviceRank.CRITICAL, response[0].rank)
        self.assertEqual("1.1.1.1", response[0].ipAddress)
        self.assertEqual(1, response[0].id)
        self.assertTrue(datetime.datetime(2020, 1, 2, 10, 11, 13) == response[0].lastAliveTimestamp)
        self.assertEqual(Status.ONLINE, response[0].status)

    @patch("server.services.DeviceService.DeviceRepository.getAllDevices")
    @patch("server.services.DeviceService.PingRepository.getPingsByDeviceId")
    @patch("server.services.DeviceService.SettingsService.getSettings")
    def test_getAllDevicesFE_noPingsForDevice_setsLastAliveTimestampToNone(self, mockGetSettings,
                                                                           mockGetPingsByDeviceId,
                                                                           mockGetAllDevices):
        dummyDeviceBE = DeviceBE("n", DeviceRank.CRITICAL, "1.1.1.1", id=1)
        dummySettings = Settings(None, 50, None, None, None, None)
        mockGetAllDevices.return_value = [dummyDeviceBE]
        mockGetPingsByDeviceId.return_value = []
        mockGetSettings.return_value = dummySettings
        response = self.deviceService.getAllDevicesFE()
        self.assertIsNone(response[0].lastAliveTimestamp)
