#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class State(BaseModel, Base):
    """ State class """
    if getenv("HBNB_TYPE_STORAGE", None) == "db":
        __tablename__ = "states"
        name = Column(String(128), nullable=False)
        cities = relationship(
            "City", backref="state", cascade="all, delete")
    else:
        name = ""
    if getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def cities(self):
            from . import storage
            from models.city import City
            cities_all = storage.all(City).values()
            city_all = []
            for city in cities_all:
                if city.state_id == self.id:
                    city_all.append(city)
            return city_all
