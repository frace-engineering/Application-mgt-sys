#!/usr/bin/python3

from sqlalchemy import ForeignKey
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from service_provider import User

Base = declarative_base()

class Client(Base):
     __tablename__ = "clients"
     client_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
     first_name = Column(String(128), nullable=False)
     last_name = Column(String(128), nullable=False)
     phone_number = Column(String(12))
     email = Column(String(128), nullable=False)
     user_id = Column(Integer, ForeignKey("users.id"))
     appointment_id = Column(Integer, ForeignKey("appointments.id"))

     user = relationship(User, back_populates="clients", cascade="all, delete-orphan")
     appointment = relationship(Appointment, back_populates="clients", cascade="all, delete-orphan")

