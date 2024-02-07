#!/usr/bin/python3

from os import getenv
from sqlalchemy import Column, String, Integer, ForeignKey 
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from service_provider import Provider

Base = declarative_base()

class Service(Base):
    __tablename__ = "services"
    service_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    service_name = Column(String(228), nullable=False)
    description = Column(String(500), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.provider_id"))

    provider = relationship(Provider, back_populates="services")

    def __repr__(self):
        return f"[Service_id: {self.service_id}, Service_name: {self.service_name},\
                 Description: {self.description}]"







