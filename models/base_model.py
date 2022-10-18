#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
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
        id = Column(String(255), default=uuid4, primary_key=True, unique=True)
        created_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)
    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        from models import storage
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            if kwargs.get("updated_at"):
                kwargs['updated_at'] = datetime.strptime(
                    kwargs['updated_at'], '%Y-%m-%dT%H:%M:%S.%f')
            else:
                kwargs["updated_at"] = datetime.utcnow()
            if kwargs.get("created_at"):
                kwargs['created_at'] = datetime.strptime(
                    kwargs['created_at'], '%Y-%m-%dT%H:%M:%S.%f')
            else:
                kwargs["created_at"] = datetime.utcnow()
            if kwargs.get("__class__"):
                del kwargs['__class__']
            if not kwargs.get("id"):
                kwargs["id"] = str(uuid.uuid4())
            self.__dict__.update(kwargs)

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return "[{}] ({}) {}".format(cls, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()
        return dictionary
