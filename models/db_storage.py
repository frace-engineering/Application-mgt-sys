#!/usr/bin/python3
from os import getenv
import sqlalchemy
from models.base_models import Provider, Client, Service, Appointment, Session
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base

class DBStorage:
    """Define the DBStorage class"""

    def all(self, cls=None):
        """Public method that returns dictionary of objects"""
        with Session() as session:
            objects_dict = {}
            if cls:
                objects = session.query(cls).all()
            else:
                classes = [Provider, Client, Service, Appointment]
                objects = []
                for c in classes:
                    objects.extend(session.query(c).all())
                    for objs in objects:
                        key = "{}.{}".format(type(objs).__name__, objs.id)
                        objects_dict[key] = objs
                    return objects_dict

    def new(self, obj):
        """Add the session to the object """
        with Session() as session:
            session.add(obj)

    def save(self):
        """Commit all changes to the current database """
        with Session() as session:
            session.commit()

    def delete(self, obj=None):
        """Delete obj if exists"""
        with Session() as session:
            if obj:
                session.delete(obj)

    def reload(self):
        """Reload the session """
        Base.metadata.create_all(self.engine)
        Session = scoped_session(sessionmaker(bind=self.engine,
                                 expire_on_commit=False))
        self.session = Session()

    def close(self):
        """ Call remove() on the __session """
        self.session.remove()
