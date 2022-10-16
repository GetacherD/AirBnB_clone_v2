#!/usr/bin/python3
"""
Base Model to be inherited
"""
from os import getenv
import uuid
from datetime import datetime
import models

Base = object
if getenv("HBNB_TYPE_STORAGE") == "db":
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()


class BaseModel:

    """ Base Model Representation """
    def __init__(self, *args, **kwargs):

        """ Initialization with or with out kwargs
        kwargs assumed to contain isoformatted datetime object
        """
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    self.__dict__[key] = datetime.fromisoformat(value)
                else:
                    self.__dict__[key] = value
            if self.__dict__.get("__class__", None):
                del self.__dict__["__class__"]
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            models.storage.new(self)

    def __str__(self):

        """ String Representation """
        return "[{}] ({}) {}".format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):

        """ save instance to file"""
        self.updated_at = datetime.utcnow()
        models.storage.save()

    def to_dict(self):

        """ Return Dict Representation """
        dic = self.__dict__.copy()
        dic["updated_at"] = dic["updated_at"].isoformat()
        dic["created_at"] = dic["created_at"].isoformat()
        dic["__class__"] = self.__class__.__name__
        return dic
