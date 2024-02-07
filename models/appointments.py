#!/usr/bin/python3

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from service_provider import Provider
from clients import Client
from services import Service

Base = declarative_base()

class Appointment(Base):
    __tablename__ = "appointments"
    appointment_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    service_name = Column(String(158), nullable=False)
    date_time = Column(DateTime, nullable=False)
    description = Column(String(300))
    location = Column(String(128))
    provider_id = Column(Integer, ForeignKey("providers.provider_id"))
    client_id = Column(Integer, ForeignKey("clients.client_id"))
    service_id = Column(Integer, ForeignKey("services.service_id"))

    provider = relationship(Provider, back_populates="appointments", cascade="all, delete-orphan")
    client = relationship(Client, back_populates="appointments", cascade="all, delete-orphan")
    service = relationship(Service, back_populates="appointments", cascade="all, delete-orphan")
