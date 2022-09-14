#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DateTime
import models


Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""

    id = Column(String(60), primary_key=True, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        self.id = str(uuid.uuid4())
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        if kwargs:
            for key, value in kwargs.items():
                if key in ["created_at", "updated_at"]:
                    if isinstance(value, str):
                        value = datetime.fromisoformat(value)
                if key != "__class__":
                    setattr(self, key, value)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = str(type(self).__name__)
        d = self.__dict__.copy()
        d.pop("_sa_instance_state", None)
        return '[{}] ({}) {}'.format(cls, self.id, d)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)

    def to_dict(self):
        """Convert instance into dict format"""
        my_dict = self.__dict__.copy()
        my_dict["__class__"] = type(self).__name__
        if my_dict.get("_sa_instance_state", None):
            del my_dict["_sa_instance_state"]
        return my_dict

    def delete(self):
        """ Delete self from database"""
        models.storage.delete(self)
