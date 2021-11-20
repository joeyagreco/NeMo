import psycopg2

from server.util.EnvironmentReader import EnvironmentReader


class SettingsRepository:

    def __init__(self):
        self.conn = psycopg2.connect(
            host=EnvironmentReader.get("DB_HOST"),
            database=EnvironmentReader.get("DB_DATABASE"),
            user=EnvironmentReader.get("DB_USER"),
            password=EnvironmentReader.get("DB_PASSWORD"))

        self.cursor = self.conn.cursor()
        self.cursor.execute("select * from nemo.setting")
        result = self.cursor.fetchall()
        print(result)

        self.conn.close()
