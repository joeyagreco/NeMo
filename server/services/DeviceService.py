import datetime
from typing import List

from server.models.DeviceBE import DeviceBE
from server.models.DeviceFE import DeviceFE
from server.repositories.DeviceRepository import DeviceRepository
from server.repositories.PingRepository import PingRepository


class DeviceService:

    def __init__(self):
        self.deviceRepository = DeviceRepository()
        self.pingRepository = PingRepository()

    def getAllDevicesFE(self) -> List[DeviceFE]:
        allDevicesBE = self.__getAllDevicesBE()
        allDevicesFE = list()
        for deviceBE in allDevicesBE:
            deviceFE = DeviceFE(deviceBE.name, deviceBE.rank, deviceBE.ipAddress, id=deviceBE.id)
            # set lastAliveTimestamp
            deviceFE.lastAliveTimestamp = self.__getLastAliveTimestampForDevice(deviceBE)
            allDevicesFE.append(deviceFE)

        return allDevicesFE

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
                print(type(timestamp))
        if timestamp is not None:
            # trim the timestamp for the front end
            timestamp = datetime.datetime(timestamp.year, timestamp.month, timestamp.day, timestamp.hour,
                                          timestamp.minute, timestamp.second)
        return timestamp
