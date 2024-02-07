#!/usr/bin/python3
import datetime
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from service_provider import Provider 
from services import Service
from appointments import Appointment
from clients import Client


Base = declarative_base()


classes = {
        "Provider": Provider, 
        "Service": Service,
        "Client": Client,
        "Appointment": Appointment
        }

APPOMS_MYSQL_USER = getenv("APPOMS_MYSQL_USER")
APPOMS_MYSQL_HOST = getenv("APPOMS_MYSQL_HOST")
APPOMS_MYSQL_PWD = getenv("APPOMS_MYSQL_PWD")
APPOMS_MYSQL_DB = getenv("APPOMS_MYSQL_DB")
if not all([APPOMS_MYSQL_USER, APPOMS_MYSQL_PWD, APPOMS_MYSQL_HOST, APPOMS_MYSQL_DB]):
     raise ValueError("Please set all required environment variables.")
db_url = f"mysql+mysqldb://{APPOMS_MYSQL_USER}:{APPOMS_MYSQL_PWD}@{APPOMS_MYSQL_HOST}/{APPOMS_MYSQL_DB}"
engine = create_engine(db_url)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)



class DBStorage:
    def create_provider(self, provider_name, provider_address, phone_number, password, email):
        with Session() as session:
            new_provider = Provider(provider_name=provider_name, provider_address=provider_address, phone_number=phone_number, password=password, email=email)
            session.add(new_provider)
            session.commit()

    def create_client(self, user_name, first_name, last_name, phone_number, password, email):
        with Session() as session:
            new_client = Client(user_name=user_name, first_name=first_name, last_name=last_name, phone_number=phone_number,\
                            password=password, email=email)
            session.add(new_client)
            session.commit()

    def create_service(self, service_name, description):
        with Session() as session:
            new_service = Service(service_name=service_name, description=description)
            session.add(new_service)
            session.commit()

    def create_appointment(self, service_name, date_time, location="", description=""):
        with Session() as session:
            new_appointment = Appointment(service_name=service_name, date_time=datetime.datetime.utcnow(), location=location, description=description)
            session.add(new_appointment)
            session.commit()

    def show_all(self, class_name):
        with Session() as session:
            if class_name not in classes:
                raise ValueError(f"Invalid class name: {class_name}")
            name = classes.get(class_name)
            instances = session.query(name).all()
            return instances
