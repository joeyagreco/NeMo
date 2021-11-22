from typing import List

from server.models.DeviceBE import DeviceBE


class DeviceUpdateWrapper:

    def __init__(self, toUpdateDevices: List[DeviceBE], toNotUpdateDevices: List[DeviceBE]):
        self.toUpdateDevices = toUpdateDevices
        self.toNotUpdateDevices = toNotUpdateDevices
