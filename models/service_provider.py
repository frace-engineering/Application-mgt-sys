#!/usr/bin/python3
""" Include the necessary packages for the script """
from os import getenv
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from users import User
""" Create an instance of the declarative_base class and call it 'Base'"""
Base = declarative_base()

""" Create a 'User' class to inherit from Base class """
class Provider(Base, User):
    """ Define a table name """
    __tablename__ = "providers"
    provider_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    provider_name = Column(String(128), nullable=False)
    provider_address = Column(String(200), nullable=False)
    phone_number = Column(String(15), nullable=False)
    password = Column(String(20), nullable=False)
    email = Column(String(128), nullable=False)


    def __init__(self, provider_name, provider_address, phone_number, password, email):
        self.provider_name = provider_name
        self.provider_address = provider_address
        self.phone_number = phone_number
        self.password = password
        self.email = email


