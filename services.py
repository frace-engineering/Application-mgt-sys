#!/usr/bin/python3

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Service(Base):
    __tablename__ "services"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    service_name = Column(String(158), nullable=False)
    description = Column(String(200), nullable=False)

    def __init__(self, args, **kwargs):
        super().__init__(*args, **kwargs)







