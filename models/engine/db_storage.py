#!/usr/bin/python3
"""This module defines a class to manage db  storage for hbnb clone"""
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from models.base_model import Base
from models.state import State
from models.city import City


class DBStorage:
    """This class manages storage of hbnb models in database"""
    __engine = None
    __session = None

    def __init__(self):
        """ initialize storage """
        print(getenv("HBNB_MYSQL_USER"),
              getenv("HBNB_MYSQL_PWD"),
              getenv("HBNB_MYSQL_HOST"),
              getenv("HBNB_MYSQL_DB"))
        self.__engine = create_engine(
            "mysql+mysqldb://{}:{}@{}:3306/{}".format(
                getenv("HBNB_MYSQL_USER"),
                getenv("HBNB_MYSQL_PWD"),
                getenv("HBNB_MYSQL_HOST"),
                getenv("HBNB_MYSQL_DB")), pool_pre_ping=True)
        if getenv("HBNB_ENV") == "test":
            Base.metadata.drop_all(self.__engine)
        print("After Delete")
        '''
        self.__session__ = sessionmaker(bind=self.__engine)
        self.__session = scoped_session(self.__session__)
        '''

    def all(self, cls=None):
        """ print all data """
        if not cls:
            result = self.__session.query(State).all()
            print(result[0].__dict__)
            result.extend(self.__session.query(City).all())
        else:
            if type(cls) == str:
                cls = eval(cls)
            result = self.__session.query(cls).all()
            print("result = ", result)
        result = {
                f"{obj.__class__.__name__}.{obj.id}":
                obj.to_dict() for obj in result}
        return result

    def new(self, obj):
        """ add new object to session"""
        self.__session.add(obj)
        print("saved data", obj.__dict__)

    def save(self):
        """ save session to database """
        self.__session.commit()

    def delete(self, obj=None):
        """ Delete object """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ reload from db """
        Base.metadata.create_all(self.__engine)
        __session = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(__session)()
