#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.orm.declarative import declarative_base
from clients import Client

Base = declarative_base()

class Appointment(Base):
    __tablename__ = "appointments"
    appointment_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    service_name = Column(String(158), nullable=False)
    date_time = Column(DateTime, nullable=False)

    client = relationship(Client, back_populates="appointments")
