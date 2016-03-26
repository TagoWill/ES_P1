from sqlalchemy import Column, ForeignKey, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    userid = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)

class Car(Base):
    __tablename__ = 'car'
    carid = Column(Integer, primary_key=True)
    brand = Column(String(250), nullable=False)
    model = Column(String(250), nullable=False)
    fuel = Column(String(250), nullable=False)
    price = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey('user.userid'))
    owner = relationship(User)

class Dealership(Base):
    __tablename__ = 'dealership'
    dealershipid = Column(Integer, primary_key=True)
    contact = Column(Integer, nullable=False)
    district = Column(String(250), nullable=False)
    location_lat = Column(Float, nullable=False)
    location_long = Column(Float, nullable=False)
    seller_id = Column(Integer, ForeignKey('user.userid'))
    seller = relationship(User)

# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///project1_sqlalchemy_db.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)