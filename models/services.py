#!/usr/bin/python3

from os import getenv
from sqlalchemy import Column, String, Integer, ForeignKey 
from sqlalchemy.orm import relationship
from sqlalchemy.orm.declarative import declarative_base
from service_provider import User

Base = declarative_base()

class Service(Base):
    __tablename__ = "services"
    service_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    service_name = Column(String(158), nullable=False)
    description = Column(String(200), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship(User, back_populates="services")

    def __repr__(self):
        return f"[Service_id: {Service.service_id}, Service_name: {Service.service_name},
                Description: {Service.description}]"







