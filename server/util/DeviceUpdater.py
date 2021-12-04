import threading
from typing import List

from server.decorators.utilDecorators import timer
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

    def getLiveDevices(self, devices: List[DeviceBE]) -> List[DeviceBE]:
        """
        pings all the given devices and returns a list of devices that are alive
        """
        self.__pingDevices(devices)
        # check which devices most recent ping is alive and add them to a list
        liveDevices = list()
        for device in devices:
            if len(device.pings) >= 1 and device.pings[-1].success:
                liveDevices.append(device)
        return liveDevices

    @staticmethod
    def __splitDevices(devices: List[DeviceBE]) -> DeviceUpdateWrapper:
        """
        Determines which devices need to be pinged and separates them from the devices that do not need to be pinged.
        """
        toUpdateDevices = list()
        toNotUpdateDevices = list()
        # TODO add rules to check which devices should be updated
        toUpdateDevices = devices
        return DeviceUpdateWrapper(toUpdateDevices, toNotUpdateDevices)

    @timer
    def __pingDevices(self, devices: List[DeviceBE]) -> None:
        # use threading to speed up pinging all devices
        # create threads, start them, and put them into a list
        threads = list()
        for device in devices:
            thread = threading.Thread(target=self.__pingAndUpdate, args=(device,))
            thread.start()
            threads.append(thread)
        # join all of the threads
        for thread in threads:
            thread.join()

    @staticmethod
    def __pingAndUpdate(device: DeviceBE) -> None:
        # a helper method
        # calls the ping() method and adds the resulting ping response to the list of pings in the given device
        ping = Pinger.ping(device.ipAddress)
        device.pings.append(ping)
