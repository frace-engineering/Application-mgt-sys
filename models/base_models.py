#!/usr/bin/python3
""" Include the necessary packages for the script """
from os import getenv
from sqlalchemy import Column, String, Integer,DateTime, create_engine, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.orm import declarative_base

""" Create an instance of the declarative_base class and call it 'Base'"""
Base = declarative_base()

""" Create a 'User' class to inherit from Base class """
class Provider(Base):
    __tablename__="providers"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    provider_name = Column(String(128), nullable=False)
    provider_address = Column(String(200), nullable=False)
    phone_number = Column(String(15), nullable=False)
    password = Column(String(20), nullable=False)
    email = Column(String(128), nullable=False)

    appointments = relationship("Appointment", back_populates="providers", cascade="all, delete-orphan")
    clients = relationship("Client", back_populates="providers", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Provider(provider_name='%s', provider_address='%s', phone_number='%s', email='%s')>" % (
                self.provider_name,
                self.provider_address,
                self.phone_number,
                self.email
                )


class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    user_name = Column(String(123), nullable=False, unique=True)
    first_name = Column(String(128), nullable=False)
    last_name = Column(String(128), nullable=False)
    phone_number = Column(String(15), nullable=False)
    password = Column(String(100), nullable=False)
    email = Column(String(255), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"))

    appointments = relationship("Appointment", back_populates="clients", cascade="all, delete-orphan")
    providers = relationship("Provider", back_populates="clients")

    def __repr__(self):
        return f"<Client(user_name='%s', first_name='%s', last_name='%s' phone_number='%s', email='%s')>" % (
                self.user_name,
                self.first_name,
                self.last_name,
                self.phone_number,
                self.email
                )


class Service(Base):
    __tablename__ = "services"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    service_name = Column(String(228), nullable=False)
    description = Column(String(500), nullable=False)
    appointments = relationship("Appointment", back_populates='services')

    def __repr__(self):
        return f"<Service(service_name='%s', description='%s', appointments='%s')>" % (
                self.service_name,
                self.description,
                self.appointments
                )


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    service_name = Column(String(158), nullable=False)
    date_time = Column(DateTime, nullable=False)
    description = Column(String(300))
    location = Column(String(128))
    provider_id = Column(Integer, ForeignKey("providers.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    service_id = Column(Integer, ForeignKey("services.id"))

    providers = relationship("Provider", back_populates="appointments")
    clients = relationship("Client", back_populates="appointments")
    services = relationship("Service", back_populates="appointments")

    def __repr__(self):
        return f"<Appointment(service_name='%s', date_time='%s', description='%s', location='%s')>" % (
                self.service_name,
                self.date_time,
                self.description,
                self.location
                )


APPOMS_MYSQL_USER = getenv("APPOMS_MYSQL_USER")
APPOMS_MYSQL_HOST = getenv("APPOMS_MYSQL_HOST")
APPOMS_MYSQL_PWD = getenv("APPOMS_MYSQL_PWD")
APPOMS_MYSQL_DB = getenv("APPOMS_MYSQL_DB")
if not all([APPOMS_MYSQL_USER, APPOMS_MYSQL_PWD, APPOMS_MYSQL_HOST, APPOMS_MYSQL_DB]):
     raise ValueError("Please set all required environment variables.")
db_url = f"mysql+mysqldb://{APPOMS_MYSQL_USER}:{APPOMS_MYSQL_PWD}@{APPOMS_MYSQL_HOST}/{APPOMS_MYSQL_DB}"

engine = create_engine(db_url, pool_pre_ping=True)
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
