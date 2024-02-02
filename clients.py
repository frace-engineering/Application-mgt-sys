#!/usr/bin/python3

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Client(Base):
    if models.storage == "db":
        __tablename__ = "clients"
        client_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
        first_name = Column(String(128), nullable=False)
        last_name = Column(String(128), nullable=False)
        phone_number = Column(String(12))
        email = Column(String(128), nullable=False)
    else:
        first_name = ""
        last_name = ""
        phone_number = ""
        email = ""

    def __init__(self, args, **kwargs):
        super().__init__(*args, **kwargs)





