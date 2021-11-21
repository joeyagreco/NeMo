from server.models.DeviceFE import DeviceFE
from server.repositories.DeviceRepository import DeviceRepository
from server.repositories.PingRepository import PingRepository


class DeviceService:

    def __init__(self):
        self.deviceRepository = DeviceRepository()
        self.pingRepository = PingRepository()

    def getAllDevices(self):
        # get all devices without pings
        allDevices = self.deviceRepository.getAllDevices()
        for device in allDevices:
            device.pings = self.pingRepository.getPingsByDeviceId(device.id)
        print(allDevices)
        return allDevices

    def tmp(self):
        allDevicesBE = self.getAllDevices()
        allDevicesFE = list()
        for deviceBE in allDevicesBE:
            allDevicesFE.append(DeviceFE(deviceBE.name, deviceBE.rank, deviceBE.ipAddress, id=deviceBE.id))
        return allDevicesFE
