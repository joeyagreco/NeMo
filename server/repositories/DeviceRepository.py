from typing import List

import psycopg2

from server.models.DeviceBE import DeviceBE
from server.util.EnvironmentReader import EnvironmentReader


class DeviceRepository:

    def __init__(self):
        self.__conn = None
        self.__deviceSchemaAndTableName = "nemo.device"
        self.__getAllDevicesQuery = f"""
                                        select id,
                                              device_name,
                                              ip_address,
                                              device_rank
                                        from {self.__deviceSchemaAndTableName}
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
                allDevices.append(DeviceBE(result[1], result[3], result[2], id=result[0]))
        self.__close()
        return allDevices
