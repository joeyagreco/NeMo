from typing import List

import pandas as pd

from server.enums.DeviceRank import DeviceRank
from server.enums.Status import Status
from server.models.Device import Device
from server.models.DeviceFE import DeviceFE
from server.repositories.DeviceRepository import DeviceRepository
from server.repositories.PingRepository import PingRepository


class DeviceService:

    def __init__(self):
        self.deviceRepository = DeviceRepository()
        self.pingRepository = PingRepository()

    def getDevicesByDeviceRank(self, deviceRank: DeviceRank) -> List[Device]:
        d1 = DeviceFE("Router", DeviceRank.CRITICAL, "192.168.1.1", id="1",
                      lastAliveTimestamp=pd.Timestamp('2017-01-01T12'), status=Status.ONLINE)
        d2 = DeviceFE("Switch", DeviceRank.CRITICAL, "192.168.1.5", id="2",
                      lastAliveTimestamp=pd.Timestamp('2017-01-01T12'), status=Status.SHAKY)
        d3 = DeviceFE("JAccessPoint", DeviceRank.CRITICAL, "192.168.1.10", id="3",
                      lastAliveTimestamp=pd.Timestamp('2017-01-01T12'), status=Status.OFFLINE)
        devices = [d1, d2, d3]
        return devices

    def getAllDevices(self):
        # get all devices without pings
        allDevices = self.deviceRepository.getAllDevices()
        for device in allDevices:
            device.pings = self.pingRepository.getPingsByDeviceId(device.id)
        print(allDevices)
        return allDevices
