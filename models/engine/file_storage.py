#!/usr/bin/python3
"""
File Storage Module
"""
import os
import json
from json import JSONEncoder
from datetime import datetime
from os.path import exists
from models.user import User
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.city import City
from models.base_model import BaseModel
from models.place import Place


class FileStorage:

    """ File Storage Objects Representation"""
    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):

        """ Return all objecsts """
        if cls is None:
            return FileStorage.__objects
        else:
            return {"{}: {}".format(
                key, value) for key, value in FileStorage.__objects.items(
                ) if eval(key.split(".")[0]) == cls}

    def new(self, obj):

        """ add new object to dictionary of objecsts"""
        FileStorage.__objects[
            f"{obj.__class__.__name__}.{obj.id}"] = obj

    def save(self):

        """ save objects dictionary to json file"""
        data = FileStorage.__objects.copy()
        mydic = {}
        for key, obj in data.items():
            mydic[key] = obj.to_dict()
        with open(FileStorage.__file_path, "w", encoding="utf-8") as f:
            json.dump(mydic, f)

    def reload(self):

        """ Deserialize, load objects from json"""
        try:
            with open(FileStorage.__file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                FileStorage.__objects = {}
                for key, value in data.items():
                    obj = eval(key.split(".")[0])(**value)
                    FileStorage.__objects[key] = obj
        except FileNotFoundError:
            pass

    def close(self):
        """ close and reload"""
        self.reload()
