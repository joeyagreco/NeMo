import unittest
from unittest.mock import patch

from server.repositories.DeviceRepository import DeviceRepository
from server.repositories.PingRepository import PingRepository
from server.services.DeviceService import DeviceService


class Test_DeviceService(unittest.TestCase):

    def setUp(self):
        self.deviceService = DeviceService()

    @patch.object(DeviceRepository, "getAllDevices", return_value=[])
    @patch.object(PingRepository, "getPingsByDeviceId", return_value=[])
    def test_test(self, deviceRepositoryMock, pingRepositoryMock):
        print(self.deviceService.getAllDevicesFE())
        self.assertTrue(True)
