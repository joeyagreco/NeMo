import psycopg2

from server.models.Settings import Settings
from server.util.EnvironmentReader import EnvironmentReader


class SettingsRepository:

    def __init__(self):
        self.__conn = None
        # since we will only ever have 1 row in this table, we know the id will always be 1
        self.__settingsRowId = 1
        self.__getAllSettingsQuery = f"""select pings_to_save,
                                              ping_online_threshold_percentage,
                                              page_refresh_frequency_seconds,
                                              ping_critical_refresh_frequency_seconds,
                                              ping_known_refresh_frequency_seconds,
                                              ping_scan_frequency_seconds
                                        from nemo.setting where id = {self.__settingsRowId}"""

    def __connect(self):
        self.__conn = psycopg2.connect(
            host=EnvironmentReader.get("DB_HOST"),
            database=EnvironmentReader.get("DB_DATABASE"),
            user=EnvironmentReader.get("DB_USER"),
            password=EnvironmentReader.get("DB_PASSWORD"))

    def __close(self):
        self.__conn.close()
        self.__conn = None

    def getSettings(self) -> Settings:
        self.__connect()
        with self.__conn.cursor() as cursor:
            cursor.execute(self.__getAllSettingsQuery)
            result = cursor.fetchone()
            settings = None if result is None else Settings(result[0], result[1], result[2], result[3], result[4],
                                                            result[5])
        self.__close()
        return settings
