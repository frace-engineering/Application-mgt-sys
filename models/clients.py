#!/usr/bin/python3

from sqlalchemy import ForeignKey
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.orm.declarative import declarative_base
from service_provider import User
from appointments import Appointment

Base = declarative_base()

class Client(Base):
     __tablename__ = "clients"
     client_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
     first_name = Column(String(128), nullable=False)
     last_name = Column(String(128), nullable=False)
     phone_number = Column(String(12))
     email = Column(String(128), nullable=False)
     user_id = Column(Integer, ForeignKey("users.id"))
     appointment_id = Column(Ingeter, ForeignKey("appointments.id"))

     user = relationship(User, back_populates="clients", cascade="All, delete-orphan")
     appointment = relationship(Appointment, back_populates="clients", cascade="All, delete-orphan")

    def __repr__(self):
        return f"[Client_id: {self.client_id}, First_name: {self.first_name}],"\
               f"[Last_name: {self.last_name}, Phone_number: {self.phone_number}],"\
               f"[E-mail: {self.email}]"
