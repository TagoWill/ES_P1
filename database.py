from sqlalchemy import Column, ForeignKey, Integer, Float, String, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()

association_table = Table('association', Base.metadata,
    Column('dealership_id', Integer, ForeignKey('dealership.dealershipid'), nullable=True),
    Column('car_id', Integer, ForeignKey('car.carid'), nullable=True)
)

class User(Base):
    __tablename__ = 'user'
    userid = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    type = Column(String(250), nullable=False)
    email = Column(String(250), nullable=False)
    password = Column(String(250), nullable=False)


class Dealership(Base):
    __tablename__ = 'dealership'
    dealershipid = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    contact = Column(Integer, nullable=False)
    district = Column(String(250), nullable=False)
    seller_id = Column(Integer, ForeignKey('user.userid'))
    seller = relationship(User)
    mycars = relationship(
        "Car",
        secondary=association_table,
        back_populates="mydealership")


class Car(Base):
    __tablename__ = 'car'
    carid = Column(Integer, primary_key=True)
    brand = Column(String(250), nullable=False)
    model = Column(String(250), nullable=False)
    fuel = Column(String(250), nullable=False)
    price = Column(Integer, nullable=False)
    kms = Column(Integer, nullable=False)
    year = Column(Integer, nullable=False)
    owner_id = Column(Integer, ForeignKey('user.userid'))
    owner = relationship(User)
    mydealership = relationship(
        "Dealership",
        secondary=association_table,
        back_populates="mycars")

# Create an engine that stores data in the local directory's
engine = create_engine('mysql+pymysql://esproject:esproject@esteste.clw9xldhi2rc.eu-west-1.rds.amazonaws.com:3306/esproject1')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
