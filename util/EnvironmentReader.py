import os

from dotenv import load_dotenv


class EnvironmentReader:

    @staticmethod
    def get(variableName: str):
        load_dotenv()
        return os.getenv(variableName)
