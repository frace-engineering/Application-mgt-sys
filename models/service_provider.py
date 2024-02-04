#!/usr/bin/python3
""" Include the necessary packages for the script """
from os import getenv
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.declarative import declarative_base
from clients import Client
from services import Service

""" Create an instance of the declarative_base class and call it 'Base'"""
Base = declarative_base()

""" Create a 'User' class to inherit from Base class """
class User(Base):
    """ Define a table name """
    __tablename__ = "users"
    user_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    business_name = Column(String(128), nullable=False)
    business_address = Column(String(128), nullable=False)
    phone_number = Column(String(12))
    password = Column(String)
    email = Column(String(128), nullable=False)

    """ Establish a bidrectional relationships between the users table and both clients and services tables """
    client = relationship(Client, back_populates="users")
    service = relationship(Service, back_populates="users", cascade="All, delete-orphan")

    def __repr__(self):
        return f"[User_id: {self.user_id}, Business_name: {self.business_name}],"\
               f"[Business_address = {self.business_address}, Phone_number: {self.phone_number}],"\
                   f"[ E-mail: {self.email}]"

    def show_service(self):
        """ Return the services available """
        pass








