#!/usr/bin/python3

from sqlalchemy import ForeignKey
from sqlalchemy import Column, String, Integer, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from users import User

Base = declarative_base()

class Client(Base, User):
     __tablename__ = "clients"
     client_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
     user_name = Column(String(123), nullable=False, unique=True)
     first_name = Column(String(128), nullable=False)
     last_name = Column(String(128), nullable=False)
     phone_number = Column(String(15), nullable=False)
     password = Column(String(100), nullable=False)
     email = Column(String(255), nullable=False)

