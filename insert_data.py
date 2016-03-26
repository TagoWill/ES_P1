from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database import User, Base, Car, Dealership

engine = create_engine('sqlite:///project1_sqlalchemy_db.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Insert a User
new_user = User(name='daniel', email='dbastos@gmail.pt', password='123')
session.add(new_user)
session.commit()

# Insert a User
new_user2 = User(name='tiago', email='tiago@gmail.pt', password='123')
session.add(new_user2)
session.commit()

# Insert a Car
new_car = Car(brand='BMW', model='320i', fuel='gasoline', price=20000, owner=new_user)
session.add(new_car)
session.commit()

# Insert a Deal
new_deal = Dealership(contact=999999999, district='Coimbra', location_lat=40.1, location_long=-8.4, seller=new_user)
session.add(new_deal)
session.commit()
