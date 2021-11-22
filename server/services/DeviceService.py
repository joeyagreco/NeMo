import datetime
from typing import List

from server.decorators.utilDecorators import timeMethod
from server.enums.DeviceRank import DeviceRank
from server.enums.Status import Status
from server.models.DeviceBE import DeviceBE
from server.models.DeviceFE import DeviceFE
from server.models.DevicesWrapper import DevicesWrapper
from server.repositories.DeviceRepository import DeviceRepository
from server.repositories.PingRepository import PingRepository
from server.services.SettingsService import SettingsService
from server.util.DeviceUpdater import DeviceUpdater


class DeviceService:

    def __init__(self):
        self.deviceRepository = DeviceRepository()
        self.pingRepository = PingRepository()
        self.settingsService = SettingsService()
        self.deviceUpdater = DeviceUpdater()

    @timeMethod
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

    @timeMethod
    def getAllDevicesFE(self) -> List[DeviceFE]:
        allDevicesBE = self.__getAllUpdatedDevicesBE()
        allDevicesFE = list()
        for deviceBE in allDevicesBE:
            deviceFE = DeviceFE(deviceBE.name, deviceBE.rank, deviceBE.ipAddress, id=deviceBE.id)
            # set lastAliveTimestamp
            deviceFE.lastAliveTimestamp = self.__getLastAliveTimestampForDevice(deviceBE)
            # set status
            deviceFE.status = self.__getStatusOfDevice(deviceBE)
            allDevicesFE.append(deviceFE)
        return allDevicesFE

    @timeMethod
    def updateDeviceAndItsPings(self, device: DeviceBE) -> None:
        # update pings
        # if number of pings for this device is less than the amount of pings we want to save,
        # just add all of the pings that do NOT have an id
        # if the number of pings for this device is greater than the amount of pings we want to save,
        # we delete the excess pings starting with the OLDEST pings and add the pings that do NOT have an id
        numberOfPingsToSave = self.settingsService.getSettings().pingsToSave
        difference = numberOfPingsToSave - len(device.pings)
        if difference < 0:
            # delete excess pings
            self.pingRepository.deleteOldestPingsByDeviceId(device.id, abs(difference))
        # add all of the pings that do NOT have an id
        for ping in device.pings:
            if ping.id is None:
                self.pingRepository.addPing(ping, device.id)
        # update device
        self.deviceRepository.updateDevice(device)

    @timeMethod
    def addDeviceAndItsPings(self, device: DeviceBE) -> None:
        # add device
        newDeviceId = self.deviceRepository.addDevice(device)
        # add device pings
        for ping in device.pings:
            self.pingRepository.addPing(ping, newDeviceId)

    def deleteDeviceAndItsPingsByDeviceId(self, deviceId: int) -> None:
        # delete pings in device first
        self.pingRepository.deletePingsByDeviceId(deviceId)
        # delete device
        self.deviceRepository.deleteDevice(deviceId)

    @timeMethod
    def __getAllUpdatedDevicesBE(self) -> List[DeviceBE]:
        # first, get all devices without pings
        allDevices = self.deviceRepository.getAllDevices()
        # next, get the pings for each device and set them
        for device in allDevices:
            device.pings = self.pingRepository.getPingsByDeviceId(device.id)
        # now that we have all of the devices, we need to update them before returning them
        deviceUpdateWrapper = self.deviceUpdater.getDeviceUpdateWrapper(allDevices)
        # update devices that need to be updated in the database
        for device in deviceUpdateWrapper.toUpdateDevices:
            self.updateDeviceAndItsPings(device)
        return deviceUpdateWrapper.toUpdateDevices + deviceUpdateWrapper.toNotUpdateDevices

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

    @timeMethod
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
