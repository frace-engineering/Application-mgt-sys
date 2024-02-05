#!/usr/bin/python3
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, Integer, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from service_provider import User
from services import Service
from appointments import Appointment


Base = declarative_base()
class Client(Base):
    __tablename__ = "clients"
    client_id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    user_name = Column(String(15), nullable=False)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    phone_number = Column(String(12))
    email = Column(String(128), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    appointment_id = Column(Integer, ForeignKey("appointments.id"))
    user = relationship(User, back_populates="clients", cascade="all, delete-orphan")
    appointment = relationship(Appointment, back_populates="clients", cascade="all, delete-orphan")

classes = {
        "User": User,
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
    def create_user(self, business_name, business_address, phone_number, password, email):
        with Session() as session:
            new_user = User(business_name=business_name, business_address=business_address, phone_number=phone_number,
                            password=password, email=email)
            session.add(new_user)
            session.commit()

    def create_client(self, user_name, first_name, last_name, phone_number, password, email):
        with Session() as session:
            new_client = Client(user_name=user_name, first_name=first_name, last_name=last_name, phone_number=phone_number,
                            password=password, email=email)
            session.add(new_client)
            session.commit()

    def create_service(self, service_name, description):
        with Session() as session:
            new_service = Service(service_name=service_name, description=description)
            session.add(new_service)
            session.commit()

    def create_appointment(self, service_name, date_time, client_name):
        with Session() as session:
            new_appointment = Appointment(service_name=service_name, date_time=datetime.datetime.utcnow(), client_name=client.user_name)
            session.add(new_appointment)
            session.commit()

    def show_all(self, class_name):
        with Session() as session:
            if class_name not in classes:
                raise ValueError(f"Invalid class name: {class_name}")
            name = classes.get(class_name)
            instances = session.query(name).all()
            return instances
