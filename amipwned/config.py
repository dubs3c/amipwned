import configparser
from configparser import NoSectionError
from pathlib import Path
import sys

class Config():
    # must be absolute path!!
    def __init__(self, filename=None):
        if filename:
            self.filename = filename
        else:
            self.filename = f"{Path.home()}/.amipwned.ini"
        self.config = configparser.ConfigParser()

    def location(self) -> str:
        path = Path(self.filename)
        if not path.exists():
            return ""
        return path

    def database(self) -> dict:
        try:
            self.config.read(self.location())

            db = {
                "host": self.config.get("postgresql", "host"),
                "port": self.config.get("postgresql", "port"),
                "username": self.config.get("postgresql", "username"),
                "password": self.config.get("postgresql", "password"),
                "name": self.config.get("postgresql", "databaseName")
                }
            return db
        except NoSectionError as e:
            print(f"[-] Could not parse configuration file at \"{self.filename}\", error: {e}")
            sys.exit(1)