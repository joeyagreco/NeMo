from typing import List

import psycopg2
from psycopg2.extras import execute_values

from server.decorators.utilDecorators import timer
from server.enums.DeviceRank import DeviceRank
from server.models.DeviceBE import DeviceBE
from server.models.Ping import Ping
from server.util.EnvironmentReader import EnvironmentReader


class DeviceAndPingRepository:

    def __init__(self):
        self.__conn = None
        self.__DEVICE_SCHEMA_AND_TABLE_NAME = "nemo.device"
        self.__PING_SCHEMA_AND_TABLE_NAME = "nemo.ping"
        # device table queries
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
        # ping table queries
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
                                        values %s
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

    @timer
    def getAllDevicesAndTheirPings(self) -> List[DeviceBE]:
        self.__connect()
        allDevices = list()
        with self.__conn.cursor() as cursor:
            # get all devices
            cursor.execute(self.__getAllDevicesQuery)
            deviceResults = cursor.fetchall()
            for deviceResult in deviceResults:
                # get all pings for each device
                cursor.execute(self.__getPingsByIdQuery.format(pingSchemaAndTableName=self.__PING_SCHEMA_AND_TABLE_NAME,
                                                               deviceId=deviceResult[0]))
                pingResults = cursor.fetchall()
                allPings = list()
                for pingResult in pingResults:
                    # build Ping model and add to ping list
                    allPings.append(Ping(pingResult[0],
                                         pingResult[2],
                                         pingResult[3]))
                # build DeviceBE model and add to device list
                allDevices.append(DeviceBE(deviceResult[1],
                                           DeviceRank.fromStr(deviceResult[3]),
                                           deviceResult[2],
                                           id=deviceResult[0],
                                           pings=allPings))
        self.__close()
        return allDevices

    @timer
    def addDeviceAndItsPings(self, device: DeviceBE) -> int:
        """
        Returns the ID of the device added.
        """
        self.__connect()
        with self.__conn.cursor() as cursor:
            # add device
            cursor.execute(self.__addDeviceQuery.format(deviceSchemaAndTableName=self.__DEVICE_SCHEMA_AND_TABLE_NAME,
                                                        deviceName=device.name,
                                                        ipAddress=device.ipAddress,
                                                        deviceRank=device.rank.name))
            newDeviceId = cursor.fetchone()[0]
            # add pings
            allPings = list()
            for ping in device.pings:
                allPings.append((device.id, ping.success, ping.timestamp))
            addPingQuery = self.__addPingQuery.format(pingSchemaAndTableName=self.__PING_SCHEMA_AND_TABLE_NAME)
            execute_values(cursor, addPingQuery, allPings)
            self.__conn.commit()
        self.__close()
        return newDeviceId

    def deleteDeviceAndItsPings(self, deviceId: int) -> None:
        self.__connect()
        with self.__conn.cursor() as cursor:
            # delete pings
            cursor.execute(
                self.__deletePingsByDeviceIdQuery.format(pingSchemaAndTableName=self.__PING_SCHEMA_AND_TABLE_NAME,
                                                         deviceId=deviceId))
            # delete device
            cursor.execute(self.__deleteDeviceQuery.format(deviceSchemaAndTableName=self.__DEVICE_SCHEMA_AND_TABLE_NAME,
                                                           deviceId=deviceId))
        self.__conn.commit()
        self.__close()

    @timer
    def updateDeviceAndItsPings(self, device: DeviceBE, deleteNOldestPings: int):
        # deleteNOldestPings is the number of pings to delete starting with the oldest and moving towards the newest
        # if number of pings for this device is less than the amount of pings we want to save,
        # just add all of the pings that do NOT have an id
        # if the number of pings for this device is greater than the amount of pings we want to save,
        # we delete the excess pings starting with the OLDEST pings and add the pings that do NOT have an id
        self.__connect()
        with self.__conn.cursor() as cursor:
            # delete old pings if necessary
            if deleteNOldestPings > 0:
                cursor.execute(
                    self.__deleteOldestPingByDeviceIdQuery.format(
                        pingSchemaAndTableName=self.__PING_SCHEMA_AND_TABLE_NAME,
                        deviceId=device.id,
                        limit=deleteNOldestPings))
            # add all new pings (pings without a pingId)
            newPings = []
            for ping in device.pings:
                if ping.id is None:
                    newPings.append((device.id, ping.success, ping.timestamp))
            addPingQuery = self.__addPingQuery.format(pingSchemaAndTableName=self.__PING_SCHEMA_AND_TABLE_NAME)
            execute_values(cursor, addPingQuery, newPings)
            # update device
            cursor.execute(self.__updateDeviceQuery.format(deviceSchemaAndTableName=self.__DEVICE_SCHEMA_AND_TABLE_NAME,
                                                           deviceName=device.name,
                                                           ipAddress=device.ipAddress,
                                                           deviceRank=device.rank.name,
                                                           deviceId=device.id))
            # commit changes [NOTE COMMITTING ONCE AFTER ALL OF THESE CHANGES MAKES THIS TRANSACTIONAL, WHICH IS WHAT WE WANT]
            self.__conn.commit()
            self.__close()
