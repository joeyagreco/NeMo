import datetime
from typing import List

from server.enums.DeviceRank import DeviceRank
from server.enums.Status import Status
from server.models.DeviceBE import DeviceBE
from server.models.DeviceFE import DeviceFE
from server.models.DevicesWrapper import DevicesWrapper
from server.repositories.DeviceAndPingRepository import DeviceAndPingRepository
from server.services.IPRangeService import IPRangeService
from server.services.SettingsService import SettingsService
from server.util.DeviceUpdater import DeviceUpdater


class DeviceService:

    def __init__(self):
        self.__deviceAndPingRepository = DeviceAndPingRepository()
        self.__settingsService = SettingsService()
        self.__ipRangeService = IPRangeService()
        self.__deviceUpdater = DeviceUpdater()
        self.__settings = self.__settingsService.getSettings()

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
        allDevicesBE = self.__getAllUpdatedDevicesBE()
        allDevicesFE = list()
        for deviceBE in allDevicesBE:
            deviceFE = DeviceFE(deviceBE.name, deviceBE.rank, deviceBE.ipAddress, id=deviceBE.id)
            # set lastAliveTimestamp
            lastAliveTimestamp = self.__getLastAliveTimestampForDevice(deviceBE)
            # format lastAliveTimestamp to be more readable in the UI
            # strftime formatting: https://www.programiz.com/python-programming/datetime/strftime
            # works on windows machines only: https://stackoverflow.com/questions/9525944/python-datetime-formatting-without-zero-padding
            deviceFE.lastAliveTimestamp = lastAliveTimestamp.strftime("%a. %#m/%#d %#I:%M %p")
            # set status
            deviceFE.status = self.__getStatusOfDevice(deviceBE)
            allDevicesFE.append(deviceFE)
        return allDevicesFE

    def updateDeviceAndItsPings(self, device: DeviceBE) -> None:
        # if number of pings for this device is less than the amount of pings we want to save,
        # just add all of the pings that do NOT have an id
        # if the number of pings for this device is greater than the amount of pings we want to save,
        # we delete the excess pings starting with the OLDEST pings and add the pings that do NOT have an id
        difference = abs(self.__settings.pingsToSave - len(device.pings))
        self.__deviceAndPingRepository.updateDeviceAndItsPings(device, difference)

    def addDeviceAndItsPings(self, device: DeviceBE) -> None:
        # add device
        self.__deviceAndPingRepository.addDeviceAndItsPings(device)

    def deleteDeviceAndItsPingsByDeviceId(self, deviceId: int) -> None:
        # delete device
        self.__deviceAndPingRepository.deleteDeviceAndItsPings(deviceId)

    def __getAllUpdatedDevicesBE(self) -> List[DeviceBE]:
        # first, get all critical and known devices
        allDevices = self.__deviceAndPingRepository.getAllDevicesAndTheirPings()
        # now we need to update the devices before returning them
        deviceUpdateWrapper = self.__deviceUpdater.getDeviceUpdateWrapper(allDevices)
        # update devices that need to be updated in the database
        for device in deviceUpdateWrapper.toUpdateDevices:
            self.updateDeviceAndItsPings(device)
        # get all devices in ranges we want to scan and add it to our list
        allUnknownDevices = self.__getAllLiveDevicesInIPRanges()
        return deviceUpdateWrapper.toUpdateDevices + deviceUpdateWrapper.toNotUpdateDevices + allUnknownDevices

    def __getAllLiveDevicesInIPRanges(self) -> List[DeviceBE]:
        # first, get all devices that can appear from any ip range
        ipRanges = self.__ipRangeService.getAllIPRanges()
        # next, get all the possible devices that could appear in this range
        ipRangeDevices = list()
        for ipRange in ipRanges:
            ipRangeDevices += self.__ipRangeService.getAllDevicesFromIPRange(ipRange)
        # ping all devices and get the ones that are alive
        liveDevices = self.__deviceUpdater.getLiveDevices(ipRangeDevices)
        return liveDevices

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
            pingOnlineThresholdPercentage = self.__settings.pingOnlineThresholdPercentage
            # dont have to worry about division by 0 here since pings will always have at least 1 in the list at this point
            actualOnlinePercentage = (alivePingCount / len(device.pings)) * 100
            if actualOnlinePercentage >= pingOnlineThresholdPercentage:
                status = Status.ONLINE
            elif actualOnlinePercentage > 0:
                status = Status.SHAKY
        return status
