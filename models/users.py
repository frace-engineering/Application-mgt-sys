#!/usr/bin/python3
""" Include the necessary packages for the script """
from os import getenv
from sqlalchemy import Column, String, Integer, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


""" Create a 'User' class to inherit from Base class """
class User():
    pass

