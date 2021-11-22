from typing import List

from server.decorators.utilDecorators import timeMethod
from server.models.DeviceBE import DeviceBE
from server.models.DeviceUpdateWrapper import DeviceUpdateWrapper
from server.util.Pinger import Pinger


class DeviceUpdater:
    """
    This class takes devices, determines if they need to be updated, and updates them if so.
    """

    def __init__(self):
        pass

    @timeMethod
    def getDeviceUpdateWrapper(self, devices: List[DeviceBE]) -> DeviceUpdateWrapper:
        """
        Updates the devices from the given list that need to be pinged and splits them from the devices that do not need to be pinged.
        """
        # split up devices
        deviceUpdateWrapper = self.__splitDevices(devices)
        # ping devices that need to be pinged
        self.__pingDevices(deviceUpdateWrapper.toUpdateDevices)
        return deviceUpdateWrapper

    @timeMethod
    def __splitDevices(self, devices: List[DeviceBE]) -> DeviceUpdateWrapper:
        """
        Determines which devices need to be pinged and separates them from the devices that do not need to be pinged.
        """
        toUpdateDevices = list()
        toNotUpdateDevices = list()
        # TODO add rules to check which devices should be updated
        toUpdateDevices = devices
        return DeviceUpdateWrapper(toUpdateDevices, toNotUpdateDevices)

    @timeMethod
    def __pingDevices(self, devices: List[DeviceBE]):
        for device in devices:
            ping = Pinger.ping(device.ipAddress)
            device.pings.append(ping)
