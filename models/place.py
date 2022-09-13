#!/usr/bin/python3
""" Place Module for HBNB project """
from os import getenv
from sqlalchemy import (
    Column, String, Integer, ForeignKey, Float, Table)
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
from models.amenity import Amenity


place_amenity = Table(
    "place_amenity", Base.metadata,
    Column("place_id", String(60),
           ForeignKey("places.id"), nullable=False),
    Column("amenity_id", String(60),
           ForeignKey("amenities.id"), nullable=False))


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
        "Amenity", secondary=place_amenity, backref="places", viewonly=False)
    reviews = relationship(
            "Review", backref="place", cascade="all, delete")
    if getenv("HBNB_TYPE_STORAGE") != "db":
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
                self.append(value)
