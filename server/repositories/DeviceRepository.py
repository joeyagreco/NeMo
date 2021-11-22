from typing import List

import psycopg2

from server.enums.DeviceRank import DeviceRank
from server.models.DeviceBE import DeviceBE
from server.util.EnvironmentReader import EnvironmentReader


class DeviceRepository:

    def __init__(self):
        self.__conn = None
        self.__DEVICE_SCHEMA_AND_TABLE_NAME = "nemo.device"
        self.__getAllDevicesQuery = f"""
                                        select id,
                                              device_name,
                                              ip_address,
                                              device_rank
                                        from {self.__DEVICE_SCHEMA_AND_TABLE_NAME}
                                        """
        self.__updateDeviceQuery = """
                                    update {deviceSchemaAndTableName} set
                                        device_name = '{deviceName}',
                                        ip_address = '{ipAddress}',
                                        device_rank = '{deviceRank}'
                                    where id = {deviceId}
                                     """
        self.__addDeviceQuery = """
                                    insert into {deviceSchemaAndTableName} (device_name, ip_address, device_rank)
                                    values ('{deviceName}',
                                            '{ipAddress}',
                                            '{deviceRank}')
                                    returning id
                                     """
        self.__deleteDeviceQuery = """
                                    delete from {deviceSchemaAndTableName}
                                    where id = {deviceId}
                                    """

    def __connect(self):
        self.__conn = psycopg2.connect(
            host=EnvironmentReader.get("DB_HOST"),
            database=EnvironmentReader.get("DB_DATABASE"),
            user=EnvironmentReader.get("DB_USER"),
            password=EnvironmentReader.get("DB_PASSWORD"))

    def __close(self):
        self.__conn.close()
        self.__conn = None

    def getAllDevices(self) -> List[DeviceBE]:
        self.__connect()
        allDevices = list()
        with self.__conn.cursor() as cursor:
            cursor.execute(self.__getAllDevicesQuery)
            results = cursor.fetchall()
            for result in results:
                allDevices.append(DeviceBE(result[1],
                                           DeviceRank.fromStr(result[3]),
                                           result[2],
                                           id=result[0]))
        self.__close()
        return allDevices

    def updateDevice(self, device: DeviceBE) -> None:
        self.__connect()
        with self.__conn.cursor() as cursor:
            cursor.execute(self.__updateDeviceQuery.format(deviceSchemaAndTableName=self.__DEVICE_SCHEMA_AND_TABLE_NAME,
                                                           deviceName=device.name,
                                                           ipAddress=device.ipAddress,
                                                           deviceRank=device.rank.name,
                                                           deviceId=device.id))
            self.__conn.commit()
        self.__close()

    def addDevice(self, device: DeviceBE) -> int:
        """
        Returns the ID of the device added.
        """
        self.__connect()
        with self.__conn.cursor() as cursor:
            cursor.execute(self.__addDeviceQuery.format(deviceSchemaAndTableName=self.__DEVICE_SCHEMA_AND_TABLE_NAME,
                                                        deviceName=device.name,
                                                        ipAddress=device.ipAddress,
                                                        deviceRank=device.rank.name))
            newDeviceId = cursor.fetchone()[0]
            self.__conn.commit()
        self.__close()
        return newDeviceId

    def deleteDevice(self, deviceId: int) -> None:
        self.__connect()
        with self.__conn.cursor() as cursor:
            cursor.execute(self.__deleteDeviceQuery.format(deviceSchemaAndTableName=self.__DEVICE_SCHEMA_AND_TABLE_NAME,
                                                           deviceId=deviceId))
        self.__conn.commit()
        self.__close()
