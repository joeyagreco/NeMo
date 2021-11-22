from typing import List

import psycopg2

from server.models.Ping import Ping
from server.util.EnvironmentReader import EnvironmentReader


class PingRepository:

    def __init__(self):
        self.__conn = None
        self.__PING_SCHEMA_AND_TABLE_NAME = "nemo.ping"
        self.__getPingsByIdQuery = """
                                    select id,
                                    device_id,
                                    success,
                                    ping_timestamp
                                    from {pingSchemaAndTableName}
                                    where device_id = {deviceId}
                                   """
        self.__deletePingsByDeviceIdQuery = """
                                delete from {pingSchemaAndTableName}
                                where device_id = {deviceId}
                              """
        self.__addPingQuery = """
                                insert into {pingSchemaAndTableName}
                                (device_id, success, ping_timestamp)
                                values ({deviceId},
                                {success},
                               '{pingTimestamp}')
                              """
        self.__deleteOldestPingByDeviceIdQuery = """
                                                delete from {pingSchemaAndTableName}
                                                where id in (
                                                select id from nemo.ping
                                                where device_id = {deviceId}
                                                order by ping_timestamp asc limit {limit})
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
            cursor.execute(self.__getPingsByIdQuery.format(pingSchemaAndTableName=self.__PING_SCHEMA_AND_TABLE_NAME,
                                                           deviceId=deviceId))
            results = cursor.fetchall()
            for result in results:
                allPings.append(Ping(result[0],
                                     result[2],
                                     result[3]))
        self.__close()
        return allPings

    def addPing(self, ping: Ping, deviceId: int) -> None:
        self.__connect()
        with self.__conn.cursor() as cursor:
            cursor.execute(self.__addPingQuery.format(pingSchemaAndTableName=self.__PING_SCHEMA_AND_TABLE_NAME,
                                                      deviceId=deviceId,
                                                      success=ping.success,
                                                      pingTimestamp=ping.timestamp))
            self.__conn.commit()
        self.__close()

    def deletePingsByDeviceId(self, deviceId: int) -> None:
        self.__connect()
        with self.__conn.cursor() as cursor:
            cursor.execute(
                self.__deletePingsByDeviceIdQuery.format(pingSchemaAndTableName=self.__PING_SCHEMA_AND_TABLE_NAME,
                                                         deviceId=deviceId))
            self.__conn.commit()
        self.__close()

    def deleteOldestPingsByDeviceId(self, deviceId: int, numberOfPingsToDelete: int) -> None:
        self.__connect()
        with self.__conn.cursor() as cursor:
            cursor.execute(
                self.__deleteOldestPingByDeviceIdQuery.format(pingSchemaAndTableName=self.__PING_SCHEMA_AND_TABLE_NAME,
                                                              deviceId=deviceId,
                                                              limit=numberOfPingsToDelete))
            self.__conn.commit()
        self.__close()
