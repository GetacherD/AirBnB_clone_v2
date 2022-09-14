#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from sqlalchemy import (
    Column, String, Integer, ForeignKey, Float)
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.amenity import Amenity


class Association(Base):
    """ Association table """
    __tablename__ = "place_amenity"
    place_id = Column(ForeignKey("places.id"),
                      primary_key=True, nullable=False)
    amenity_id = Column(ForeignKey("amenities.id"),
                        primary_key=True, nullable=False)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = "places"
    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenities = relationship(
        "Amenity", secondary="place_amenity", viewonly=False)
    reviews = relationship(
            "Review", backref="place", cascade="delete")
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE", None) != "db":
        @property
        def reviews(self):
            """ Return reviews in file storage system"""
            return []

        @property
        def amenities(self):
            """ get amenities from file storage"""
            return []

        @amenities.setter
        def amenities(self, value):
            """ set / append amenities """
            if type(value) is Amenity:
                self.amenity_ids.append(value.id)
