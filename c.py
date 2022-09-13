#!/usr/bin/python3
""" Console Module """
import cmd
import sys
from os import getenv
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from utils import clean
print(getenv("HBNB_TYPE_STORAGE"))
