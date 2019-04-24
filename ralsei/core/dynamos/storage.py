from .modules import Cog

from pymongo import MongoClient


class Storage:

    user_default = {

    }

    def register_config(self, cog: Cog):
        """
        Registers a cog to the storage dynamo

        Adds the cog's respective user config to the default configuration which user data will all comply with.
        :param cog:
        """
        if cog.user_config is not None:
            for k, v in cog.user_config.items():
                self.user_default[k] = v

            self.reload()

    def __init__(self, bot):
        """
        Storage dynamo for managing data specific to users.

        :param bot:
        """
        self.bot = bot

        db_config = self.bot.config["RalseiDB"]

        self._client = MongoClient(db_config["access_string"])
        self._db = self._client[db_config["database"]][db_config["users_collection"]]

        del db_config

        self._cache = {}

    def reload(self) -> dict:
        """
        Reloads the dynamo's internal cache and ensures all user data has all default items

        :return _cache:
        """
        for i in self._db.find():
            for k, v in {k: v for k, v in self.user_default.items() if k not in i.keys()}.items():
                i[k] = v

            self[i["_id"]] = i
        return self._cache

    def __getitem__(self, item):
        """
        Retrieves item from internal cache if possible,
        retrieves from database if not in cache.
        If not in database, creates document with default config.

        :param item:
        :return item document:
        """
        if item in self._cache.keys():
            return self._cache[item]
        else:
            self._cache[item] = self._db.find_one({"_id": item})
            if self._cache[item] is None:
                self[item] = self.user_default
            return self._cache[item]

    def __setitem__(self, key, value):
        """
        Updates document key to value, inserting document if necessary

        :param key:
        :param value:
        """
        value["_id"] = key
        self._db.update_one({"_id": key}, {"$set": value}, upsert=True)
        self._cache[key] = self._db.find_one({"_id": key})
