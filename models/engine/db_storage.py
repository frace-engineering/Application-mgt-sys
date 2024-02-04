#!/usr/bin/python3

from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.clients import Client
from models.appointments import Appointment
from models.services import Service
from models.service_provider import User

classes = {
        "User": User,
        "Service": Service,
        "Client": Client,
        "Appointment": Appointment
        }

class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        """ Set the environment variables """
        APPOMS_MYSQL_USER = getenv("APPOMS_MYSQL_USER")
        APPOMS_MYSQL_PWD = getenv("APPOMS_MYSQL_PWD")
        APPOMS_MYSQL_HOST = getenv("APPOMS_MYSQL_HOST")
        APPOMS_MYSQL_DB = getenv("APPOMS_MYSQL_DB")

        """ Test to ensure that all the required environment variables are set, else raise a ValueError """
        if not all([APPOMS_MYSQL_USER, APPOMS_MYSQL_PWD, APPOMS_MYSQL_HOST, APPOMS_MYSQL_DB]):
             raise ValueError("Please set all required environment variables.")

        db_url = f"mysql+mysqldb://{APPOMS_MYSQL_USER}:{APPOMS_MYSQL_PWD}@{APPOMS_MYSQL_HOST}/{APPOMS_MYSQL_DB}"
        self._engine = create_engine(db_url)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)

    def __repr__(self):
        return f"[User_id: {self.user_id}, Business_name: {self.business_name}],"\
               f"[Business_address = {self.business_address}, Phone_number: {self.phone_number}],"\
               f"[ E-mail: {self.email}]"

    def show_service(self):
        """ Return the services available """
                                                                                                  pass
        services = self.__session.query(classes).all(User)
        return services

    def creat_user(self, business_name, business_address, phone_number, password, email):
        with Session() as session:
            new_user = User(business_name=business_name, business_address=business_address,
                           phone_number=phonenumber, password=password, email=email)
            session.add(new_user)
            session.commit()

    def creat_client(self, first_name, last_name, phone_number, password, email):
        with Session() as session:
            new_client = Client(first_name=first_name, last_name=last_name,
                           phone_number=phonenumber, password=password, email=email)
            session.add(new_client)
            session.commit()

    def creat_service(self, service_name, description):
        with Session() as session:
            new_service = Service(service_name=service_name, description=description)
            session.add(new_service)
            session.commit()

    def creat_ppointment(self, service_name, date_time, client_id):
        with Session() as session:
            new_appointment = Appointment(service_name=service_name, date_time=date_time, client_id=client_id)
            session.add(new_appointment)
            session.commit()

