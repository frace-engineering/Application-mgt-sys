#!/usr/bin/python3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.review import Review
from models.amenity import Amenity
from models.place import Place


class DBStorage:
    """Define the DBStorage class"""
    __engine = None
    __session = None

    def __init__(self):
        """Create the storage engine"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")
        db_path = f'mysql+mysqldb://{user}:{pwd}@{host}/{db}'
        self.__engine = create_engine(db_path, pool_pre_ping=True)
        if getenv("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                        expire_on_commit=False))

    def all(self, cls=None):
        """Public method that returns dictionary of objects"""
        objects_dict = {}
        if cls:
            objects = self.__session.query(cls).all()
        else:
            classes = [User, State, City, Amenity, Place, Review]
            objects = []
            for c in classes:
                objects.extend(self.__session.query(c).all())
        for objs in objects:
            key = "{}.{}".format(type(objs).__name__, objs.id)
            objects_dict[key] = objs
        return objects_dict

    def new(self, obj):
        """Add the session to the object """
        self.__session.add(obj)

    def save(self):
        """Commit all changes to the current database """
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj if exists"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Reload the session """
        Base.metadata.create_all(self.__engine)
        Session = scoped_session(sessionmaker(bind=self.__engine,
                                 expire_on_commit=False))
        self.__session = Session()

    def close(self):
        """ Call remove() on the __session """
        self.__session.remove()
