from typing import Dict

from .modules import Cog
from pymongo import MongoClient
from configparser import ConfigParser, ExtendedInterpolation
from warnings import warn


class Config:
    """
    Serves as the main config interaction, as well as providing a connection to individual server configs
    """
    _default_config: Dict[str, dict] = {
        "Ralsei":
            {
                "name": "Ralsei",
                "token": "--- fill in token ---",
                "owner_id": "",
                "command_prefix": "!!",
                "presence": "In an unknown world",
                "case_insensitive": False
            },
        "RalseiDB":
            {
                "access_string": "--- fill in access ---",
                "database": "ralsei",
                "servers_collection": "server_configs",
                "users_collection": "user_storage"
            }
    }

    def register_cog(self, cog: Cog):
        self._ServerInterface.register_cog(cog)

    class ServerInterface:
        """
        Interface between database collection and bot for storing configuration of servers
        """
        server_default: dict = {
            "prefix": "!!",
        }

        def register_cog(self, cog: Cog):
            """
            Registers a cog to the Server Interface

            Adds the cog's respective server config to the default configuration which servers will all comply with.
            :param cog:
            """
            if cog.server_config is not None:
                for k, v in cog.server_config.items():
                    self.server_default[k] = v

                self.reload()

        def __init__(self, db_tuple):
            """
            Setup interface between the database collection and bot

            When something is retrieved, grabs from cache if available and from database if not.
            When an item is changed, updates cache version and database version

            :param db_tuple:
            """

            access, database, collection = db_tuple

            self._client = MongoClient(access)

            self.db = self._client[database][collection]

            self._cache: dict = {}

            self.reload()

        def reload(self) -> dict:
            """
            Reloads the interface's internal cache and ensures all server data has all default items

            :return _cache:
            """
            for i in self.db.find():
                for k, v in {k: v for k, v in self.server_default.items() if k not in i.keys()}.items():
                    i[k] = v

                self[i["_id"]] = i
            return self._cache

        def __getitem__(self, item):
            """
            Retrieves item from cache with database as fallback

            :param item:
            :return server config:
            """
            if item in self._cache.keys():
                return self._cache[item]

            else:
                self._cache[item] = self.db.find_one({"_id": item})
                if self._cache[item] is None:
                    self[item] = self.server_default
                return self._cache[item]

        def __setitem__(self, key, value):
            """
            Set key's cache/database document to value

            :param key:
            :param value:
            """
            value["_id"] = key
            self.db.update_one({"_id": key}, {"$set": value}, upsert=True)
            self._cache[key] = value

    def _generate(self):
        """
        Generates config file

        :return:
        """
        config = ConfigParser(interpolation=ExtendedInterpolation())
        for key, value in self._default_config.items():
            config[key] = value

        with open(self.config_file, "w") as file:
            config.write(file)

        del config

    def _read(self) -> ConfigParser:
        """
        Reads config file and returns ConfigParser object

        :return config:
        """
        config = ConfigParser(interpolation=ExtendedInterpolation())
        config.read(self.config_file)

        if not config.sections():
            del config
            self._generate()
            raise Warning("Configuration File Not Found: generated configuration and exited")

        return config

    def __init__(self, config_file):
        """
        Main interface for interacting with all configurations within Ralsei

        If you access a key tied to a configuration value in the config file, it returns the respective value.
        Otherwise, it checks if that value is within the configuration database for server configs.
        If it is in neither, a server configuration file is created and tied to that key.

        :param config_file:
        """

        self.config_file = config_file

        self._config_raw = self._read()

        self._config = {s: dict(self._config_raw.items(s)) for s in self._config_raw.sections()}

        self._ServerInterface = self.ServerInterface((self._config["RalseiDB"]["access_string"],
                                                      self._config["RalseiDB"]["database"],
                                                      self._config["RalseiDB"]["servers_collection"]))

    def __getitem__(self, item):
        """
        Retrieves section of config if item is a valid section,
        otherwise returns respective document from ServerInterface

        :param item:
        :return config item:
        """
        if item in self._config.keys():
            return self._config[item]
        else:
            return self._ServerInterface[item]

    def __setitem__(self, key, value):
        """
        Sets key's config document to value.
        If attempting to modify the config file, aborts.
        Otherwise attempts to use the respective update action on key's document in ServerInstance

        :param key:
        :param value:
        """
        if key in self._config.keys():
            warn("Warning: You cannot modify the file based configuration. Operation aborted")
            return

        else:
            self._ServerInterface[key] = value
