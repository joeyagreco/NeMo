from typing import List

import psycopg2

from server.decorators.utilDecorators import timer
from server.models.IPRange import IPRange
from server.util.EnvironmentReader import EnvironmentReader


class IPRangeRepository:

    def __init__(self):
        self.__conn = None
        self.__IP_RANGE_SCHEMA_AND_TABLE_NAME = "nemo.ip_range"
        self.__getAllIPRangesQuery = f"""
                                        select id, range_start, range_end
                                         from {self.__IP_RANGE_SCHEMA_AND_TABLE_NAME}
                                     """

    def __connect(self):
        self.__conn = psycopg2.connect(
            host=EnvironmentReader.get("DB_HOST"),
            database=EnvironmentReader.get("DB_DATABASE"),
            user=EnvironmentReader.get("DB_USER"),
            password=EnvironmentReader.get("DB_PASSWORD"))

    def __close(self):
        self.__conn.close()

    @timer
    def getAllIPRanges(self) -> List[IPRange]:
        self.__connect()
        ipRanges = list()
        with self.__conn.cursor() as cursor:
            cursor.execute(self.__getAllIPRangesQuery)
            results = cursor.fetchall()
            for result in results:
                ipRanges.append(IPRange(result[0], result[1], result[2]))
        self.__close()
        return ipRanges
