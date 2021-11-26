from typing import List

from server.enums.DeviceRank import DeviceRank
from server.models.DeviceBE import DeviceBE
from server.models.IPRange import IPRange
from server.repositories.IPRangeRepository import IPRangeRepository


class IPRangeService:

    def __init__(self):
        self.__ipRangeRepository = IPRangeRepository()
        self.__UNKNOWN_DEVICE_RANK = DeviceRank.UNKNOWN

    def getAllIPRanges(self) -> List[IPRange]:
        return self.__ipRangeRepository.getAllIPRanges()

    def getAllDevicesFromIPRange(self, ipRange: IPRange) -> List[DeviceBE]:
        devices = list()
        # TODO: make this work with non /24 subnets
        # TODO: for now, we just check the range from the last octet of the ip addresses
        ipBase = ".".join(ipRange.rangeStart.split(".")[:3])
        startNumber = int(ipRange.rangeStart.split(".")[-1])
        endNumber = int(ipRange.rangeEnd.split(".")[-1])
        for num in range(startNumber, endNumber + 1):
            devices.append(DeviceBE("UNKNOWN", self.__UNKNOWN_DEVICE_RANK, f"{ipBase}.{num}"))
        return devices
