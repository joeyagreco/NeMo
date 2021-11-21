from typing import List

import psycopg2

from server.models.Ping import Ping
from server.util.EnvironmentReader import EnvironmentReader


class PingRepository:

    def __init__(self):
        self.__conn = None
        self.pingSchemaAndTableName = "nemo.ping"
        self.__getPingsByIdQuery = """
                                    select id,
                                    device_id,
                                    success,
                                    ping_timestamp
                                    from {pingSchemaAndTableName}
                                    where device_id = {deviceId}
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

    def getPingsByDeviceId(self, deviceId: int) -> List[Ping]:
        self.__connect()
        allPings = list()
        with self.__conn.cursor() as cursor:
            cursor.execute(self.__getPingsByIdQuery.format(pingSchemaAndTableName=self.pingSchemaAndTableName,
                                                           deviceId=deviceId))
            results = cursor.fetchall()
            for result in results:
                allPings.append(Ping(result[2],
                                     result[3]))
        self.__close()
        return allPings
