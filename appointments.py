#!/usr/bin/python3

import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Appointment(Base):
    __tablename__ "appointments"
    appointment_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    service_name = Column(String(158), nullable=False)
    date_time = Column(DateTime, nullable=False)

    def __init__(self, args, **kwargs):
        super().__init__(*args, **kwargs)







