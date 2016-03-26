from database import User, Base, Car, Dealership
from sqlalchemy import create_engine

engine = create_engine('sqlite:///project1_sqlalchemy_db.db')
Base.metadata.bind = engine

from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()
# Make a query to find all Users in the database
session.query(User).all()

# Return the first User from all Users in the database
user = session.query(User).first()
user.name
'daniel'