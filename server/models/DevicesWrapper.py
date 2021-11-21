from typing import List

from server.models.DeviceFE import DeviceFE


class DevicesWrapper:
    """
    This class is used to hold and separate the various ranks of devices.
    """

    def __init__(self, criticalDevices: List[DeviceFE], knownDevices: List[DeviceFE], unknownDevices: List[DeviceFE]):
        self.criticalDevices = criticalDevices
        self.knownDevices = knownDevices
        self.unknownDevices = unknownDevices
