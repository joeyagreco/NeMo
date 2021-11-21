import datetime
from typing import List

from server.enums.DeviceRank import DeviceRank
from server.enums.Status import Status
from server.models.DeviceBE import DeviceBE
from server.models.DeviceFE import DeviceFE
from server.models.DevicesWrapper import DevicesWrapper
from server.repositories.DeviceRepository import DeviceRepository
from server.repositories.PingRepository import PingRepository
from server.services.SettingsService import SettingsService


class DeviceService:

    def __init__(self):
        self.deviceRepository = DeviceRepository()
        self.pingRepository = PingRepository()
        self.settingsService = SettingsService()

    def getDevicesWrapper(self):
        allDevices = self.getAllDevicesFE()
        criticalDevices = list()
        knownDevices = list()
        unknownDevices = list()
        for device in allDevices:
            if device.rank == DeviceRank.CRITICAL:
                criticalDevices.append(device)
            elif device.rank == DeviceRank.KNOWN:
                knownDevices.append(device)
            else:
                unknownDevices.append(device)
        return DevicesWrapper(criticalDevices, knownDevices, unknownDevices)

    def getAllDevicesFE(self) -> List[DeviceFE]:
        allDevicesBE = self.__getAllDevicesBE()
        allDevicesFE = list()
        for deviceBE in allDevicesBE:
            deviceFE = DeviceFE(deviceBE.name, deviceBE.rank, deviceBE.ipAddress, id=deviceBE.id)
            # set lastAliveTimestamp
            deviceFE.lastAliveTimestamp = self.__getLastAliveTimestampForDevice(deviceBE)
            # set status
            deviceFE.status = self.__getStatusOfDevice(deviceBE)
            allDevicesFE.append(deviceFE)
        return allDevicesFE

    def updateDevice(self, device: DeviceBE) -> None:
        self.deviceRepository.updateDevice(device)

    def addDevice(self, device: DeviceBE) -> None:
        self.deviceRepository.addDevice(device)

    def deleteDevice(self, deviceId: int) -> None:
        self.deviceRepository.deleteDevice(deviceId)

    def __getAllDevicesBE(self) -> List[DeviceBE]:
        # get all devices without pings
        allDevices = self.deviceRepository.getAllDevices()
        # get the pings for each device and set them
        for device in allDevices:
            device.pings = self.pingRepository.getPingsByDeviceId(device.id)
        return allDevices

    @staticmethod
    def __getLastAliveTimestampForDevice(device: DeviceBE) -> datetime:
        """
        Returns the most recent ping timestamp for the given device.
        """
        timestamp = None
        for ping in device.pings:
            if timestamp is None or ping.timestamp > timestamp:
                timestamp = ping.timestamp
        if timestamp is not None:
            # trim the timestamp for the front end
            timestamp = datetime.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour,
                                          timestamp.minute, timestamp.second)
        return timestamp

    def __getStatusOfDevice(self, device: DeviceBE) -> Status:
        """
        Checks if the percentage of "alive" pings in this device meets the ping online threshold.
        """
        # default to offline if a device has no pings
        status = Status.OFFLINE
        if device.pings:
            alivePingCount = 0
            for ping in device.pings:
                if ping.success:
                    alivePingCount += 1
            # get ping online threshold
            pingOnlineThresholdPercentage = self.settingsService.getSettings().pingOnlineThresholdPercentage
            # dont have to worry about division by 0 here since pings will always have at least 1 in the list at this point
            actualOnlinePercentage = (alivePingCount / len(device.pings)) * 100
            if actualOnlinePercentage >= pingOnlineThresholdPercentage:
                status = Status.ONLINE
            elif actualOnlinePercentage > 0:
                status = Status.SHAKY
        return status
