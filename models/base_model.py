#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
import models
from datetime import datetime
from os import getenv
from uuid import uuid4
from sqlalchemy import Column, String, DateTime


if getenv("HBNB_TYPE_STORAGE") == "db":
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    if getenv("HBNB_TYPE_STORAGE") == "db":
        id = Column(String(60), default=uuid4,
                    primary_key=True, unique=True, nullable=False)
        created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
        updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        if kwargs and kwargs.get("__class__", None):
            del kwargs["__class__"]
        if kwargs:
            if kwargs.get("updated_at", None) and isinstance(
                    kwargs.get("updated_at", None), str):
                kwargs['updated_at'] = datetime.fromisoformat(
                    kwargs['updated_at'])
            else:
                kwargs["updated_at"] = datetime.utcnow()
            if kwargs.get("created_at", None) and isinstance(
                    kwargs.get("created_at", None), str):
                kwargs['created_at'] = datetime.fromisoformat(
                    kwargs['created_at'])
            else:
                kwargs["created_at"] = datetime.utcnow()
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = self.__class__.__name__
        rec = self.__dict__.copy()
        if '_sa_instance_state' in rec.keys():
            del rec['_sa_instance_state']
        return "[{}] ({}) {}".format(cls, self.id, rec)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        res = self.__dict__.copy()
        if res.get("_sa_instance_state", None):
            del res["_sa_instance_state"]
        res["created_at"] = datetime.isoformat(res["created_at"])
        res["updated_at"] = datetime.isoformat(res["updated_at"])
        res["__class__"] = self.__class__.__name__
        return res

    def delete(self):
        """ delete self"""
        models.storage.delete(self)
