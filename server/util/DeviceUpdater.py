from typing import List

from server.models.DeviceBE import DeviceBE
from server.models.DeviceUpdateWrapper import DeviceUpdateWrapper
from server.util.Pinger import Pinger


class DeviceUpdater:
    """
    This class takes devices, determines if they need to be updated, and updates them if so.
    """

    def __init__(self):
        pass

    def getDeviceUpdateWrapper(self, devices: List[DeviceBE]) -> DeviceUpdateWrapper:
        """
        Updates the devices from the given list that need to be pinged and splits them from the devices that do not need to be pinged.
        """
        # split up devices
        deviceUpdateWrapper = self.__splitDevices(devices)
        # ping devices that need to be pinged
        self.__pingDevices(deviceUpdateWrapper.toUpdateDevices)
        return deviceUpdateWrapper

    def __splitDevices(self, devices: List[DeviceBE]) -> DeviceUpdateWrapper:
        """
        Determines which devices need to be pinged and separates them from the devices that do not need to be pinged.
        """
        toUpdateDevices = list()
        toNotUpdateDevices = list()
        # TODO add rules to check which devices should be updated
        toUpdateDevices = devices
        return DeviceUpdateWrapper(toUpdateDevices, toNotUpdateDevices)

    def __pingDevices(self, devices: List[DeviceBE]):
        for device in devices:
            pingResponse = Pinger.ping(device.ipAddress)
            print(pingResponse)
        test = Pinger.ping("192.168.1.201")
        print(test)
