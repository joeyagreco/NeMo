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
    def test_getAllDevicesFE_noPingsForDevice_setsLastAliveTimestampToNone_setsStatusToOffline(self, mockGetSettings,
                                                                                               mockGetPingsByDeviceId,
                                                                                               mockGetAllDevices):
        dummyDeviceBE = DeviceBE("n", DeviceRank.CRITICAL, "1.1.1.1", id=1)
        dummySettings = Settings(None, 50, None, None, None, None)
        mockGetAllDevices.return_value = [dummyDeviceBE]
        mockGetPingsByDeviceId.return_value = []
        mockGetSettings.return_value = dummySettings
        response = self.deviceService.getAllDevicesFE()
        self.assertIsNone(response[0].lastAliveTimestamp)
        self.assertEqual(Status.OFFLINE, response[0].status)

    @patch("server.services.DeviceService.DeviceRepository.getAllDevices")
    @patch("server.services.DeviceService.PingRepository.getPingsByDeviceId")
    @patch("server.services.DeviceService.SettingsService.getSettings")
    def test_getAllDevicesFE_percentageOfPingsAliveGreaterThanZeroButBelowOnlineThresholdPercentage_setsStatusToShaky(
            self,
            mockGetSettings,
            mockGetPingsByDeviceId,
            mockGetAllDevices):
        dummyDeviceBE = DeviceBE("n", DeviceRank.CRITICAL, "1.1.1.1", id=1)
        dummyPing1 = Ping(True, datetime.datetime(2020, 1, 2, 10, 11, 12, 13))
        dummyPing2 = Ping(False, datetime.datetime(2020, 1, 2, 10, 11, 12, 13))
        dummyPing3 = Ping(False, datetime.datetime(2020, 1, 2, 10, 11, 12, 13))
        dummySettings = Settings(None, 50, None, None, None, None)
        mockGetAllDevices.return_value = [dummyDeviceBE]
        mockGetPingsByDeviceId.return_value = [dummyPing1, dummyPing2, dummyPing3]
        mockGetSettings.return_value = dummySettings
        response = self.deviceService.getAllDevicesFE()
        self.assertEqual(Status.SHAKY, response[0].status)

    @patch("server.services.DeviceService.DeviceRepository.getAllDevices")
    @patch("server.services.DeviceService.PingRepository.getPingsByDeviceId")
    @patch("server.services.DeviceService.SettingsService.getSettings")
    def test_getDevicesWrapper_happyPath(self, mockGetSettings, mockGetPingsByDeviceId, mockGetAllDevices):
        dummyDeviceBECritical = DeviceBE("c", DeviceRank.CRITICAL, "1.1.1.1", id=1)
        dummyDeviceBEKnown = DeviceBE("k", DeviceRank.KNOWN, "2.2.2.2", id=2)
        dummyDeviceBEUnknown = DeviceBE("u", DeviceRank.UNKNOWN, "2.2.2.2", id=3)
        dummySettings = Settings(None, 50, None, None, None, None)
        mockGetAllDevices.return_value = [dummyDeviceBECritical, dummyDeviceBEKnown, dummyDeviceBEUnknown]
        mockGetPingsByDeviceId.return_value = []
        mockGetSettings.return_value = dummySettings
        response = self.deviceService.getDevicesWrapper()
        self.assertEqual(1, len(response.criticalDevices))
        self.assertEqual(1, len(response.knownDevices))
        self.assertEqual(1, len(response.unknownDevices))
        self.assertEqual(1, response.criticalDevices[0].id)
        self.assertEqual(2, response.knownDevices[0].id)
        self.assertEqual(3, response.unknownDevices[0].id)

    @patch("server.services.DeviceService.DeviceRepository.updateDevice")
    def test_updateDevice_happyPath(self, mockUpdateDevice):
        dummyDeviceBE = DeviceBE("n", DeviceRank.CRITICAL, "1.1.1.1", id=1)
        self.deviceService.updateDevice(dummyDeviceBE)
        mockUpdateDevice.assert_called_once_with(dummyDeviceBE)

    @patch("server.services.DeviceService.DeviceRepository.addDevice")
    def test_addDevice_happyPath(self, mockAddDevice):
        dummyDeviceBE = DeviceBE("n", DeviceRank.CRITICAL, "1.1.1.1", id=1)
        self.deviceService.addDeviceWithPings(dummyDeviceBE)
        mockAddDevice.assert_called_once_with(dummyDeviceBE)

    @patch("server.services.DeviceService.DeviceRepository.deleteDevice")
    def test_deleteDevice_happyPath(self, mockDeleteDevice):
        self.deviceService.deleteDeviceAndPingsByDeviceId(1)
        mockDeleteDevice.assert_called_once_with(1)
