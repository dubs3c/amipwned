import configparser
from pathlib import Path


class Config():
    # must be absolute path!!
    def __init__(self, filename=f"{Path.home()}/.amipwned.ini"):
        self.filename = filename
        self.config = configparser.ConfigParser()
        self.config.read(self.location())

    def location(self) -> str:
        path = Path(self.filename)
        if not path.exists():
            return ""
        return path

    def database(self) -> dict:
        db = {
            "host": self.config.get("postgresql", "host"),
            "port": self.config.get("postgresql", "port"),
            "username": self.config.get("postgresql", "username"),
            "password": self.config.get("postgresql", "password"),
            "name": self.config.get("postgresql", "databaseName")
            }
        return db
