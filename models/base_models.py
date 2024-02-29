#!/usr/bin/python3
""" Include the necessary packages for the script """
from os import getenv
from sqlalchemy import Column, String, Integer,DateTime, create_engine, ForeignKey, Time, Enum
from sqlalchemy.orm import sessionmaker, relationship, scoped_session
from sqlalchemy.orm import declarative_base
from datetime import datetime
from flask_login import UserMixin

""" Create an instance of the declarative_base class and call it 'Base'"""
Base = declarative_base()

""" Create a 'User' class to inherit from Base class """
class User(UserMixin, Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(128), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    phone_number = Column(String(20), nullable=False)

    providers = relationship("Provider", back_populates="users", cascade="all, delete-orphan")
    clients = relationship("Client", back_populates="users", cascade="all, delete-orphan")
    admin = relationship('Admin', back_populates='users', cascade='all, delete-orphan')

    def __repr__(self):
        return f"User(username='%s', email='%s', phone_number='%s')" % (
                self.username,
                self.email,
                self.phone_number
                )

""" Create a 'Admin' class to inherit from Base class """
class Admin(UserMixin, Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(128), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(128), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    phone_number = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship('User', back_populates='admin')

    def __repr__(self):
        return f"Admin(username='%s', email='%s', phone_number='%s')" % (
                self.username,
                self.email,
                self.phone_number
                )


class Provider(UserMixin, Base):
    __tablename__="providers"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    username = Column(String(123), nullable=False)
    provider_name = Column(String(128))
    provider_address = Column(String(200))
    email = Column(String(128), nullable=False)
    password = Column(String(20), nullable=False)
    phone_number = Column(String(15), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("User", back_populates="providers")
    appointments = relationship("Appointment", back_populates="providers", cascade="all, delete-orphan")
    clients = relationship("Client", back_populates="providers", cascade="all, delete-orphan")
    services = relationship("Service", back_populates="providers", cascade="all, delete-orphan")
    slots = relationship('Slot', back_populates="providers")

    def __repr__(self):
        return f"<Provider(provider_name='%s', provider_address='%s', phone_number='%s', email='%s')>" % (
                self.provider_name,
                self.provider_address,
                self.phone_number,
                self.email
                )


class Client(UserMixin, Base):
    __tablename__ = "clients"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    username = Column(String(123), nullable=False)
    first_name = Column(String(128))
    last_name = Column(String(128))
    email = Column(String(255), nullable=False)
    password = Column(String(100), nullable=False)
    phone_number = Column(String(15), nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    users = relationship("User", back_populates="clients")
    appointments = relationship("Appointment", back_populates="clients", cascade="all, delete-orphan")
    providers = relationship("Provider", back_populates="clients")
    slots = relationship('Slot', back_populates="clients")

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
    service_name = Column(String(228))
    description = Column(String(500))
    provider_id = Column(Integer, ForeignKey("providers.id"))
    appointments = relationship("Appointment", back_populates='services')
    providers = relationship("Provider", back_populates="services")

    def __repr__(self):
        return f"<Service(service_name='%s', description='%s', appointments='%s')>" % (
                self.service_name,
                self.description,
                self.appointments
                )


class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    service_name = Column(String(158))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    description = Column(String(300), default="")
    location = Column(String(128), default="")
    slot_id = Column(Integer, ForeignKey("slots.id"))
    provider_id = Column(Integer, ForeignKey("providers.id"))
    client_id = Column(Integer, ForeignKey("clients.id"))
    service_id = Column(Integer, ForeignKey("services.id"))

    providers = relationship("Provider", back_populates="appointments")
    clients = relationship("Client", back_populates="appointments")
    services = relationship("Service", back_populates="appointments")
    slots = relationship('Slot', back_populates="appointments")

    def __repr__(self):
        return f"<Appointment(service_name='%s', date_time='%s', description='%s', location='%s')>" % (
                self.service_name,
                self.week_day,
                self.description,
                self.location
                )

class Slot(Base):
    __tablename__ = "slots"
    id = Column(Integer, autoincrement=True, primary_key=True, nullable=False)
    service_name = Column(String(228))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    client_id = Column(Integer, ForeignKey('clients.id'))
    provider_id = Column(Integer, ForeignKey('providers.id'))

    clients = relationship('Client', back_populates="slots")
    providers = relationship('Provider', back_populates="slots")
    appointments = relationship('Appointment', back_populates="slots")

#Provider.appointments = relationship('Appointment', back_populates="providers")

APPOMS_MYSQL_USER = getenv("APPOMS_MYSQL_USER")
APPOMS_MYSQL_HOST = getenv("APPOMS_MYSQL_HOST")
APPOMS_MYSQL_PWD = getenv("APPOMS_MYSQL_PWD")
APPOMS_MYSQL_DB = getenv("APPOMS_MYSQL_DB")
APPOMS_KEY = getenv('APPOMS_KEY')
if not all([APPOMS_MYSQL_USER, APPOMS_MYSQL_PWD, APPOMS_MYSQL_HOST, APPOMS_MYSQL_DB]):
     raise ValueError("Please set all required environment variables.")
db_url = f"mysql+mysqldb://{APPOMS_MYSQL_USER}:{APPOMS_MYSQL_PWD}@{APPOMS_MYSQL_HOST}/{APPOMS_MYSQL_DB}"

engine = create_engine(db_url, pool_pre_ping=True)
Base.metadata.create_all(engine)
Session = scoped_session(sessionmaker(bind=engine, expire_on_commit=False))
