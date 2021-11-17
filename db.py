# This module will connect the app to it's data
from os.path import exists
from pickle import load, dump as save


class DataBaseMother:
    """
    This is the mother class of all DataBase Managers.
    """
    name: str = ""  # name of the DataBase manager that user sees.

    def __getitem__(self, item):
        """
        This method should return the value with key
        :param item: key of a previously save value
        :return: value of the key
        """
        raise NotImplemented

    def __setitem__(self, key, value):
        """
        This method saves or replaces the value for the key
        :param key: key
        :param value: value
        :return: nothing
        """
        raise NotImplemented

    def __contains__(self, item) -> bool:
        """
        This method returns whether a key exists
        :param item: key
        :return: True if the key is present otherwise False
        """
        raise NotImplemented

    def save(self):
        """
        This method saves data to file, usually called when exiting the app
        :return: nothing
        """
        raise NotImplemented


class SimpleDB(DataBaseMother):
    name = "default (pickle)"
    appdata = None

    def __init__(self):
        if exists("data.bin"):
            with open("data.bin", "rb") as f:
                SimpleDB.appdata = load(f)
        else:
            with open("data.bin", "wb") as f:
                SimpleDB.appdata = {}
                save(SimpleDB.appdata, f)

    def __getitem__(self, item):
        return self.appdata[item]

    def __setitem__(self, key, value):
        self.appdata[key] = value

    def __contains__(self, item):
        return item in self.appdata

    def save(self):
        with open("data.bin", "wb") as f:
            SimpleDB.appdata = {}
            save(SimpleDB.appdata, f)
