#!/usr/bin/python3

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from models.services import Service

Base = declarative_base()

class User(Base):
    if models.storage == "db":
        __tablename__ = "service_provider"
        user_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
        business_name = Column(String(128), nullable=False)
        business_address = Column(String(128), nullable=False)
        phone_number = Column(String(12))
        email = Column(String(128), nullable=False)
    else:
        first_name = ""
        last_name = ""
        phone_number = ""
        email = ""

    def __init__(self, args, **kwargs):
        super().__init__(*args, **kwargs)

    def show_service(self):
        """ Return the services available """
        pass








