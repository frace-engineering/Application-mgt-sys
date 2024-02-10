#!/usr/bin/python3
""" Include the necessary packages for the script """
from os import getenv
from base_models import Session, Provider, Client, Service, Appointment
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base


""" Create a 'User' class to inherit from Base class """
class Provider:
    def __init__(self, name, address, phone, passwd, email):
        self.name = name
        self.address = address
        self.phone = phone
        self.passwd = passwd
        self.email = email
    @property
    def get_name(self, name):
        return self.name

class 
    pass

