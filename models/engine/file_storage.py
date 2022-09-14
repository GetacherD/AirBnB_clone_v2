#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
from datetime import datetime


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if not cls:
            return FileStorage.__objects
        res = {}
        for key, value in FileStorage.__objects.items():
            if str(key).split(".")[0] == cls.__name__ or str(
                    key).split(".")[0] == str(cls):
                res[key] = value
        return res

    def new(self, obj):
        """Adds new object to storage dictionary"""
        FileStorage.__objects[obj.to_dict()['__class__'] + '.' + obj.id] = obj

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w', encoding="utf-8") as f:
            temp = {}
            if FileStorage.__objects:
                temp = FileStorage.__objects.copy()
            for key, val in temp.items():
                val = val.to_dict()
                for k, v in val.items():
                    if isinstance(v, datetime):
                        val[k] = datetime.isoformat(v)
                temp[key] = val
            json.dump(temp, f)

    def delete(self, obj):
        """ Delete object """
        if obj:
            cls_name = obj.to_dict().get("__class__", None)
            if cls_name:
                _id = obj.to_dict().get("id")
                key = f"{cls_name}.{_id}"
                if key in FileStorage.__objects:
                    del FileStorage.__objects[key]
                    self.save()

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = f.read()
                print("data = ", temp)
                temp = {}
                for key, val in temp.items():
                    FileStorage.__objects[key] = classes[
                        val['__class__']](**val)
        except FileNotFoundError:
            pass
